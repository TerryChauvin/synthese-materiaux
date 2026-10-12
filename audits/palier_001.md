# Audit du palier 1

Genere le 2026-10-12T14:03:59Z — publications n°1 a n°50 (50 sur 50).

## Volume

- Voies : 465 (78 de base, 387 branches)
- Citations verifiees : 5330 — exactes : 5330 (100.0 %)
- Completude moyenne : 0.77
- Familles : {'composite': 103, 'MOF': 55, 'autre': 42, 'oxyde': 41, 'batterie': 41, 'perovskite': 38, 'nanoparticule_metallique': 29, 'chalcogenure': 25, 'materiau_2D': 17, 'ceramique': 17, 'zeolithe': 15, 'carbure': 14, 'quantum_dot': 14, 'carbone': 8, 'silice_mesoporeuse': 6}
- Methodes : {None: 123, 'aqueous-phase glucose reduction with hexadecylamine capping (one-pot, oil bath)': 18, 'extrusion-dripping ionic gelation of sodium alginate in CaCl2 aqueous solution': 17, 'hydrothermal synthesis (point central du plan composite centré, 130 °C, 7 h, pH 7)': 16, 'one-step hydrothermal synthesis (gel formation, aging, crystallization) from diatomite and aluminum hydroxide in NaOH solution': 15, 'coulée en solution de MOF-808 et de copolyimide 6FDD dans du THF, évaporation lente puis recuit': 13, 'sonochemical synthesis in water with a direct immersion ultrasonic probe (70% amplitude, 1 h), thioacetamide as sulfur precursor': 12, 'catalyst-free vapor–solid growth from silicon and carbon black powders in a home-built low-pressure CVD tube furnace under argon': 12, 'soft-templating synthesis in a surfactant-stabilized oil-in-water microemulsion (n-hexane/HFS), ultrasonication then low-temperature synthesis at 30 °C': 11, 'pre-reduction assisted electrospinning, drying, then calcination under Ar': 9, 'solvothermal synthesis in water/ethanol with CTAB at 120 °C': 8, 'room temperature, open atmosphere anti-solvent precipitation in ethyl acetate with oleylamine and oleic acid as capping ligands': 8}

## Anomalies ouvertes

| Controle | Bloquant | Avertissement | Info |
|---|---|---|---|
| citation | 0 | 0 | 0 |
| physique | 0 | 0 | 0 |
| chimie | 0 | 0 | 289 |
| coherence | 0 | 0 | 52 |

| id | Gravite | Controle | Article | Cible | Description |
|---|---|---|---|---|---|

Anomalies de niveau info : 341 (table audit_findings).

## Echantillon a relire a la main

Pour chaque ligne : la citation soutient-elle bien cette valeur, pour cette etape et cette branche ? Consigner le resultat dans `audits/palier_001_relecture.md`, avec le controle de stoechiometrie de 5 voies.

