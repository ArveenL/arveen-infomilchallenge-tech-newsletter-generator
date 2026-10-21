# Lettre d’actualité technologique Infomil

Retrouvez notre sélection d’actualités du développement logiciel, avec des résumés techniques en français et les points à retenir pour votre pratique.

## 1. Bring Your Own Model to the GitHub Copilot SDK with C#

**Thème :** .NET

**Source :** Microsoft .NET Blog

**Date de publication :** Mon, 19 Oct 2026 16:00:00 +0000

Microsoft montre comment créer une application qui utilise les outils de GitHub Copilot tout en choisissant le service d’intelligence artificielle chargé de répondre. Le modèle, c’est le programme qui produit les réponses. Dans cet exemple, il est hébergé sur Microsoft Foundry. Copilot continue d’organiser les échanges, mais les questions sont envoyées au fournisseur choisi. L’application commence par un test simple : poser une question, sans autoriser d’autres actions. La connexion utilise de préférence un compte Microsoft Entra ID. Une clé d’accès reste possible et doit être conservée en dehors du code.

**Pourquoi c’est important**

Une équipe peut garder les outils de Copilot tout en choisissant le service d’IA utilisé. L’exemple permet de vérifier que la connexion fonctionne avant de donner davantage de capacités à l’assistant.

