import json
P='extractions/PMC13315215.json'
d=json.load(open(P,encoding='utf-8'))
r=d['routes'][0]
L=r['characterizations']; O=r['outcomes']
RT="Ce(NDC)MOF@Bentonite"

# 1. reutilisation
L.append({"technique":"réutilisation du catalyseur (5 cycles, Fig. 12)",
 "result":"catalyseur séparé à température ambiante après l'hydrolyse, lavé à l'eau distillée, séché une nuit (overnight), puis réutilisé pour les cycles suivants ; durée totale d'hydrolyse de 47 à 57 min sur cinq cycles (outcomes total_time_for_hydrolysis_cycle_1 à 5)",
 "instrument":None,
 "conditions":"hydrolyse de NaBH4 (0.05 mol/L) avec 50 mg de Ce(NDC)MOF@Bentonite ; température « room temperature » selon la légende de la Fig. 12 ; 5 cycles ; durée du séchage « overnight » (température non donnée)",
 "quote":"In order to assess the catalyst’s reusability in the catalytic hydrolysis of NaBH4 (0.05 mol/L) with the Ce(NDC)MOF@Bentonite (50 mg), the catalyst was separated at room temperature following the hydrolysis, cleaned with distilled water, and then dried overnight to recover it for additional cycles."})

# 2. conditions fixes des series
L.append({"technique":"hydrolyse catalytique — série en dose de catalyseur (Tableaux 1-2, Fig. 9)",
 "result":"volume de H2 suivi pendant toute la réaction pour chaque dose ; constantes K (Tableau 1), HGR (Tableau 2), R (Fig. 9c)",
 "instrument":None,
 "conditions":"0.05 mol/L NaBH4 solution at 30 °C ; catalyst weights ranging from 16 to 100 mg",
 "quote":"In this study using 0.05 mol/L NaBH4 solution at 30 °C, in the presence of various catalyst weights ranging from 16 to 100 mg"})
L.append({"technique":"hydrolyse catalytique — série en concentration de NaBH4 (Tableau 3, Fig. 10)",
 "result":"volume de H2 en fonction du temps pour chaque concentration ; constantes K (Tableau 3), R (Fig. 10c), pente log-log (Fig. 10d)",
 "instrument":None,
 "conditions":"30˚C ; 50 mg of catalyst ; NaBH4 0.01–0.10 mol/L",
 "quote":"such measurements were carried out at 30˚C using 50 mg of catalyst under various concentrations of NaBH4 (0.01–0.10 mol/L)"})
L.append({"technique":"hydrolyse catalytique — série en température (Tableaux 2 et 4, Fig. 11)",
 "result":"volume de H2 en fonction du temps à chaque température ; HGR (Tableau 2), R (Fig. 11c), K et grandeurs d'activation (Tableau 4), énergie d'activation (Fig. 11e)",
 "instrument":None,
 "conditions":"50 ml of 0.05 mol/L NaBH4 solution together with 50 mg of the catalyst ; temperature ranging from 25 to 45 ˚C",
 "quote":"50 ml of 0.05 mol/L NaBH4 solution together with 50 mg of the catalyst, then the reaction proceeded at a temperature ranging from 25 to 45 ˚C"})

# 3. TGA etapes 2 et 3
O.append({"property":"TGA_second_stage_maximum_temperature","value_num":198,"unit":"°C",
 "quote":"The second stage is maximized at 198 °C and related to the evaluation of organic solvent used during synthesis process."})
O.append({"property":"TGA_third_stage_onset_temperature","value_num":240,"unit":"°C",
 "quote":"the thired stage which startes at 240 °C"})

# 4. XPS O 1s
L.append({"technique":"XPS (O 1s)","result":"O 1s : pics à 531 et 531,9 eV attribués à l'oxygène de réseau (lattice oxygen) et à l'oxygène adsorbé en surface ; le texte annonce trois pics et n'en donne que deux",
 "instrument":None,"conditions":"Al-Kα, hν = 1486.6 eV (voir la caractérisation XPS)",
 "quote":"O 1 s peak analysis resolves three peaks at 531, and 531.9 eV assignable are attributed to the lattice oxygen and surface adsorbed oxygen Fig. 8c, respectively."})

# 5. references XRD et FT-IR
L.append({"technique":"XRD (échantillons de référence : bentonite brute et NDC)",
 "result":"bentonite brute : trois pics principaux à 2θ = 5,8 ; 12,3 et 24,5 attribués à la smectite, à la kaolinite et au quartz ; NDC seul : pic principal à 2θ = 13,24 ; ces pics disparaissent dans le diffractogramme du composite",
 "instrument":None,"conditions":"voir la caractérisation XRD du composite",
 "quote":"The x-ray diffraction pattern of the raw sample indicates the appearance of three main peaks located at 2Ɵ equal 5.8, 12.3, and 24.5 which are related to smectite, kaolinite, and quartz minerals respectively."})
