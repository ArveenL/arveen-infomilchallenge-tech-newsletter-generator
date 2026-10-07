# Imports
import feedparser
from bs4 import BeautifulSoup
import json
import requests


# Maquillage (might delete later)
print("🕺🏽 Infomil Tech Newsletter Generator 🫈")
print()


# =========================== ❗️GitHub Releases API❗️ ===========================

# URLs des API GitHub Releases
dotnet_github_releases_url = "https://api.github.com/repos/dotnet/core/releases"
angular_github_releases_url = "https://api.github.com/repos/angular/angular/releases"
react_github_releases_url = "https://api.github.com/repos/facebook/react/releases"

# Envoyer les requêtes à l'API GitHub
dotnet_response = requests.get(dotnet_github_releases_url)
angular_response = requests.get(angular_github_releases_url)
react_response = requests.get(react_github_releases_url)

# Transformer les réponses GitHub en données Python
dotnet_releases = dotnet_response.json()
angular_releases = angular_response.json()
react_releases = react_response.json()


# Listes pour stocker uniquement les versions qui nous intéressent
dotnet10_releases = []
angular22_releases = []
react_filtered_releases = []


# Filtrer uniquement les releases .NET 10
for release in dotnet_releases:
    if release["name"].startswith(".NET 10"):
        dotnet10_releases.append(release)


# Filtrer uniquement les releases Angular 22
for release in angular_releases:
    if release["name"].startswith("22."):
        angular22_releases.append(release)


# Filtrer uniquement les releases React 19
for release in react_releases:
    if release["name"].startswith("19."):
        react_filtered_releases.append(release)


# =========================== ❗️End of GitHub Releases API❗️ ===========================



# =========================== ❗️RSS❗️ ===========================

# URLs des flux RSS
dotnet_rss_url = "https://devblogs.microsoft.com/dotnet/feed/"
devto_rss_url = "https://dev.to/feed"

# Télécharger et lire les flux RSS
dotnet_feed = feedparser.parse(dotnet_rss_url)
devto_feed = feedparser.parse(devto_rss_url)


# Prendre un flux RSS brut et transformer chaque entrée
# en un article structuré et prêt pour notre JSON
def process_feed(feed, source, category, start_id=1):

    articles = []
    article_id = start_id

    for article in feed.entries:
        article_data = {}

        article_data["id"] = article_id
        article_data["source"] = source
        article_data["category"] = category
        article_data["relevance_score"] = 0
        article_data["title"] = article.title
        article_data["link"] = article.link
        article_data["published"] = article.published

        # Nettoyer le HTML du résumé RSS
        soup = BeautifulSoup(article.summary, "html.parser")
        article_data["summary"] = soup.get_text(" ", strip=True)

        articles.append(article_data)

        article_id += 1

    return articles


# Traiter les articles RSS Microsoft .NET
dotnet_articles = process_feed(
    dotnet_feed,
    "Microsoft .NET Blog",
    ".NET"
)


# Traiter les articles RSS Dev.to
devto_articles = process_feed(
    devto_feed,
    "Dev.to",
    "General Tech",
    len(dotnet_articles) + 1
)


# =========================== ❗️End RSS❗️ ===========================



# =========================== ❗️Web Scraper❗️ ===========================

# URLs des sites à scraper
dotnet_scraper_url = "https://devblogs.microsoft.com/dotnet/"
devto_scraper_url = "https://dev.to/"


# Télécharger les pages web
dotnet_scraper_response = requests.get(dotnet_scraper_url)
devto_scraper_response = requests.get(devto_scraper_url)


# Transformer les pages HTML en objets BeautifulSoup
dotnet_scraper_soup = BeautifulSoup(
    dotnet_scraper_response.text,
    "html.parser"
)

devto_scraper_soup = BeautifulSoup(
    devto_scraper_response.text,
    "html.parser"
)


# Récupérer tous les liens <a> présents dans les deux pages
dotnet_article_links = dotnet_scraper_soup.find_all("a")
devto_article_links = devto_scraper_soup.find_all("a")



# ---------- Filtrer les liens d'articles Microsoft .NET ----------

# Liste qui contiendra uniquement les liens d'articles .NET
dotnet_scraped_article_links = []


for link in dotnet_article_links:

    # Récupérer l'adresse contenue dans href
    href = link.get("href")

    # Garder uniquement les liens du blog .NET
    if href and href.startswith("https://devblogs.microsoft.com/dotnet/"):

        # Retirer le domaine pour analyser le reste de l'URL
        slug = href.replace(
            "https://devblogs.microsoft.com/dotnet/",
            ""
        ).strip("/")

        # Exclure les pages qui ne sont pas des articles
        if (
            slug
            and "/" not in slug
            and not slug.startswith("wp-")
            and slug != "feed"
        ):
            dotnet_scraped_article_links.append(href)


# Supprimer les liens .NET en double
dotnet_scraped_article_links = list(
    set(dotnet_scraped_article_links)
)



# ---------- Scraper les articles Microsoft .NET ----------

# Liste qui contiendra les articles .NET scrapés
dotnet_scraped_articles = []