[Lire l’article complet](https://devblogs.microsoft.com/dotnet/bring-your-own-model-to-the-github-copilot-sdk-with-csharp)

---

## 2. 22.2.3

**Thème :** Angular

**Source :** GitHub Releases

**Date de publication :** 2026-10-14T23:38:58Z

Angular, un outil utilisé pour construire des applications web, reçoit une mise à jour corrective. La version 22.2.3 renforce des protections contre la modification indésirable de certains objets internes du programme. Elle corrige aussi plusieurs erreurs dans la préparation et l’exécution des pages. Certains correctifs concernent les animations ou les situations où plusieurs applications fonctionnent ensemble. Les formulaires évitent désormais de lancer systématiquement une vérification des changements quand on quitte un champ. Enfin, la gestion du passage entre les pages vérifie plus tôt si une opération a déjà été annulée.

**Pourquoi c’est important**

Ces corrections visent la sécurité et la fiabilité des applications web utilisant Angular. Elles limitent aussi certaines vérifications inutiles lors de l’utilisation des formulaires.

[Lire l’article complet](https://github.com/angular/angular/releases/tag/v22.2.3)

---

## 3. 19.3.0 (September 9, 2026)

**Thème :** React

**Source :** GitHub Releases

**Date de publication :** 2026-09-09T18:01:33Z

React sert à construire les interfaces des sites et applications. Sa version 19.3.0 ajoute des outils pour animer les changements à l’écran. Elle permet aussi de réserver certaines parties d’une page au navigateur, plutôt que de les préparer sur le serveur qui héberge le site. Les mises à jour d’affichage deviennent plus indépendantes : une opération lente ne bloque plus les autres opérations sans rapport. Cette version corrige également de nombreux problèmes de fonctionnement. Elle améliore le traitement des données échangées avec le serveur et renforce les protections contre certains blocages et tentatives de surcharge.

**Pourquoi c’est important**

Ces nouveautés donnent aux équipes davantage de moyens pour rendre les interfaces fluides et fiables. Les corrections concernent aussi la préparation des pages sur le serveur et les échanges nécessaires à leur affichage.

[Lire l’article complet](https://github.com/react/react/releases/tag/v19.3.0)

---

## 4. Introducing sqlsimtools

**Thème :** SQL Server

**Source :** Microsoft SQL Server Blog

**Date de publication :** 2026-10-14T05:19:22.512-07:00

sqlsimtools est un ensemble gratuit d’outils dont le code est accessible publiquement. Il permet de tester des bases de données, les systèmes qui organisent et stockent les informations des applications. Il simule notamment les demandes de nombreux utilisateurs en même temps. Les équipes peuvent reproduire une activité passée, observer les performances et comparer les résultats avant et après une modification. Une interface visuelle est proposée sur Windows. Plusieurs outils fonctionnent aussi sur Ubuntu Linux. Le projet est encore en version d’essai publique. Ce n’est pas un produit Microsoft officiel bénéficiant de son assistance.

**Pourquoi c’est important**

Ces tests aident à repérer des ralentissements et à évaluer les effets d’un changement sur une base de données. Ils permettent de comparer des résultats mesurés plutôt que de se fier à une impression.

[Lire l’article complet](https://techcommunity.microsoft.com/blog/sqlserver/introducing-sqlsimtools/4563955)

---

## 5. How to Coordinate Role-Based CLI Seats & Session Handovers for AI Agents: A Governance MCP Server

**Thème :** IA Générative

**Source :** Dev.to

**Date de publication :** Wed, 21 Oct 2026 05:06:41 +0000

Quand plusieurs assistants d’intelligence artificielle travaillent sur le même projet, ils peuvent modifier les mêmes fichiers et se gêner. L’article présente CliSeat, un outil conçu pour organiser ce travail. Il attribue à un seul assistant à la fois le droit de modifier une partie donnée du projet. Il prévoit aussi un compte rendu pour transmettre le travail à l’assistant suivant. Des fonctions limitent les commandes autorisées et masquent certains identifiants secrets. Une version gratuite existe. L’historique persistant, la récupération automatique des accès abandonnés et le masquage des identifiants sont présentés dans l’offre payante.

**Pourquoi c’est important**

La coordination des assistants peut aider à éviter qu’ils écrasent leurs modifications respectives. Un historique de transmission permet aussi de reprendre le travail en sachant ce qui a déjà été fait.

[Lire l’article complet](https://dev.to/johann_schiffer/how-to-coordinate-role-based-cli-seats-session-handovers-for-ai-agents-a-governance-mcp-server-2bl8)

---

## 6. I Built a Small LLM From Scratch — Here’s What I Finally Understood About Transformer

**Thème :** IA Générative

**Source :** Dev.to

**Date de publication :** Wed, 21 Oct 2026 05:13:19 +0000

Pour comprendre comment une intelligence artificielle produit du texte, l’auteur a construit un petit modèle de langage. Ce programme apprend, à partir de textes de Shakespeare, à prévoir le caractère suivant. Les lettres sont d’abord transformées en nombres. Le modèle apprend ensuite à utiliser le texte précédent pour proposer une suite. L’article explique comment il repère les relations entre les caractères et tient compte de leur position. Il décrit aussi l’apprentissage et la production de texte. L’objectif est pédagogique : comprendre les mécanismes, sans prétendre créer un concurrent de ChatGPT.

**Pourquoi c’est important**

Cet exemple rend plus concret le fonctionnement des outils qui génèrent du texte. Il montre aussi qu’un réglage produisant des réponses plus variées ne rend pas le modèle plus intelligent.

[Lire l’article complet](https://dev.to/onlydev75/i-built-a-small-llm-from-scratch-heres-what-i-finally-understood-about-transformer-2h2o)

---

## 7. Durable Task in the Real World: What Problems Does It Actually Solve?

**Thème :** .NET

**Source :** Microsoft .NET Blog

**Date de publication :** Mon, 12 Oct 2026 16:30:00 +0000

Un logiciel peut être interrompu alors qu’il attend une validation ou un paiement. Durable Task aide à mémoriser les étapes accomplies et à reprendre le travail après un redémarrage. L’article présente cinq situations, dont le traitement de factures, les paiements et l’intervention d’un assistant d’IA sur un incident. Mais cet outil ne vérifie pas tout à la place de l’application. Si la réponse d’un service de paiement est perdue, il faut contrôler si le débit a eu lieu avant de réessayer. Une action proposée par une IA doit aussi rester liée à la proposition précisément approuvée.

**Pourquoi c’est important**

Reprendre un traitement après une panne ne suffit pas à garantir un résultat correct. Il faut aussi éviter les paiements en double et vérifier que les actions exécutées correspondent bien aux décisions autorisées.

[Lire l’article complet](https://devblogs.microsoft.com/dotnet/durable-task-in-the-real-world)

---

Bonne lecture et à bientôt pour une nouvelle sélection technologique.