L.append({"technique":"FT-IR (échantillons de référence : bentonite brute et NDC)",
 "result":"bentonite : bandes à 3701 cm−1 (O-H internes), 3740 et 3650 cm−1 (minéral à l'état organisé), 1031 cm−1 (Si-O symétrique), 913 cm−1 (déformation Al-OH), 787 cm−1 (Si-O du quartz) ; NDC : 1519 cm−1 (élongation C=C)",
 "instrument":None,"conditions":"voir la caractérisation FT-IR du composite",
 "quote":"Meanwhile, the appearance of the bands at 3740 and 3650 cm− 1 suggested that the mineral is present in the organized state."})
for c in L:
    if c['technique']=="FT-IR":
        c['result']+=" ; bandes à 790 et 661 cm−1 attribuées aux groupes OH et C-H de la partie ligand du composite"
    if c['technique']=="TGA/DSC":
        c['result']="trois étapes, perte totale d'environ 47 % jusqu'à 500 °C : 1re étape d'environ 8 % entre 30 et 150 °C (eau), 2e étape maximale à 198 °C (solvant organique), 3e étape débutant à 240 °C avec une chute abrupte de 40 % à 315 °C (décomposition vers l'oxyde de cérium) ; pic DTG à 339"

# inventaire : resultats des references
for s in d['sample_inventory']:
    if s['sample'].startswith('bentonite brute') or s['sample'].startswith('NDC'):
        s['why']+=" ; pics XRD et bandes FT-IR de référence extraits en caractérisations « échantillons de référence »"

# doutes
d['doubts'].append({"where":"TGA, texte contre Fig. 2",
 "issue":"Les valeurs du texte sont retenues (perte abrupte de 40 % à 315 °C, 3e étape débutant à 240 °C, 2e étape maximale à 198 °C). Sur la Fig. 2, la chute abrupte se situe plutôt vers 340 °C (cohérent avec le pic DTG à 339) et vaut environ 30 % (de 83 % à 53 % de masse environ) ; la masse remonte ensuite jusqu'à environ 57 % à 590 °C. La somme des étapes (8 % + 2e étape + 40 %) dépasse aussi la perte totale de 47 % annoncée pour trois étapes."})
d['doubts'].append({"where":"XPS O 1s",
 "issue":"Le texte annonce « three peaks » pour O 1s mais ne donne que deux énergies (531 et 531,9 eV) ; les deux valeurs sont extraites, le troisième pic n'est pas donné."})

def ann(text):
    return {"type":"limite_reproductibilite","route":RT,"text":text}
