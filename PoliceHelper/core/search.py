from data.articles import ARTICLES
from data.fines import FINES


def search_articles(query: str):
    """
    Поиск по статьям розыска.
    """

    query = query.casefold().strip()

    if not query:
        return ARTICLES

    result = []

    for number, title, minutes in ARTICLES:

        if (
            query in number.casefold()
            or query in title.casefold()
        ):
            result.append((number, title, minutes))

    return result


def search_fines(query: str):
    """
    Поиск по штрафам.
    """

    query = query.casefold().strip()

    if not query:
        return FINES

    result = []

    for number, title, price in FINES:

        if (
            query in number.casefold()
            or query in title.casefold()
        ):
            result.append((number, title, price))

    return result


def universal_search(query: str, mode: str):
    """
    Универсальный поиск.

    mode:
        "articles" - статьи
        "fines"    - штрафы
    """

    if mode == "articles":
        return search_articles(query)

    if mode == "fines":
        return search_fines(query)

    return []