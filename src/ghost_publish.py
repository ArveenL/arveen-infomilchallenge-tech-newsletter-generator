"""Créer un brouillon Ghost à partir de newsletter.html, sans publication."""

import base64
import hashlib
import hmac
import json
import os
from pathlib import Path
import sys
import time
from urllib.parse import urlsplit

from dotenv import load_dotenv
import requests


PROJECT_ROOT = Path(__file__).resolve().parent.parent
TITLE = "Lettre d’actualité technologique Infomil"


def create_token(api_key):
    """Signer un JWT HS256 valable cinq minutes pour Ghost Admin API."""
    try:
        key_id, secret = api_key.split(":", 1)
        secret_bytes = bytes.fromhex(secret)
        if not key_id or not secret_bytes:
            raise ValueError
    except ValueError:
        raise ValueError("GHOST_ADMIN_API_KEY doit être au format identifiant:secret_hex.") from None

    def encode(value):
        return base64.urlsafe_b64encode(value).rstrip(b"=")

    now = int(time.time())
    header = {"alg": "HS256", "typ": "JWT", "kid": key_id}
    payload = {"iat": now, "exp": now + 300, "aud": "/admin/"}
    unsigned = b".".join(
        encode(json.dumps(part, separators=(",", ":")).encode("utf-8"))
        for part in (header, payload)
    )
    signature = hmac.new(secret_bytes, unsigned, hashlib.sha256).digest()
    return (unsigned + b"." + encode(signature)).decode("ascii")


def main():
    load_dotenv(PROJECT_ROOT / ".env")
    api_url = os.getenv("GHOST_ADMIN_API_URL", "").strip().rstrip("/")
    api_key = os.getenv("GHOST_ADMIN_API_KEY", "").strip()

    try:
        if not api_url or not api_key:
            raise ValueError("Renseignez GHOST_ADMIN_API_URL et GHOST_ADMIN_API_KEY dans .env.")
        parsed_url = urlsplit(api_url)
        if (
            parsed_url.scheme not in {"http", "https"}
            or not parsed_url.hostname
            or parsed_url.username is not None
            or parsed_url.password is not None
            or parsed_url.query
            or parsed_url.fragment
        ):
            raise ValueError("GHOST_ADMIN_API_URL doit être une URL HTTP(S) sans identifiants ni paramètres.")
        html = (PROJECT_ROOT / "newsletter.html").read_text(encoding="utf-8")
        if not html.strip():
            raise ValueError("newsletter.html est vide.")
        token = create_token(api_key)
    except (OSError, UnicodeError):
        print("Erreur : impossible de lire newsletter.html en UTF-8.", file=sys.stderr)
        return 1
    except ValueError as error:
        print(f"Erreur : {error}", file=sys.stderr)
        return 1

    # Un seul appel, sans redirection ni nouvelle tentative automatique.
    # Aucun paramètre de publication ou d'envoi d'e-mail n'est transmis.
    try:
        response = requests.post(
            f"{api_url}/ghost/api/admin/posts/",
            params={"source": "html"},
            headers={"Authorization": f"Ghost {token}"},
            json={"posts": [{"title": TITLE, "html": html, "status": "draft"}]},
            timeout=30,
            allow_redirects=False,
        )
    except requests.Timeout:
        print("Erreur : délai de réponse Ghost dépassé. Vérifiez dans Ghost si le brouillon a été créé avant de relancer.", file=sys.stderr)
        return 1
    except requests.RequestException:
        print("Erreur : connexion à Ghost impossible. Vérifiez son adresse et que le serveur est démarré.", file=sys.stderr)
        return 1

    if not 200 <= response.status_code < 300:
        # Ne pas afficher le corps HTTP ou les en-têtes : ils peuvent contenir des secrets.
        print(f"Erreur HTTP {response.status_code} : Ghost n’a pas confirmé la création du brouillon.", file=sys.stderr)
        return 1

    try:
        post = response.json()["posts"][0]
        if post["status"] != "draft":
            raise ValueError
        title = post["title"]
    except (ValueError, KeyError, IndexError, TypeError):
        print("Erreur : réponse Ghost inattendue ; création en statut draft non confirmée. Vérifiez dans Ghost avant de relancer.", file=sys.stderr)
        return 1

    print("Succès : brouillon Ghost créé (statut : draft).")
    print(f"Titre : {title}")
    if post.get("id"):
        print(f"ID : {post['id']}")
    if post.get("url"):
        print(f"URL : {post['url']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
