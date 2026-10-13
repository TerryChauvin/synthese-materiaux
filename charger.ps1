# Chargement d'une publication apres sa mise a niveau au format 2 (PC, orchestrateur) ; lancer ensuite les deux critiques.
#   .\charger.ps1 PMC123
param([string]$P)
python -I load.py check $P | Select-Object -Last 1
python -I load.py load $P | Select-Object -Last 1
if ($LASTEXITCODE -ne 0) { "ARRET: chargement en echec"; exit 1 }
python -I state.py doubts $P "Lecture de l'extracteur conservee a la mise a niveau format 2 ; point soumis au critique de fidelite, qui relit l'article independamment." | Out-Null
python -I fiche.py $P | Out-Null
python -I state.py touch
