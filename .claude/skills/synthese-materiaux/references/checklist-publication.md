# Liste à cocher pour une publication (de la file à la clôture)

Commandes depuis la racine du dépôt, `python -I` (PC) ou `python3 -I` (cloud).

## 0. Avant de lancer quoi que ce soit

- [ ] `state.py status` lu : `review_pending`, `full_review_due`, `critic_pending`, `format1_to_upgrade`, `audit_du` vides ou traités d'abord.
- [ ] Le texte de l'article contient `## Supporting Information` ou `si_status` vaut `absent` (sinon `enrich.py <PMCID>` sur le PC).
- [ ] `corpus/refs/<PMCID>.txt` existe.

## 1. Extraction (ou mise à niveau)

- [ ] Agent Sonnet lancé avec le prompt de `CLAUDE.md` (mise à niveau : consigne « Mise à niveau d'une extraction existante » du RUNBOOK, ne rien retirer).
- [ ] `REJET` → vérifier dans le texte (`Grep` sur « was dissolved », « autoclave », « Methods ») avant `state.py reject`.
- [ ] `load.py check <PMCID>` relancé soi-même : 0 erreur ; avertissements lus.
- [ ] `load.py load <PMCID>`.

## 2. Relecture par l'orchestrateur

- [ ] `review.py <PMCID> doubts` : arbre des voies, variations, doutes.
- [ ] Chaque doute tranché en relisant le passage ; corrections dans le JSON puis rechargement ; `state.py doubts <PMCID> "<résolution>"`.
- [ ] Toutes les conditions comparées par l'article ont une branche (tableaux : afficher les lignes ` | `).
- [ ] Relecture intégrale si `full_review_due` le dit : chaque valeur contre l'article ; `state.py review <PMCID> full <erreurs> <valeurs>` ; sinon `state.py review <PMCID> doubts`.

## 3. Critique de fidélité

- [ ] Agent Sonnet (`CRITIQUE.md`) → `critiques/<PMCID>.json`.
- [ ] `critic_load.py <PMCID>` : 0 erreur.
- [ ] Chaque constat `faux`, `attribution`, `manquant`, `non_cite_a_tort`, `deduit` vérifié dans le texte → correction + rechargement (`status='corrige'`) ou rejet motivé (`status='rejete'`, `resolution=…`). `mineur` → accepté ou corrigé.

## 4. Critique scientifique

- [ ] Agent Opus (`PLAUSIBILITE.md`, web) → `critiques/<PMCID>_science.json`.
- [ ] `critic_load.py <PMCID>` : 0 erreur.
- [ ] `sources_check.py <PMCID> 3` (PC) : DOI et titres confirmés ; une source ouverte pour vérifier qu'elle dit ce qu'on lui attribue.
- [ ] Problèmes (`status = probleme`) lus : incohérence de l'article → annotation `limite_reproductibilite` ajoutée au JSON et rechargée ; erreur de l'extraction → corrigée.

## 5. Clôture

- [ ] `state.py critic <PMCID> done "<bilan en une phrase>"`.
- [ ] `fiche.py <PMCID>` régénérée (fiche lisible avec les « non cité »).
- [ ] Commit + push après le lot.

## 6. Tous les 50 : audit de palier (`CLAUDE.md`, section « Audit de palier »)

- [ ] `audit.py N` → bloquants et avertissements traités en retournant à l'article.
- [ ] `sources_check.py --palier N 10`.
- [ ] Contrôle croisé `compare.py` sur les matériaux présents plusieurs fois.
- [ ] Échantillon de 30 valeurs et stœchiométrie de 5 voies relus à la main.
- [ ] `audits/palier_NNN_relecture.md` écrit ; `audit.py N` relancé jusqu'à 0 bloquant.
