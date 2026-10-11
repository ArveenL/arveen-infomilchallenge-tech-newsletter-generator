# ❗❗❗ IMPORTS ❗❗❗

# Lire les flux RSS
import feedparser

# Lire et analyser du HTML
from bs4 import BeautifulSoup

# Créer et écrire du JSON
import json

# Télécharger des données depuis Internet
import requests



# ❗❗❗ MAQUILLAGE / AFFICHAGE ❗❗❗
print("🕺🏽 Infomil Tech Newsletter Generator 🫈")
print()



# ❗❗❗ GITHUB RELEASES API ❗❗❗

# ---------- URLs des API GitHub Releases ----------

# Adresse des releases .NET
dotnet_github_releases_url = "https://api.github.com/repos/dotnet/core/releases"

# Adresse des releases Angular
angular_github_releases_url = "https://api.github.com/repos/angular/angular/releases"

# Adresse des releases React
react_github_releases_url = "https://api.github.com/repos/facebook/react/releases"


# ---------- Télécharger les releases ----------

# Demander les releases .NET à GitHub
dotnet_response = requests.get(dotnet_github_releases_url)

# Demander les releases Angular à GitHub
angular_response = requests.get(angular_github_releases_url)

# Demander les releases React à GitHub
react_response = requests.get(react_github_releases_url)


# ---------- Transformer les réponses JSON ----------

# Transformer la réponse .NET en données Python
dotnet_releases = dotnet_response.json()

# Transformer la réponse Angular en données Python
angular_releases = angular_response.json()

# Transformer la réponse React en données Python
react_releases = react_response.json()


# ---------- Préparer les listes filtrées ----------

# Liste qui gardera seulement .NET 10
dotnet10_releases = []

# Liste qui gardera seulement Angular 22
angular22_releases = []

# Liste qui gardera seulement React 19
react_filtered_releases = []


# ---------- Filtrer .NET 10 ----------

# Parcourir toutes les releases .NET
for release in dotnet_releases:

    # Garder seulement celles qui commencent par ".NET 10"
    if release["name"].startswith(".NET 10"):

        # Ajouter la release à notre liste
        dotnet10_releases.append(release)


# ---------- Filtrer Angular 22 ----------

# Parcourir toutes les releases Angular
for release in angular_releases:

    # Garder seulement les versions 22
    if release["name"].startswith("22."):

        # Ajouter la release à notre liste
        angular22_releases.append(release)


# ---------- Filtrer React 19 ----------

# Parcourir toutes les releases React
for release in react_releases:

    # Garder seulement les versions 19
    if release["name"].startswith("19."):

        # Ajouter la release à notre liste
        react_filtered_releases.append(release)


# ❗❗❗ END GITHUB RELEASES API ❗❗❗



# ❗❗❗ RSS ❗❗❗

# ---------- URLs des flux RSS ----------

# Adresse du flux RSS Microsoft .NET
dotnet_rss_url = "https://devblogs.microsoft.com/dotnet/feed/"

# Adresse du flux RSS Dev.to
devto_rss_url = "https://dev.to/feed"


# ---------- Lire les flux RSS ----------

# Télécharger et lire le RSS .NET
dotnet_feed = feedparser.parse(dotnet_rss_url)

# Télécharger et lire le RSS Dev.to
devto_feed = feedparser.parse(devto_rss_url)


# ---------- Structurer les articles RSS ----------

# Transformer un flux RSS en liste d'articles propres
def process_feed(feed, source, category):

    # Liste qui stockera les articles
    articles = []

    # Parcourir chaque article du flux RSS
    for article in feed.entries:

        # Créer un dictionnaire vide pour l'article
        article_data = {}

        # Ajouter la source
        article_data["source"] = source

        # Ajouter la catégorie
        article_data["category"] = category

        # Le score sera calculé plus tard
        article_data["relevance_score"] = 0

        # Ajouter le titre
        article_data["title"] = article.title

        # Ajouter le lien
        article_data["link"] = article.link

        # Ajouter la date de publication
        article_data["published"] = article.published

        # Transformer le résumé HTML en BeautifulSoup
        soup = BeautifulSoup(article.summary, "html.parser")

        # Transformer le résumé HTML en texte propre
        article_data["summary"] = soup.get_text(" ", strip=True)

        # Ajouter l'article terminé dans la liste
        articles.append(article_data)

    # Retourner tous les articles trouvés
    return articles


