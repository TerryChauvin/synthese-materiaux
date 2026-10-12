# Base de voies de synthèse de matériaux

`synthese.db` (SQLite) — voies de synthèse extraites d'articles open access, chaque valeur accompagnée de sa citation exacte. `synthese_dump.sql` en est l'export texte, régénéré à chaque audit de palier.

Ouvrir la base : [DB Browser for SQLite](https://sqlitebrowser.org/), DBeaver, ou Python (`sqlite3.connect("synthese.db")`).

## Tables

| Table | Contenu |
|---|---|
| `papers` | article, licence, URL, PDF local, rang et palier, niveau de relecture |
| `materials` | matériau visé : nom, formule, famille, phase, morphologie |
| `synthesis_routes` | une voie ou une branche (`parent_route_id`), méthode, rendement, score de complétude |
| `route_variations` | ce qu'une branche change par rapport à son parent |
| `reagents` | réactifs : rôle, quantité, pureté, fournisseur |
| `steps` | étapes ordonnées du protocole |
| `parameters` | paramètres d'une étape : valeur d'origine + valeur SI |
| `equipment` | matériel d'une étape |
| `characterizations` | techniques et résultats de caractérisation |
| `outcomes` | propriétés mesurées du produit de chaque voie |
| `annotations` | explications rédigées par Claude (résumé, objectif, comparaison des branches…) |
| `doubts`, `audit_findings` | points ambigus et anomalies d'audit, avec leur traitement |

Colonnes de traçabilité présentes partout : `quote` (passage exact), `section`, `char_start`/`char_end` (position dans `corpus/text/<PMCID>.txt`).

Une branche hérite des étapes et des réactifs de son parent, et `route_variations` dit ce qui change. Les réactifs enregistrés sur une branche (additif, dopant, substitut) s'ajoutent à ceux de ses ancêtres. Une branche qui possède ses propres étapes remplace celles du parent. Les vues font la reconstitution.

## Requêtes utiles

Protocole complet d'une voie ou d'une branche, avec citations :

```sql
SELECT step_order, action, description, parameter, value_num, value_text, unit,
       overridden_by_branch, quote
FROM v_route_complete
WHERE pmcid = 'PMC0000000' AND branch_label = 'ZnO-180'
ORDER BY step_order;
```

Réactifs d'une voie de base :

```sql
SELECT g.name, g.formula, g.role, g.amount, g.unit, g.purity, g.supplier, g.quote
FROM reagents g JOIN synthesis_routes r ON r.id = g.route_id
JOIN papers p ON p.id = r.paper_id
WHERE p.pmcid = 'PMC0000000' AND r.branch_label = 'ZnO-120';
```

Arbre des branches d'un article, puis effet de chaque variation :

```sql
SELECT * FROM v_branches WHERE pmcid = 'PMC0000000';
SELECT * FROM v_comparaison WHERE pmcid = 'PMC0000000' ORDER BY parameter, branch_label;
```

Toutes les synthèses hydrothermales d'un oxyde entre 150 et 200 °C :

```sql
SELECT DISTINCT pmcid, branch_label, material, value_num AS temp_C, quote
FROM v_route_complete
WHERE method LIKE '%hydrothermal%' AND parameter = 'temperature'
  AND unit = '°C' AND value_num BETWEEN 150 AND 200;
```

Ce que Claude a compris d'un article :

```sql
SELECT a.type, r.branch_label, a.text FROM annotations a
JOIN papers p ON p.id = a.paper_id
LEFT JOIN synthesis_routes r ON r.id = a.route_id
WHERE p.pmcid = 'PMC0000000';
```

## Limites

- Open access uniquement ; le Supporting Information n'est pas lu. Une voie dont les quantités sont dans le SI a un `completeness_score` bas et ses manques sont listés dans `missing_fields`.
- Les valeurs sont celles écrites par les auteurs. Les contrôles physique/chimie repèrent des incohérences, ils ne garantissent pas qu'un protocole publié fonctionne.
- Les annotations sont des interprétations, pas des données.

Fonctionnement du pipeline et procédure de reprise : voir `CLAUDE.md` ; consignes d'extraction : `RUNBOOK.md`.
