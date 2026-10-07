# imports
import feedparser
from bs4 import BeautifulSoup # to clean RSS flux
import json

# feedpasser
dotnet_rss_url = "https://devblogs.microsoft.com/dotnet/feed/"
devto_rss_url = "https://dev.to/feed"
dotnet_feed = feedparser.parse(dotnet_rss_url)
devto_feed = feedparser.parse(devto_rss_url)

# maquillage(might delete later)
print("🕺🏽 Infomil Tech Newsletter Generator 🫈")
print()

# revise to understand
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

# name for easy revision/understanding
dotnet_articles = process_feed(dotnet_feed,"Microsoft .NET Blog", ".NET")
devto_articles = process_feed(devto_feed, "Dev.to", "General Tech", len(dotnet_articles) + 1)

articles = dotnet_articles + devto_articles



# ==========================================================================================
# Crée articles.json + ouvre le pour écrire dedans + appele ce dernier 'file' pour l'instant
with open("articles.json", "w") as file:
    json.dump(articles, file, indent=4)
# ==========================================================================================

print("Articles saved in articles.json")