# ---------- Traiter Microsoft .NET ----------

# Transformer le RSS .NET en articles structurés
dotnet_articles = process_feed(
    dotnet_feed,
    "Microsoft .NET Blog",
    ".NET"
)


# ---------- Traiter Dev.to ----------

# Transformer le RSS Dev.to en articles structurés
devto_articles = process_feed(
    devto_feed,
    "Dev.to",
    "General Tech"
)


# ❗❗❗ END RSS ❗❗❗



# ❗❗❗ WEB SCRAPER ❗❗❗

# ---------- URLs des sites ----------

# Page principale du blog .NET
dotnet_scraper_url = "https://devblogs.microsoft.com/dotnet/"

# Page principale Dev.to
devto_scraper_url = "https://dev.to/"


# ---------- Télécharger les pages principales ----------

# Télécharger le HTML de la page .NET
dotnet_scraper_response = requests.get(dotnet_scraper_url)

# Télécharger le HTML de Dev.to
devto_scraper_response = requests.get(devto_scraper_url)


# ---------- Transformer HTML en BeautifulSoup ----------

# Rendre le HTML .NET facilement analysable
dotnet_scraper_soup = BeautifulSoup(
    dotnet_scraper_response.text,
    "html.parser"
)

# Rendre le HTML Dev.to facilement analysable
devto_scraper_soup = BeautifulSoup(
    devto_scraper_response.text,
    "html.parser"
)


# ---------- Récupérer les liens ----------

# Récupérer tous les <a> présents sur la page .NET
dotnet_article_links = dotnet_scraper_soup.find_all("a")

# Récupérer tous les <a> présents sur Dev.to
devto_article_links = devto_scraper_soup.find_all("a")


# ---------- Filtrer les liens Microsoft .NET ----------

# Liste qui gardera seulement les vrais liens d'articles
dotnet_scraped_article_links = []

# Parcourir tous les liens trouvés
for link in dotnet_article_links:

    # Récupérer l'adresse du lien
    href = link.get("href")

    # Garder seulement les liens appartenant au blog .NET
    if href and href.startswith(
        "https://devblogs.microsoft.com/dotnet/"
    ):

        # Retirer le domaine pour obtenir seulement le slug
        slug = href.replace(
            "https://devblogs.microsoft.com/dotnet/",
            ""
        ).strip("/")

        # Vérifier que le lien ressemble à un article
        if (
            slug
            and "/" not in slug
            and not slug.startswith("wp-")
            and slug != "feed"
        ):

            # Ajouter le lien valide
            dotnet_scraped_article_links.append(href)


# ---------- Supprimer les doublons .NET ----------

# Transformer en set puis en list pour garder chaque URL une seule fois
dotnet_scraped_article_links = list(
    set(dotnet_scraped_article_links)
)


# ---------- Scraper les articles Microsoft .NET ----------

# Liste qui stockera les articles .NET complets
dotnet_scraped_articles = []

# Parcourir chaque URL d'article .NET
for article_url in dotnet_scraped_article_links:

    # Télécharger la page de l'article
    article_response = requests.get(
        article_url,
        timeout=10
    )

    # Transformer la page HTML en BeautifulSoup
    article_soup = BeautifulSoup(
        article_response.text,
        "html.parser"
    )

    # Chercher le titre
    article_title = article_soup.find("h1")

    # Chercher le contenu principal
    article_content = article_soup.find("article")

    # Continuer seulement si titre et contenu existent
    if article_title and article_content:

        # Transformer le titre HTML en texte propre
        article_title = article_title.get_text(
            " ",
            strip=True
        )

        # Transformer le contenu HTML en texte propre
        article_content = article_content.get_text(
            " ",
            strip=True
        )

        # Chercher la date dans les métadonnées
        article_date = article_soup.find(
            "meta",
            property="article:published_time"
        )

        # Si la date existe
        if article_date:

            # Récupérer sa valeur
            article_date = article_date.get("content")

        # Sinon
        else:

            # Indiquer qu'aucune date n'a été trouvée
            article_date = None

        # Créer le dictionnaire de l'article
        scraped_article = {}

        # Ajouter la source
        scraped_article["source"] = "Microsoft .NET Blog"

        # Ajouter la catégorie
        scraped_article["category"] = ".NET"

        # Le score sera calculé plus tard
        scraped_article["relevance_score"] = 0

        # Ajouter le titre
        scraped_article["title"] = article_title

        # Ajouter le lien
        scraped_article["link"] = article_url

        # Ajouter la date
        scraped_article["published"] = article_date

        # Ajouter le contenu
        scraped_article["summary"] = article_content

        # Ajouter l'article terminé à la liste
        dotnet_scraped_articles.append(scraped_article)


