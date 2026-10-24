#!/usr/bin/env python3
"""Fiches par lieu et index des occurrences, dérivés du registre 04_Donnees/lieux.json.

Produit :
  03_Fiches/par_lieu/<secteur>/<code>_<nom>.md   une fiche par notice du registre
  03_Fiches/par_lieu/README.md                   index des fiches par secteur
  01_Corpus/index_occurrences.md                 concordance automatique lieu → paragraphes

Les occurrences sont cherchées dans le témoin EPUB (convention P, cf.
01_Corpus/NOTICE.md) à l'aide des motifs déclarés dans le registre (champ
`motifs` ; préfixe « CS: » = sensible à la casse). Les lieux désignés par
périphrase échappent en partie à ce relevé automatique : les relevés par
chapitre (01_Corpus/releves_par_chapitre/) et le champ `refs` le complètent.
Bibliothèque standard uniquement ; aucun accès réseau.
"""
import json
import re
import shutil
import unicodedata
from collections import OrderedDict

from corpus import ROOT, paragraphes

SECTEURS = OrderedDict([
    ("G", ("Guillotiere", "La Guillotière et le cours Gambetta")),
    ("B", ("Brotteaux_et_3e_nord", "Le 3e nord, la place Morand et les Brotteaux")),
    ("P", ("Presqu_ile", "La Presqu'île (Bellecour, Terreaux, Perrache)")),
    ("D", ("Rive_droite", "La rive droite de la Saône (Fourvière, Saint-Jean, Saint-Just)")),
    ("E", ("Environs", "Les environs de Lyon")),
    ("R", ("Region", "La région lyonnaise et au-delà")),
])
STATUTS = OrderedDict([("atteste", "identification retenue"), ("probable", "identification probable"),
                       ("hypothese", "hypothèse à vérifier"), ("non_localise", "non localisé")])
CERTITUDES = {"A": "certain", "B": "très probable", "C": "probable", "D": "hypothèse",
              "E": "fictif ou non localisable"}
NOMS = {"reel": "nom réel", "surnom": "surnom donné par les personnages", "deguise": "nom déguisé",
        "fictif": "lieu ou enseigne inventés", "implicite": "lieu non nommé"}
ORDRE_CH = None


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_")[:50]


def compiler(motif):
    return re.compile(motif[3:]) if motif.startswith("CS:") else re.compile(motif, re.I)


def grouper(refs):
    par = OrderedDict()
    for ch, n in refs:
        par.setdefault(ch, []).append(n)
    return " ; ".join(f"{ch} §{', '.join(map(str, ns))}" for ch, ns in par.items())


def ancre(g):
    if not g:
        return None
    if g["type"] == "Point":
        return g["coordinates"]
    pts = g["coordinates"] if g["type"] == "LineString" else g["coordinates"][0][:-1]
    if g["type"] == "LineString":
        return pts[len(pts) // 2]
    return [sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)]


def chemin_fiche(l):
    rep = SECTEURS[l["secteur"]][0]
    return f"03_Fiches/par_lieu/{rep}/{l['code']}_{slug(l['nom'])}.md"


def fiche(l, occ):
    lignes = [f"# {l['code']} — {l['nom']}", ""]
    meta = [f"*Secteur :* {SECTEURS[l['secteur']][1]}"]
    if l.get("categorie"):
        meta.append(f"*Catégorie :* {l['categorie']}")
    if l.get("statut_nom"):
        meta.append(f"*Nom :* {NOMS.get(l['statut_nom'], l['statut_nom'])}")
    lignes += [" · ".join(meta), ""]
    cert = f" · degré de certitude {l['certitude']} ({CERTITUDES[l['certitude']]})" if l.get("certitude") else ""
    lignes += [f"**Statut : {STATUTS[l['statut']]}**{cert} · notice `{l['id']}` du registre "
               f"[`04_Donnees/lieux.json`](../../../04_Donnees/lieux.json)", ""]
    lignes += ["## Identification", "", (l.get("identification") or l["description"]).strip(), ""]
    if l.get("identification") and l["description"].strip() != l["identification"].strip():
        lignes += [f"*Notice cartographique :* {l['description'].strip()}", ""]
    a = ancre(l.get("geometry"))
    tab = ["| | |", "|---|---|"]
    if l.get("nom_1925"):
        tab.append(f"| Désignation vers 1925 | {l['nom_1925']} |")
    if l.get("nom_actuel"):
        tab.append(f"| Désignation actuelle | {l['nom_actuel']} |")
    if a:
        lon, lat = a
        forme = {"Point": "point", "LineString": "segment de recherche", "Polygon": "zone"}[l["geometry"]["type"]]
        marge = f", marge ≈ {l['precision_m']} m" if l.get("precision_m") else ""
        tab.append(f"| Repère cartographique | {lat:.5f}, {lon:.5f} ({forme}{marge}) |")
        if (l.get("georeferencement") or {}).get("methode"):
            tab.append(f"| Géoréférencement | {l['georeferencement']['methode']} |")
        osm = f"https://www.openstreetmap.org/?mlat={lat:.5f}&mlon={lon:.5f}#map=18/{lat:.5f}/{lon:.5f}"
        geop = (f"https://www.geoportail.gouv.fr/carte?c={lon:.5f},{lat:.5f}&z=18"
                "&l0=ORTHOIMAGERY.ORTHOPHOTOS.1950-1965::GEOPORTAIL:OGC:WMTS(1)&permalink=yes")
        tab.append(f"| Voir | [plan actuel]({osm}) · [photographies aériennes 1950-1965]({geop}) |")
    else:
        tab.append("| Repère cartographique | aucun : pas de localisation défendable (non placé sur les cartes) |")
    lignes += tab + [""]
    if l.get("cle"):
        lignes += ["## Citation-clé", "", "> " + l["cle"], ""]
    if l.get("arguments"):
        lignes += ["## Arguments", "", l["arguments"].strip(), ""]
    if l.get("fiche") and "par_lieu" not in l["fiche"]:
        cible = l["fiche"].replace("../03_Fiches/", "../../")
        lignes += [f"Dossier d'argumentation : [{cible.split('/')[-1].split('#')[0]}]({cible})", ""]
    if l.get("temoignages"):
        lignes += ["## Sources extérieures (témoignages, biographies)", ""]
        lignes += [f"- {t}" for t in l["temoignages"]] + [""]
    lignes += ["## Passages du roman", ""]
    if l.get("refs"):
        lignes += ["Passages retenus : " + " ; ".join(r.split("#p")[0] if "#p" not in r else r for r in l["refs"]) + ".", ""]
    if l.get("motifs"):
        lignes += [f"Occurrences relevées automatiquement ({len(occ)} paragraphe(s)) : "
                   f"{grouper(occ) or 'aucune occurrence littérale (lieu désigné par périphrase)'}.", "",
                   "Motifs recherchés : " + ", ".join(f"`{m}`" for m in l["motifs"]) + ".", ""]
    if l.get("sources"):
        lignes += ["## Sources", ""] + [f"- {s}" for s in l["sources"]] + [""]
    lignes += ["---", "[Index des fiches](../README.md) · [Synthèse lyonnaise](../../../README.md) · "
               "[Protocole](../../../00_Methode/PROTOCOLE.md)", ""]
    return "\n".join(lignes)


