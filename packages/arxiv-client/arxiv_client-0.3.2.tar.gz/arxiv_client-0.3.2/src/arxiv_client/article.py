import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from functools import cached_property
from typing import Self

import feedparser  # type: ignore

from arxiv_client import Link

logger = logging.getLogger(__name__)


@dataclass(init=False, repr=True, eq=False)
class Article:
    """
    Article from the Arxiv API
    """

    arxiv_id: str
    """
    The bare arXiv ID of the article. This differs from the ID field returned by the API which is a URL to the abstract.
    This should not include the version number suffix
    """
    title: str
    """
    The title of the article
    """
    categories: list[str]
    """
    The categories of the article. May include categories outside of the ArXiv taxonomy
    """
    authors: list[str]
    """
    The authors of the article
    """
    summary: str
    """
    The abstract for the article
    """
    comment: str | None
    """
    The author's comment if present
    """
    links: list[Link]
    """
    Links to associated with the article. Up to 3 links are provided by arXiv: PDF, DOI, and arxiv abstract page
    """
    journal_ref: str | None
    """
    Author provided journal reference
    """
    doi: str | None
    """
    Author provided DOI
    """
    version: int
    """
    The version of the article this data represents
    """
    published: datetime | None
    """
    The datetime that `version 1` of the article was submitted
    """
    updated: datetime | None
    """
    The datetime that the retrieved version was submitted
    """
    _raw_entry: feedparser.FeedParserDict = field(repr=False)
    """
    The raw feedparser entry for the article, helpful for debugging or accessing additional information
    """

    _versioned_id_re = re.compile(r"([^vV]+)[vV]?(\d*)")
    _id_search_prefix_len = len("http://arxiv.org/abs/")
    _rss_atom_desc_re = re.compile(r"^[^:]*:(\S*)\s+.*Abstract: (.*)$", re.DOTALL)
    _atom_id_re = re.compile(r"^[^:]+:[^:]+:(.*)$")

    def __init__(
        self,
        arxiv_id: str,
        title: str,
        categories: list[str],
        authors: list[str],
        summary: str,
        comment: str | None,
        links: list[Link],
        journal_ref: str | None,
        doi: str | None,
        version: int,
        published: datetime | None,
        updated: datetime | None,
        _raw_entry: feedparser.FeedParserDict,
    ) -> None:
        self.arxiv_id = arxiv_id
        self.title = title
        self.categories = categories
        self.authors = authors
        self.summary = summary
        self.comment = comment
        self.links = links
        self.journal_ref = journal_ref
        self.doi = doi
        self.version = version
        self.published = published
        self.updated = updated
        self._raw_entry = _raw_entry

    def __str__(self) -> str:
        return repr(self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Article):
            return False
        return self.arxiv_id == other.arxiv_id and self.version == other.version

    @cached_property
    def pdf_url(self) -> str | None:
        """
        Get the URL to the PDF of the article. A PDF link should always be present

        :return: The URL to the PDF
        """
        for link in self.links:
            if link.title == "pdf":
                return link.href
        return None

    @cached_property
    def doi_url(self) -> str | None:
        """
        Get the DOI URL for the article if it exists. May not be needed as the doi field may already contain the URL

        :return: The URL to the resolved DOI
        """
        for link in self.links:
            if link.title == "doi":
                return link.href
        return None

    @property
    def raw_entry(self) -> feedparser.FeedParserDict:
        """
        Get the raw feedparser entry for the article

        :return: The raw entry
        """
        return self._raw_entry

    @classmethod
    def from_rss_atom_entry(cls, entry: feedparser.FeedParserDict) -> Self:
        """
        Article factory from the daily RSS feeds

        See https://info.arxiv.org/help/rss_specifications.html
        https://info.arxiv.org/help/atom_specifications.html
        """
        idv = Article._atom_id_re.match(entry.id).group(1)
        id_matcher = Article._versioned_id_re.match(idv)
        arxiv_id = id_matcher.group(1)
        version = id_matcher.group(2) or 1
        desc_matcher = Article._rss_atom_desc_re.match(entry.description)
        if not desc_matcher:
            logger.error("WTF happened: %r", entry.description)
        abstract = desc_matcher.group(2)
        return cls(
            arxiv_id=arxiv_id,
            title=entry.title if hasattr(entry, "title") else "0",
            categories=[tag["term"] for tag in entry.tags],
            authors=entry.get("author", "").split(", "),
            summary=abstract,
            comment=None,  # not included in RSS/Atom
            links=[Link.from_feed_link(link) for link in entry.links],
            journal_ref=entry.get("arxiv_journal_ref"),
            doi=entry.get("arxiv_DOI"),
            version=version,
            published=None,  # not included in RSS/Atom
            updated=datetime.fromisoformat(entry.updated) if hasattr(entry, "updated") else None,  # not included in RSS
            _raw_entry=entry
        )

    @classmethod
    def from_search_entry(cls, entry: feedparser.FeedParserDict) -> Self:
        """
        Create an article from a feed entry

        :param entry: The feed entry
        :return: The article
        """

        # https://info.arxiv.org/help/api/user-manual.html#3321-title-id-published-and-updated
        # We should strip version suffixes
        match = Article._versioned_id_re.match(entry.id[Article._id_search_prefix_len:])
        arxiv_id = match.group(1)
        version = match.group(2) or 1
        title = entry.title if hasattr(entry, "title") else "0"
        return cls(
            arxiv_id=arxiv_id,
            title=title,
            categories=[tag["term"] for tag in entry.tags],
            authors=[author["name"] for author in entry.authors],
            summary=entry.summary,
            comment=entry.get("arxiv_comment"),
            links=[Link.from_feed_link(link) for link in entry.links],
            journal_ref=entry.get("arxiv_journal_ref"),
            doi=entry.get("arxiv_doi"),
            version=version,
            published=datetime.fromisoformat(entry.published),
            updated=datetime.fromisoformat(entry.updated),
            _raw_entry=entry,
        )
