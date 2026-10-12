# ❗❗❗ NETTOYAGE DES DONNÉES ❗❗❗

# ---------- Fonction de nettoyage ----------

# Nettoyer une valeur texte
def clean_text(text):
    # Si la valeur est vide
    if text is None:
        return ""

    # Transformer en texte
    text = str(text)

    # Retirer les espaces inutiles
    text = text.strip()

    # Remplacer plusieurs espaces par un seul
    text = " ".join(text.split())

    # Retourner le résultat
    return text


# ---------- Dédoublonner et nettoyer les articles ----------

def clean_articles(articles):
    """
    Deduplicate articles by normalized URL, clean strings, handle None values.
    """
    # Déduplication
    unique_articles = []
    seen_links = set()

    # Copier et nettoyer les liens
    processed_articles = []
    for article in articles:
        # Créer une copie pour éviter de modifier l'original si nécessaire
        article_copy = dict(article)
        link = article_copy.get("link", "")
        if link:
            # Retirer ? et # du lien
            link_cleaned = link.split("?")[0].split("#")[0]
            # Retirer le / final
            link_cleaned = link_cleaned.rstrip("/")
            article_copy["link"] = link_cleaned
        else:
            article_copy["link"] = ""
        processed_articles.append(article_copy)

    # Vérifier les doublons
    for article in processed_articles:
        link = article["link"]
        if link and link not in seen_links:
            unique_articles.append(article)
            seen_links.add(link)

    # Nettoyer les champs texte
    for article in unique_articles:
        article["source"] = clean_text(
            article["source"]
        )
        article["category"] = clean_text(
            article["category"]
        )
        article["title"] = clean_text(
            article["title"]
        )
        article["link"] = clean_text(
            article["link"]
        )
        article["published"] = clean_text(
            article["published"]
        )
        article["summary"] = clean_text(
            article["summary"]
        )

    return unique_articles


# ❗❗❗ END NETTOYAGE DES DONNÉES ❗❗❗
