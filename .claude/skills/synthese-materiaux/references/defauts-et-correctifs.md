# Catalogue des défauts rencontrés, comment les reconnaître, ce qui les a corrigés

Chaque entrée : symptôme, cause, correctif, et ce qu'il faut faire si le défaut réapparaît. Les correctifs marqués « code » sont dans les scripts ; ceux marqués « consigne » sont dans `RUNBOOK.md`, `CRITIQUE.md` ou `CLAUDE.md`. Tenir ce fichier à jour : une erreur vue deux fois doit y figurer.

## A. Erreurs d'extraction (valeur ≠ article)

| Symptôme | Cause | Correctif | Si ça réapparaît |
|---|---|---|---|
| Pureté/fournisseur présents sans citation qui les contienne | section « Materials » séparée, citée nulle part | champ `supplier_quote`, contrôle bloquant (code + consigne) | vérifier que `supplier_quote` est une phrase de l'article |
| Variation libellée « more layers » alors que l'article ne dit que « ∼140 nm » | l'extracteur traduit en réglage ce que l'auteur donne en grandeur | règle « `value_text` reprend les mots de la citation » (consigne) | remplacer par la grandeur donnée |
| Une branche mélange deux observations (température du four et du substrat) | fusion de deux phrases | règle « une branche = une condition » (consigne) | scinder |
| Branches créées pour les bornes d'une plage (« 1 to 5 hours ») ; branches héritant de 3 h alors que l'article ne donne qu'une plage | lecture trop généreuse | règle des criblages par plages (consigne) | supprimer les branches de bornes, mettre la plage en `value_text` |
| Rapport masse/volume nommé `molar_ratio` | vocabulaire forcé | rôle/nom explicite (`solid_to_liquid_ratio`) | renommer |
| `mecanisme_analyse` affirmant un « excès de soufre » pour un rapport 3:2 stœchiométrique | raisonnement faux de l'extracteur | trouvé par le critique de fidélité ; corrigé à la main | le critique scientifique recalcule la stœchiométrie |
| Efficacités coulombiques nommées « à 200 mA g−1 » sans que l'article le dise | déduction à partir du contexte | nom de propriété sans la condition déduite | retirer la condition du nom |
| Quantités déclarées manquantes alors qu'elles sont dans le tableau S1 de l'annexe | annexes non lues | `enrich.py` ajoute le texte des annexes ; grille `not_stated` (code + consigne) | relancer `enrich.py`, mettre à niveau |

Erreur dominante restante : **valeur juste, échantillon faux** (rangées de tableaux, « respectively », séries de figures). Parade : afficher les lignes ` | ` du texte à la relecture ; critique de fidélité qui relit l'article avant l'extraction.

## B. Contrôles automatiques (faux positifs et trous)

| Symptôme | Cause | Correctif |
|---|---|---|
| 32 avertissements physiques au premier audit, presque tous faux | unités non reconnues (« minutes », « hr », « mTorr », « °C·min–1 ») ; `concentration_rate`/`addition_rate` pris pour des vitesses de chauffe ; pyrolyses comparées au point d'ébullition du solvant ; recuit de film à 70 °C jugé « inhabituel » ; « FA » de FAPbBr3 lu comme du fluor ; cystéine non reconnue comme source de soufre | normalisation des unités, test sur le nom exact du paramètre, pas de test solvant au-delà de 350 °C, seuil 40 °C pour `anneal`, cations organiques FA/MA, mots-clés soufrés (code) |
| Nombre « 1,226.1 » refusé par le contrôle valeur-dans-citation | séparateur de milliers | `number_forms` accepte la forme avec virgule (code) |
| Réactifs propres à une branche (dopant) ignorés par la complétude et le bilan d'éléments | héritage « bloc » des réactifs | les réactifs d'une branche s'ajoutent à ceux des ancêtres (code) |
| Anomalies d'audit acceptées puis réapparues au rechargement | cible = identifiant de ligne SQL, qui change | cible = « voie / étape / paramètre » (code) |
| Manques listés librement, impossibles à distinguer d'un oubli | `missing_fields` non contrôlé | grille `not_stated` : chaque case attendue est extraite ou déclarée ; contrôle bloquant (code + consigne) |
| `critic_load.py` effaçait les décisions de l'orchestrateur quand le critique scientifique rechargeait aussi le fichier de fidélité | suppression/réinsertion sans mémoire | statut et résolution conservés par (lieu, citation) (code) |
| Les verdicts du critique scientifique disparaissaient après un rechargement d'extraction | cascade sur `route_id` | plus de clé étrangère sur `route_id`, lien par `branch_label` rétabli par `load.py` (code) |
| Titres d'articles avec balises HTML échappées | API Europe PMC | `strip_tags` + `html.unescape` (code) |

