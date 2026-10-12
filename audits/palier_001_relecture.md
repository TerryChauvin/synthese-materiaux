# Relecture du palier 1 (publications 1 à 50)

Relecture faite par l'orchestrateur le 2026-10-12, après `audit.py 1`.

## Bilan

- 50 publications, 465 voies (78 de base, 387 branches), 5 330 citations.
- Citations : 100 % retrouvées mot pour mot dans le texte des articles (contrôle automatique), et chaque valeur numérique apparaît dans sa citation.
- 0 anomalie bloquante. 5 avertissements, tous examinés et acceptés (ci-dessous).
- Tous les doutes des extracteurs (environ 280) ont été tranchés en relisant le passage concerné.

## Relectures intégrales

| Lot | Articles | Valeurs contrôlées | Valeurs corrigées |
|---|---|---|---|
| Calibrage (publications 1 à 10) | 10 | 561 | 9 (1,6 %) |
| Échantillon 1 sur 5 (publications 11 à 50) | 10 | 746 | 1 (0,13 %) |

Erreurs du calibrage, toutes devenues des règles de `RUNBOOK.md` :
- pureté et fournisseur sans citation propre → champ `supplier_quote` et contrôle bloquant ;
- libellé de variation ajoutant des mots absents de l'article (« more layers ») → `value_text` reprend les mots de la citation ;
- une branche mêlant deux observations distinctes (température de croissance et température du substrat) → une branche = une condition ;
- branches créées pour les bornes d'une plage, et branches héritant à tort d'une valeur du parent quand l'article ne donne qu'une plage → règle des criblages par plages.

Erreur de l'échantillon : un rapport masse/volume nommé `molar_ratio` (PMC3833323), renommé.

## Échantillon de 30 valeurs du rapport d'audit

Les 30 lignes de `palier_001.md` ont été relues : dans les 30 cas la citation contient la valeur, pour la bonne étape et la bonne voie. 0 erreur.

## Contrôle de stœchiométrie et de cohérence chimique (5 voies)

| Voie | Contrôle | Verdict |
|---|---|---|
| PMC6199062 Sb2S3-150 | 2 mmol SbCl3 + 3 mmol L-cystéine → Sb:S = 2:3 | conforme à Sb2S3 |
| PMC6631201 MnO2NFs | 1 mmol KMnO4 + 1,5 mmol MnSO4 → 2 MnO4⁻ + 3 Mn²⁺ → 5 MnO2 | stœchiométrie exacte |
| PMC7578857 CsPbBr3 | 0,1 mmol PbBr2 + 0,1 mmol CsBr → Cs:Pb = 1:1 | conforme ; le dopage Nd (0,15 mmol pour x = 7,2 %) est incohérent chez les auteurs, signalé |
| PMC5309769 MAPbBr3 | 0,16 mmol MABr + 0,2 mmol PbBr2 (MA:Pb = 0,8) | conforme au protocole LARP cité par les auteurs |
| PMC6994313 Zn-MOF | 0,120 mmol nitrate de zinc + 0,120 mmol ligand → 1:1 | plausible ; formule du MOF non donnée par l'article |

Atmosphères vérifiées contre l'état d'oxydation visé : Na3V2(PO4)3 calciné sous argon (V³⁺), ZnSe sélénié sous vide, LiCoO2 recuit sous air (Co³⁺), SiC et V2C traités sous argon : cohérent partout.

Incohérences qui viennent des articles eux-mêmes, conservées telles quelles et signalées dans les doutes : rapport Ca/P de PMC6928996, masses de nanotubes de PMC9300655, « 0.2 g » de NrGO de PMC6631201, rapport Na2O/SiO2 de 3.0 de PMC6025012.

## Avertissements acceptés

- PMC11231976 (4 avertissements) : 230 °C dans la section de préchauffage d'une pyrolyse par pulvérisation, au-dessus du point d'ébullition de l'eau. C'est le principe du procédé (vaporisation des gouttelettes), pas une erreur.
- PMC10529665 : deux branches aux conditions identiques. L'article donne bien deux rangées identiques dans son tableau 1, avec deux diamètres mesurés différents.

## Corrections apportées aux contrôles pendant l'audit

Le premier passage donnait 37 avertissements, dont 32 faux positifs du script, corrigés dans `audit.py` et `load.py` :
- unités « minutes », « hr », « mTorr », « °C·min–1 » non reconnues ;
- paramètres dont le nom contient « rate » (concentration, débit) traités à tort comme des vitesses de chauffe ;
- comparaison au point d'ébullition du solvant appliquée à des pyrolyses à plus de 350 °C ;
- seuil de 100 °C appliqué aux recuits doux de films ;
- « FA » de FAPbBr3 lu comme du fluor ; cystéine non reconnue comme source de soufre.

Les 50 extractions ont été rechargées après ces corrections (`reload_all.py`), puis l'audit relancé.

## Limites constatées sur ce palier

- 123 voies sur 465 n'ont pas de méthode propre (branches héritant de leur parent) : normal.
- 289 voies sans formule chimique du matériau (composites, MOF sans formule, membranes) : le bilan d'éléments n'y est pas applicable.
- Un seul article (PMC9026548, membranes MOF/polymère) pèse 79 voies : ce sont les cases de trois tableaux de formulation, avec pour seul résultat une appréciation visuelle (++/+/−) dont la légende n'est pas dans le texte converti.
- Le Supporting Information n'est pas lu : plusieurs articles y renvoient leurs quantités exactes.
