#!/usr/bin/env python3
"""Construit les données dérivées du répertoire des lieux (05_Donnees/lieux.yaml).

Produit :
  05_Donnees/lieux.geojson, 05_Donnees/lieux.csv
  01_Releve_textuel/index_occurrences.md   (concordance chapitre / paragraphe)
  03_Fiches_lieux/<secteur>/<id>_<nom>.md  (une fiche par lieu)
  03_Fiches_lieux/README.md                (index des fiches)

Prérequis : avoir lancé 01_extraire_texte.py (texte numéroté dans scripts/_texte).
"""
import csv
import json
import os
import re
import unicodedata
from collections import OrderedDict

import yaml

from geolib import resoudre

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
TEXTE = os.path.join(ICI, "_texte")

SECTEURS = OrderedDict([
    ("G", ("Guillotiere", "La Guillotière et le cours Gambetta")),
    ("B", ("Brotteaux_et_3e_nord", "Le 3e nord, la place Morand et les Brotteaux")),
    ("P", ("Presqu_ile", "La Presqu'île (Bellecour, Perrache, Terreaux)")),
    ("D", ("Rive_droite", "La rive droite de la Saône (Fourvière, Saint-Jean)")),
    ("E", ("Environs", "Les environs de Lyon")),
    ("R", ("Region", "La région lyonnaise et au-delà")),
])
CERTITUDES = OrderedDict([
    ("A", "certain"), ("B", "très probable"), ("C", "probable"),
    ("D", "hypothèse"), ("E", "fictif ou non localisable"),
])
STATUTS = {"reel": "nom réel", "surnom": "surnom des personnages", "deguise": "nom déguisé",
           "fictif": "lieu ou enseigne fictifs", "implicite": "lieu non nommé"}


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_")[:50]


def etiquette_chapitre(nom_fichier):
    base = nom_fichier[3:-4]
    if base.startswith("intermedes"):
        return "Intermèdes"
    if base.startswith("recit_de_guitte"):
        return "Récit de Guitte"
    if base.startswith("notes"):
        return "Notes"
    m = re.match(r"([IVXL]+)(_|$)", base)
    return m.group(1) if m else None


def charger_texte():
    """Liste ordonnée de (chapitre, numéro de paragraphe, texte)."""
    paras = []
    for fn in sorted(os.listdir(TEXTE)):
        ch = etiquette_chapitre(fn)
        if not ch:
            continue
        n, buf = 0, []
        with open(os.path.join(TEXTE, fn), encoding="utf-8") as f:
            for ligne in f:
                m = re.match(r"\[§(\d+)\] (.*)", ligne)
                if m:
                    if buf:
                        paras.append((ch, n, " ".join(buf)))
                    n, buf = int(m.group(1)), [m.group(2)]
                else:
                    buf.append(ligne.strip())
        if buf:
            paras.append((ch, n, " ".join(buf)))
    return paras


def compiler(motif):
    if motif.startswith("CS:"):
        return re.compile(motif[3:])
    return re.compile(motif, re.IGNORECASE)


def concordance(lieux, paras):
    occ = {}
    for l in lieux:
        motifs = [compiler(m) for m in l.get("motifs", [])]
        refs = []
        for ch, n, t in paras:
            if any(m.search(t) for m in motifs):
                refs.append((ch, n))
        occ[l["id"]] = refs
    return occ


def grouper_refs(refs):
    """[(ch, n)] -> 'I § 3, 7 ; IV § 29'"""
    par_ch = OrderedDict()
    for ch, n in refs:
        par_ch.setdefault(ch, []).append(n)
    return " ; ".join(f"{ch} § {', '.join(map(str, ns))}" for ch, ns in par_ch.items())


