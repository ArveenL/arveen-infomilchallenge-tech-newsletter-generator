from bs4 import BeautifulSoup
from markdownify import markdownify


def clean_text(text):
    """Nettoyer les métadonnées sur une ligne."""
    return " ".join(str(text or "").split())


def clean_content(text):
    """Conserver les paragraphes et l'indentation du Markdown existant."""
    return str(text or "").replace("\r\n", "\n").replace("\r", "\n").strip("\n")


def html_to_markdown(html):
    """Convertir uniquement le corps fourni, sans scripts ni contrôles UI."""
    soup = BeautifulSoup(str(html or ""), "html.parser")
    for element in soup.select(
        "script, style, button, form, input, select, textarea, "
        ".highlight__panel, .copy-code-button, .anchor"
    ):
        element.decompose()
    return clean_content(markdownify(str(soup), heading_style="ATX"))


def make_summary(content):
    """Un extrait court, distinct du corps complet."""
    return clean_text(content)[:400]


def clean_articles(articles):
    """Dédupliquer par URL en conservant le contenu le plus riche."""
    by_link = {}
    for article in articles:
        cleaned = dict(article)
        for field in ("source", "category", "title", "link", "published"):
            cleaned[field] = clean_text(cleaned.get(field))
        link = cleaned["link"].split("?")[0].split("#")[0].rstrip("/")
        if not link:
            continue
        cleaned["link"] = link
        cleaned["content"] = clean_content(
            cleaned.get("content") or cleaned.get("summary", "")
        )
        cleaned["summary"] = make_summary(
            cleaned.get("summary") or cleaned["content"]
        )
        existing = by_link.get(link)
        if existing is None:
            by_link[link] = cleaned
            continue
        # La longueur du corps est un critère MVP simple, indépendant de l'ordre.
        if len(cleaned["content"]) > len(existing["content"]):
            existing["content"] = cleaned["content"]
        for field in ("source", "category", "title", "published", "summary"):
            if not existing.get(field):
                existing[field] = cleaned[field]
    return list(by_link.values())
