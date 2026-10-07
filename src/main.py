# ===========================imports =======================
import feedparser             
from bs4 import BeautifulSoup 
import json
import requests               
# ===========================imports =======================


# ================================Github releases API ==========================
dotnet_github_releases_url = "https://api.github.com/repos/dotnet/core/releases"
dotnet_response = requests.get(dotnet_github_releases_url) # Envoyer la requête à l’API GitHub
dotnet_releases = dotnet_response.json() # Transformer la réponse GitHub en données Python

#Stocker uniquement releases .NET 10
dotnet10_releases = []

# Filtrer uniquement les releases .NET 10
for release in dotnet_releases:
    if release["name"].startswith(".NET 10"):
        dotnet10_releases.append(release)

print(len(dotnet10_releases))
# ================================Github releases API ==========================

# ==========================Feedpasser ========================
dotnet_rss_url = "https://devblogs.microsoft.com/dotnet/feed/"
devto_rss_url = "https://dev.to/feed"
dotnet_feed = feedparser.parse(dotnet_rss_url)
devto_feed = feedparser.parse(devto_rss_url)
# ==========================feedpasser ========================


# maquillage(might delete later)
print("🕺🏽 Infomil Tech Newsletter Generator 🫈")
print()


# Prendre un flux RSS brut et transformer chaque entrée en un article propre, 
# structuré et prêt à être ajouté dans notre JSON
def process_feed(feed, source, category, start_id = 1):
    
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


# On traite séparément les articles .NET et Dev.to, on donne des IDs continus, 
# puis on les rassemble dans une seule liste finale appelée articles
dotnet_articles = process_feed(dotnet_feed,"Microsoft .NET Blog", ".NET")
devto_articles = process_feed(devto_feed, "Dev.to", "General Tech", len(dotnet_articles) + 1)

articles = dotnet_articles + devto_articles



# ============================================JSON===========================================
# Crée articles.json + ouvre le pour écrire dedans + appele ce dernier 'file' pour l'instant
with open("articles.json", "w") as file:
    json.dump(articles, file, indent=4)
# ============================================JSON===========================================

print("Articles saved in articles.json")