A=[
"Sur la Fig. 2, la chute abrupte de l'ATG se situe vers 340 °C (cohérent avec le pic DTG à 339) et vaut environ 30 % de la masse, et non 40 % à 315 °C comme dans le texte ; la méthode annonce 700 °C alors que la courbe s'arrête vers 590 °C. Le critère de décomposition du MOF (jusqu'à 330 °C pour les MOF de Ce(IV) de type UiO, d'après Cryst. Growth Des. 2017, 10.1021/acs.cgd.6b01512) reste plausible, mais les chiffres de pourcentage sont à prendre avec réserve.",
"L'énergie d'activation de 217,8 kJ/mol est incompatible avec les constantes de vitesse du tableau 4 : la régression d'Arrhenius de ces k donne environ 22 kJ/mol (environ 35 kJ/mol avec les HGR, 56 kJ/mol avec les R de la Fig. 11c), soit un facteur proche de 10. La valeur publiée, qualifiée de « faible » en conclusion, dépasserait même l'énergie apparente de l'auto-hydrolyse non catalysée (65 à 162 kJ/mol, Retnamma et al., Int. J. Hydrogen Energy 2014, 10.1016/j.ijhydene.2014.02.035) : elle est reprise telle quelle, mais ne doit pas servir à comparer ce catalyseur.",
"Les grandeurs du tableau 4 ne sont pas utilisables : les paramètres d'Eyring recalculés avec les k des auteurs donnent ΔH‡ d'environ +19,5 kJ/mol, ΔS‡ d'environ −200 J/(mol·K) et ΔG‡ d'environ +80 kJ/mol, alors que le tableau donne ΔH = −(Ea + RT), un ΔS d'environ +1 kJ/(mol·K) irréaliste et un ΔG égal à ΔH − TΔS au signe inversé. Des grandeurs d'activation ne prouvent d'ailleurs pas qu'une réaction est spontanée (Brack et al., Energy Sci. Eng. 2015, 10.1002/ese3.67) ; les constantes kB et h sont aussi mal recopiées dans le texte.",
"Les constantes de vitesse du tableau 4 sont notées en s−1 alors que, pour les mêmes conditions, les tableaux 1 et 3 les donnent en min−1 (0,087 à 0,105) : en s−1 la demi-vie serait d'environ 9 s, incompatible avec des essais de 47 à 57 min ; ce sont des min−1. La pente log-log de 0,63 (environ 0,72 recalculé sur la Fig. 10c) correspond à un ordre fractionnaire et non à l'ordre 1 affirmé, et les k « du premier ordre » du tableau 3 augmentent avec la concentration initiale, ce qui contredit aussi l'ordre 1.",
"Aucun essai à blanc n'est rapporté : ni NaBH4 seul, ni bentonite seule, ni MOF seul, et le pH n'est pas donné. NaBH4 est utilisé sans NaOH ; la demi-vie d'auto-hydrolyse à 30 °C est d'environ 13 min à pH 9,5, 41 min à pH 10 et 130 min à pH 10,5 (relation de Kreevoy et Jacobson, 1979, reprise par DergiPark 2020, https://dergipark.org.tr/tr/download/article-file/1180786), soit l'échelle de temps des essais de 47 à 57 min. La part de l'hydrogène due au catalyseur, donc les HGR, k et Ea, n'est pas établie.",
"L'activité de 116 mL min−1 g−1 est faible parmi les catalyseurs de cette réaction (Brack et al., Energy Sci. Eng. 2015, 10.1002/ese3.67) ; le meilleur HGR à 16 mg est un effet de normalisation par la masse, car le débit absolu y est le plus faible (environ 1,9 mL/min). Les HGR du tableau 2 ne concordent avec les R de la Fig. 9c qu'à 90 et 100 mg, et le tableau 5 compare des conditions et des unités hétérogènes ; les qualificatifs « highly active » et « superior » ne sont pas soutenus.",
"La surface BET de 58,5 m²/g, avec une isotherme de type IV et une boucle H2/H3, est très inférieure à celle de Ce-UiO-66-BDC (1282 m²/g) pour un composite censé contenir environ 60 % de MOF en masse ; elle indique un MOF peu ou pas poreux (effondré, amorphe ou minoritaire). Le Ce-UiO-66 à ligand naphtalénique se décompose à l'activation sous vide dès 100 °C et perd sa cristallinité dans l'eau, l'éthanol et à l'air (Lammert et al., Chem. Commun. 2015, 10.1039/C5CC02606G), alors que le dégazage est fait ici à 110 °C après lavage à l'éthanol. Le « 196 ˚C » de l'azote doit se lire −196 °C et la section de 16,2 Å, 16,2 Å².",
"Le pic de la bentonite brute à 2θ = 24,5° (d = 3,63 Å) n'est pas le quartz (raie principale à 3,34 Å, 26,64°) ; surtout, la disparition annoncée de toutes les raies de l'argile, quartz compris, n'est pas crédible pour un composite contenant environ 40 % d'argile, et la « phase cristalline pure » du résumé est incompatible avec un support naturel contenant quartz et kaolinite. Les deux pics à 7 et 8° concordent en revanche avec les raies (111) et (200) calculées d'un réseau de type UiO-66 au cérium (7,12 et 8,23°, d'après Lammert et al. 2015, 10.1039/C5CC02606G).",
"Les paires XPS Ce 3d attribuées par les auteurs ne respectent pas l'écart spin-orbite d'environ 18,6 eV du cérium : 900 et 914,7 eV pour Ce(IV) (écart de 14,7 eV) et 878,4 et 903,2 eV pour Ce3+ (écart de 24,8 eV), et 900 eV appartient à la région 3d3/2 ; la signature de Ce(IV) est le pic vers 916,7 eV (Bêche et al., Surf. Interface Anal. 2008, cité par la fiche Thermo Fisher « Cerium »). La proportion de Ce3+ n'est donc pas établie.",
"La synthèse s'écarte des conditions connues de Ce-UiO-66 : le cérium est en excès (rapport Ce:NDC d'environ 1,33 si le ligand est l'acide et 1,60 si c'est le sel disodique, contre 1:1 pour [Ce6O4(OH)4(L)6]), le Ce(IV) reste 24 h au contact du DMF avant le chauffage (la synthèse de référence retient 15 min à 100 °C ; Lammert et al. 2015, 10.1039/C5CC02606G), ce qui peut réduire une partie du cérium et former des phases non poreuses, et le milieu est à environ 64 % d'eau. Le devenir de l'excès de cérium (33 à 60 %) n'est pas analysé, et le récipient du chauffage à 120 °C n'est pas précisé : ouvert, l'eau s'évapore ; fermé, la pression de vapeur de l'eau atteint environ 1,8 à 2 bar (NIST Chemistry WebBook).",
]
d['annotations'].extend(ann(t) for t in A)
json.dump(d,open(P,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
