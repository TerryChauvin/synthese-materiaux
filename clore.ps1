# Cloture d'une publication apres l'agent de correction (PC, orchestrateur).
#   .\clore.ps1 PMC123 "note des constats corriges" "bilan des deux critiques" [-Rej 6,12 -RejNote "raison"]
# -Rej : numeros des constats de fidelite rejetes, dans l'ordre du fichier (a partir de 1).
param([string]$P, [string]$Note, [string]$Bilan, [int[]]$Rej = @(), [string]$RejNote = "Rejete par l'agent de correction, texte a l'appui.")
python -I load.py check $P | Select-Object -Last 1
python -I load.py load $P | Select-Object -Last 1
if ($LASTEXITCODE -ne 0) { "ARRET: chargement en echec"; exit 1 }
python -I critic_load.py $P
# voie supprimee apres la critique scientifique : poser "route_removed" sur son entree du fichier _science.json
if ($LASTEXITCODE -ne 0) { "ARRET: critic_load en echec, statuts non modifies"; exit 1 }
$ids = python -I state.py critiques $P | Select-String "^\d+" | ForEach-Object { ($_ -split "`t")[0] }
foreach ($n in $Rej) { python -I state.py critiques $P $ids[$n - 1] rejete $RejNote | Out-Null }
python -I state.py critiques $P all corrige $Note | Out-Null   # "all" ne touche que les constats encore ouverts
# les doutes recrees ou reecrits par la correction restent dans la base comme avertissements au lecteur
python -I state.py doubts $P "Doute conserve apres les critiques de fidelite et scientifique : la lecture retenue est celle decrite dans le doute ; l'article ne permet pas de trancher davantage." | Out-Null
python -I fiche.py $P | Out-Null
python -I graphe.py $P | Out-Null   # graphes/<PMCID>.html : reactifs -> etapes -> materiau, par voie
python -I sources_check.py $P 4 | Select-Object -Last 5
python -I state.py critic $P done $Bilan
python -I state.py critiques $P | Select-String "^\d+" | Group-Object { ($_ -split "`t")[1] } | ForEach-Object { "$($_.Name): $($_.Count)" }
