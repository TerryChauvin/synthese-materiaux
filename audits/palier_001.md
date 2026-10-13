# Audit du palier 1

Genere le 2026-10-13T13:05:36Z — publications n°1 a n°50 (50 sur 50).

## Volume

- Voies : 609 (124 de base, 485 branches)
- Citations verifiees : 8709 — exactes : 8709 (100.0 %)
- Completude moyenne : 0.74
- Familles : {'composite': 121, 'perovskite': 62, 'MOF': 61, 'autre': 60, 'batterie': 54, 'oxyde': 50, 'zeolithe': 40, 'materiau_2D': 37, 'nanoparticule_metallique': 30, 'chalcogenure': 26, 'carbone': 17, 'ceramique': 17, 'carbure': 14, 'quantum_dot': 14, 'silice_mesoporeuse': 6}
- Methodes : {None: 147, 'one-step hydrothermal synthesis (gel formation, aging, crystallization) from diatomite and aluminum hydroxide in NaOH solution': 40, 'aqueous-phase glucose reduction with hexadecylamine capping (one-pot, oil bath)': 18, 'extrusion-dripping ionic gelation of sodium alginate in CaCl2 aqueous solution': 17, 'hydrothermal synthesis (point central du plan composite centré, 130 °C, 7 h, pH 7)': 16, 'room temperature, open atmosphere anti-solvent precipitation in ethyl acetate with oleylamine and oleic acid as capping ligands': 15, 'self-limiting chemical vapor deposition in a tube furnace from MoCl5 and sulfur powders under Ar flow': 15, 'coulée en solution de MOF-808 et de copolyimide 6FDD dans du THF, évaporation lente puis recuit': 13, 'sonochemical synthesis in water with a direct immersion ultrasonic probe (70% amplitude, 1 h), thioacetamide as sulfur precursor': 12, 'catalyst-free vapor–solid growth from silicon and carbon black powders in a home-built low-pressure CVD tube furnace under argon': 12, 'acid-assisted hydrothermal treatment in HCl aqueous solution at 150 °C for 24 h': 11, 'soft-templating synthesis in a surfactant-stabilized oil-in-water microemulsion (n-hexane/HFS), ultrasonication then low-temperature synthesis at 30 °C': 11}

## Anomalies ouvertes

| Controle | Bloquant | Avertissement | Info |
|---|---|---|---|
| citation | 0 | 0 | 0 |
| physique | 0 | 0 | 0 |
| chimie | 0 | 0 | 383 |
| coherence | 0 | 0 | 85 |

| id | Gravite | Controle | Article | Cible | Description |
|---|---|---|---|---|---|

Anomalies de niveau info : 468 (table audit_findings).

## Echantillon a relire a la main

Pour chaque ligne : la citation soutient-elle bien cette valeur, pour cette etape et cette branche ? Consigner le resultat dans `audits/palier_001_relecture.md`, avec le controle de stoechiometrie de 5 voies.

