# ❗❗❗ IMPORTS ❗❗❗

# Télécharger des données depuis Internet
import requests


# ❗❗❗ GITHUB RELEASES API ❗❗❗

# ---------- URLs des API GitHub Releases ----------

# Adresse des releases .NET
DOTNET_GITHUB_RELEASES_URL = "https://api.github.com/repos/dotnet/core/releases"

# Adresse des releases Angular
ANGULAR_GITHUB_RELEASES_URL = "https://api.github.com/repos/angular/angular/releases"

# Adresse des releases React
REACT_GITHUB_RELEASES_URL = "https://api.github.com/repos/facebook/react/releases"


# ---------- Obtenir les articles GitHub ----------

def get_github_articles():
    """
    Fetch GitHub Releases API for .NET, Angular, and React releases.
    Filter .NET 10, Angular 22, and React 19.
    Convert releases into common article structure.
    """
    # Demander les releases .NET à GitHub
    dotnet_response = requests.get(
        DOTNET_GITHUB_RELEASES_URL,
        timeout=10
    )

    # Demander les releases Angular à GitHub
    angular_response = requests.get(
        ANGULAR_GITHUB_RELEASES_URL,
        timeout=10
    )

    # Demander les releases React à GitHub
    react_response = requests.get(
        REACT_GITHUB_RELEASES_URL,
        timeout=10
    )

    # Transformer la réponse en données Python
    dotnet_releases = dotnet_response.json()
    angular_releases = angular_response.json()
    react_releases = react_response.json()

    # Préparer les listes filtrées
    dotnet10_releases = []
    angular22_releases = []
    react_filtered_releases = []

    # Filtrer .NET 10
    for release in dotnet_releases:
        if release["name"].startswith(".NET 10"):
            dotnet10_releases.append(release)

    # Filtrer Angular 22
    for release in angular_releases:
        if release["name"].startswith("22."):
            angular22_releases.append(release)

    # Filtrer React 19
    for release in react_releases:
        if release["name"].startswith("19."):
            react_filtered_releases.append(release)

    # Structurer .NET 10
    dotnet10_articles = []
    for release in dotnet10_releases:
        release_data = {}
        release_data["source"] = "GitHub Releases"
        release_data["category"] = ".NET"
        release_data["relevance_score"] = 0
        release_data["title"] = release.get("name", "")
        release_data["link"] = release.get("html_url", "")
        release_data["published"] = release.get(
            "published_at",
            ""
        )
        release_data["summary"] = release.get(
            "body",
            ""
        )
        dotnet10_articles.append(release_data)

    # Structurer Angular 22
    angular_articles = []
    for release in angular22_releases:
        release_data = {}
        release_data["source"] = "GitHub Releases"
        release_data["category"] = "Angular"
        release_data["relevance_score"] = 0
        release_data["title"] = release.get("name", "")
        release_data["link"] = release.get("html_url", "")
        release_data["published"] = release.get(
            "published_at",
            ""
        )
        release_data["summary"] = release.get(
            "body",
            ""
        )
        angular_articles.append(release_data)

    # Structurer React 19
    react_articles = []
    for release in react_filtered_releases:
        release_data = {}
        release_data["source"] = "GitHub Releases"
        release_data["category"] = "React"
        release_data["relevance_score"] = 0
        release_data["title"] = release.get("name", "")
        release_data["link"] = release.get("html_url", "")
        release_data["published"] = release.get(
            "published_at",
            ""
        )
        release_data["summary"] = release.get(
            "body",
            ""
        )
        react_articles.append(release_data)

    return dotnet10_articles + angular_articles + react_articles


# ❗❗❗ END GITHUB RELEASES API ❗❗❗
