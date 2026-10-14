import json
P = "extractions/PMC11345764.json"
d = json.load(open(P, encoding="utf-8"))
R = {r["label"]: r for r in d["routes"]}

APPAR = ("pressurized fixed-bed reactor, stainless steel reactor tube (i.d. = 10 mm); "
         "NH3 absorbée dans H2SO4 dilué 0,2 mol L−1 et dosée par ion chromatography "
         "(Thermo Scientific, DIONEX, ICS-600)")
STD_COND = ("0,2 g de catalyseur (20−40 mesh) dilué avec de la poudre de quartz ; prétraitement dans "
            "25%N2-75%H2 à 500 °C pendant 2 h ; alimentation 25%N2–75%H2, WHSV 60 000 mL g–1 h–1")
RATE_Q = ("The NH3 synthesis rates over Co/Mo2CTx, Ni/Mo2CTx, and Re/Mo2CTx are 15.2, 21.5, and 22.4 "
          "mmol g–1 h–1 at 400 °C and 1 MPa, respectively.")
ARRH_Q = ("Apparent activation energies of the as-prepared catalysts were calculated from Arrhrenius "
          "plots of the NH3 synthesis rates in the temperature range of 300−400 °C.")
WO3_Q = ("Figure S27. Photographs of WO3, the mixture of WO3 and NPMs/Mo2CTx catalysts before "
         "treatment and after hydrogen treatment at 250 °C for 10 min.")
S3 = "Table S3"
S4 = "Table S4"

# --- constat 6 : nom du materiau et etat du Mo2CTx
m = R["Mo2CTx"]
m["material"]["name"] = "Mo2CTx MXene (tel que synthétisé ; réduit à 500 °C avant l'essai catalytique)"
note = "Mo2CTx supposé tel que synthétisé (non réduit) : le texte ne le dit pas explicitement"
for c in m["characterizations"]:
    t = c["technique"]
    if t in ("XRD", "Raman", "SEM", "EDX", "ICP-AES", "H2-TPR"):
        c["conditions"] = (c["conditions"] + " ; " if c.get("conditions") else "") + note
    elif t == "catalytic NH3 synthesis test":
        c["instrument"] = APPAR
        c["conditions"] = STD_COND + " ; Mo2CTx réduit (« fresh Mo2CTx was reduced at 500 °C for 2 h »)"

# --- constat 4 : conditions de l'essai catalytique et Arrhenius
for lab in ("Mo2CTx", "Re/Mo2CTx", "Ni/Mo2CTx", "Co/Mo2CTx"):
    r = R[lab]
    r.setdefault("characterizations", [])
    ch = r["characterizations"]
    for c in ch:
        if c["technique"] == "catalytic NH3 synthesis test":
            c["instrument"] = APPAR
            if lab == "Re/Mo2CTx":
                c["conditions"] = STD_COND
    if lab in ("Ni/Mo2CTx", "Co/Mo2CTx"):
        ch.append({
            "technique": "catalytic NH3 synthesis test (conditions standard)",
            "result": f"vitesse de synthèse de NH3 de {lab} à 400 °C et 1 MPa",
            "instrument": APPAR, "conditions": STD_COND, "quote": RATE_Q})
    ch.append({
        "technique": "Arrhenius analysis (apparent activation energy)",
        "result": "énergie d'activation apparente tirée de droites d'Arrhenius entre 300 et 400 °C",
        "instrument": None, "conditions": "plage de température 300−400 °C", "quote": ARRH_Q})

# Ni : l'essai a 0,9 MPa garde son apparatus complet (fait ci-dessus)