for article_url in dotnet_scraped_article_links:

    # Télécharger la page de l'article
    article_response = requests.get(article_url)

    # Transformer la page en objet BeautifulSoup
    article_soup = BeautifulSoup(
        article_response.text,
        "html.parser"
    )

    # Récupérer le titre de l'article
    article_title = article_soup.find("h1")
    article_title = article_title.get_text(" ", strip=True)

    # Récupérer le contenu principal de l'article
    article_content = article_soup.find("article")
    article_content = article_content.get_text(" ", strip=True)

    # Chercher la date de publication dans les métadonnées
    article_date = article_soup.find(
        "meta",
        property="article:published_time"
    )

    # Récupérer la date si elle existe
    if article_date:
        article_date = article_date.get("content")
    else:
        article_date = None

    # Créer le dictionnaire de l'article
    scraped_article = {}

    scraped_article["title"] = article_title
    scraped_article["link"] = article_url
    scraped_article["source"] = "Microsoft .NET Blog"
    scraped_article["category"] = ".NET"
    scraped_article["relevance_score"] = 0
    scraped_article["summary"] = article_content
    scraped_article["published"] = article_date

    # Ajouter l'article dans la liste
    dotnet_scraped_articles.append(scraped_article)



# ---------- Filtrer les liens d'articles Dev.to ----------

# Liste qui contiendra uniquement les liens d'articles Dev.to
devto_scraped_article_links = []


for link in devto_article_links:

    # Récupérer l'adresse contenue dans href
    href = link.get("href")

    # Garder uniquement les liens complets vers Dev.to
    if href and href.startswith("https://dev.to/"):

        # Retirer le domaine pour analyser le reste de l'URL
        slug = href.replace(
            "https://dev.to/",
            ""
        ).strip("/")

        # Un article Dev.to possède généralement auteur/article
        if "/" in slug:

            # Exclure les pages de tags comme t/react
            if not slug.startswith("t/"):
                devto_scraped_article_links.append(href)


# Supprimer les liens Dev.to en double
devto_scraped_article_links = list(
    set(devto_scraped_article_links)
)


# Liste qui contiendra les articles Dev.to scrapés
devto_scraped_articles = []


# La récupération du contenu des articles Dev.to
# sera ajoutée à la prochaine étape.


# =========================== ❗️End Web Scraper❗️ ===========================



# =========================== ❗️Structure GitHub .NET 10 ❗️===========================

# Liste pour stocker les releases .NET 10 structurées
dotnet10_articles = []

# Les IDs commencent après les articles RSS
release_id = len(dotnet_articles) + len(devto_articles) + 1


for release in dotnet10_releases:

    release_data = {}

    release_data["id"] = release_id
    release_data["source"] = "GitHub Releases"
    release_data["category"] = ".NET"
    release_data["relevance_score"] = 0
    release_data["title"] = release["name"]
    release_data["link"] = release["html_url"]
    release_data["published"] = release["published_at"]
    release_data["summary"] = release["body"]

    dotnet10_articles.append(release_data)

    release_id += 1


# =========================== ❗️End Structure GitHub .NET 10❗️ ===========================



# =========================== ❗️Structure GitHub Angular 22❗️ ===========================

# Liste pour stocker les releases Angular 22 structurées
angular_articles = []

# Les IDs commencent après RSS et .NET 10
release_id = (
    len(dotnet_articles)
    + len(devto_articles)
    + len(dotnet10_articles)
    + 1
)


for release in angular22_releases:

    release_data = {}

    release_data["id"] = release_id
    release_data["source"] = "GitHub Releases"
    release_data["category"] = "Angular"
    release_data["relevance_score"] = 0
    release_data["title"] = release["name"]
    release_data["link"] = release["html_url"]
    release_data["published"] = release["published_at"]
    release_data["summary"] = release["body"]

    angular_articles.append(release_data)

    release_id += 1


# =========================== ❗️End Structure GitHub Angular 22❗️ ===========================



# =========================== ❗️Structure GitHub React❗️ ===========================

# Liste pour stocker les releases React 19 structurées
react_articles = []

# Les IDs commencent après RSS, .NET 10 et Angular 22
release_id = (
    len(dotnet_articles)
    + len(devto_articles)
    + len(dotnet10_articles)
    + len(angular_articles)
    + 1
)


for release in react_filtered_releases:

    release_data = {}

    release_data["id"] = release_id
    release_data["source"] = "GitHub Releases"
    release_data["category"] = "React"
    release_data["relevance_score"] = 0
    release_data["title"] = release["name"]
    release_data["link"] = release["html_url"]
    release_data["published"] = release["published_at"]
    release_data["summary"] = release["body"]

    react_articles.append(release_data)

    release_id += 1


# =========================== ❗️End Structure GitHub React❗️ ===========================



# =========================== ❗️Liste générale❗️ ===========================

articles = (
    dotnet_articles
    + devto_articles
    + dotnet10_articles
    + angular_articles
    + react_articles
    + dotnet_scraped_articles
    + devto_scraped_articles
)


# =========================== ❗️End Liste générale❗️ ===========================



# =========================== ❗️JSON❗️ ===========================

# Créer articles.json et y enregistrer tous les articles
with open("articles.json", "w") as file:
    json.dump(articles, file, indent=4)


print("Articles saved in articles.json")


# =========================== ❗️End JSON❗️ ===========================