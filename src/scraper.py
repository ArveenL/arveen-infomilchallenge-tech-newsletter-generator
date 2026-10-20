import json
from urllib.parse import urljoin, urlsplit

import requests
from bs4 import BeautifulSoup

from cleaning import html_to_markdown, make_summary


DOTNET_SCRAPER_URL = "https://devblogs.microsoft.com/dotnet/"
DEVTO_SCRAPER_URL = "https://dev.to/"
SQL_SERVER_BASE_URL = "https://techcommunity.microsoft.com"
SQL_SERVER_BLOG_URL = (
    SQL_SERVER_BASE_URL + "/category/SQL-Server/blog/SQLServer"
)


def download_page(url):
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as error:
        print(f"Source indisponible : {url} ({error})")
        return None


def publication_date(soup):
    time = soup.select_one("time[datetime]")
    if time:
        return time["datetime"]
    meta = soup.find("meta", property="article:published_time")
    return meta.get("content", "") if meta else ""


def sql_server_article(soup, article_url):
    """Le corps complet est dans le cache Apollo de la page Next.js."""
    script = soup.select_one("script#__NEXT_DATA__")
    if not script:
        return None
    try:
        state = json.loads(script.string or script.get_text())["props"]["pageProps"]["apolloState"]
    except (ValueError, KeyError, TypeError):
        return None
    article_id = urlsplit(article_url).path.rstrip("/").rsplit("/", 1)[-1]
    message = state.get(f"BlogTopicMessage:message:{article_id}", {})
    if not message.get("subject") or not message.get("body"):
        return None
    return (
        message["subject"],
        message.get("postTime") or message.get("lastPublishTime", ""),
        html_to_markdown(message["body"]),
    )


def get_scraped_articles():
    scraped_articles = []
    sources = (
        (DOTNET_SCRAPER_URL, "Microsoft .NET Blog", ".NET"),
        (DEVTO_SCRAPER_URL, "Dev.to", "General Tech"),
        (SQL_SERVER_BLOG_URL, "Microsoft SQL Server Blog", "SQL Server"),
    )
    for index_url, source, category in sources:
        soup = download_page(index_url)
        if soup is None:
            continue

        # Sélecteurs ciblés pour éviter les profils, tags et pages d'interface.
        anchors = soup.select(
            "a.crayons-story__hidden-navigation-link[href], "
            "a.crayons-story__title[href], .crayons-story__title a[href]"
        ) if source == "Dev.to" else soup.select("a[href]")
        links = []
        for anchor in anchors:
            url = urljoin(index_url, anchor["href"]).split("?")[0].split("#")[0]
            path = urlsplit(url).path
            if category == ".NET":
                slug = path.removeprefix("/dotnet/").strip("/")
                valid = (
                    url.startswith(DOTNET_SCRAPER_URL)
                    and slug and "/" not in slug
                    and not slug.startswith("wp-") and slug != "feed"
                )
            elif source == "Dev.to":
                valid = urlsplit(url).netloc == "dev.to" and len(path.strip("/").split("/")) == 2
            else:
                valid = (
                    urlsplit(url).netloc == urlsplit(SQL_SERVER_BASE_URL).netloc
                    and "/blog/sqlserver/" in path.lower()
                )
            if valid and url not in links:
                links.append(url)

        source_articles = []
        for article_url in links:
            article_soup = download_page(article_url)
            if article_soup is None:
                continue
            if category == "SQL Server":
                extracted = sql_server_article(article_soup, article_url)
                if extracted is None:
                    continue
                title, published, content = extracted
            else:
                title_node = article_soup.find("h1")
                selector = (
                    "#article-body, .crayons-article__body"
                    if source == "Dev.to" else ".entry-content"
                )
                body = article_soup.select_one(selector)
                if title_node is None or body is None:
                    continue
                title = title_node.get_text(" ", strip=True)
                published = publication_date(article_soup)
                content = html_to_markdown(str(body))
            if not content.strip():
                continue
            source_articles.append({
                "source": source,
                "category": category,
                "relevance_score": 0,
                "title": title,
                "link": article_url,
                "published": published,
                "summary": make_summary(content),
                "content": content,
            })
        print(f"Scraping {category if source != 'Dev.to' else source}: {len(source_articles)}")
        scraped_articles.extend(source_articles)
    return scraped_articles
