# ❗❗❗ IMPORTS ❗❗❗

# Lire et analyser du HTML
from bs4 import BeautifulSoup

# Télécharger des données depuis Internet
import requests


# ❗❗❗ WEB SCRAPER ❗❗❗

# ---------- URLs des sites ----------

# Page principale Microsoft .NET
DOTNET_SCRAPER_URL = "https://devblogs.microsoft.com/dotnet/"

# Page principale Dev.to
DEVTO_SCRAPER_URL = "https://dev.to/"


# ---------- Obtenir les articles scrapés ----------

def get_scraped_articles():
    """
    Scrape Microsoft .NET and Dev.to pages to collect article links,
    extract title, content, publication date using BeautifulSoup.
    Handle requests timeouts and request errors.
    """
    scraped_articles = []

    # Télécharger Microsoft .NET
    try:
        dotnet_scraper_response = requests.get(
            DOTNET_SCRAPER_URL,
            timeout=10
        )
    except requests.RequestException:
        dotnet_scraper_response = None

    # Télécharger Dev.to
    try:
        devto_scraper_response = requests.get(
            DEVTO_SCRAPER_URL,
            timeout=10
        )
    except requests.RequestException:
        devto_scraper_response = None

    # ---------- Scraper Microsoft .NET ----------
    if dotnet_scraper_response is not None:
        try:
            dotnet_scraper_soup = BeautifulSoup(
                dotnet_scraper_response.text,
                "html.parser"
            )
            dotnet_article_links = dotnet_scraper_soup.find_all("a")
            dotnet_scraped_article_links = []

            for link in dotnet_article_links:
                href = link.get("href")
                if href and href.startswith(
                    "https://devblogs.microsoft.com/dotnet/"
                ):
                    slug = href.replace(
                        "https://devblogs.microsoft.com/dotnet/",
                        ""
                    ).strip("/")
                    if (
                        slug
                        and "/" not in slug
                        and not slug.startswith("wp-")
                        and slug != "feed"
                    ):
                        dotnet_scraped_article_links.append(href)

            # Supprimer les doublons
            dotnet_scraped_article_links = list(
                set(dotnet_scraped_article_links)
            )

            # Scraper chaque article
            dotnet_scraped_articles = []
            for article_url in dotnet_scraped_article_links:
                try:
                    article_response = requests.get(
                        article_url,
                        timeout=10
                    )
                    article_soup = BeautifulSoup(
                        article_response.text,
                        "html.parser"
                    )
                    article_title = article_soup.find("h1")
                    article_content = article_soup.find("article")

                    if article_title and article_content:
                        article_title_clean = article_title.get_text(
                            " ",
                            strip=True
                        )
                        article_content_clean = article_content.get_text(
                            " ",
                            strip=True
                        )
                        article_date = article_soup.find(
                            "meta",
                            property="article:published_time"
                        )
                        if article_date:
                            article_date = article_date.get("content")
                        else:
                            article_date = ""

                        scraped_article = {}
                        scraped_article["source"] = "Microsoft .NET Blog"
                        scraped_article["category"] = ".NET"
                        scraped_article["relevance_score"] = 0
                        scraped_article["title"] = article_title_clean
                        scraped_article["link"] = article_url
                        scraped_article["published"] = article_date
                        scraped_article["summary"] = article_content_clean
                        dotnet_scraped_articles.append(scraped_article)
                except requests.RequestException:
                    continue
            scraped_articles.extend(dotnet_scraped_articles)
        except Exception:
            pass

    # ---------- Scraper Dev.to ----------
    if devto_scraper_response is not None:
        try:
            devto_scraper_soup = BeautifulSoup(
                devto_scraper_response.text,
                "html.parser"
            )
            devto_article_links = devto_scraper_soup.find_all("a")
            devto_scraped_article_links = []

            for link in devto_article_links:
                href = link.get("href")
                if href and href.startswith("https://dev.to/"):
                    slug = href.replace(
                        "https://dev.to/",
                        ""
                    ).strip("/")
                    if "/" in slug:
                        if not slug.startswith("t/"):
                            clean_href = href.split("?")[0].split("#")[0]
                            devto_scraped_article_links.append(
                                clean_href
                            )

            # Supprimer les doublons
            devto_scraped_article_links = list(
                set(devto_scraped_article_links)
            )

            devto_scraped_articles = []
            for article_url in devto_scraped_article_links:
                try:
                    article_response = requests.get(
                        article_url,
                        timeout=10
                    )
                    article_soup = BeautifulSoup(
                        article_response.text,
                        "html.parser"
                    )
                    article_title = article_soup.find("h1")
                    article_content = article_soup.find("article")

                    if article_title and article_content:
                        article_title_clean = article_title.get_text(
                            " ",
                            strip=True
                        )
                        article_content_clean = article_content.get_text(
                            " ",
                            strip=True
                        )
                        article_date = article_soup.find(
                            "meta",
                            property="article:published_time"
                        )
                        if article_date:
                            article_date = article_date.get("content")
                        else:
                            article_date = ""

                        scraped_article = {}
                        scraped_article["source"] = "Dev.to"
                        scraped_article["category"] = "General Tech"
                        scraped_article["relevance_score"] = 0
                        scraped_article["title"] = article_title_clean
                        scraped_article["link"] = article_url
                        scraped_article["published"] = article_date
                        scraped_article["summary"] = article_content_clean
                        devto_scraped_articles.append(scraped_article)
                except requests.RequestException:
                    continue
            scraped_articles.extend(devto_scraped_articles)
        except Exception:
            pass

    return scraped_articles


# ❗❗❗ END WEB SCRAPER ❗❗❗
