# ❗❗❗ DÉTECTION DES THÈMES ❗❗❗

# ---------- Mots-clés par thème ----------

# Regrouper les mots-clés qui permettent d'identifier chaque thème
TOPIC_KEYWORDS = {
    ".NET": [
        ".net 10",
        "dotnet 10",
        "c#",
        "asp.net",
        "ef core"
    ],

    "Angular": [
        "angular 22",
        "angular"
    ],

    "React": [
        "react 19",
        "react"
    ],

    "SQL Server": [
        "sql server",
        "azure sql",
        "sql database"
    ],

    "IA Générative": [
        "generative ai",
        "artificial intelligence",
        "llm",
        "large language model",
        "prompt engineering",
        "openai",
        "ai agent",
        "ai agents"
    ]
}


# ---------- Fonction pour vérifier le mot AI ----------

# Vérifier si "ai" apparaît comme un mot complet
def contains_ai(text):

    # Ajouter des espaces autour du texte pour faciliter la recherche
    text = f" {text.lower()} "

    # Chercher " ai " pour éviter des faux résultats comme "training"
    return " ai " in text


# ---------- Fonction pour trouver le thème ----------

# Déterminer le thème principal d'un article
def detect_topic(article):

    # Récupérer le titre en minuscules
    title = article.get(
        "title",
        ""
    ).lower()

    # Récupérer le résumé en minuscules
    summary = (article.get("content") or article.get("summary", "")).lower()

    # Récupérer la catégorie d'origine
    category = article.get(
        "category",
        ""
    )

    # Garder temporairement la catégorie comme thème par défaut
    best_topic = category

    # Garder le meilleur score de thème
    best_score = 0


    # Parcourir chaque thème
    for topic, keywords in TOPIC_KEYWORDS.items():

        # Commencer le score du thème à 0
        topic_score = 0


        # Parcourir les mots-clés du thème
        for keyword in keywords:

            # Donner plus d'importance au titre
            if keyword in title:

                # Ajouter 3 points si le mot est dans le titre
                topic_score += 3

            # Sinon vérifier le résumé
            elif keyword in summary:

                # Ajouter 1 point si le mot est seulement dans le résumé
                topic_score += 1


        # ---------- Détection spéciale du mot AI ----------

        # Faire cette vérification seulement pour le thème IA
        if topic == "IA Générative":

            # Donner 3 points si AI apparaît comme mot complet dans le titre
            if contains_ai(title):
                topic_score += 3

            # Sinon donner 1 point si AI apparaît dans le résumé
            elif contains_ai(summary):
                topic_score += 1


        # ---------- Bonus pour la catégorie d'origine ----------

        # Favoriser le thème correspondant à la source déjà connue
        if category == topic:

            # Ajouter un bonus pour conserver le contexte de la source
            topic_score += 4


        # ---------- Comparer avec le meilleur thème ----------

        # Vérifier si ce thème obtient un meilleur score
        if topic_score > best_score:

            # Garder ce nouveau meilleur score
            best_score = topic_score

            # Garder ce nouveau meilleur thème
            best_topic = topic


    # Retourner le thème ayant obtenu le meilleur score
    return best_topic


# ❗❗❗ END DÉTECTION DES THÈMES ❗❗❗



# ❗❗❗ SCORING ❗❗❗

# ---------- Mots-clés prioritaires ----------

# Donner un poids aux sujets importants
KEYWORDS = {
    ".net 10": 5,
    "dotnet 10": 5,
    "c#": 3,
    "asp.net": 3,
    "ef core": 3,

    "angular 22": 5,
    "angular": 3,

    "react 19": 4,
    "react": 2,

    "sql server": 5,
    "azure sql": 4,
    "sql database": 4,

    "generative ai": 5,
    "artificial intelligence": 4,
    "llm": 5,
    "large language model": 5,
    "prompt engineering": 5,
    "openai": 3,
    "ai agent": 4,
    "ai agents": 4
}


# ---------- Calculer le score ----------

# Calculer la pertinence d'un article
def calculate_score(article):

    # Commencer le score à 0
    score = 0

    # Récupérer le titre en minuscules
    title = article.get(
        "title",
        ""
    ).lower()

    # Récupérer le résumé en minuscules
    summary = (article.get("content") or article.get("summary", "")).lower()


    # ---------- Chercher les mots-clés ----------

    # Parcourir tous les mots-clés importants
    for keyword, points in KEYWORDS.items():

        # Vérifier si le mot-clé apparaît dans le titre
        if keyword in title:

            # Le titre est important : multiplier le poids par 3
            score += points * 3

        # Sinon vérifier le résumé
        elif keyword in summary:

            # Ajouter le poids normal
            score += points


    # ---------- Donner un score au mot AI ----------

    # Vérifier AI comme mot complet dans le titre
    if contains_ai(title):

        # Donner un bonus important au titre
        score += 9

    # Sinon vérifier AI dans le résumé
    elif contains_ai(summary):

        # Donner un plus petit bonus au résumé
        score += 3


    # ---------- Retourner le résultat ----------

    # Retourner le score final
    return score


# ---------- Scorer et détecter les thèmes des articles ----------

# Ajouter un thème et un score à chaque article
def score_articles(articles):

    # Liste qui contiendra les articles scorés
    scored_articles = []


    # Parcourir tous les articles
    for article in articles:

        # Faire une copie pour ne pas modifier l'article original
        article_copy = dict(article)


        # Détecter le thème principal
        article_copy["topic"] = detect_topic(
            article_copy
        )


        # Calculer le score de pertinence
        article_copy["relevance_score"] = calculate_score(
            article_copy
        )


        # Ajouter l'article terminé à la liste
        scored_articles.append(
            article_copy
        )


    # Retourner tous les articles avec thème et score
    return scored_articles


# ❗❗❗ END SCORING ❗❗❗
