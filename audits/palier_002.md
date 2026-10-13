# Audit du palier 2

Genere le 2026-10-13T20:36:36Z — publications n°51 a n°100 (50 sur 50).

## Volume

- Voies : 581 (111 de base, 470 branches)
- Citations verifiees : 8796 — exactes : 8796 (100.0 %)
- Completude moyenne : 0.75
- Familles : {'composite': 93, 'perovskite': 89, 'nanoparticule_metallique': 78, 'oxyde': 69, 'zeolithe': 61, 'quantum_dot': 35, 'MOF': 32, 'autre': 22, 'batterie': 22, 'silice_mesoporeuse': 20, 'materiau_2D': 16, 'chalcogenure': 15, 'ceramique': 12, 'nitrure': 9, 'carbone': 8}
- Methodes : {None: 96, 'ligand-assisted precipitation (antisolvent precipitation of a DMF precursor solution into toluene at 3–4 °C)': 46, 'solvothermal (zinc acetylacetonate monohydrate in ethanol–water, Teflon lined autoclave), point central du plan Box–Behnken': 28, 'sonochemical TiO2 shell deposition (TTIP hydrolysis under ultrasound) on CdS cores; central point of the central composite design': 27, 'sonochemical (probe ultrasound) precipitation in water; centre point of the central composite design (90 min, 55 amplitude, 9.4 mmol/L); runs Ce-MOF15 to Ce-MOF20 are replicates': 16, 'Stober sol–gel process with pluronic P123 template, TEOS, glycerol and HCl, aging at 100 °C, calcination at 550 °C': 13, 'sol impregnation (sol–gel puis imprégnation à volume constant, calcination)': 13, 'room-temperature co-precipitation with ammonia in the presence of ammonium persulfate': 13, 'alkaline hydrothermal treatment of anatase TiO2 in 10 M NaOH, then washing with HCl and water': 12, 'adsorption des N-CDs sur MSN-NH2 en solution aqueuse': 11, 'green synthesis: reduction of HAuCl4 by caffeic acid on a hotplate then 12 h in an oven at 85 °C': 11, 'seed-assisted hydrothermal synthesis (170 °C, 48 h) followed by ion exchange to the H form': 10}

## Anomalies ouvertes

| Controle | Bloquant | Avertissement | Info |
|---|---|---|---|
| citation | 0 | 0 | 0 |
| physique | 0 | 1 | 0 |
| chimie | 0 | 0 | 207 |
| coherence | 0 | 2 | 101 |

| id | Gravite | Controle | Article | Cible | Description |
|---|---|---|---|---|---|
| 1937 | avertissement | coherence | PMC8941405 | route 'S60' | voie de base sans reactif |
| 1939 | avertissement | coherence | PMC8941405 | route 'S80' | voie de base sans reactif |
| 1634 | avertissement | physique | PMC8941405 | voie 'S60-0.2-0.5' etape 3 temperature | 170 °C au-dessus du point d'ebullition du solvant (100 °C) sans autoclave, reflux ni enceinte fermee mentionnes |

Anomalies de niveau info : 308 (table audit_findings).

## Echantillon a relire a la main

Pour chaque ligne : la citation soutient-elle bien cette valeur, pour cette etape et cette branche ? Consigner le resultat dans `audits/palier_002_relecture.md`, avec le controle de stoechiometrie de 5 voies.

