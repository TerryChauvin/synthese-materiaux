# Complément PMC9181868 — tableaux du texte (8 présents, 2 exploitables)

- Constat principal : sur les 7 tableaux annoncés, seuls les Tables 7 et 8 ont des rangées dans `corpus/text/PMC9181868.txt`. Les Tables 1 à 6 (constantes cinétiques k1, k2, qe, R2 ; paramètres de Langmuir et de Freundlich) n'ont que leur légende dans le texte, alors que leurs rangées existent dans `corpus/xml/PMC9181868.xml`. Sans rangée dans le texte, aucune citation valide n'est possible : rien n'est extrait de ces six tableaux, et un doute le dit. Le rendu de ces tableaux par `sections.py` est donc encore défaillant (probablement les en-têtes à colspan et les lignes de sous-titre).
- Table 8 (rendement d'élimination de Pb2+, Cu2+, Zn2+ après calcination à 500, 600, 700 °C) : 6 valeurs ajoutées sur `MgFe2O4-NH2-600` (58, 58, 58 %) et `MgFe2O4-NH2-700` (55, 56, 56 %), colonne choisie par l'en-tête. Les valeurs à 500 °C (73, 59, 62), déjà extraites de la phrase du résumé, concordent.
- Table 7 (comparaison de qm) : 12 rangées de la littérature, non extraites. La rangée « Present work » (145.04 et 55.7 mg/g) ne dit pas à quelle température de calcination elle se rapporte ; la rattacher à une voie reviendrait à deviner, donc doute et pas de valeur.
- Les valeurs de pente, ordonnée et R2 déjà extraites des figures 7 à 18 ne sont pas touchées ; elles seraient à recouper avec les Tables 1 à 6 quand celles-ci seront rendues.
- Trois doutes ajoutés (Table 8, Tables 1 à 6 absentes du texte, Table 7).
- Contrôle : `load.py check` 0 erreur, 0 avertissement.
