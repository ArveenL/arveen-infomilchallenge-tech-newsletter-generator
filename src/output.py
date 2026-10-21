# ❗❗❗ IMPORTS ❗❗❗

# Créer et écrire du JSON
import json
from pathlib import Path


# ❗❗❗ OUTPUT ❗❗❗

def generate_newsletter():
    """Générer la newsletter finale à partir des résumés français validés."""
    project_root = Path(__file__).resolve().parent.parent
    with (project_root / "llm_summaries.json").open(encoding="utf-8") as file:
        summaries = json.load(file)

    newsletter = "# Lettre d’actualité technologique Infomil\n\n"
    newsletter += (
        "Retrouvez notre sélection d’actualités du développement logiciel, "
        "avec des résumés techniques en français et les points à retenir "
        "pour votre pratique.\n\n"
    )
    for index, article in enumerate(summaries, start=1):
        if not all(
            isinstance(article.get(field), str) and article[field].strip()
            for field in ("summary_fr", "why_it_matters_fr")
        ):
            raise ValueError(f"Article {index} : résumé français incomplet")
        newsletter += (
            f"## {index}. {article['title']}\n\n"
            f"**Thème :** {article['topic']}\n\n"
            f"**Source :** {article['source']}\n\n"
            f"**Date de publication :** {article['published']}\n\n"
            f"{article['summary_fr']}\n\n"
            f"**Pourquoi c’est important**\n\n"
            f"{article['why_it_matters_fr']}\n\n"
            f"[Lire l’article complet]({article['link']})\n\n"
            "---\n\n"
        )
    newsletter += "Bonne lecture et à bientôt pour une nouvelle sélection technologique.\n"
    output_path = project_root / "newsletter.md"
    output_path.write_text(newsletter, encoding="utf-8")
    return output_path


def save_results(articles, selected_articles):
    """
    Manage article IDs, create articles.json, selected_articles.json,
    newsletter_preview.md, and print final results and statistics.
    """
    # Ajouter les IDs pour tous les articles
    article_id = 1
    for article in articles:
        article["id"] = article_id
        article_id += 1

    # Ajouter les IDs pour les articles sélectionnés
    selection_id = 1
    for article in selected_articles:
        article["selection_id"] = selection_id
        selection_id += 1

    # Sauvegarder tous les articles
    with open(
        "articles.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            articles,
            file,
            indent=4,
            ensure_ascii=False
        )

    # Sauvegarder la sélection
    with open(
        "selected_articles.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            selected_articles,
            file,
            indent=4,
            ensure_ascii=False
        )

    # Export minimal : uniquement les articles de la sélection finale.
    llm_input = [
        {
            "title": article.get("title", ""),
            "source": article.get("source", ""),
            "topic": article.get("topic", ""),
            "published": article.get("published", ""),
            "link": article.get("link", ""),
            "content": article.get("content", ""),
        }
        for article in selected_articles
    ]
    with open("llm_input.json", "w", encoding="utf-8") as file:
        json.dump(llm_input, file, indent=4, ensure_ascii=False)

    # Préparer le Markdown
    newsletter = "# Lettre d’actualité technologique Infomil\n\n"
    newsletter += (
        "Sélection automatique des actualités "
        "technologiques les plus pertinentes.\n\n"
    )

    # Ajouter les articles
    for article in selected_articles:
        preview = article.get("summary", "")[:400]
        newsletter += (
            f"## {article.get('selection_id', '')}. "
            f"{article.get('title', '')}\n\n"
        )
        newsletter += (
            f"**Thème :** {article.get('topic', '')}\n\n"
        )
        newsletter += (
            f"**Source :** {article.get('source', '')}\n\n"
        )
        newsletter += (
            f"**Score :** "
            f"{article.get('relevance_score', '')}\n\n"
        )
        newsletter += (
            f"**Date :** "
            f"{article.get('published', '')}\n\n"
        )
        newsletter += (
            f"{preview}...\n\n"
        )
        newsletter += (
            f"{article.get('link', '')}\n\n"
        )
        newsletter += "---\n\n"

    # Sauvegarder le preview
    with open(
        "newsletter_preview.md",
        "w",
        encoding="utf-8"
    ) as file:
        file.write(newsletter)

    # Afficher les résultats
    print()
    print("========================================")
    print("         RÉSULTAT DU PIPELINE")
    print("========================================")

    # Compter les articles pertinents pour affichage
    relevant_articles_for_display = [
        a for a in articles if a.get("relevance_score", 0) > 0
    ]

    print(
        "Articles collectés:",
        len(articles)
    )
    print(
        "Articles pertinents:",
        len(relevant_articles_for_display)
    )
    print(
        "Articles sélectionnés:",
        len(selected_articles)
    )
    print()

    for article in selected_articles:
        print(
            f"{article.get('selection_id', '')}. "
            f"{article.get('title', '')}"
        )
        print(
            "   Thème:",
            article.get("topic", "")
        )
        print(
            "   Score:",
            article.get("relevance_score", "")
        )
        print(
            "   Source:",
            article.get("source", "")
        )
        print(
            "   Lien:",
            article.get("link", "")
        )
        print()

    print("✅ articles.json créé")
    print("✅ selected_articles.json créé")
    print("✅ llm_input.json créé")
    print("✅ newsletter_preview.md créé")
    print()
    print(
        "✅ Pipeline terminé avec succès."
    )


# ❗❗❗ END OUTPUT ❗❗❗

if __name__ == "__main__":
    print(f"✅ {generate_newsletter().name} créé")