| Article | Voie | Etape | Parametre | Valeur | Citation |
|---|---|---|---|---|---|
| PMC8941405 | S60-5d | 1 | duration | 5.0 d | Figure 2. SEM images of ZSM-5 synthesized by using 0.2 wt.% S60 crystallized with different times (crystallization time: (a) 0 d (no seeds), (b) 1 d, (c) 3 d, (d) 5 d, (e) 10 d and (f) 20 d). |
| PMC10780621 | NaOH_0.25 |  | sodium hydroxide | 0.25 NaOH/Si | 5 / 0.25 / 214 / 190 / 24 / 0.11 / 0.08 / 0.03 |
| PMC7996286 | Met-GO/SA | 5 | duration | 24.0 h | harden after staying 24 h in the CaCl2 solution, to yield stable beads |
| PMC9060541 | CdS-core | 2 | power | 45.0 W | Typically, 1 mL of ethylenediamine was added to 50 mL water in a beaker at room temperature, and then, 0.3 mL of CS2 was added to complete the oil phase, which was irradiated for 20 min using ultrasound waves (TOMY, UD 201, acoustic power 45 W with digital water bath temperature controller) at 40 °C until the solution became clear. |
| PMC10324055 | Ce-BDC_RT | 3 | temperature | room temperature  | Ce(III)-BDC MOF was synthesized in water as a sole solvent by direct precipitation at room temperature |
| PMC6720160 | TPPH2 | 1 | temperature | 141.0 °C | The synthesis of CuInS core and CuInS/ZnS core/shell (S1), TPPH2 (S2) and TPPS4 (S3), is extensively reported in the supplementary information. |
| PMC8159122 | ZnO-r opt |  | zinc acetylacetonate monohydrate (ZnAA2) | 0.068 M | Optimized r(002)/(100) (ZnO-r opt) / 190 / 0.068 / 90 / 7.56 / 74.90 / 0.873 / 77.30 / 0.834 |
| PMC7760056 | AgNPs-opt | 6 | wash_solvent | double-distilled water followed by methanol  | Finally, the biomolecule-capped AgNPs were washed several times with double-distilled water followed by methanol and dried at room temperature for further analysis and applications. |
| PMC6104471 | Br_n6 |  | layer_number_n | 6.0  | TEM images of 2D Br-series perovskite QDs with n= 3,4 and 6. |
| PMC3477086 | TOPO_ODA_1to1 |  | TOPO/ODA mass ratio | 1:1  | Figure 7 Fluorescence spectra of Cd-doped ZnO QDs for different TOPO/ODA mass ratios. (a)1:5, (b) 1:3, (c) 1:2, (d) 1:1, (e) 2:1. |
| PMC9631917 | TNT_130C_96h | 3 | duration | 96.0 h | the reactions were performed at 130 °C for 24, 30, 36, 42, 54, 60, and 96 h |
| PMC10780621 | NaHCO3_HF1 |  | hydrofluoric acid | 1.0 HF/Si | 4 / 1 / 240 / 211 / 29 / 0.17 / 0.08 / 0.09 |
| PMC11266555 | Ce-MOF-HT | 3 | duration | 5.0 min | It was then collected by centrifugation at 4000 rpm for 5 min at RT. |
| PMC10293723 | VaAgNPs_MDW-1to1_screen | 1 | wash_solvent | double-distilled water  | The V. amygdalina leaves were thoroughly washed three times with double-distilled water to remove debris and dust particles. |
| PMC9060541 | CCD-Run10 | 2 | duration | 60.0 min | 10 / 76.00 / 60.00 / 41.00 / 3.00 / 24.62 / 25 / 67.00 / 75.00 / 45.00 / 4.50 / 19.19 |
| PMC3293091 | LiFePO4_C10_170 | 4 | temperature | 170.0 °C | The bomb was sealed and heated at 170°C for 16 h in a high-temperature conventional oven. |
| PMC9060541 | CCD-Run10 | 1 | molar_ratio | 3.0  | 10 / 76.00 / 60.00 / 41.00 / 3.00 / 24.62 / 25 / 67.00 / 75.00 / 45.00 / 4.50 / 19.19 |
| PMC9866506 | FeVO4_nH2O | 9 | duration | overnight  | vacuum dried at 60 °C overnight |
| PMC9866506 | FV500_PVDF |  | polyacrylic acid (PAA) solution, 35 weight % in ethanol | replaced by PVDF binder solution, 5 weight % in NMP (voie PVDF_binder_solution)  | Two different binder materials [35 weight % polyacrylic acid (PAA) in ethanol solvent and 5 weight % of polyvinylidene fluoride (PVDF) in NMP (2-N-Methyl-pyrrolidone) solvent] were used for fabricating the working electrodes of FV500, FV600, and FV700. |
| PMC9059895 | CdS-1 | 3 | duration | 40.0 min | The samples were named as CdS-1, CdS-2, and CdS-3 corresponding to 40 min, 100 min and 4 h of reaction time, respectively. |
| PMC5327880 | Heat100C_10min | 1 | atmosphere | Argon  | All syntheses were performed under Argon. |
| PMC10870029 | CsPbBr3_NC | 14 | temperature | 5.0 °C | The supernatant was removed; the pellets were dispersed in hexane and centrifugated at 8500 rpm at 5 °C for 5 min. |
| PMC8125239 | LaCoO3/CeO2-6h | 7 | duration | 6.0 h | The effects of different calcination times (5, 6, 7, 8, 9, and 10 h) on the catalytic activity of LaCoO3/CeO2 were investigated (Figure 4). |
| PMC3477086 | TOPO_ODA_modified | 1 | addition_rate | slowly  | were slowly mixed |
| PMC9316793 | CDs-1 | 1 | 3-aminophenylboronic acid | 0.01 mol/L | For comparison, the effect of doping amount on the lignin-derived CDs was investigated by only varying the acid concentrations (0.01, 0.04, 0.07 and 0.10 mol/L). |
| PMC6315938 | Support_mullite_alumina | 3 | temperature | 1300.0 °C | Combined mullite-alumina supports with a 50 wt.% alumina powder content were synthesized in a similar way but were calcinated at 1300 °C. |
| PMC10780621 | NaHCO3_t72h | 7 | duration | 72.0 h | With a prolonged reaction time of 72 h, single hexahedron grew into multilayers. |
| PMC10780621 | NaHCO3_t36h | 6 | temperature | 80.0 °C | Next, the mixture was heated at 80 °C |
| PMC7023346 | PAN_OMMT_fibers | 1 | temperature | 50.0 °C | O-MMT and PAN solid powder were dried at 50 °C for 12 h before use. |
| PMC3088885 | CoFe2O4-SiO2_800C | 2 | temperature | 800.0 °C | TEM images and selected area electron diffraction (SAED) pattern of the nanocomposites calcined at 600 and 800°C were shown in Figure 4. |