def main():
    lieux = json.loads((ROOT / "04_Donnees" / "lieux.json").read_text(encoding="utf-8"))
    ps = paragraphes()
    ordre = list(OrderedDict.fromkeys(ch for ch, *_ in ps))
    occ = {}
    for l in lieux:
        motifs = [compiler(m) for m in l.get("motifs", [])]
        occ[l["id"]] = [(ch, n) for ch, n, _, t in ps if motifs and any(m.search(t) for m in motifs)]
    base = ROOT / "03_Fiches" / "par_lieu"
    if base.exists():
        shutil.rmtree(base)
    for l in lieux:
        chemin = ROOT / chemin_fiche(l)
        chemin.parent.mkdir(parents=True, exist_ok=True)
        chemin.write_text(fiche(l, occ[l["id"]]), encoding="utf-8")
    # Index des fiches
    t = ["# Fiches par lieu", "",
         "Une fiche par notice du registre [`04_Donnees/lieux.json`](../../04_Donnees/lieux.json), générée par "
         "`06_Outils/fiches_lieux.py` (ne pas modifier à la main : corriger le registre puis régénérer). "
         "Les dossiers d'argumentation thématiques sont dans [`03_Fiches/`](../). Statuts et degrés de "
         "certitude : [PROTOCOLE](../../00_Methode/PROTOCOLE.md).", ""]
    for code, (rep, titre) in SECTEURS.items():
        ls = [l for l in lieux if l["secteur"] == code]
        if not ls:
            continue
        t += [f"## {titre}", "", "| Code | Lieu | Désignation actuelle | Statut | Occ. |", "|---|---|---|---|---:|"]
        for l in sorted(ls, key=lambda l: l["code"]):
            occs = len(occ[l["id"]]) if l.get("motifs") else "—"
            t.append(f"| {l['code']} | [{l['nom']}]({chemin_fiche(l).split('par_lieu/')[1]}) | "
                     f"{l.get('nom_actuel') or ''} | {STATUTS[l['statut']]} | {occs} |")
        t.append("")
    (base / "README.md").write_text("\n".join(t), encoding="utf-8")
    # Index des occurrences
    avec = [l for l in lieux if l.get("motifs")]
    t = ["# Index des occurrences des lieux lyonnais", "",
         "Concordance automatique (`06_Outils/fiches_lieux.py`) : pour chaque notice du registre qui déclare "
         "des motifs de recherche, les paragraphes du roman où l'une de ses désignations apparaît "
         "(convention P, voir [NOTICE](NOTICE.md)). Les lieux désignés par périphrase (« chez elle », « la "
         "petite rue ») échappent en partie à ce relevé : voir les [relevés par chapitre]"
         "(releves_par_chapitre/) et l'[inventaire lexical](INVENTAIRE.md).", "",
         "| Lieu | Occ. | Paragraphes |", "|---|---:|---|"]
    for l in sorted(avec, key=lambda l: l["code"]):
        t.append(f"| [{l['code']}](../{chemin_fiche(l)}) {l['nom']} | {len(occ[l['id']])} | "
                 f"{grouper(occ[l['id']]) or '—'} |")
    top = sorted(avec, key=lambda l: -len(occ[l["id"]]))[:20]
    t += ["", "## Répartition par chapitre des vingt lieux les plus cités", "",
          "| Chapitre | " + " | ".join(l["code"] for l in top) + " |", "|---|" + "---:|" * len(top)]
    for ch in ordre:
        cells = [str(sum(1 for c, _ in occ[l["id"]] if c == ch) or "") for l in top]
        if any(cells):
            t.append(f"| {ch} | " + " | ".join(cells) + " |")
    t += ["", "Colonnes : " + " ; ".join(f"{l['code']} = {l['nom']}" for l in top) + ".", ""]
    (ROOT / "01_Corpus" / "index_occurrences.md").write_text("\n".join(t), encoding="utf-8")
    print(f"{len(lieux)} fiches ; {len(avec)} lieux avec motifs ; "
          f"{sum(len(occ[l['id']]) for l in avec)} occurrences")


if __name__ == "__main__":
    main()
