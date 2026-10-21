# Lettre d’actualité technologique Infomil

Retrouvez notre sélection d’actualités du développement logiciel, avec des résumés techniques en français et les points à retenir pour votre pratique.

## 1. Bring Your Own Model to the GitHub Copilot SDK with C#

**Thème :** .NET

**Source :** Microsoft .NET Blog

**Date de publication :** Mon, 19 Oct 2026 16:00:00 +0000

L’article présente une application console .NET 10 utilisant GitHub.Copilot.SDK 1.0.11 pour diriger l’inférence vers un déploiement Microsoft Foundry. ProviderConfig sépare le choix du fournisseur du runtime Copilot, qui reste nécessaire pour gérer le client et les sessions. L’exemple configure un endpoint compatible avec la Responses API et privilégie Microsoft Entra ID via AzureCliCredential ; une clé API reste une option. Les paramètres sont chargés avec User Secrets. La session désactive outils, skills et opérations Git pour isoler une requête. Avec un modèle de raisonnement, la limite de sortie inclut aussi les tokens de raisonnement.

**Pourquoi c’est important**

Cette séparation permet de conserver l’orchestration du GitHub Copilot SDK tout en choisissant son propre fournisseur d’inférence. L’exemple fournit une base C# minimale pour vérifier le routage et l’authentification avant d’ajouter des capacités à l’agent.