def main():
    with open(os.path.join(RACINE, "05_Donnees", "lieux.yaml"), encoding="utf-8") as f:
        lieux = yaml.safe_load(f)["lieux"]
    paras = charger_texte()
    occ = concordance(lieux, paras)
    ordre_ch = list(OrderedDict.fromkeys(ch for ch, _, _ in paras))

    # Géolocalisation
    for l in lieux:
        lat, lon, methode = resoudre(l["geo"])
        l["lat"], l["lon"], l["methode_geo"] = round(lat, 6), round(lon, 6), methode
        l["rayon"] = l["geo"].get("rayon", 0)
        rep, _ = SECTEURS[l["secteur"]]
        l["fiche"] = f"03_Fiches_lieux/{rep}/{l['id']}_{slug(l['nom'])}.md"
        l["occurrences"] = len(occ[l["id"]])
        l["chapitres"] = list(OrderedDict.fromkeys(ch for ch, _ in occ[l["id"]]))

    # GeoJSON
    champs = ["id", "nom", "secteur", "categorie", "statut_nom", "certitude", "identification",
              "nom_1925", "nom_actuel", "rayon", "methode_geo", "occurrences", "chapitres",
              "cle", "fiche", "enquete"]
    features = [{"type": "Feature",
                 "geometry": {"type": "Point", "coordinates": [l["lon"], l["lat"]]},
                 "properties": {k: l.get(k) for k in champs}} for l in lieux]
    with open(os.path.join(RACINE, "05_Donnees", "lieux.geojson"), "w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection", "features": features}, f, ensure_ascii=False, indent=1)

    # CSV
    with open(os.path.join(RACINE, "05_Donnees", "lieux.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "nom", "secteur", "categorie", "statut_nom", "certitude", "lat", "lon",
                    "rayon_m", "nom_1925", "nom_actuel", "occurrences", "chapitres", "methode_geo",
                    "identification"])
        for l in lieux:
            w.writerow([l["id"], l["nom"], l["secteur"], l["categorie"], l["statut_nom"],
                        l["certitude"], l["lat"], l["lon"], l["rayon"], l.get("nom_1925", ""),
                        l.get("nom_actuel", ""), l["occurrences"], " ".join(l["chapitres"]),
                        l["methode_geo"], l["identification"]])

    # Concordance
    lignes = ["# Index des occurrences des lieux lyonnais",
              "",
              "Concordance automatique (scripts/02_construire_donnees.py) : pour chaque lieu du",
              "répertoire, les paragraphes du roman où l'une de ses désignations apparaît, d'après",
              "les motifs déclarés dans `05_Donnees/lieux.yaml`. Référence : chapitre, § (numérotation",
              "des paragraphes de l'EPUB Gallimard, voir 00_Methode). Les lieux désignés seulement par",
              "périphrase (« chez elle », « la petite rue ») échappent en partie à ce relevé",
              "automatique : les relevés par chapitre (`releves_par_chapitre/`) les complètent.",
              "", "| Lieu | Occ. | Paragraphes |", "|---|---:|---|"]
    for l in lieux:
        lignes.append(f"| [{l['id']}](../{l['fiche']}) {l['nom']} | {l['occurrences']} | "
                      f"{grouper_refs(occ[l['id']]) or '—'} |")
    lignes += ["", "## Répartition par chapitre (lieux les plus cités)", ""]
    top = sorted(lieux, key=lambda l: -l["occurrences"])[:25]
    lignes.append("| Chapitre | " + " | ".join(l["id"] for l in top) + " |")
    lignes.append("|---|" + "---:|" * len(top))
    for ch in ordre_ch:
        cells = [str(sum(1 for c, _ in occ[l["id"]] if c == ch) or "") for l in top]
        lignes.append(f"| {ch} | " + " | ".join(cells) + " |")
    lignes += ["", "Légende des colonnes : " + " ; ".join(f"{l['id']} = {l['nom']}" for l in top), ""]
    with open(os.path.join(RACINE, "01_Releve_textuel", "index_occurrences.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lignes))

    # Fiches
    for l in lieux:
        chemin = os.path.join(RACINE, l["fiche"])
        os.makedirs(os.path.dirname(chemin), exist_ok=True)
        osm = f"https://www.openstreetmap.org/?mlat={l['lat']}&mlon={l['lon']}#map=18/{l['lat']}/{l['lon']}"
        geop = f"https://www.geoportail.gouv.fr/carte?c={l['lon']},{l['lat']}&z=18&l0=ORTHOIMAGERY.ORTHOPHOTOS.1950-1965::GEOPORTAIL:OGC:WMTS(1)&permalink=yes"
        t = [f"# {l['id']} — {l['nom']}", "",
             f"*Secteur :* {SECTEURS[l['secteur']][1]} · *Catégorie :* {l['categorie']} · "
             f"*Statut du nom :* {STATUTS[l['statut_nom']]}",
             "",
             f"**Degré de certitude : {l['certitude']} ({CERTITUDES[l['certitude']]})**", "",
             "## Identification", "", l["identification"].strip(), "",
             "| | |", "|---|---|",
             f"| Nom en 1925 | {l.get('nom_1925', '—')} |",
             f"| Nom actuel | {l.get('nom_actuel', '—')} |",
             f"| Coordonnées | {l['lat']}, {l['lon']}" + (f" (zone de ~{l['rayon']} m)" if l["rayon"] else "") + " |",
             f"| Méthode de localisation | {l['methode_geo']} |",
             f"| Voir | [OpenStreetMap]({osm}) · [Géoportail, photos 1950-1965]({geop}) |", ""]
        if l.get("cle"):
            t += ["## Citation-clé", "", "> " + l["cle"], ""]
        if l.get("arguments"):
            t += ["## Arguments", "", l["arguments"].strip(), ""]
        if l.get("enquete"):
            t += [f"Dossier d'enquête détaillé : [{l['enquete']}](../../{l['enquete']})", ""]
        t += ["## Occurrences relevées automatiquement", "",
              f"{l['occurrences']} paragraphe(s) : {grouper_refs(occ[l['id']]) or 'aucune occurrence littérale (lieu désigné par périphrase)'}.",
              "", "Motifs recherchés : " + ", ".join(f"`{m}`" for m in l.get("motifs", [])), ""]
        if l.get("sources"):
            t += ["## Sources", ""] + [f"- {s}" for s in l["sources"]] + [""]
        t += ["---", "[Retour à l'index des fiches](../README.md) · "
              "[Synthèse lyonnaise](../../README.md)", ""]
        with open(chemin, "w", encoding="utf-8") as f:
            f.write("\n".join(t))

    # Index des fiches
    t = ["# Fiches des lieux", "",
         "Une fiche par lieu, générée à partir de `05_Donnees/lieux.yaml`. Les degrés de "
         "certitude sont définis dans [00_Methode](../00_Methode/methode.md).", ""]
    for code, (rep, titre) in SECTEURS.items():
        t += [f"## {titre}", "", "| Id | Lieu | Identification (résumé) | Certitude | Occ. |",
              "|---|---|---|:---:|---:|"]
        for l in lieux:
            if l["secteur"] != code:
                continue
            resume = l.get("nom_actuel") or ""
            t.append(f"| {l['id']} | [{l['nom']}]({rep}/{os.path.basename(l['fiche'])}) | {resume} | "
                     f"{l['certitude']} | {l['occurrences']} |")
        t.append("")
    with open(os.path.join(RACINE, "03_Fiches_lieux", "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(t))

    print(f"{len(lieux)} lieux ; {sum(l['occurrences'] for l in lieux)} occurrences.")
    for l in lieux:
        print(f"{l['id']:4} {l['certitude']} {l['occurrences']:4}  {l['lat']:.5f} {l['lon']:.5f}  {l['nom'][:45]:45} {l['methode_geo']}")


if __name__ == "__main__":
    main()
