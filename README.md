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

Configurer aussi `OPENAI_API_KEY` dans l’environnement avant l’exécution, sans
inscrire sa valeur dans le code ni la versionner. `OPENAI_MODEL` est facultatif
et vaut `gpt-4.1-mini` par défaut. Les fichiers d’entrée et de sortie sont résolus
depuis la racine du projet. Un éventuel fichier `.env` n’est pas chargé automatiquement.

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