# ---------- Filtrer les liens Dev.to ----------

# Liste qui gardera seulement les liens d'articles Dev.to
devto_scraped_article_links = []

# Parcourir tous les liens trouvés
for link in devto_article_links:

    # Récupérer l'adresse du lien
    href = link.get("href")

    # Garder seulement les URLs complètes Dev.to
    if href and href.startswith("https://dev.to/"):

        # Retirer le domaine pour obtenir le slug
        slug = href.replace(
            "https://dev.to/",
            ""
        ).strip("/")

        # Un article ressemble généralement à auteur/article
        if "/" in slug:

            # Exclure les pages de tags comme t/react
            if not slug.startswith("t/"):

                # Retirer les paramètres ? et les ancres #
                clean_href = href.split("?")[0].split("#")[0]

                # Ajouter le lien propre
                devto_scraped_article_links.append(clean_href)


# ---------- Supprimer les doublons Dev.to ----------

# Garder chaque URL Dev.to une seule fois
devto_scraped_article_links = list(
    set(devto_scraped_article_links)
)


# ---------- Scraper les articles Dev.to ----------

# Liste qui stockera les articles Dev.to complets
devto_scraped_articles = []

# Parcourir chaque article Dev.to
for article_url in devto_scraped_article_links:

    # Télécharger la page de l'article
    article_response = requests.get(
        article_url,
        timeout=10
    )

    # Transformer la page en BeautifulSoup
    article_soup = BeautifulSoup(
        article_response.text,
        "html.parser"
    )

    # Chercher le titre
    article_title = article_soup.find("h1")

    # Chercher le contenu
    article_content = article_soup.find("article")

    # Continuer seulement si les deux existent
    if article_title and article_content:

        # Transformer le titre en texte propre
        article_title = article_title.get_text(
            " ",
            strip=True
        )

        # Transformer le contenu en texte propre
        article_content = article_content.get_text(
            " ",
            strip=True
        )

        # Chercher la date dans les métadonnées
        article_date = article_soup.find(
            "meta",
            property="article:published_time"
        )

        # Si la date existe
        if article_date:

            # Récupérer sa valeur
            article_date = article_date.get("content")

        # Sinon
        else:

            # Indiquer qu'aucune date n'a été trouvée
            article_date = None

        # Créer le dictionnaire de l'article
        scraped_article = {}

        # Ajouter la source
        scraped_article["source"] = "Dev.to"

        # Ajouter la catégorie
        scraped_article["category"] = "General Tech"

        # Le score sera calculé plus tard
        scraped_article["relevance_score"] = 0

        # Ajouter le titre
        scraped_article["title"] = article_title

        # Ajouter le lien
        scraped_article["link"] = article_url

        # Ajouter la date
        scraped_article["published"] = article_date

        # Ajouter le contenu
        scraped_article["summary"] = article_content

        # Ajouter l'article terminé à la liste
        devto_scraped_articles.append(scraped_article)


# ❗❗❗ END WEB SCRAPER ❗❗❗



# ❗❗❗ STRUCTURE GITHUB .NET 10 ❗❗❗

# ---------- Préparer la liste ----------

# Liste qui contiendra les releases .NET 10 structurées
dotnet10_articles = []


# ---------- Structurer les releases ----------

# Parcourir les releases .NET 10 filtrées
for release in dotnet10_releases:

    # Créer un dictionnaire
    release_data = {}

    # Ajouter la source
    release_data["source"] = "GitHub Releases"

    # Ajouter la catégorie
    release_data["category"] = ".NET"

    # Le score sera calculé plus tard
    release_data["relevance_score"] = 0

    # Utiliser le nom de la release comme titre
    release_data["title"] = release["name"]

    # Ajouter le lien GitHub
    release_data["link"] = release["html_url"]

    # Ajouter la date
    release_data["published"] = release["published_at"]

    # Ajouter les release notes
    release_data["summary"] = release["body"]

    # Ajouter la release structurée à la liste
    dotnet10_articles.append(release_data)