## C. Corpus et réseau

| Symptôme | Cause | Correctif |
|---|---|---|
| Articles sans section expérimentale acceptés, ou à l'inverse écartés à tort | heuristique trop stricte/laxiste | filtre « protocole » dans la requête Europe PMC + tri grossier dans `sections.py` ; l'extracteur peut toujours répondre `REJET` |
| PDF introuvables (403 Europe PMC, PMC) | téléchargement direct bloqué | dépôt S3 PMC Open Access (`fetch.py --pdfs`, `enrich.py`) |
| Téléchargements interrompus (`IncompleteRead`, `SSLError`) non rattrapés | exceptions hors du `except` | `fetch.get` rattrape `HTTPException` et `ssl.SSLError` et réessaie (code) |
| Erreur 500 sur un article bloquant toute la recherche | pas de rattrapage par article | on passe à l'article suivant (code) |
| Console Windows cp1252 qui plante sur « ε » | encodage | `sys.stdout.reconfigure(utf-8)` dans `db.py` ; guillemets PowerShell : écrire un script plutôt qu'un `python -c` |
| Europe PMC bloqué depuis le cloud (403 du proxy) | règle réseau du sandbox | réapprovisionner la file depuis le PC avant de basculer ; `fetch.py` interdit dans le cloud (consigne) |
| Plus de la moitié des articles sans annexe dans le dépôt PMC | elles ne sont pas déposées | `si_status = absent` ; rien à faire, mais le dire dans les limites |
| Citation d'une rangée d'annexe refusée alors qu'elle « est » dans le texte (« 40 L » pour « 40 µL ») | les PDF en police Symbol laissent un caractère privé (`` pour µ, `` pour ~) que la console n'affiche pas | copier la citation depuis le fichier (ou via `repr`), jamais depuis l'affichage ; l'extracteur recopie le fichier, donc il n'est pas touché |
| Sources du critique scientifique « non trouvées » par `sources_check` alors qu'elles existent | titres Crossref avec `<sub>`, tirets typographiques ; sources données par URL et non par DOI ; DOI de matériel supplémentaire | comparaison normalisée sans espaces ni balises ; recherche du DOI par titre ; suffixe `.sNNN` retiré (code) |

## D. Qualité du corpus et biais

- Open access seul → biais de revues ; licences NC/ND → dépôt privé obligatoire.
- Un article peut peser 79 voies (grille de formulations de membranes) avec pour seul résultat une note visuelle : les totaux de voies ne mesurent pas la richesse. D'où la cible en publications.
- Le tri de la file par « indice d'étude paramétrique » (`param_score`) privilégie les articles qui comparent des conditions ; vérifié utile (deux articles → 50 voies).
- Les annexes PDF perdent leur mise en page : tableaux aplatis, cellules fusionnées → risque d'attribution. Le critique doit vérifier rangée par rangée.

## E. Méthode de travail (orchestration)

| Problème | Correctif |
|---|---|
| Sorties de `review.py` trop longues pour le contexte | filtrer (`Select-String -NotMatch "^ANNOT|^  CARAC|^DOUTE|^  MANQUE"`) ; `review.py <PMCID> doubts` pour l'arbre seul |
| Agents qui mettent des remarques générales dans `doubts` | `doubts` réservé aux vraies ambiguïtés touchant une donnée (consigne) |
| Prompt des extracteurs trop long et chemins Windows en dur | prompt court dans `CLAUDE.md`, « racine du dépôt », `python3` dans le cloud |
| Tâche planifiée locale et session cloud qui pourraient se marcher dessus | tâche locale désactivée avant bascule ; verrou `run.lock` inutile dans le cloud |
| Bascule cloud refusée sur un tour automatique | elle ne se fait que sur un message tapé par l'utilisateur ; lui demander « bascule » |
| Travail non poussé perdu à la fin d'une session cloud | commit + push après chaque lot et chaque audit (consigne) |