| Article | Voie | Etape | Parametre | Valeur | Citation |
|---|---|---|---|---|---|
| PMC11231976 | A900_A750_3h | 4 | temperature | 900.0 °C | Conversely, particles synthesized from acetate precursors at 900 °C and annealed at 750 °C underwent testing |
| PMC5122874 | NC12_toluene |  | ethyl acetate (anti-solvent) | toluene  | By changing the anti-solvent to toluene |
| PMC6769153 | CQD_500C_3h | 2 | temperature | 500.0 °C | was heated using a heat plate (AS ONE, Japan) at a constant temperature of 500 °C for 3 hours. |
| PMC6266651 | V2C-Ar-375 | 1 | atmosphere | Ar  | after heating at 375 °C in Ar, the sample’s main composition was still V2C MXene |
| PMC10906077 | FAPbBr3_purified_R-MBA | 6 | centrifuge_speed | 7500.0 rpm | the mixture was stirred mildly for 5 min at room temperature and then centrifuged at 7500 rpm for 5 min to precipitate the aggregated particles; the supernatant was collected. |
| PMC7578857 | CsPbBr3-Nd7.2 |  | dopant | 0.15 mmol | the precursor solution of CsPbBr3:xNd3+ (x = 7.2%) NCs was prepared by dissolving NdBr3 (0.15 mmol), PbBr2 (0.1 mmol), and CsBr (0.1 mmol) in DMF (2.5 mL) |
| PMC5376314 | Ni5 | 1 | molar_ratio | 1:2  | Ni5 / C2H5NS / 1:2 / - / 60 / 70 / NiS / 14 / 46.9 |
| PMC11231976 | A900_A750_15h | 7 | duration | 15.0 h | 15 / 0.96 / 1.29 / 0.97 / 4.9914 / 1.65 / 1.42 |
| PMC9043336 | AGO2–CTS5 |  | graphene oxide dispersion | AGO powder  | The same procedure was carried out for AGO powder with the replacement of GO by AGO. |
| PMC5858874 | Ni/TiO2 | 2 | temperature | 25.0 °C | Then the impregnation solution (100 mL) was dropped onto TiO2 powder (20 g) with continuous stirring in a 250 mL beaker at room temperature (25 °C). |
| PMC4456781 | Al_BTC 1 | 3 | molar_ratio_ctab_al | 0.6  | The final CTAB/Al and H2O/EtOH molar ratios were 0.6 and 3.4, respectively, and the pH of the synthesis solution was 2.1. |
| PMC10906077 | FAPbBr3_x25 | 1 | duration | 30.0 min | In a three-necked round-bottom flask, 15 mmol (1.563 g) of FA-acetate, 15 mL of OA, and 15 mL of ODE were degassed under a vacuum at room temperature and 50 °C for 30 min, respectively. |
| PMC4456781 | Al_BTC 4 | 3 | ph | 2.5  | Al_BTC 4 / 100/110 / 2.5 / 1280 / 740 / 530 / 0.72 / 0.30 |
| PMC6199062 | Sb2S3-150 | 5 | temperature | 80.0 °C | dried at 80 °C for 5 h in vacuum |
| PMC7184584 | CsPbBr3_130C_0.8 | 3 | duration | 2.0 h | The mixture was then dried under vacuum for 2 h at 120 °C. |
| PMC4923881 | ZnO-1000 rpm | 3 | stirring_speed | 1000.0 rpm | The whole apparatus was kept on mechanical stirrer under different stirring conditions viz. 500 rpm, 1000 rpm, 1500 rpm and 2000 rpm. |
| PMC9026548 | DCM_P5-L-M30 | 4 | casting_solution_mass | 6.0 g | while the ones cast from 6 g of polymer solutions were denoted as L-version |
| PMC4735866 | AgNPs_AloeVera | 5 | centrifuge_speed | 12000.0 rpm | centrifuged at 12,000 rpm for 15 min at 4 °C |
| PMC7014116 | PLA-HA-2 |  | hydroxyapatite particles | 2.0 wt.% | The hydroxyapatite particles were dispersed by ultrasonication for 30 min into the polymer solution at three different concentrations (1, 2, and 4 wt.%, respectively) in order to obtain a homogenous solution. |
| PMC6631201 | MnO2NFs-NrGO | 6 | temperature | 60.0 °C | The resultant product was collected by centrifugation at 12,000 rpm, followed by cleaning alternately with absolute alcohol and deionized water three times, and dried at 60 °C in a vacuum oven overnight. |
| PMC6812203 | NH2-SBA-15 | 1 | duration | 3.0 h | At first, 1 g of calcined SBA-15 was dried for 3 hr at 100 °C. |
| PMC9026548 | THF_P3-S-M10_medium | 5 | evaporation_rate | medium: funnel placed upside-down over the dish  | (ii) solvent evaporation was slowed down by placing a funnel upside-down |
| PMC10906077 | FAPbBr3_x25 | 9 | volume | 5.0 mL | The precipitate was dispersed in 5 mL of hexane, then centrifuged at 7500 rpm for 5 min to remove the precipitated large particles. |
| PMC5122874 | QD_EtOAc | 3 | addition_mode | drop wise  | 200 μL of precursor solution was added drop wise into the stirring solution. |
| PMC4923881 | ZnO-500 rpm | 2 | concentration | 1.0 % | 10 mL of 1% Zn(CH3COO)2·2H2O solution was added |
| PMC4102124 | size_45nm | 1 | temperature | room temperature  | were added in a 20-ml vial at room temperature. After the vial had been capped |
| PMC6199062 | Sb2S3-150 | 1 | duration | 15.0 min | 3 mmol l-cysteine was dissolved in 30 mL distilled water under magnetic stirring for 15 min to obtain a colorless solution |
| PMC9048217 | Ag/AgCl(20)@ZIF-8 |  | silver nitrate | 20.0 mmol | Adding 20 mmol AgNO3, some Ag/AgCl nanoparticles with an average size of 200 ± 35 nm are formed and adhere on the surface of the ZIF-8. |
| PMC6025012 | ZeoX-NS1.3 | 1 | molar_ratio_na2o_sio2 | 1.3  | Figure 9 shows that all samples with Na2O/SiO2 ratios of 1.3, 1.4 and 1.5 exhibited high crystallinity with smooth faces. |
| PMC6994313 | Zn-MOF_UARM | 5 | duration | 30.0 min | After 30 min, the Zn-MOF crystals are formed |
