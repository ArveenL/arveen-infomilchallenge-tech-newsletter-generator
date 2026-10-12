# ❗❗❗ IMPORTS ❗❗❗

from rss import get_rss_articles
from github import get_github_articles
from scraper import get_scraped_articles
from cleaning import clean_articles
from scoring import score_articles
from selection import select_articles
from output import save_results


# ❗❗❗ MAQUILLAGE / AFFICHAGE ❗❗❗

# Afficher le nom du programme
print("🕺🏽 Infomil Tech Newsletter Generator 🫈")
print()


# ❗❗❗ PIPELINE PRINCIPAL ❗❗❗

# Récupérer les articles depuis toutes les sources
rss_articles = get_rss_articles()

github_articles = get_github_articles()

scraped_articles = get_scraped_articles()


# Regrouper tous les articles
articles = (
    rss_articles
    + github_articles
    + scraped_articles
)


# Nettoyer et dédupliquer les articles
articles = clean_articles(articles)

# Calculer les scores et détecter les thèmes
articles = score_articles(articles)

# Sélectionner les articles pour la newsletter
selected_articles = select_articles(articles)

# Sauvegarder les résultats et afficher le résumé
save_results(
    articles,
    selected_articles
)


# ❗❗❗ END PIPELINE PRINCIPAL ❗❗❗