| Article | Voie | Etape | Parametre | Valeur | Citation |
|---|---|---|---|---|---|
| PMC10906077 | FAPbBr3_purified | 2 | duration | 5.0 min | To purify the FAPbBr3 NCs, 10 mL of MeOAc was added to 5 mL of a stock solution; then it was centrifuged at 7500 rpm for 5 min. |
| PMC5122874 | EtOAc_noligand | 4 | duration | 1.0 min | 0 mL 0 mL 1 min Immediate formation of nonfluorescent yellow precipitate consists of smaller sphere (100 nm) to larger cubes (500 nm) |
| PMC10529665 | Alg/CS_0rpm | 5 | stirring_speed | 0.0 rpm | Stirring rates from 0 to 800 rpm were experimented with, and the resulting size of alginate beads was measured from the digital images (Figure 3). |
| PMC10326808 | HFS_0hexane | 4 | duration | a range of synthesis times (0.5, 1, 1.5, 2, 6, 14, and 24 h)  | maintained at 30 °C and 500 rpm for a range of synthesis times (0.5, 1, 1.5, 2, 6, 14, and 24 h) |
| PMC6025012 | ZeoX-age20 | 4 | duration | 20.0 min | Figure 7 Effect of (a) aging temperature and (b) aging time on CEC of zeolites prepared upon hydrothermal treatment at 110 °C and 5 h. |
| PMC3659320 | MoS2-1L-sapphire | 2 | substrate | sapphire  | Fig. 1 a–b show optical images of the MoS2 monolayer and bilayer films grown on sapphire substrates. |
| PMC6702676 | ZnSe@N-C | 4 | temperature | 80.0 °C | directly dried at 80°C overnight |
| PMC10906077 | FAPbBr3_x25 | 1 | temperature_final | 50.0 °C | In a three-necked round-bottom flask, 15 mmol (1.563 g) of FA-acetate, 15 mL of OA, and 15 mL of ODE were degassed under a vacuum at room temperature and 50 °C for 30 min, respectively. |
| PMC10529665 | Alg/Z5A/Cur | 7 | repetitions | three times  | followed by rinsing the beads three times in deionized water |
| PMC6025012 | ZeoX-agetemp50 | 4 | duration | 60.0 min | Figure 6 XRD patterns showing the effect of (a) aging temperature at aging time of 60 min and (b) aging time at aging temperature of 30 °C on zeolite formation after treatment at 110 °C and 5 h. |
| PMC10326808 | ZIF-8-Ins_tube_furnace | 1 | temperature | 250.0 °C | Later, the hollow ZIF-8 spheres were heated in a tube furnace at 250 °C at a heating rate of 10° min-1 in a continuous flow of N2 gas for 2 hours. |
| PMC5858874 | Ni/TiO2 | 6 | duration | 4.0 h | a calcination process in a muffle oven at 600 °C for 4 h |
| PMC5977331 | ZnO-MCM-0 |  | anhydrous magnesium sulfate | absent  | Additionally, mesoporous silica without salicylaldimine modification was synthesized and noted as MCM-41. |
| PMC6025012 | ZeoX-opt | 5 | duration | 5.0 h | the optimum preparation conditions of zeolite X were 5 h of crystallization time, 110 °C of crystallization temperature, 30 °C of aging temperature, 30 min of aging time, H2O/Na2O ratio of 40 and Na2O/SiO2 ratio of 1.4 |
| PMC10131834 | LED_BCDs |  | WCDs (route WCDs) | replaced by BCDs (monochrome CDs)  | The multicolor CDs/PVP complex solution was prepared from a mixture of monochrome CDs and PVP ethanol solution under ultrasonic for 5 min. |
| PMC3833323 | AgNPs-Ganoderma | 5 | solid_to_liquid_ratio | 1:20  | the freeze-dried mycelia were soaked in distilled water at a ratio of 1:20 and double-boiled for 30 minutes |
| PMC3497326 | CTAB:SDS=1:0 | 2 | ph | 13.0  | 5 mol/L NaOH solution was gradually introduced to the mentioned solution until pH reached at 13 |
| PMC10529665 | Z5A/Cur | 3 | concentration | 0.05 mol/L | a solution of curcumin in ethanol (0.05 mol/L) |
| PMC4735866 | AgNPs_AloeVera | 9 | concentration | 1.0 mM | Aqueous solution of 1 mM silver nitrate (AgNO3) |
| PMC9026548 | DCM_P5-L-M0 | 2 | casting_solution_mass | 6.0 g | while the ones cast from 6 g of polymer solutions were denoted as L-version |
| PMC10529665 | Alg2_Ca10_27G_0rpm_1.6cm | 2 | needle_gauge | 27.0 G | 10 / 27 / 0 / 1.6 / 1.95 ± 0.30 |
| PMC6297875 | NVP_800C_10h_2.5 | 1 | concentration | 0.12 M | 0.12 M solution (30 mL) was prepared using H2C2O4·2H2O and deionized water |
| PMC10131834 | WLED_WCDs | 1 | duration | 5.0 min | under ultrasonic treatment for 5 min |
| PMC3659320 | MoS2-1L-SiO2Si | 2 | substrate | silicon substrates with 280 nm thick silicon oxide (SiO2/Si)  | The optical images of MoS2 monolayer and bilayer films grown on silicon substrates with 280 nm thick silicon oxide (SiO2/Si) are also given as insets. |
| PMC6025012 | ZeoX-agetemp60 | 4 | temperature | 60.0 °C | Figure 7 Effect of (a) aging temperature and (b) aging time on CEC of zeolites prepared upon hydrothermal treatment at 110 °C and 5 h. |
| PMC6025012 | ZeoX-NS2.0 | 3 | molar_ratio_na2o_sio2 | 2.0  | Figure 10 Effect of (a) H2O/Na2O ratio and (b) Na2O/SiO2 ratio on CEC upon hydrothermal treatment at 110 °C and 5 h. |
| PMC6199062 | Sb2S3-150 | 4 | wash_solvent | absolute ethyl alcohol and deionized water  | The Sb2S3 was gathered and washed several times with absolute ethyl alcohol and deionized water |
| PMC7578857 | CsPbBr3-Nd7.2 |  | nd_doping_ratio | 7.2 % | the precursor solution of CsPbBr3:xNd3+ (x = 7.2%) NCs was prepared by dissolving NdBr3 (0.15 mmol), PbBr2 (0.1 mmol), and CsBr (0.1 mmol) in DMF (2.5 mL) |
| PMC10326808 | ZIF-8Lit | 6 | duration | overnight  | Finally, the obtained powder was dried overnight using an air oven at 60 °C. |
| PMC2964502 | TiO2_HCl_protocol | 8 | temperature | 60.0 °C | dried in a vacuum oven overnight at 60°C |
