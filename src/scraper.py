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

# Page officielle du blog SQL Server
SQL_SERVER_BLOG_URL = (
    "https://techcommunity.microsoft.com/"
    "category/SQL-Server/blog/SQLServer"
)

# Domaine principal de Microsoft Tech Community
SQL_SERVER_BASE_URL = "https://techcommunity.microsoft.com"


# ---------- Obtenir les articles scrapés ----------

def get_scraped_articles():

    # Liste qui contiendra tous les articles scrapés
    scraped_articles = []


    # ❗❗❗ SCRAPING MICROSOFT .NET ❗❗❗

    # ---------- Télécharger Microsoft .NET ----------

    # Essayer de télécharger la page Microsoft .NET
    try:
        dotnet_scraper_response = requests.get(
            DOTNET_SCRAPER_URL,
            timeout=10
        )

    # Si la requête échoue
    except requests.RequestException:

        # Garder une valeur vide
        dotnet_scraper_response = None


    # ---------- Scraper Microsoft .NET ----------

    # Continuer seulement si la page a été téléchargée
    if dotnet_scraper_response is not None:

        try:

            # Transformer le HTML en BeautifulSoup
            dotnet_scraper_soup = BeautifulSoup(
                dotnet_scraper_response.text,
                "html.parser"
            )

            # Chercher tous les liens de la page
            dotnet_article_links = dotnet_scraper_soup.find_all("a")

            # Liste qui stockera les liens des articles .NET
            dotnet_scraped_article_links = []


            # Parcourir tous les liens trouvés
            for link in dotnet_article_links:

                # Récupérer l'adresse du lien
                href = link.get("href")


                # Garder seulement les liens du blog .NET
                if href and href.startswith(
                    "https://devblogs.microsoft.com/dotnet/"
                ):

                    # Retirer le domaine pour obtenir le slug
                    slug = href.replace(
                        "https://devblogs.microsoft.com/dotnet/",
                        ""
                    ).strip("/")


                    # Garder seulement les vraies pages d'articles
                    if (
                        slug
                        and "/" not in slug
                        and not slug.startswith("wp-")
                        and slug != "feed"
                    ):

                        # Ajouter le lien à la liste
                        dotnet_scraped_article_links.append(href)


            # Supprimer les doublons
            dotnet_scraped_article_links = list(
                set(dotnet_scraped_article_links)
            )


            # Liste qui stockera les articles .NET complets
            dotnet_scraped_articles = []


            # Parcourir chaque article .NET
            for article_url in dotnet_scraped_article_links:

                try:

                    # Télécharger la page de l'article
                    article_response = requests.get(
                        article_url,
                        timeout=10
                    )

                    # Transformer le HTML en BeautifulSoup
                    article_soup = BeautifulSoup(
                        article_response.text,
                        "html.parser"
                    )

                    # Chercher le titre
                    article_title = article_soup.find("h1")

                    # Chercher le contenu principal
                    article_content = article_soup.find("article")

                    # Vérifier si BeautifulSoup trouve le titre
                    print(
                        "Titre trouvé:",
                        article_title is not None
                        )

                    # Vérifier si BeautifulSoup trouve la balise article
                    print(
                        "Contenu trouvé:",
                        article_content is not None
                        )   


                    # Continuer seulement si titre et contenu existent
                    if article_title and article_content:

                        # Transformer le titre en texte propre
                        article_title_clean = article_title.get_text(
                            " ",
                            strip=True
                        )

                        # Transformer le contenu en texte propre
                        article_content_clean = article_content.get_text(
                            " ",
                            strip=True
                        )

                        # Chercher la date de publication
                        article_date = article_soup.find(
                            "meta",
                            property="article:published_time"
                        )


                        # Récupérer la date si elle existe
                        if article_date:
                            article_date = article_date.get("content")

                        # Sinon garder une valeur vide
                        else:
                            article_date = ""


                        # Créer un dictionnaire vide
                        scraped_article = {}

                        # Ajouter la source
                        scraped_article["source"] = "Microsoft .NET Blog"

                        # Ajouter la catégorie
                        scraped_article["category"] = ".NET"

                        # Le score sera calculé plus tard
                        scraped_article["relevance_score"] = 0

                        # Ajouter le titre
                        scraped_article["title"] = article_title_clean

                        # Ajouter le lien
                        scraped_article["link"] = article_url

                        # Ajouter la date
                        scraped_article["published"] = article_date

                        # Ajouter le contenu comme résumé
                        scraped_article["summary"] = article_content_clean


                        # Ajouter l'article à la liste .NET
                        dotnet_scraped_articles.append(
                            scraped_article
                        )


                # Si un article ne peut pas être téléchargé
                except requests.RequestException:

                    # Passer à l'article suivant
                    continue


            # Ajouter les articles .NET à la liste générale
            scraped_articles.extend(
                dotnet_scraped_articles
            )


        # Éviter que le programme s'arrête si le HTML change
        except Exception:
            pass


    # ❗❗❗ END SCRAPING MICROSOFT .NET ❗❗❗



    # ❗❗❗ SCRAPING DEV.TO ❗❗❗

    # ---------- Télécharger Dev.to ----------

    # Essayer de télécharger la page Dev.to
    try:
        devto_scraper_response = requests.get(
            DEVTO_SCRAPER_URL,
            timeout=10
        )

    # Si la requête échoue
    except requests.RequestException:

        # Garder une valeur vide
        devto_scraper_response = None


    # ---------- Scraper Dev.to ----------

    # Continuer seulement si la page a été téléchargée
    if devto_scraper_response is not None:

        try:

            # Transformer le HTML en BeautifulSoup
            devto_scraper_soup = BeautifulSoup(
                devto_scraper_response.text,
                "html.parser"
            )

            # Chercher tous les liens de la page
            devto_article_links = devto_scraper_soup.find_all("a")

            # Liste qui stockera les liens des articles Dev.to
            devto_scraped_article_links = []


            # Parcourir tous les liens
            for link in devto_article_links:

                # Récupérer l'adresse du lien
                href = link.get("href")


                # Garder seulement les liens complets Dev.to
                if href and href.startswith("https://dev.to/"):

                    # Retirer le domaine pour obtenir le slug
                    slug = href.replace(
                        "https://dev.to/",
                        ""
                    ).strip("/")


                    # Un article contient normalement auteur/article
                    if "/" in slug:

                        # Exclure les pages de tags
                        if not slug.startswith("t/"):

                            # Retirer paramètres et ancres
                            clean_href = (
                                href
                                .split("?")[0]
                                .split("#")[0]
                            )

                            # Ajouter le lien
                            devto_scraped_article_links.append(
                                clean_href
                            )


            # Supprimer les doublons
            devto_scraped_article_links = list(
                set(devto_scraped_article_links)
            )


            # Liste qui stockera les articles Dev.to
            devto_scraped_articles = []


            # Parcourir chaque article Dev.to
            for article_url in devto_scraped_article_links:

                try:

                    # Télécharger la page de l'article
                    article_response = requests.get(
                        article_url,
                        timeout=10
                    )

                    # Transformer le HTML en BeautifulSoup
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

                        # Transformer le titre en texte propre
                        article_title_clean = article_title.get_text(
                            " ",
                            strip=True
                        )

                        # Transformer le contenu en texte propre
                        article_content_clean = article_content.get_text(
                            " ",
                            strip=True
                        )

                        # Chercher la date de publication
                        article_date = article_soup.find(
                            "meta",
                            property="article:published_time"
                        )


                        # Récupérer la date si elle existe
                        if article_date:
                            article_date = article_date.get("content")

                        # Sinon garder une valeur vide
                        else:
                            article_date = ""


                        # Créer un dictionnaire vide
                        scraped_article = {}

                        # Ajouter la source
                        scraped_article["source"] = "Dev.to"

                        # Ajouter la catégorie
                        scraped_article["category"] = "General Tech"

                        # Le score sera calculé plus tard
                        scraped_article["relevance_score"] = 0

                        # Ajouter le titre
                        scraped_article["title"] = article_title_clean

                        # Ajouter le lien
                        scraped_article["link"] = article_url

                        # Ajouter la date
                        scraped_article["published"] = article_date

                        # Ajouter le contenu comme résumé
                        scraped_article["summary"] = article_content_clean


                        # Ajouter l'article à la liste Dev.to
                        devto_scraped_articles.append(
                            scraped_article
                        )


                # Si un article ne peut pas être téléchargé
                except requests.RequestException:

                    # Passer à l'article suivant
                    continue


            # Ajouter les articles Dev.to à la liste générale
            scraped_articles.extend(
                devto_scraped_articles
            )


        # Éviter que le programme s'arrête si le HTML change
        except Exception:
            pass


    # ❗❗❗ END SCRAPING DEV.TO ❗❗❗



    # ❗❗❗ SCRAPING SQL SERVER ❗❗❗

    # ---------- Télécharger SQL Server ----------

    # Essayer de télécharger la page du blog SQL Server
    try:
        sql_server_response = requests.get(
            SQL_SERVER_BLOG_URL,
            timeout=10
        )

    # Si la requête échoue
    except requests.RequestException:

        # Garder une valeur vide
        sql_server_response = None


    # ---------- Scraper SQL Server ----------

    # Continuer seulement si la page a été téléchargée
    if sql_server_response is not None:

        try:

            # Transformer le HTML SQL Server en BeautifulSoup
            sql_server_soup = BeautifulSoup(
                sql_server_response.text,
                "html.parser"
            )

            # Chercher tous les liens de la page SQL Server
            sql_server_links = sql_server_soup.find_all("a")

            # Liste qui stockera les liens uniques SQL Server
            sql_server_article_links = []


            # Parcourir tous les liens trouvés
            for link in sql_server_links:

                # Récupérer l'adresse du lien
                href = link.get("href")


                # Garder seulement les liens des articles SQL Server
                if href and "/blog/sqlserver/" in href:

                    # Transformer le lien relatif en URL complète
                    full_url = SQL_SERVER_BASE_URL + href


                    # Ajouter le lien seulement s'il n'est pas déjà présent
                    if full_url not in sql_server_article_links:

                        # Ajouter l'URL complète à la liste
                        sql_server_article_links.append(
                            full_url
                        )


            # Liste qui stockera les articles SQL Server complets
            sql_server_scraped_articles = []


            # Parcourir chaque article SQL Server
            for article_url in sql_server_article_links:

                try:

                    # Télécharger la page de l'article
                    article_response = requests.get(
                        article_url,
                        timeout=10
                    )

                    # Transformer le HTML en BeautifulSoup
                    article_soup = BeautifulSoup(
                        article_response.text,
                        "html.parser"
                    )

                    # Chercher le titre de l'article
                    article_title = article_soup.find("h1")

                    # Chercher le contenu principal
                    article_content = article_soup.find("article")


                    # Continuer seulement si titre et contenu existent
                    if article_title and article_content:

                        # Transformer le titre en texte propre
                        article_title_clean = article_title.get_text(
                            " ",
                            strip=True
                        )

                        # Transformer le contenu en texte propre
                        article_content_clean = article_content.get_text(
                            " ",
                            strip=True
                        )

                        # Chercher la date de publication
                        article_date = article_soup.find(
                            "meta",
                            property="article:published_time"
                        )


                        # Récupérer la date si elle existe
                        if article_date:
                            article_date = article_date.get("content")

                        # Sinon garder une valeur vide
                        else:
                            article_date = ""


                        # Créer un dictionnaire vide
                        scraped_article = {}

                        # Ajouter la source
                        scraped_article["source"] = (
                            "Microsoft SQL Server Blog"
                        )

                        # Ajouter la catégorie
                        scraped_article["category"] = "SQL Server"

                        # Le score sera calculé plus tard
                        scraped_article["relevance_score"] = 0

                        # Ajouter le titre
                        scraped_article["title"] = article_title_clean

                        # Ajouter le lien
                        scraped_article["link"] = article_url

                        # Ajouter la date
                        scraped_article["published"] = article_date

                        # Ajouter le contenu comme résumé
                        scraped_article["summary"] = (
                            article_content_clean
                        )


                        # Ajouter l'article SQL Server à la liste
                        sql_server_scraped_articles.append(
                            scraped_article
                        )


                # Si un article ne peut pas être téléchargé
                except requests.RequestException:

                    # Passer à l'article suivant
                    continue

            # Afficher le nombre d'articles SQL Server récupérés
            print(
                "Scraping SQL Server:",
                len(sql_server_scraped_articles)
            )           

            # Ajouter les articles SQL Server à la liste générale
            scraped_articles.extend(
                sql_server_scraped_articles
            )


        # Éviter que le programme s'arrête si le HTML change
        except Exception:
            pass


    # ❗❗❗ END SCRAPING SQL SERVER ❗❗❗



    # ---------- Retourner tous les articles scrapés ----------

    # Retourner .NET + Dev.to + SQL Server
    return scraped_articles


# ❗❗❗ END WEB SCRAPER ❗❗❗