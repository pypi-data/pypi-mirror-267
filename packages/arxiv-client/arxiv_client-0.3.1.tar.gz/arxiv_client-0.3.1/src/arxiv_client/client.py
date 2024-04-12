import copy
import logging
import time
from collections.abc import Iterator
from datetime import UTC, datetime, timedelta

import feedparser  # type: ignore
import requests

from arxiv_client import Article, Query, __about__, Subject, Category

logger = logging.getLogger(__name__)


class Client:
    """
    Structured Python3 client for the Arxiv API
    """

    base_search_url = "https://export.arxiv.org/api/query"
    """
    Base URL for Arxiv API
    """
    base_rss_url = "https://rss.arxiv.org/rss"
    """
    Base URL for arXiv RSS feeds
    """

    _session: requests.Session
    _last_request_dt: datetime | None

    def __init__(self) -> None:
        self._session = requests.Session()
        self._session.headers.update({"User-Agent": f"arxiv-client-py/{__about__.__version__}"})
        self._last_request_dt = None

    def rss_by_subject(self, subject: Subject) -> Iterator[Article]:
        """
        Get articles from the arXiv daily RSS feed. Only broad subjects are supported.
        Use `rss_by_category` for more specific category.

        Pages are updated daily at midnight EST.
        More info: https://info.arxiv.org/help/rss.html
        """
        url = f"{self.base_rss_url}/{subject.value}"
        feed = self._get_parsed_rss(url)
        for entry in feed.entries:
            yield Article.from_feed_entry(entry)

    def rss_by_category(self, categories: list[Category]) -> Iterator[Article]:
        """
        Get articles from the arXiv daily RSS feed. Pages are updated daily at midnight EST

        More info: https://info.arxiv.org/help/rss.html
        """
        cats = "+".join(cat.value for cat in categories)
        url = f"{self.base_rss_url}/{cats}"
        feed = self._get_parsed_rss(url)
        for entry in feed.entries:
            yield Article.from_feed_entry(entry)

    def search(
        self,
        query: Query,
        page_size: int | None = None,
        paging_delay_ms: int = 250,
        paging_max_retries: int = 4,
    ) -> Iterator[Article]:
        """
        Search the Arxiv API.

        The paging parameters allow for the search to be broken up into smaller queries.
        This is useful for large result sets, which can be processed as a stream of smaller pages.
        In cases of failure, you can resume from last successful article processed by using
        the start parameter in the Query object.

        Raises an exception if a paging request fails after `paging_max_retries` attempts.

        :param query: The query to search with
        :param page_size: The number of results to get in each page. None will fetch all results in one chunk
        :param paging_delay_ms: The delay in milliseconds between each page request
        :param paging_max_retries: The max number of retries for each page request
        :return: The search results
        """
        logger.debug("Searching arXiv with query: %r", query)
        subquery = copy.deepcopy(query)
        if page_size is not None and page_size < query.max_results:
            subquery.max_results = page_size

        total_retrieved = 0
        while total_retrieved < (query.max_results or float("inf")):
            feed = self._get_sub_page(subquery, paging_delay_ms, paging_max_retries)
            total_retrieved += len(feed.entries)
            total_results = int(feed.feed.opensearch_totalresults)

            logger.debug("Retrieved %d of %d total articles", total_retrieved, total_results)
            for entry in feed.entries:
                yield Article.from_feed_entry(entry)

            if not feed.entries or total_retrieved >= total_results:
                return

            if page_size is not None:
                subquery.start += len(feed.entries)
                if query.max_results is not None:
                    subquery.max_results = min(query.max_results - total_retrieved, page_size)

    def _get_sub_page(self, query: Query, paging_delay_ms: int, paging_max_retries: int) -> feedparser.FeedParserDict:
        """
        Get a page of search results from the Arxiv API.

        Will raise a RuntimeError if the page request fails after `page_max_retries` attempts.

        :param query: The query to search with
        :param paging_delay_ms: The delay in milliseconds between each chunk request
        :param paging_max_retries: The max number of retries for each chunk request
        :return: The search results
        """
        try_count = 0
        while try_count <= paging_max_retries:
            try:
                self._apply_paging_delay(paging_delay_ms)
                with self._session.get(self.base_search_url, params=query._to_url_params(), stream=True) as r:  # noqa SLF001
                    self._last_request_dt = datetime.now(tz=UTC)
                    r.raise_for_status()
                    feed = feedparser.parse(r.content)
                    logger.debug("Response headers: %r", r.headers)
                    if Client._should_retry_search_page(feed):
                        try_count += 1
                        if try_count <= paging_max_retries:
                            logger.debug("Incomplete response, retrying request")
                        continue
                    if feed.bozo:
                        logger.warning("Feed parser encountered a bozo error: %s", feed.bozo_exception)

            except (requests.HTTPError, requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout) as e:
                logger.warning("Failed to retrieve page of articles: %s", e)
                try_count += 1
            else:
                logger.debug("Successfully retrieved page of %d articles", len(feed.entries))
                return feed

        msg = f"Failed to retrieve page of articles after {paging_max_retries} retries"
        logger.error(msg, extra={"page_query": query})
        raise RuntimeError(msg)

    def _apply_paging_delay(self, delay_ms: int) -> None:
        """
        Ensure a minimum delay of delay_ms since the last request. This is to avoid violating arXiv rate limit
        while fetching results in chunks.
        """
        if self._last_request_dt is None:
            return

        min_delay = timedelta(milliseconds=delay_ms)
        elapsed = datetime.now(tz=UTC) - self._last_request_dt
        if elapsed < min_delay:
            wait_time = (min_delay - elapsed).total_seconds()
            logger.debug("Waiting %s seconds before next request", wait_time)
            time.sleep(wait_time)

    def _get_parsed_rss(self, url: str) -> feedparser.FeedParserDict:
        """
        Get and parse an RSS feed from arXiv
        """
        r = self._session.get(url)
        r.raise_for_status()
        feed = feedparser.parse(r.content)
        logger.debug("Retrieved RSS feed '%s' containing %d articles", feed.feed.title, len(feed.entries))
        return feed

    @staticmethod
    def _should_retry_search_page(feed: feedparser.FeedParserDict) -> bool:
        """
        Determine if a request should be retried based on response content.

        Sometimes arXiv will return a valid response with no content. This issue has been
        discussed here (https://github.com/lukasschwab/arxiv.py/issues/43) and it is
        believed to be an issue on the arXiv side that is sometimes resolved through
        retries.

        Separately, arXiv sometimes returns fewer entries than available.
        It's currently believed that a retry is not necessary and advancing
        the cursor should yield correct results, but this is not confirmed.

        :param feed: The feed parsed from the response
        :return: True if the request should be retried, False otherwise
        """
        num_available = int(feed.feed.opensearch_totalresults) - int(feed.feed.opensearch_startindex)
        if not feed.entries and num_available > 0:
            msg = "Feed unexpectedly has no entries, even though there are %d articles available"
            logger.warning(msg, num_available)
            return True

        return False
