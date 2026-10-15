#!/bin/bash
# charger.sh PMCID jetons appels duree "resolution des doutes"
set -e; cd /home/user/synthese-materiaux; P=$1
echo "$P,extraction,sonnet,$2,$3,$4" >> audits/jetons.csv
python3 -I load.py check $P | tail -1
python3 -I load.py load $P | tail -1; cp extractions/$P.json /tmp/claude-0/-home-user-synthese-materiaux/1b4e6909-0b5d-5c6e-b438-5ad76e738164/scratchpad/charge/
python3 -I state.py doubts $P "$5" >/dev/null || true
python3 -I state.py review $P doubts | tail -1
python3 -I fiche.py $P | tail -1
git add -A && git commit -qm "$P chargée (palier 5)

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01XpBfw837etGcfE2KpDthTP" && git push -q origin main 2>&1 | tail -2