# --- constat 5 : essais de marquage et WO3
re = R["Re/Mo2CTx"]
re["characterizations"] += [
    {"technique": "D2 isotopic exchange",
     "result": "signaux H2 (m/z 2) et HD (m/z 3) générés simultanément après l'introduction de D2",
     "instrument": "Autochem 2920 avec spectromètre de masse en ligne",
     "conditions": "traitement 10%H2/Ar à 500 °C pendant 2 h, puis 400 °C sous 5%D2/Ar",
     "quote": "Isothermal D2 isotopic exchange experiments show that the signals of H2 (m/z = 2) and HD (m/z = 3) simultaneously generate after the introduction of D2 over Re/Mo2CTx (Figure S26)"},
    {"technique": "14N2/15N2/H2 isothermal isotopic labeling",
     "result": "signal 14N15N (m/z 29) net sur Re/Mo2CTx et Mo2CTx, quasi absent sur β-Mo2C",
     "instrument": "Autochem 2920 avec spectromètre de masse en ligne",
     "conditions": "traitement 10%H2/Ar à 500 °C pendant 2 h, puis 400 °C sous 14N2/15N2/H2 = 2:1:6 (volume)",
     "quote": "After the introduction of the 15N2–14N2–H2 mixture, almost no 14N15N signal (m/z = 29) was detected over β-Mo2C (Figure 5c), while the 14N15N signal could be clearly discerned over Re/Mo2CTx (Figure 5d) and Mo2CTx (Figure S29)."},
]
for lab in ("Re/Mo2CTx", "Ni/Mo2CTx", "Co/Mo2CTx"):
    R[lab]["characterizations"].append({
        "technique": "WO3 colour test (H spillover)",
        "result": ("mélange WO3 + " + lab + " : passage du jaune clair au bleu foncé sous H2 ; pas de changement net pour WO3 seul"
                   if lab == "Re/Mo2CTx" else "changement de couleur analogue à celui observé avec Re/Mo2CTx"),
        "instrument": None,
        "conditions": "traitement sous H2 à 250 °C pendant 10 min (légende de la Fig. S27, valable pour NPMs/Mo2CTx)",
        "quote": WO3_Q})

# --- constat 2 : Table S3
def oc(prop, val, quote, unit=None):
    o = {"property": prop, "quote": quote, "value_num": val}
    if unit:
        o["unit"] = unit
    return o
row = lambda a: a
re["outcomes"] += [
    oc("Mo4+_fraction_after_N2_400C_2h", 78, "2.5%N2/Ar 78 22 3.5 50.5 49.5 1.02", "%"),
    oc("Mo4+_fraction_after_N2_H2_400C_2h", 81, "2.5%N2+7.5%H2/Ar 81 19 4.3 51.2 48.8 1.05", "%"),
    oc("Mo4+_Mo6+_ratio_after_N2_H2_400C_2h", 4.3, "2.5%N2+7.5%H2/Ar 81 19 4.3 51.2 48.8 1.05"),
    oc("Re0_Re2+_ratio_fresh", 0.82, "Fresh 65 35 1.9 45.1 54.9 0.82"),
    oc("Re0_Re2+_ratio_after_H2_400C_2h", 1.03, "10%H2/Ar 88 12 7.3 51.0 49.0 1.03"),
    oc("Re0_Re2+_ratio_after_N2_400C_2h", 1.02, "2.5%N2/Ar 78 22 3.5 50.5 49.5 1.02"),
    oc("Re0_Re2+_ratio_after_N2_H2_400C_2h", 1.05, "2.5%N2+7.5%H2/Ar 81 19 4.3 51.2 48.8 1.05"),
]
# --- constat 3 : Table S4 et EXAFS in situ
re["outcomes"] += [
    oc("N2_desorption_N2-TPD", 0.62, "Re/Mo2CTx 10 0.62 0.51 0.71", "mmol gcat-1"),
    oc("N2_desorption_after_N2_H2_coadsorption", 0.51, "Re/Mo2CTx 10 0.62 0.51 0.71", "mmol gcat-1"),
    oc("H2_desorption_after_N2_H2_coadsorption_per_g_catalyst", 0.71, "Re/Mo2CTx 10 0.62 0.51 0.71", "mmol gcat-1"),
]
EX = ("the first shell of the Mo–C(N) coordination number gradually increases from 5.6 to 6.3 "
      "with an increase of time-on-stream")
re["outcomes"] += [
    oc("Mo_C(N)_first_shell_CN_in_situ_EXAFS_start_of_time-on-stream", 5.6, EX),
    oc("Mo_C(N)_first_shell_CN_in_situ_EXAFS_end_of_time-on-stream", 6.3, EX),
]
ni, co = R["Ni/Mo2CTx"], R["Co/Mo2CTx"]
NIQ, COQ = "Ni/Mo2CTx 20 -- 0.41 0.72", "Co/Mo2CTx 10 -- 0.43 0.65"
ni["outcomes"] += [
    oc("N2_desorption_after_N2_H2_coadsorption", 0.41, NIQ, "mmol gcat-1"),
    oc("H2_desorption_after_N2_H2_coadsorption_per_g_catalyst", 0.72, NIQ, "mmol gcat-1")]
co["outcomes"] += [
    oc("N2_desorption_after_N2_H2_coadsorption", 0.43, COQ, "mmol gcat-1"),
    oc("H2_desorption_after_N2_H2_coadsorption_per_g_catalyst", 0.65, COQ, "mmol gcat-1")]

