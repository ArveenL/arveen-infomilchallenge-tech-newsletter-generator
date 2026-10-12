New project tree
src/
│
├── main.py
├── rss.py
├── github.py
├── scraper.py
├── cleaning.py
├── scoring.py
├── selection.py
└── output.py
What each file does
- rss.py: Fetches Microsoft .NET and Dev.to RSS feeds (feedparser), converts entries to common article structure, extracts title/link/published/summary (cleaned from HTML). Exports get_rss_articles().
- github.py: Calls GitHub Releases API for dotnet/core, angular/angular, facebook/react with 10s timeout; filters .NET 10 (names starting .NET 10), Angular 22 (names starting 22.), React 19 (names starting 19.); converts to common structure. Exports get_github_articles().
- scraper.py: Scrapes devblogs.microsoft.com/dotnet/ and dev.to/, collects/filters real article links, deduplicates (sets), extracts title (h1), content (article), publication date (article:published_time), handles request timeouts/errors. Exports get_scraped_articles().
- cleaning.py: Deduplicates by normalized URL (strip query/fragment, trailing slash), cleans strings (strip, collapse spaces), handles None. Exports clean_articles(articles).
- scoring.py: Detects topics (.NET/Angular/React/SQL Server/IA Générative) and preserves existing category fallback; computes relevance scores with keyword weights (including title bonus); returns scored articles. Exports score_articles(articles). Also keeps original keyword set unchanged.
- selection.py: Filters articles with relevance_score > 0, sorts by score desc; selects up to 7 with max 2 per topic (fills remaining if diversity blocks reaching 7). Exports select_articles(articles).
- output.py: Adds id to all articles (incremental), selection_id to selected; writes articles.json, selected_articles.json, newsletter_preview.md (preserves preview format/truncation); prints pipeline stats and selected articles with topic/score/source/link. Exports save_results(articles, selected_articles).
- main.py: Orchestrator (keeps French headers/comments where helpful), imports from modules, runs pipeline: get RSS/GitHub/scraped → combine → clean → score → select → save_results.
Changes to original logic
- Minimal restructuring only. Moved code to modules preserving all logic, URLs, filtering rules, keywords, diversity rule (max 2 per topic, up to 7). No features removed/added.
- Scraper resilience (defensive): Wrapped network calls/parsing in try-except blocks so one failed scrape doesn’t crash whole pipeline (matches original behavior intent of continuing on RequestException; also guards response parsing). This is a safe refactor improvement, doesn’t alter selection/filtering.
- No circular imports: Modules depend on stdlib/third-party libs only; main orchestrates. 
- Behavior preserved: Same data sources, same outputs format, same counts/selection logic.
Running result
$ python3 src/main.py
🕺🏽 Infomil Tech Newsletter Generator 🫈

Articles pertinents: 84
Articles sélectionnés: 7

1. What LLMs 'Know' That You Don't Know They Know: Stop Inventing Prompt DSLs and Ride 50 Years of Unix Pre-Training Gravity
   Thème: React
   Score: 25
   Source: Dev.to
   Lien: https://dev.to/gde/what-llms-know-that-you-dont-know-they-know-stop-inventing-prompt-dsls-and-ride-50-years-of-2bl6
...
✅ articles.json créé
✅ selected_articles.json créé
✅ newsletter_preview.md créé
✅ Pipeline terminé avec succès.
Confirmed generated files
- articles.json (702K) ✓
- selected_articles.json (133K) ✓  
- newsletter_preview.md (4.6K) ✓
The program still runs as python3 src/main.py from repo root and produces all three files with reasonable article counts and correct selected articles.