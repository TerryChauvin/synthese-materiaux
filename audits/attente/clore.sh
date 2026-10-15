#!/bin/bash
S=/tmp/claude-0/-home-user-synthese-materiaux/1b4e6909-0b5d-5c6e-b438-5ad76e738164/scratchpad
# transposition de clore.ps1 : clore.sh PMCID "bilan" [ids rejetes separes par des virgules] ["note rejet"]
set -e; cd /home/user/synthese-materiaux; P=$1
REV=$S/charge/$P.json; [ -f $REV ] || REV=$(git log --format=%h -- extractions/$P.json | tail -1); python3 -I diff_valeurs.py $P $REV | tail -4
python3 -I load.py check $P | tail -1
python3 -I load.py load $P | tail -1
python3 -I critic_load.py $P | tail -2
if [ -n "$3" ]; then IFS=, read -ra R <<< "$3"; ids=($(python3 -I state.py critiques $P | awk -F'\t' '/^[0-9]/{print $1}')); for n in "${R[@]}"; do python3 -I state.py critiques $P ${ids[$((n-1))]} rejete "${4:-Rejete par l'agent de correction, texte a l'appui.}" >/dev/null; done; fi
python3 -I state.py critiques $P all corrige "Appliqué par l'agent de correction, contrôlé par l'orchestrateur (load.py check, diff_valeurs)." >/dev/null
python3 -I state.py doubts $P "Doute conservé après les critiques de fidélité et scientifique : la lecture retenue est celle décrite dans le doute ; l'article ne permet pas de trancher davantage." >/dev/null || true
python3 -I fiche.py $P | tail -1; python3 -I graphe.py $P | tail -1
python3 -I state.py critic $P done "$2"
python3 -I state.py critiques $P | awk -F'\t' '/^[0-9]/{print $2}' | sort | uniq -c
python3 -I -c "import re,json,sys;print('$P',' '.join(sorted(set(re.findall(r'10\.\d{4,}/[^\s\"\',;]+',open('critiques/$P'+'_science.json').read())))))" >> /tmp/claude-0/-home-user-synthese-materiaux/1b4e6909-0b5d-5c6e-b438-5ad76e738164/scratchpad/doi.txt
