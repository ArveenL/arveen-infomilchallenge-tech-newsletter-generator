# arveen-infomilchallenge-tech-newsletter-generator
'Automated tech newsletter generator' for the Infomil Technical Challenge.

## Résumé avec LLM

Après la collecte et la sélection (`python src/main.py`), cette étape indépendante
lit uniquement les 5 à 7 articles de `llm_input.json`. Elle ne relance pas la
collecte et produit `llm_summaries.json`, prêt pour la préparation de la newsletter.

```sh
python -m pip install -r requirements.txt
export OPENAI_MODEL="gpt-4.1-mini"
python src/llm_summary.py
```

Configurer aussi `OPENAI_API_KEY` dans `.env` ou dans l’environnement avant l’exécution,
sans inscrire sa valeur dans le code ni la versionner. `OPENAI_MODEL` est facultatif
et vaut `gpt-4.1-mini` par défaut. Les fichiers d’entrée et de sortie sont résolus
depuis la racine du projet. Le fichier `.env` à la racine est chargé automatiquement.
Les variables déjà définies dans l’environnement sont prioritaires.

### Choisir le niveau de résumé

Dans `.env`, choisir l’une des trois valeurs :

```dotenv
SUMMARY_LEVEL=accessible
```

| Niveau | Public et consignes |
| --- | --- |
| `technical` | Développeurs expérimentés : vocabulaire technique accepté, détails importants conservés. |
| `accessible` | Lecteurs avec quelques connaissances tech : termes importants expliqués simplement, jargon inutile évité, précision conservée. |
| `general` | Grand public / non-tech : vocabulaire simple, phrases courtes, termes indispensables expliqués, priorité à l’impact concret plutôt qu’à l’implémentation. |

Le niveau s’applique à `summary_fr` et à `why_it_matters_fr`. Sans variable,
le niveau par défaut est `accessible`. Une valeur vide ou inconnue produit une
erreur avant tout appel API ou écriture de résumés. Les sources, le scoring,
la sélection, l’ordre et les titres originaux restent identiques.

### MVP : génération avec OpenCode/ChatGPT

Pour l’étape manuelle actuellement utilisée par le MVP, afficher le prompt
correspondant au niveau configuré :

```sh
venv/bin/python src/llm_summary.py --print-prompt
```

Cette commande lit `SUMMARY_LEVEL` et affiche les mêmes consignes de rédaction
que la génération par API, complétées par le format JSON attendu. Elle n’appelle
pas OpenAI, ne nécessite pas de clé API et ne modifie aucun fichier.

Copier le prompt affiché dans OpenCode/ChatGPT et lui fournir `llm_input.json`
(en pièce jointe ou en lui demandant de lire le fichier dans le projet). Lui faire
créer `llm_summaries.json` conformément au prompt. Dans ChatGPT, enregistrer le JSON
retourné sous ce nom à la racine du projet. Ne pas joindre `.env` ni de clé API.

Après chaque changement de niveau, réafficher le prompt et régénérer les résumés.
Les résumés et newsletters déjà créés ne changent pas automatiquement.

### Génération par API OpenAI

Chaque article fait l’objet d’un appel OpenAI avec son contenu complet. Le fichier
de sortie conserve l’ordre et les métadonnées exactes (`title`, `source`, `topic`,
`published`, `link`), avec `summary_fr` et `why_it_matters_fr`.
Une réponse tronquée, vide ou ne respectant pas les deux sections attendues est
considérée comme invalide. Un échec laisse les deux champs vides et ajoute `error`,
sans interrompre le traitement des autres articles. Le script affiche les erreurs
et les compteurs, et retourne un code non nul si une erreur survient.

Avant d’utiliser les résumés, vérifier le nombre d’entrées, l’absence d’erreurs et
relire chaque texte pour contrôler le français et la fidélité à l’article fourni.
Ces deux derniers contrôles sont éditoriaux : le script ne certifie pas la langue
ni l’absence d’inventions. Cette étape ne publie rien et n’intègre pas Ghost.
