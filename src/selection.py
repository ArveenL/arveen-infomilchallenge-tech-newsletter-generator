# ❗❗❗ FILTRAGE ❗❗❗

# ---------- Garder seulement les articles pertinents ----------

# Garder uniquement les articles avec un score supérieur à 0
def filter_relevant_articles(articles):

    # Liste qui contiendra les articles pertinents
    relevant_articles = []


    # Parcourir tous les articles
    for article in articles:

        # Récupérer le score de l'article
        score = article.get(
            "relevance_score",
            0
        )

        # Vérifier si l'article a obtenu au moins 1 point
        if score > 0:

            # Ajouter l'article à la liste des articles pertinents
            relevant_articles.append(article)


    # Retourner seulement les articles pertinents
    return relevant_articles


# ❗❗❗ END FILTRAGE ❗❗❗



# ❗❗❗ CLASSEMENT ❗❗❗

# ---------- Vérifier si une release est une pré-version ----------

# Détecter les versions next, beta, alpha ou release candidate
def is_prerelease(article):

    # Récupérer le titre en minuscules
    title = article.get(
        "title",
        ""
    ).lower()


    # Liste des mots indiquant une pré-version
    prerelease_words = [
        "next",
        "beta",
        "alpha",
        "rc"
    ]


    # Parcourir les mots de pré-version
    for word in prerelease_words:

        # Vérifier si le mot apparaît dans le titre
        if word in title:

            # L'article est une pré-version
            return True


    # Sinon l'article est considéré comme stable
    return False


# ---------- Trier les articles par score ----------

# Mettre les articles les plus intéressants en premier
def sort_by_score(articles):

    # Faire une copie de la liste
    sorted_articles = list(articles)


    # Trier la liste
    sorted_articles.sort(

        # Trier d'abord par stabilité puis par score
        key=lambda article: (

            # Une version stable passe avant une pré-version
            is_prerelease(article),

            # Un gros score passe avant un petit score
            -article.get(
                "relevance_score",
                0
            )
        )
    )


    # Retourner les articles triés
    return sorted_articles


# ❗❗❗ END CLASSEMENT ❗❗❗



# ❗❗❗ SÉLECTION NEWSLETTER ❗❗❗

# ---------- Thèmes prioritaires ----------

# Thèmes que la newsletter doit essayer de représenter
PRIORITY_TOPICS = [
    ".NET",
    "Angular",
    "React",
    "SQL Server",
    "IA Générative"
]


# ---------- Sélectionner les articles ----------

# Sélectionner entre 5 et 7 articles avec une bonne diversité
def select_articles(articles):

    # Garder seulement les articles pertinents
    relevant_articles = filter_relevant_articles(
        articles
    )

    # Trier les articles du meilleur au moins bon
    relevant_articles = sort_by_score(
        relevant_articles
    )


    # Liste finale des articles sélectionnés
    selected_articles = []


    # Compter combien d'articles ont été sélectionnés par thème
    topic_counts = {}


    # ---------- Étape 1 : représenter les thèmes prioritaires ----------

    # Parcourir chaque thème prioritaire
    for priority_topic in PRIORITY_TOPICS:

        # Chercher le meilleur article disponible pour ce thème
        for article in relevant_articles:

            # Récupérer le thème de l'article
            topic = article.get(
                "topic",
                ""
            )


            # Vérifier si l'article appartient au thème recherché
            if topic == priority_topic:

                # Vérifier qu'il n'est pas déjà sélectionné
                if article not in selected_articles:

                    # Ajouter l'article
                    selected_articles.append(article)

                    # Compter un article pour ce thème
                    topic_counts[topic] = 1

                    # Passer au prochain thème prioritaire
                    break


    # ---------- Étape 2 : compléter jusqu'à 7 articles ----------

    # Parcourir les articles classés
    for article in relevant_articles:

        # Arrêter dès que 7 articles sont sélectionnés
        if len(selected_articles) == 7:
            break


        # Ne pas reprendre un article déjà sélectionné
        if article in selected_articles:
            continue


        # Récupérer le thème
        topic = article.get(
            "topic",
            ""
        )


        # Récupérer le nombre déjà sélectionné pour ce thème
        count = topic_counts.get(
            topic,
            0
        )


        # Garder maximum 2 articles du même thème
        if count < 2:

            # Ajouter l'article
            selected_articles.append(article)

            # Ajouter 1 au compteur du thème
            topic_counts[topic] = count + 1


    # ---------- Étape 3 : sécurité si moins de 5 articles ----------

    # Si la sélection contient moins de 5 articles
    if len(selected_articles) < 5:

        # Parcourir à nouveau les articles pertinents
        for article in relevant_articles:

            # Vérifier que l'article n'est pas déjà sélectionné
            if article not in selected_articles:

                # Ajouter l'article
                selected_articles.append(article)


            # Arrêter dès que nous avons au moins 5 articles
            if len(selected_articles) == 5:
                break


    # ---------- Retourner la sélection ----------

    # Retourner entre 5 et 7 articles
    return selected_articles


# ❗❗❗ END SÉLECTION NEWSLETTER ❗❗❗