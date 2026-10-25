#!/usr/bin/env python3
"""Lieux par secteur et export GeoJSON, dérivés du registre donnees/lieux.json.

Produit :
  lieux/<secteur>.md      une section par lieu (identification, arguments, témoignages, passages, sources)
  donnees/lieux.geojson   export WGS84 du registre (géométrie null pour les lieux non localisés)

Les occurrences sont cherchées dans le témoin EPUB à l'aide des motifs du registre
(champ `motifs` ; préfixe « CS: » = sensible à la casse). Ne pas retoucher les
fichiers produits : corriger le registre, puis relancer ce script.
Bibliothèque standard uniquement ; aucun accès réseau.
"""
import json
import re
from collections import OrderedDict

from corpus import ROOT, paragraphes

SECTEURS = OrderedDict([
    ("G", ("G_Guillotiere.md", "La Guillotière et le cours Gambetta")),
    ("B", ("B_Brotteaux.md", "Le 3e nord, la place Morand et les Brotteaux")),
    ("P", ("P_Presquile.md", "La Presqu'île : Bellecour, Terreaux, Perrache")),
    ("D", ("D_Rive_droite.md", "La rive droite de la Saône : Fourvière, Saint-Jean, Saint-Just")),
    ("E", ("E_Environs.md", "Les environs de Lyon")),
    ("R", ("R_Region.md", "La région lyonnaise et au-delà")),
])
STATUTS = OrderedDict([("atteste", "identifié"), ("probable", "probable"),
                       ("hypothese", "hypothèse"), ("non_localise", "non localisé")])
CERTITUDES = {"A": "certain", "B": "très probable", "C": "probable", "D": "hypothèse",
              "E": "fictif ou non localisable"}
NOMS = {"reel": "nom réel", "surnom": "surnom donné par les personnages", "deguise": "nom déguisé",
        "fictif": "lieu ou enseigne inventés", "implicite": "lieu non nommé"}
FORMES = {"Point": "point", "LineString": "segment", "Polygon": "zone"}


def chemin_fiche(l):
    """Chemin de la section d'un lieu, relatif à la racine du dossier."""
    return f"lieux/{SECTEURS[l['secteur']][0]}#{l['code'].lower()}"


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
    if g["type"] == "LineString":
        pts = g["coordinates"]
        return pts[len(pts) // 2]
    pts = g["coordinates"][0][:-1]
    return [sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)]


def section(l, occ):
    s = [f'<a id="{l["code"].lower()}"></a>', "", f"### {l['code']} · {l['nom']}", ""]
    tete = [f"**{STATUTS[l['statut']].capitalize()}**"]
    if l.get("certitude"):
        tete.append(f"certitude {l['certitude']} ({CERTITUDES[l['certitude']]})")
    if l.get("categorie"):
        tete.append(l["categorie"])
    if l.get("statut_nom"):
        tete.append(NOMS.get(l["statut_nom"], l["statut_nom"]))
    s.append(" · ".join(tete) + "  ")
    if l.get("nom_1925") or l.get("nom_actuel"):
        s.append(f"Vers 1925 : {l.get('nom_1925') or '—'} — aujourd'hui : {l.get('nom_actuel') or '—'}  ")
    a = ancre(l.get("geometry"))
    if a:
        lon, lat = a
        marge = f", ± {l['precision_m']} m" if l.get("precision_m") else ""
        osm = f"https://www.openstreetmap.org/?mlat={lat:.5f}&mlon={lon:.5f}#map=18/{lat:.5f}/{lon:.5f}"
        geop = (f"https://www.geoportail.gouv.fr/carte?c={lon:.5f},{lat:.5f}&z=18"
                "&l0=ORTHOIMAGERY.ORTHOPHOTOS.1950-1965::GEOPORTAIL:OGC:WMTS(1)&permalink=yes")
        s.append(f"Repère : {lat:.5f}, {lon:.5f} ({FORMES[l['geometry']['type']]}{marge}) · "
                 f"[plan actuel]({osm}) · [photographies 1950-1965]({geop})")
        if (l.get("georeferencement") or {}).get("methode"):
            s[-1] += "  "
            s.append(f"Géoréférencement : {l['georeferencement']['methode']}")
    else:
        s.append("Repère : aucun (pas de localisation défendable ; absent des cartes)")
    s += ["", l["description"].strip(), ""]
    ident = (l.get("identification") or "").strip()
    if ident and ident != l["description"].strip():
        s += [f"**Identification.** {ident}", ""]
    if l.get("cle"):
        s += ["> " + l["cle"], ""]
    if l.get("arguments"):
        s += [f"**Arguments.** {l['arguments'].strip()}", ""]
    if l.get("temoignages"):
        s += ["**Témoignages et archives**", ""] + [f"- {t}" for t in l["temoignages"]] + [""]
    passages = "**Passages du roman :** " + " ; ".join(l.get("refs", [])) + "."
    if l.get("motifs"):
        passages += (f" Occurrences du nom ({len(occ)} paragraphe{'s' if len(occ) > 1 else ''}) : "
                     f"{grouper(occ) or 'aucune (lieu désigné par périphrase)'}.")
    s += [passages, ""]
    if l.get("sources"):
        s += ["**Sources**", ""] + [f"- {x}" for x in l["sources"]] + [""]
    if l.get("fiche"):
        cible = l["fiche"]
        s += [f"Dossier : [{cible.split('/')[-1].split('#')[0].removesuffix('.md')}](../{cible})", ""]
    return s


def main():
    lieux = json.loads((ROOT / "donnees" / "lieux.json").read_text(encoding="utf-8"))
    ps = paragraphes()
    occ = {}
    for l in lieux:
        motifs = [compiler(m) for m in l.get("motifs", [])]
        occ[l["id"]] = [(ch, n) for ch, n, _, t in ps if motifs and any(m.search(t) for m in motifs)]
    rep = ROOT / "lieux"
    rep.mkdir(exist_ok=True)
    for f in rep.glob("*.md"):
        f.unlink()
    for code, (fichier, titre) in SECTEURS.items():
        ls = sorted((l for l in lieux if l["secteur"] == code), key=lambda l: l["code"])
        t = [f"# {titre}", "",
             f"{len(ls)} lieux du secteur {code}, tirés du registre [`donnees/lieux.json`](../donnees/lieux.json) "
             "(fichier produit par `outils/fiches.py` : corriger le registre, puis relancer le script). "
             "Statuts et degrés de certitude : [METHODE](../METHODE.md).", "",
             "| Code | Lieu | Aujourd'hui | Statut |", "|---|---|---|---|"]
        for l in ls:
            t.append(f"| [{l['code']}](#{l['code'].lower()}) | {l['nom']} | {l.get('nom_actuel') or ''} | "
                     f"{STATUTS[l['statut']]} |")
        t.append("")
        for l in ls:
            t += section(l, occ[l["id"]])
        (rep / fichier).write_text("\n".join(t).rstrip() + "\n", encoding="utf-8")
    features = [{"type": "Feature", "id": x["id"], "geometry": x["geometry"],
                 "properties": {k: v for k, v in x.items() if k != "geometry"}} for x in lieux]
    (ROOT / "donnees" / "lieux.geojson").write_text(json.dumps(
        {"type": "FeatureCollection", "name": "Lieux lyonnais des Deux Étendards", "features": features},
        ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    avec = [l for l in lieux if l.get("motifs")]
    print(f"{len(lieux)} lieux en {len(SECTEURS)} fichiers ; {sum(len(occ[l['id']]) for l in avec)} occurrences ; "
          "lieux.geojson écrit")


if __name__ == "__main__":
    main()