# --- constat 1 : Co, teneur de 10 wt % citee depuis le tableau S4, variation sans changement retirée
co["variations"] = [v for v in co["variations"] if v.get("parameter") != "metal_loading"]
co["characterizations"].append({
    "technique": "N2/H2 TPD (co-adsorption), metal loading",
    "result": "Co/Mo2CTx à 10 wt % de Co (colonne Metal loading, catalyseurs as-synthesized) ; désorption de N2 0,43 et de H2 0,65 mmol gcat-1",
    "instrument": None, "conditions": None, "quote": COQ})

# --- constat 7 : ref15 retiré (conditions écrites dans l'article)
d["method_sources"] = [s for s in d["method_sources"] if s.get("ref_id") != "ref15"]

# --- doutes
dbt = d["doubts"]
for x in dbt:
    if x["where"].startswith("Re/Mo2CTx, étape 2"):
        x["where"] = "Re/Mo2CTx, étape 2 (taux de charge) ; Ni/Mo2CTx ; Co/Mo2CTx"
        x["issue"] = ("La partie Méthodes ne donne que les teneurs en Re (5, 10 et 15 wt %). Le taux de 10 wt % de la voie de base "
                      "se lit dans le tableau S1 (22,4), dans la phrase « maximum of 10 wt % Re, 20 wt % Ni, and 10 wt % Co » et dans "
                      "le tableau S4 (colonne Metal loading des catalyseurs as-synthesized : Re/Mo2CTx 10, Ni/Mo2CTx 20, Co/Mo2CTx 10). "
                      "Pour Co/Mo2CTx, le tableau S4 donne 10 wt % : c'est la teneur de l'échantillon (15,2 mmol g–1 h–1) pris dans "
                      "l'article, la voie hérite donc des 10 wt % du parent et ne porte pas de variation de teneur ; la citation de la "
                      "teneur est la rangée du tableau S4 (caractérisation de la voie Co). Les autres teneurs de Ni et de Co (Fig. S9–S10) "
                      "sont inconnues.")
    if x["where"].startswith("Fig. 4c"):
        x["issue"] = ("La Fig. 4c a deux axes (Mo4+/Mo6+ à gauche, Re0/Re2+ à droite). Les points qui semblent valoir la moitié "
                      "des valeurs du texte (≈ 3,6 au lieu de 7,3) viennent très probablement de l'axe de droite ; le tableau S3 "
                      "(65/35 = 1,9 ; 88/12 = 7,3 ; 78/22 = 3,5 ; 81/19 = 4,3) est cohérent avec le texte, qui est retenu. La figure n'est pas lue.")
dbt.append({"where": "Mo2CTx, état (frais ou réduit) des caractérisations",
            "issue": ("Le nom du matériau décrit le Mo2CTx réduit à 500 °C avant l'essai catalytique (« fresh Mo2CTx was reduced at 500 °C "
                      "for 2 h … before measurements »), alors que XRD, Raman, SEM, EDX, ICP-AES et H2-TPR sont décrits dans la partie "
                      "« Structure Properties » sans dire si l'échantillon est réduit : ils sont enregistrés comme portant sur le Mo2CTx "
                      "tel que synthétisé, ce que le texte ne précise pas. L'état de l'échantillon mesuré par EXAFS (Mo–C(O) 6,6) n'est pas dit non plus.")})

# --- annotations limite_reproductibilite (critique scientifique)
def lim(route, text):
    d["annotations"].append({"type": "limite_reproductibilite", "route": route, "text": text})

lim("Re/Mo2CTx", "L'indexation de la frange de 0,23 nm (AC-HAADF-STEM) au plan (002) de Mo2CTx est incompatible avec l'XRD de l'article : "
    "le pic (002) à 2θ = 8,39° donne d ≈ 1,05 nm (Bragg, Cu Kα 1,5406 Å). Une distance de 0,23 nm correspond plutôt à Re(002) (≈ 0,223 nm), "
    "Re(100) (≈ 0,239 nm) ou β-Mo2C(002) (≈ 0,237 nm), d'après les paramètres de maille usuels ; elle ne prouve donc pas l'interface Re/MXene "
    "et laisse ouverte la présence de β-Mo2C formé par le traitement à 500 °C.")
lim("Re/Mo2CTx", "Les teneurs en Re (5, 10, 15 wt %) sont nominales : aucun dosage du rhénium après réduction (l'ICP-AES ne porte que sur Ga). "
    "NH4ReO4 se décompose en Re2O7 volatil dès ≈ 250 °C (source secondaire : fiche « Ammonium perrhenate », Wikipedia) et la montée à "
    "2 °C min–1 passe ≈ 1 h entre 250 et 360 °C : une perte de Re est possible, et les vitesses par gramme reposent sur des charges non vérifiées.")