[Lire l’article complet](https://devblogs.microsoft.com/dotnet/bring-your-own-model-to-the-github-copilot-sdk-with-csharp)

---

## 2. 22.2.3

**Thème :** Angular

**Source :** GitHub Releases

**Date de publication :** 2026-10-14T23:38:58Z

Angular 22.2.3 renforce l’encodage des paramètres et la compilation JIT contre la prototype pollution. Le compiler prend en charge les points dans les noms de class bindings et les property bindings de popover, tout en corrigeant plusieurs diagnostics. Dans core, les correctifs concernent notamment initEventReplay lorsque deux applications partagent un APP_ID, la destruction de vues avec animations et les ticks imbriqués pendant une détection de changements. Le module forms utilise addEventListener pour éviter une planification systématique de la détection de changements sur blur. Le router vérifie l’état du signal d’annulation dès la souscription.

**Pourquoi c’est important**

Cette version combine des renforcements contre la prototype pollution avec des corrections de compilation et d’exécution. Elle évite aussi de déclencher systématiquement la détection de changements lors des événements blur dans forms.

[Lire l’article complet](https://github.com/angular/angular/releases/tag/v22.2.3)

---

## 3. 19.3.0 (September 9, 2026)

**Thème :** React

**Source :** GitHub Releases

**Date de publication :** 2026-09-09T18:01:33Z

React 19.3.0 introduit ViewTransition et addTransitionType pour les animations, ainsi que les refs sur Fragment. Dans react-dom, browser() permet de réserver un sous-arbre au navigateur avec use(browser()) dans Suspense ; onBrowserBailout signale ce report côté serveur. Les transitions sont désormais rendues indépendamment : une transition lente ne bloque plus les autres. La version active l’intégration de Trusted Types et corrige Fast Refresh, Activity, la propagation du contexte et useDeferredValue. Elle améliore également le décodage et la sérialisation des échanges Flight, ajoute des protections contre les cycles et les dénis de service, et corrige plusieurs problèmes de rendu serveur.

**Pourquoi c’est important**

Les nouvelles API facilitent les animations et la délimitation des parties exclusivement exécutées dans le navigateur. Les changements touchent aussi l’indépendance des transitions, la fiabilité du rendu serveur et la robustesse des échanges React Server Components.

[Lire l’article complet](https://github.com/react/react/releases/tag/v19.3.0)

---

## 4. Introducing sqlsimtools

**Thème :** SQL Server

**Source :** Microsoft SQL Server Blog

**Date de publication :** 2026-10-14T05:19:22.512-07:00

sqlsimtools est une suite gratuite et open source de simulation de charges SQL, disponible en public preview. Elle cible SQL Server 2019, 2022 et 2025, Azure SQL Database, Azure SQL Managed Instance et SQL database dans Microsoft Fabric. sqlsim fournit une CLI native fondée sur ODBC pour Windows x64 et ARM64 et Ubuntu Linux ; sqlpysim utilise le driver mssql-python. sqlsim Studio, disponible sur Windows x64, configure, exécute et compare les charges dans une application locale accessible par navigateur. La suite permet les tests de charge, le rejeu d’activité, le suivi des performances et l’automatisation via des résultats JSON.

**Pourquoi c’est important**

Ces outils permettent de reproduire des charges concurrentes et de comparer les performances avant et après un changement. Le projet reste en preview et ne constitue pas un produit Microsoft officiel couvert par son support.

[Lire l’article complet](https://techcommunity.microsoft.com/blog/sqlserver/introducing-sqlsimtools/4563955)

---

## 5. Promise Delivered: Welcome to the DEV Hall of Fame (65 Authors, 65 Masterpieces)

**Thème :** IA Générative

**Source :** Dev.to

**Date de publication :** 2026-10-18T10:55:38Z

Ce catalogue rassemble 65 articles publiés sur DEV, chacun choisi par son auteur, et représente plus de 600 minutes de lecture annoncée. Les contributions sont regroupées par thèmes : apprentissage, systèmes, IA, architecture et outils. Les sujets techniques incluent les interfaces, AWS VPC, les CTE SQL, l’idempotence, WebRTC, les write-ahead logs et WebGPU. La partie IA aborde notamment les comparaisons d’assistants de programmation, la recherche sémantique, les contrôles d’approbation, les tests de prompt injection et l’évaluation du RAG. Chaque entrée comporte un commentaire de l’organisateur et, lorsqu’elle est disponible, la raison du choix de l’auteur.

**Pourquoi c’est important**

Le classement thématique facilite la découverte de retours d’expérience techniques au-delà des seuls articles les plus populaires. Plusieurs contributions sur l’IA examinent concrètement les défauts de validation, de tests et de contrôle des outils.

[Lire l’article complet](https://dev.to/georgekobaidze/promise-delivered-welcome-to-the-dev-hall-of-fame-65-authors-65-masterpieces-15fa)

---

## 6. Durable Task in the Real World: What Problems Does It Actually Solve?

**Thème :** .NET

**Source :** Microsoft .NET Blog

**Date de publication :** Mon, 12 Oct 2026 16:30:00 +0000

L’article illustre Durable Task .NET SDK v1.26.0 avec Durable Task Scheduler à travers cinq scénarios : approbation de factures, provisioning Azure, paiements, webhooks désordonnés et investigation d’incidents assistée par IA. L’historique permet de rejouer l’orchestrateur avec les résultats d’activités enregistrés et de reprendre des attentes durables après un redémarrage. Il ne garantit pas des effets externes exactement une fois. L’application conserve les responsabilités d’autorisation, d’idempotence et de réconciliation. Pour les agents, l’appel au modèle appartient à une activité qui sauvegarde une proposition immuable ; l’approbation doit porter sur cette proposition précise, sans la régénérer silencieusement après une interruption.

**Pourquoi c’est important**

Durable Task devient utile lorsque mémoriser et reprendre un processus métier nécessite une coordination complexe. Ses garanties ne remplacent ni les registres faisant autorité, ni la vérification des opérations externes dont le résultat reste incertain.

[Lire l’article complet](https://devblogs.microsoft.com/dotnet/durable-task-in-the-real-world)

---

## 7. Your agent's retry bug isn't an AI problem. It's a distributed-systems problem with an LLM on top.

**Thème :** IA Générative

**Source :** Dev.to

**Date de publication :** 2026-10-19T06:42:45Z

L’article explique pourquoi les nouvelles tentatives d’un agent relèvent des systèmes distribués : un timeout ne prouve pas qu’une action distante a échoué. Un remboursement peut ainsi être exécuté deux fois si sa première réponse est perdue. L’application doit enregistrer durablement l’intention avant l’exécution, générer une clé d’idempotence stable et la réutiliser à chaque tentative. Le suivi distingue submitted, confirmed, failed et unknown. Ce dernier état bloque les tentatives automatiques et déclenche une réconciliation avec le service concerné ou son registre. Le modèle propose l’action, tandis que l’application possède son état d’exécution et sa politique de reprise.

**Pourquoi c’est important**

Un meilleur prompt ne résout pas une réponse réseau perdue après une écriture réussie. Les actions modifiant des données doivent utiliser des mécanismes d’idempotence et de réconciliation pour éviter les effets dupliqués.

[Lire l’article complet](https://dev.to/cyclopt_dimitrisk/your-agents-retry-bug-isnt-an-ai-problem-its-a-distributed-systems-problem-with-an-llm-on-top-1i6k)

---

Bonne lecture et à bientôt pour une nouvelle sélection technologique.
