# ❗❗❗ IMPORTS ❗❗❗

# Lire les flux RSS
import feedparser

# Lire et analyser du HTML
from bs4 import BeautifulSoup


# ❗❗❗ RSS ❗❗❗

# ---------- URLs des flux RSS ----------

# Adresse du flux RSS Microsoft .NET
DOTNET_RSS_URL = "https://devblogs.microsoft.com/dotnet/feed/"

# Adresse du flux RSS Dev.to
DEVTO_RSS_URL = "https://dev.to/feed"


# ---------- Structurer les articles RSS ----------

# Transformer un flux RSS en liste d'articles structurés
def process_feed(feed, source, category):
    # Liste qui stockera les articles
    articles = []

    # Parcourir chaque article du flux RSS
    for article in feed.entries:
        # Créer un dictionnaire vide
        article_data = {}

        # Ajouter la source
        article_data["source"] = source

        # Ajouter la catégorie
        article_data["category"] = category

        # Le score sera calculé plus tard
        article_data["relevance_score"] = 0

        # Ajouter le titre
        article_data["title"] = article.get(
            "title",
            ""
        )

        # Ajouter le lien
        article_data["link"] = article.get(
            "link",
            ""
        )

        # Ajouter la date
        article_data["published"] = article.get(
            "published",
            ""
        )

        # Récupérer le résumé
        article_summary = article.get(
            "summary",
            ""
        )

        # Transformer le résumé HTML en BeautifulSoup
        soup = BeautifulSoup(
            article_summary,
            "html.parser"
        )

        # Transformer le résumé HTML en texte propre
        article_data["summary"] = soup.get_text(
            " ",
            strip=True
        )

        # Ajouter l'article terminé
        articles.append(article_data)

    # Retourner tous les articles
    return articles


# ---------- Obtenir les articles RSS ----------

def get_rss_articles():
    """
    Fetch Microsoft .NET and Dev.to RSS feeds and convert to common article structure.
    """
    # Télécharger et lire le RSS .NET
    dotnet_feed = feedparser.parse(DOTNET_RSS_URL)

    # Télécharger et lire le RSS Dev.to
    devto_feed = feedparser.parse(DEVTO_RSS_URL)

    # Transformer le RSS .NET en articles structurés
    dotnet_articles = process_feed(
        dotnet_feed,
        "Microsoft .NET Blog",
        ".NET"
    )

    # Transformer le RSS Dev.to en articles structurés
    devto_articles = process_feed(
        devto_feed,
        "Dev.to",
        "General Tech"
    )

    return dotnet_articles + devto_articles


# ❗❗❗ END RSS ❗❗❗