lim("Mo2CTx", "Le lavage par NaOH 0,2 mol L–1 + NH3·H2O 1 mol L–1 intercale normalement des cations Na+ entre les feuillets ; le sodium résiduel "
    "n'est ni dosé (l'EDX ne porte que sur Mo, C, O, Ga, F) ni discuté. Les alcalins étant des promoteurs électroniques connus de la synthèse "
    "de NH3, une part de l'activité de Mo2CTx et de M/Mo2CTx pourrait venir du sodium ; à doser avant de comparer à β-Mo2C non lavé.")
lim("Ni/Mo2CTx", "Pour Ni et Co, les nitrates (rapport NO3−/Mo ≈ 1 pour 20 wt % Ni, ≈ 0,44 pour 10 wt % Co, par calcul) se décomposent vers "
    "200–300 °C, avant ou pendant la réduction par H2, et peuvent oxyder la surface du MXene en MoOx ; XPS et XAS ne portent que sur "
    "Re/Mo2CTx, et aucune caractérisation (XRD, MET, réductibilité, taille de particules) n'est donnée pour Ni et Co. L'état du support de "
    "Ni/Mo2CTx et Co/Mo2CTx n'est donc pas démontré identique à celui de Re/Mo2CTx.")
lim("Re/Mo2CTx", "Le « maximum » de 33,0 mmol g–1 h–1 à 475 °C et 1 MPa correspond à 1,36 % de NH3 en sortie pour un équilibre d'environ 1,65 % "
    "(≈ 83 % de l'équilibre, d'après NIST-JANAF, table H-083) : à cette température la vitesse est limitée par la thermodynamique, et la baisse "
    "au-delà n'est pas une propriété du catalyseur. À 400 °C (≈ 23 % de l'équilibre) le régime est cinétique, et la comparaison des catalyseurs y est valable.")
lim("Re/Mo2CTx", "Le test de couleur WO3 n'a qu'un témoin (WO3 seul) ; il manque WO3 + Mo2CTx sans métal. Il prouve un transfert d'hydrogène du "
    "métal vers WO3 au contact, pas un débordement de Re vers Mo2CTx. De même, la désorption de H2 de Re/Mo2CTx supérieure à Mo2CTx + Re massif "
    "s'explique déjà par la surface de Re de particules de 2,3 nm : ces preuves ne distinguent pas spillover et simple addition de sites (Prins, "
    "Chem. Rev. 112, 2714–2738, 2012).")
lim("Mo2CTx", "Les terminaisons sont décrites tantôt comme OH (résumé « Tx denotes the OH group », EXAFS, modèle DFT Mo2COH à 1/2 ML d'OH), "
    "tantôt comme O (Raman, Mo2CO2) ; les bandes Raman à ≈ 489 et 680 cm–1 peuvent aussi venir d'un MoOx de surface. La coordinence Mo–C(O) de 6,6 "
    "dépasse le maximum de 6 d'un M2XT2 idéal (incertitude EXAFS ±20 % au tableau S5) et l'état réduit ou non de l'échantillon mesuré n'est pas précisé. "
    "F < 0,01 wt % par EDX est sous la limite de détection usuelle de la technique (≈ 0,1 wt %) et doit se lire « non détecté ».")
lim(None, "Les ordres de réaction en H2 de NPMs/Mo2CTx sont donnés dans le texte comme « in the range of 0.6–2.1 », alors que le tableau 1 "
    "donne 0,63 à 0,91 pour Re, Ni et Co (2,07 est la valeur de β-Mo2C) ; les valeurs du tableau sont retenues. L'énergie d'activation de "
    "Re/Mo2CTx est de 57 kJ mol–1 dans le texte et de 56,5 au tableau S1 : simple arrondi.")
lim("Mo2CTx", "La gravure dans HF 40 % à 65 °C pendant 72 h (60 mL, ≈ 1,36 mol de HF pour ≈ 11,7 mmol de Ga, soit ≈ 39 fois le besoin) dégage "
    "environ 17,5 mmol de H2 (≈ 0,43 L à 25 °C) : un flacon fermé se met en pression, et un récipient ouvert perd du HF en 72 h ; le matériau et la "
    "fermeture du récipient ne sont pas dits. Précautions non écrites : HF (hypocalcémie, brûlures profondes différées ; gel de gluconate de "
    "calcium), effluents fluorés à traiter (Alhabeb et al., Chem. Mater. 2017, 10.1021/acs.chemmater.7b02847).")

json.dump(d, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
