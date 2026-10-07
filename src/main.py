# =========================== imports =======================
import feedparser
from bs4 import BeautifulSoup
import json
import requests
# =========================== imports =======================


# =========================== GitHub Releases API =======================
dotnet_github_releases_url = "https://api.github.com/repos/dotnet/core/releases"
angular_github_releases_url = "https://api.github.com/repos/angular/angular/releases"

# Envoyer la requête à l'API GitHub
dotnet_response = requests.get(dotnet_github_releases_url)
angular_response = requests.get(angular_github_releases_url)

# Transformer la réponse GitHub en données Python/JSON
dotnet_releases = dotnet_response.json()
angular_releases = angular_response.json()



# Liste pour stocker uniquement les releases .NET 10 et Angular
dotnet10_releases = []
angular22_releases = []

# Filtrer uniquement les releases .NET 10
for release in dotnet_releases:
    if release["name"].startswith(".NET 10"):
        dotnet10_releases.append(release)

# Filtrer uniquement les releases Angular 22
for release in angular_releases:
        if release["name"].startswith("22."):
            angular22_releases.append(release)

#TEST temporaire


# =========================== end GitHub Releases API =======================


# =========================== Struture RSS =======================
dotnet_rss_url = "https://devblogs.microsoft.com/dotnet/feed/"
devto_rss_url = "https://dev.to/feed"

dotnet_feed = feedparser.parse(dotnet_rss_url)
devto_feed = feedparser.parse(devto_rss_url)


# Maquillage (might delete later)
print("🕺🏽 Infomil Tech Newsletter Generator 🫈")
print()


# Prendre un flux RSS brut et transformer chaque entrée en un article propre,
# structuré et prêt à être ajouté dans notre JSON
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

        soup = BeautifulSoup(article.summary, "html.parser")
        article_data["summary"] = soup.get_text(" ", strip=True)

        articles.append(article_data)

        article_id += 1

    return articles


# Traiter séparément les articles RSS
dotnet_articles = process_feed(
    dotnet_feed,
    "Microsoft .NET Blog",
    ".NET"
)

devto_articles = process_feed(
    devto_feed,
    "Dev.to",
    "General Tech",
    len(dotnet_articles) + 1
)
# =========================== end Struture RSS =======================


# =========================== Structure GitHub .NET 10 =======================

# Liste pour stocker les releases .NET 10 structurées
dotnet10_articles = []

# Les IDs GitHub commencent après les articles RSS
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
# =========================== end Structure GitHub .NET 10 =======================


# =========================== Structure GitHub Angular 22 =======================

# Liste pour stocker les releases Angular 22 structurées
angular_articles = []

# Les IDs Angular commencent après les articles RSS et .NET 10
release_id = len(dotnet_articles) + len(devto_articles) + len(dotnet10_articles) + 1

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

# =========================== Structure GitHub Angular 22 =======================

# TEST temporaire




# =========================== Liste générale =======================
articles = dotnet_articles + devto_articles + dotnet10_articles + angular_articles
# =========================== Liste générale =======================

# TEST temporaire
print("Total articles:", len(articles))

# =========================== JSON =======================
# Crée articles.json, l'ouvre en écriture et appelle temporairement le fichier "file"
with open("articles.json", "w") as file:
    json.dump(articles, file, indent=4)

print("Articles saved in articles.json")
# =========================== end JSON =======================