# arxiv-client

Python3 client for the [arXiv API](https://info.arxiv.org/help/api/user-manual.html).
Install package [`arxiv_client`](https://pypi.org/project/arxiv-client/) from PyPI.

This differs from the pre-existing [arxiv.py](https://github.com/lukasschwab/arxiv.py) project 
in that it further abstracts away the arXiv API so you do not need to learn to construct
query strings. The overall goal is to enable users to skip reading the API docs entirely.

## Basic Features

- Simple structured queries
- Comprehensive entity models, with documentation
  - For example, see the [Category](src/arxiv_client/category.py) enum for arXiv's subject taxonomy
- Fully type annotated

## Usage

In a nutshell:

```py
import arxiv_client as arx


categories = [arx.Category.CS_AI, arx.Category.CS_CL, arx.Category.CS_IR]
client = arx.Client()
articles = client.search(arx.Query(keywords=["llm"], categories=categories, max_results=10))
for article in articles:
    print(article)
```

### Structured Query Logic

When using the structured `Query` fields, multiple values within a single field are combined using `OR`, 
and multiple fields are combined using `AND`.

#### Searchable Fields

The `Query` object accepts the following field filters:

- `keywords`: terms across all fields
- `title_keywords`: terms in the article title
- `author_names`: names in the author list
- `categories`: arXiv subject categories
- `abstract_keywords`: terms in the article abstract
- `comment_keywords`: terms in the author provided comment
- `article_ids`: arXiv article IDs
- `custom_params`: custom query string

#### Example

```py
Query(keywords=["llm"], categories=[Category.CS_AI, Category.CS_IR], max_results=5)
# Query(
#     keywords=['llm'],
#     title_keywords=[],
#     author_names=[],
#     categories=[<Category.CS_AI: 'cs.AI'>, <Category.CS_IR: 'cs.IR'>],
#     abstract_keywords=[],
#     comment_keywords=[],
#     article_ids=[],
#     custom_params=None,
#     sort_criterion=SortCriterion(sort_by=<SortBy.LAST_UPDATED_DATE: 'lastUpdatedDate'>, sort_order=<SortOrder.DESC: 'descending'>),
#     start=0,
#     max_results=5
# )
```

Results in the following query logic:

```
("llm") in any field AND (cs.AI OR cs.IR) in the categories
```

See the [Query](src/arxiv_client/query.py) class for more information.

### Custom Queries

If the provided simple query logic is insufficient, the `Query` object takes a self-built query string through the `custom_params` attribute. You do not need to URL encode this value.

See [arXiv Query Construction](https://info.arxiv.org/help/api/user-manual.html#51-details-of-query-construction) for more information on building your own queries.

#### Example

```py
custom = f"cat:{Category.CS_AI.value} ANDNOT cat:{Category.CS_RO.value}"
Query(keywords=["paged attention", "attention window"], custom_params=custom)
# Query(
#     keywords=['paged attention', 'attention window'],
#     title_keywords=[],
#     author_names=[],
#     categories=[],
#     abstract_keywords=[],
#     comment_keywords=[],
#     article_ids=[],
#     custom_params='cat:cs.AI ANDNOT cat:cs.RO',
#     sort_criterion=SortCriterion(sort_by=<SortBy.LAST_UPDATED_DATE: 'lastUpdatedDate'>, sort_order=<SortOrder.DESC: 'descending'>),
#     start=0,
#     max_results=10
# )
```

Results in the following query logic:

```
("paged attention" OR "attention window") in any field AND (cs.AI AND NOT cs.RO) in the categories
```

Equivalent query string:

```
(all:"paged attention" OR all:"attention window") AND (cat:cs.AI ANDNOT cat:cs.RO)
```

## Development

This uses [hatch](https://hatch.pypa.io/latest/) for project management.