# ❗❗❗ END STRUCTURE GITHUB .NET 10 ❗❗❗



# ❗❗❗ STRUCTURE GITHUB ANGULAR 22 ❗❗❗

# ---------- Préparer la liste ----------

# Liste qui contiendra les releases Angular 22
angular_articles = []


# ---------- Structurer les releases ----------

# Parcourir les releases Angular 22
for release in angular22_releases:

    # Créer un dictionnaire
    release_data = {}

    # Ajouter la source
    release_data["source"] = "GitHub Releases"

    # Ajouter la catégorie
    release_data["category"] = "Angular"

    # Le score sera calculé plus tard
    release_data["relevance_score"] = 0

    # Ajouter le titre
    release_data["title"] = release["name"]

    # Ajouter le lien
    release_data["link"] = release["html_url"]

    # Ajouter la date
    release_data["published"] = release["published_at"]

    # Ajouter les release notes
    release_data["summary"] = release["body"]

    # Ajouter la release à la liste
    angular_articles.append(release_data)


# ❗❗❗ END STRUCTURE GITHUB ANGULAR 22 ❗❗❗



# ❗❗❗ STRUCTURE GITHUB REACT 19 ❗❗❗

# ---------- Préparer la liste ----------

# Liste qui contiendra les releases React 19
react_articles = []


# ---------- Structurer les releases ----------

# Parcourir les releases React 19
for release in react_filtered_releases:

    # Créer un dictionnaire
    release_data = {}

    # Ajouter la source
    release_data["source"] = "GitHub Releases"

    # Ajouter la catégorie
    release_data["category"] = "React"

    # Le score sera calculé plus tard
    release_data["relevance_score"] = 0

    # Ajouter le titre
    release_data["title"] = release["name"]

    # Ajouter le lien
    release_data["link"] = release["html_url"]

    # Ajouter la date
    release_data["published"] = release["published_at"]

    # Ajouter les release notes
    release_data["summary"] = release["body"]

    # Ajouter la release à la liste
    react_articles.append(release_data)


# ❗❗❗ END STRUCTURE GITHUB REACT 19 ❗❗❗



# ❗❗❗ LISTE GÉNÉRALE ❗❗❗

# ---------- Regrouper toutes les sources ----------

# Mettre RSS + GitHub + scraping dans une seule liste
articles = (
    dotnet_articles
    + devto_articles
    + dotnet10_articles
    + angular_articles
    + react_articles
    + dotnet_scraped_articles
    + devto_scraped_articles
)


# ---------- Ajouter les IDs ----------

# Commencer les IDs à 1
article_id = 1

# Parcourir tous les articles
for article in articles:

    # Donner l'ID actuel à l'article
    article["id"] = article_id

    # Préparer l'ID suivant
    article_id += 1


# ❗❗❗ END LISTE GÉNÉRALE ❗❗❗



# ❗❗❗ TESTS TERMINAL ❗❗❗

# ---------- Compter les articles récupérés ----------

# Nombre d'articles RSS .NET
print("RSS .NET:", len(dotnet_articles))

# Nombre d'articles RSS Dev.to
print("RSS Dev.to:", len(devto_articles))

# Nombre de releases .NET 10
print("GitHub .NET 10:", len(dotnet10_articles))

# Nombre de releases Angular 22
print("GitHub Angular 22:", len(angular_articles))

# Nombre de releases React 19
print("GitHub React 19:", len(react_articles))

# Nombre d'articles .NET scrapés
print("Scraping .NET:", len(dotnet_scraped_articles))

# Nombre d'articles Dev.to scrapés
print("Scraping Dev.to:", len(devto_scraped_articles))

# Nombre total avant déduplication
print("TOTAL:", len(articles))


# ❗❗❗ END TESTS TERMINAL ❗❗❗



# ❗❗❗ JSON ❗❗❗

# ---------- Créer articles.json ----------

# Ouvrir ou créer articles.json en écriture
with open("articles.json", "w") as file:

    # Écrire tous les articles dans le fichier
    json.dump(
        articles,
        file,
        indent=4
    )


# ---------- Confirmation ----------

# Ajouter une ligne vide
print()

# Confirmer que le fichier a été créé
print("Articles saved in articles.json")


# ❗❗❗ END JSON ❗❗❗