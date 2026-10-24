#!/usr/bin/env python3
"""Cartes sur fonds historiques de l'IGN (carte de 1950, photographies aériennes 1950-1965).

Complète generer_cartes.py (cartes vectorielles autonomes sur fond OSM moderne) :
mêmes données (04_Donnees/lieux.json, itineraires.geojson), même palette, même
numérotation des notices. Les tuiles IGN (Géoplateforme, Licence ouverte Etalab
2.0) sont téléchargées une fois puis conservées dans 06_Outils/_cache/ (ignoré
par git). Le fond de 1950 est postérieur au roman d'une génération : il est plus
proche de la ville de 1925 qu'un fond actuel, sans la restituer (ponts
reconstruits après 1944, percées, etc.).

Sorties (05_Cartes/) :
  lyon_carte_ign_1950.png        centre de Lyon sur la carte IGN de 1950
  guillotiere_photo_1950.png     de la place Morand à Saint-Louis, photo aérienne 1950-1965
  itineraires.png                vue d'ensemble des cinq itinéraires reconstitués
  itineraires/itineraire_N.png   une planche par itinéraire (photographies 1950-1965)
  environs_ign_1950.png          Lyon et ses environs
  region_ign_1950.png            Beaujolais, Dombes, Dauphiné : les lieux régionaux

Dépendances : matplotlib, pillow, pyyaml (aucune autre). Usage :
  python3 06_Outils/cartes_historiques.py [--hors-ligne]
"""
import io
import json
import math
import os
import ssl
import sys
import time
import urllib.request
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Polygon as MplPolygon, Rectangle
from matplotlib import patheffects as pe
from PIL import Image, ImageEnhance, ImageOps

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fiches_lieux import chemin_fiche  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DONNEES, CARTES = ROOT / "04_Donnees", ROOT / "05_Cartes"
CACHE = Path(__file__).resolve().parent / "_cache" / "tuiles"
HORS_LIGNE = "--hors-ligne" in sys.argv

# Palette commune avec generer_cartes.py
COL = {"atteste": "#235460", "probable": "#b07125", "hypothese": "#b45942", "non_localise": "#7a7772"}
PAPER, INK, MUTED = "#f7f2e8", "#243a3f", "#687778"
LIB = {"atteste": "Localisation identifiée", "probable": "Localisation probable",
       "hypothese": "Hypothèse à vérifier"}
ITI_COL = ["#7b3f8c", "#1f7a63", "#c0392b", "#2e5fa8", "#a0522d"]
plt.rcParams.update({"font.family": "Liberation Sans", "font.size": 10})
SERIF = "Liberation Serif"

COUCHES = {
    "carte1950": ("GEOGRAPHICALGRIDSYSTEMS.MAPS.SCAN50.1950", "PM_3_15", "image/jpeg"),
    "photo1950": ("ORTHOIMAGERY.ORTHOPHOTOS.1950-1965", "PM_0_18", "image/png"),
}
CREDIT = {
    "carte1950": "Fond : IGN, Carte 1950 (SCAN 50, type 1950), Géoplateforme, Licence ouverte Etalab 2.0",
    "photo1950": "Fond : IGN, photographies aériennes historiques 1950-1965, Géoplateforme, Licence ouverte Etalab 2.0",
}

# ------------------------------------------------------------ projection et tuiles
R_TERRE = 6378137.0


def merc(lon, lat):
    return (math.radians(lon) * R_TERRE,
            math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)) * R_TERRE)


def tuile(couche, z, x, y):
    chemin = CACHE / couche / str(z) / f"{x}_{y}"
    if not chemin.exists():
        if HORS_LIGNE:
            return Image.new("RGB", (256, 256), (236, 233, 222))
        nom, tms, fmt = COUCHES[couche]
        url = ("https://data.geopf.fr/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0"
               f"&LAYER={nom}&STYLE=normal&TILEMATRIXSET={tms}&TILEMATRIX={z}"
               f"&TILEROW={y}&TILECOL={x}&FORMAT={fmt}")
        ca = "/root/.ccr/ca-bundle.crt"
        ctx = ssl.create_default_context(cafile=ca) if os.path.exists(ca) else None
        req = urllib.request.Request(url, headers={"User-Agent": "Rebatet-IdentificationsLieux/1.0"})
        for essai in range(4):
            try:
                with urllib.request.urlopen(req, context=ctx, timeout=60) as r:
                    data = r.read()
                break
            except Exception:
                time.sleep(2 * (essai + 1))
        else:
            return Image.new("RGB", (256, 256), (236, 233, 222))
        chemin.parent.mkdir(parents=True, exist_ok=True)
        chemin.write_bytes(data)
    return Image.open(chemin).convert("RGB")


def mosaique(couche, lon0, lat0, lon1, lat1, z):
    n = 2 ** z

    def num(lon, lat):
        return ((lon + 180) / 360 * n,
                (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n)
    xa, ya = num(lon0, lat1)
    xb, yb = num(lon1, lat0)
    tx0, ty0, tx1, ty1 = int(xa), int(ya), int(xb), int(yb)
    im = Image.new("RGB", ((tx1 - tx0 + 1) * 256, (ty1 - ty0 + 1) * 256))
    for tx in range(tx0, tx1 + 1):
        for ty in range(ty0, ty1 + 1):
            im.paste(tuile(couche, z, tx, ty), ((tx - tx0) * 256, (ty - ty0) * 256))
    res = 2 * math.pi * R_TERRE / n
    return im, (tx0 * res - math.pi * R_TERRE, (tx1 + 1) * res - math.pi * R_TERRE,
                math.pi * R_TERRE - (ty1 + 1) * res, math.pi * R_TERRE - ty0 * res)


def adoucir(im, couche):
    """Atténue le fond pour que les repères restent lisibles."""
    if couche == "photo1950":
        g = ImageOps.grayscale(im)
        g = ImageEnhance.Contrast(g).enhance(0.9)
        im = ImageOps.colorize(g, black="#2b2620", white="#f4ead6")
        return Image.blend(im, Image.new("RGB", im.size, (247, 242, 232)), 0.18)
    im = ImageEnhance.Color(im).enhance(0.75)
    return Image.blend(im, Image.new("RGB", im.size, (247, 242, 232)), 0.38)


# ------------------------------------------------------------------- données
def charger_lieux():
    lieux = json.loads((DONNEES / "lieux.json").read_text(encoding="utf-8"))
    for i, l in enumerate(lieux, 1):
        l["num"] = i
    return lieux


def ancre(l):
    g = l.get("geometry")
    if not g:
        return None
    if g["type"] == "Point":
        return g["coordinates"]
    pts = g["coordinates"] if g["type"] == "LineString" else g["coordinates"][0]
    return pts[len(pts) // 2] if g["type"] == "LineString" else [
        sum(p[0] for p in pts[:-1]) / (len(pts) - 1), sum(p[1] for p in pts[:-1]) / (len(pts) - 1)]


def dans(l, lon0, lat0, lon1, lat1):
    a = ancre(l)
    return a is not None and lon0 <= a[0] <= lon1 and lat0 <= a[1] <= lat1


# ------------------------------------------------------------------ dessin
def cadre_figure(titre, sous_titre, largeur=16, hauteur=12.8):
    fig = plt.figure(figsize=(largeur, hauteur), dpi=100, facecolor=PAPER)
    fig.text(0.036, 0.955, "LES DEUX ÉTENDARDS · ATLAS CRITIQUE · FONDS HISTORIQUES",
             fontsize=11, color=MUTED, fontweight="bold")
    fig.text(0.034, 0.895, titre, fontsize=40, family=SERIF, color=INK)
    fig.text(0.036, 0.858, sous_titre, fontsize=14, color=MUTED)
    return fig


def fond(ax, couche, lon0, lat0, lon1, lat1, z):
    im, (X0, X1, Y0, Y1) = mosaique(couche, lon0, lat0, lon1, lat1, z)
    ax.imshow(adoucir(im, couche), extent=(X0, X1, Y0, Y1), interpolation="lanczos", zorder=0)
    x0, y0 = merc(lon0, lat0)
    x1, y1 = merc(lon1, lat1)
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_edgecolor("#cfc8b8")


def echelle(ax, lat, metres, etiquette):
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    k = 1 / math.cos(math.radians(lat))
    bx, by = x0 + 0.04 * (x1 - x0), y0 + 0.04 * (y1 - y0)
    ax.add_patch(Rectangle((bx - 0.01 * (x1 - x0), by - 0.015 * (y1 - y0)), metres * k + 0.03 * (x1 - x0),
                           0.06 * (y1 - y0), fc=PAPER, ec="none", alpha=0.85, zorder=8))
    ax.plot([bx, bx + metres * k], [by, by], color=INK, lw=2.2, zorder=9, solid_capstyle="butt")
    ax.text(bx, by + 0.012 * (y1 - y0), etiquette, fontsize=10, color=INK, zorder=9)
    nx, ny = x0 + 0.95 * (x1 - x0), y0 + 0.9 * (y1 - y0)
    ax.annotate("", xy=(nx, ny + 0.05 * (y1 - y0)), xytext=(nx, ny),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=2), zorder=9)
    ax.text(nx, ny + 0.06 * (y1 - y0), "N", ha="center", fontsize=12, color=INK, zorder=9,
            path_effects=[pe.withStroke(linewidth=3, foreground=PAPER)])


def marqueur(ax, l, taille=1.0, avec_zone=True):
    statut = l["statut"]
    c = COL[statut]
    g = l["geometry"]
    lat_ref = ancre(l)[1]
    k = 1 / math.cos(math.radians(lat_ref))
    if avec_zone and g["type"] == "Polygon":
        pts = [merc(*p) for p in g["coordinates"][0]]
        ax.add_patch(MplPolygon(pts, closed=True, fc=c, ec=c, alpha=0.22, lw=1.4, ls="--", zorder=3))
    elif avec_zone and g["type"] == "LineString":
        pts = [merc(*p) for p in g["coordinates"]]
        ax.plot([p[0] for p in pts], [p[1] for p in pts], color=c, lw=9 * taille, alpha=0.28,
                solid_capstyle="round", zorder=3)
        ax.plot([p[0] for p in pts], [p[1] for p in pts], color=c, lw=1.4, ls="--", zorder=3)
    elif avec_zone and l.get("precision_m"):
        x, y = merc(*g["coordinates"])
        ax.add_patch(Circle((x, y), l["precision_m"] * k, fc=c, ec=c, alpha=0.16, lw=1, ls="--", zorder=3))
    x, y = merc(*ancre(l))
    s = 230 * taille
    if statut == "probable":
        ax.scatter([x], [y], s=s * 1.1, marker="D", c=c, edgecolors="white", linewidths=1.5, zorder=6)
        couleur_txt = "white"
    elif statut == "hypothese":
        ax.scatter([x], [y], s=s, marker="o", c="white", edgecolors=c, linewidths=1.8, zorder=6)
        couleur_txt = c
    else:
        ax.scatter([x], [y], s=s, marker="o", c=c, edgecolors="white", linewidths=1.5, zorder=6)
        couleur_txt = "white"
    ax.text(x, y, str(l["num"]), ha="center", va="center", fontsize=8.5 * taille, fontweight="bold",
            color=couleur_txt, zorder=7)


def legende(fig, lieux, x=0.69, y=0.80, titre="LIEUX & DEGRÉS DE CERTITUDE", rues=()):
    """Légende : symboles de statut, puis liste numérotée (sur deux colonnes si elle est longue)."""
    fig.text(x, y, titre, fontsize=11, color=MUTED, fontweight="bold")
    yy = y - 0.035
    for statut, lib in LIB.items():
        ax = fig.add_axes([x, yy - 0.006, 0.012, 0.015])
        ax.axis("off")
        ax.scatter([0.5], [0.5], s=110, marker="D" if statut == "probable" else "o",
                   c="white" if statut == "hypothese" else COL[statut], edgecolors=COL[statut], linewidths=1.6)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        fig.text(x + 0.02, yy, lib, fontsize=11.5, color=INK, va="center")
        yy -= 0.026
    yy -= 0.01
    note = "Une zone ou un segment ne désignent pas une adresse."
    if rues:
        note += " Rues nommées : filets de couleur, sans numéro."
    fig.text(x, yy, note, fontsize=9.5, color=MUTED, wrap=True)
    yy -= 0.032
    deux = len(lieux) > 30
    pas = 0.0158 if deux else 0.0205
    largeur, corps = (0.148, 8.6) if deux else (0.30, 10)
    coupe = 31 if deux else 52
    y0, col = yy, 0
    for l in lieux:
        if yy < 0.075:
            if deux and col == 0:
                col, yy = 1, y0
            else:
                fig.text(x + col * largeur, yy, "… voir l'atlas et le registre.", fontsize=8.5, color=MUTED)
                break
        xx = x + col * largeur
        fig.text(xx + 0.011, yy, f"{l['num']}", fontsize=corps, color=COL[l["statut"]], fontweight="bold",
                 va="center", ha="right")
        nom = l.get("carte_nom") or l["nom"].split(" — ")[0]
        nom = nom if len(nom) <= coupe else nom[:coupe - 1] + "…"
        fig.text(xx + 0.015, yy, nom, fontsize=corps, color=INK, va="center")
        yy -= pas


def pied(fig, couche, note):
    fig.text(0.036, 0.035, CREDIT[couche] + ". " + note, fontsize=9.5, color=MUTED)
    fig.text(0.036, 0.016, "Repères de lecture, non cadastraux : voir les fiches, le registre (04_Donnees/lieux.json) "
             "et la méthode (00_Methode).", fontsize=9.5, color=MUTED)


def est_rue(l):
    return l.get("categorie") == "voie" and l["geometry"]["type"] == "LineString"


def rue(ax, l):
    pts = [merc(*p) for p in l["geometry"]["coordinates"]]
    c = COL[l["statut"]]
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color="white", lw=4.2, alpha=0.8, zorder=2,
            solid_capstyle="round")
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=c, lw=2.2, alpha=0.85, zorder=2,
            solid_capstyle="round")


def carte_lieux(nom, titre, sous_titre, couche, z, bbox, ech, note, taille=1.0, exclure=(), secteurs=None):
    lon0, lat0, lon1, lat1 = bbox
    lieux = [l for l in charger_lieux() if dans(l, *bbox) and l["id"] not in exclure
             and (secteurs is None or l.get("secteur") in secteurs)
             and l.get("categorie") != "quartier"]  # les quartiers restent dans l'atlas
    rues = [l for l in lieux if est_rue(l)]
    reperes = [l for l in lieux if not est_rue(l)]
    fig = cadre_figure(titre, sous_titre)
    ax = fig.add_axes([0.036, 0.075, 0.63, 0.76])
    fond(ax, couche, lon0, lat0, lon1, lat1, z)
    for l in rues:
        rue(ax, l)
    for l in sorted(reperes, key=lambda l: {"hypothese": 0, "probable": 1, "atteste": 2}[l["statut"]]):
        marqueur(ax, l, taille)
    echelle(ax, (lat0 + lat1) / 2, *ech)
    legende(fig, reperes, rues=rues)
    pied(fig, couche, note)
    fig.savefig(CARTES / nom, dpi=100, facecolor=PAPER)
    plt.close(fig)
    print(f"{nom} : {len(reperes)} repères numérotés, {len(rues)} rues")


def cadrage(points, ratio, marge=0.18, mini=700):
    """Emprise mercator (x0, y0, x1, y1) englobant les points, au rapport largeur/hauteur voulu."""
    xs, ys = zip(*[merc(*p) for p in points])
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    k = 1 / math.cos(math.radians(sum(p[1] for p in points) / len(points)))
    w = max(max(xs) - min(xs), mini * k) * (1 + 2 * marge)
    h = max(max(ys) - min(ys), mini * k) * (1 + 2 * marge)
    if w / h < ratio:
        w = h * ratio
    else:
        h = w / ratio
    return cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2


def inv_merc(x, y):
    return (math.degrees(x / R_TERRE), math.degrees(2 * math.atan(math.exp(y / R_TERRE)) - math.pi / 2))


def lignes_itineraire(it):
    g = it["geometry"]
    return [g["coordinates"]] if g["type"] == "LineString" else g["coordinates"]


def tracer(ax, it, c, fleches=True, lw=3.2):
    for ligne in lignes_itineraire(it):
        pts = [merc(*p) for p in ligne]
        ax.plot([p[0] for p in pts], [p[1] for p in pts], color="white", lw=lw + 2.6, alpha=0.9, zorder=3,
                solid_joinstyle="round", solid_capstyle="round")
        ax.plot([p[0] for p in pts], [p[1] for p in pts], color=c, lw=lw, zorder=4, solid_joinstyle="round",
                solid_capstyle="round")
        if fleches and len(pts) > 8:
            for f in (0.3, 0.7):
                i = int(len(pts) * f)
                a, b = pts[max(0, i - 2)], pts[min(len(pts) - 1, i + 2)]
                if a != b:
                    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=20, color=c, lw=0,
                                                 zorder=5))


def etapes_de(etapes, it):
    return [e for e in etapes if e["properties"]["itineraire"] == it["properties"]["id"]]


def carte_itineraire(it, etapes, k):
    """Une planche par itinéraire : carte cadrée sur le trajet, étapes numérotées et références."""
    import textwrap
    pr, c = it["properties"], ITI_COL[k]
    es = etapes_de(etapes, it)
    pts = [p for l in lignes_itineraire(it) for p in l] + [e["geometry"]["coordinates"] for e in es
                                                          if not e["properties"]["hors_carte"]]
    fig = plt.figure(figsize=(16, 10.5), dpi=100, facecolor=PAPER)
    fig.text(0.036, 0.952, f"LES DEUX ÉTENDARDS · ITINÉRAIRE {pr['id'][2:]} · {pr['date'].upper()}",
             fontsize=11, color=MUTED, fontweight="bold")
    fig.text(0.034, 0.895, textwrap.fill(pr["titre"], 62), fontsize=26, family=SERIF, color=INK, va="center")
    axw, axh = 0.58, 0.80
    ax = fig.add_axes([0.036, 0.07, axw, axh])
    x0, y0, x1, y1 = cadrage(pts, (axw * 16) / (axh * 10.5))
    (lon0, lat0), (lon1, lat1) = inv_merc(x0, y0), inv_merc(x1, y1)
    largeur_m = (x1 - x0) * math.cos(math.radians((lat0 + lat1) / 2))
    z = 17 if largeur_m < 1800 else 16
    fond(ax, "photo1950", lon0, lat0, lon1, lat1, z)
    tracer(ax, it, c)
    reperes = {}  # une seule pastille par emplacement (étapes revisitées : « 10·11 »)
    for e in es:
        p = e["properties"]
        if p["hors_carte"]:
            continue
        cle = tuple(round(v, 5) for v in e["geometry"]["coordinates"])
        reperes.setdefault(cle, []).append(p)
    for cle, ps in reperes.items():
        x, y = merc(*cle)
        txt = "·".join(str(p["ordre"]) for p in ps)
        ax.scatter([x], [y], s=330 if len(txt) < 3 else 520, c="white", edgecolors=c, linewidths=2.4, zorder=6,
                   linestyle="--" if any(p["a_confirmer"] for p in ps) else "-")
        ax.text(x, y, txt, ha="center", va="center", fontsize=10 if len(txt) < 3 else 8.5, fontweight="bold",
                color=c, zorder=7)
    pas = 100 if largeur_m < 1500 else 250 if largeur_m < 3500 else 500
    echelle(ax, (lat0 + lat1) / 2, pas, f"{pas} m")
    # colonne de droite
    x = 0.645
    y = 0.835
    fig.text(x, y, textwrap.fill(pr["resume"], 64), fontsize=10.5, color=INK, va="top", linespacing=1.35)
    y -= 0.022 * (len(textwrap.wrap(pr["resume"], 64)) + 1.4)
    fig.text(x, y, "ÉTAPES ATTESTÉES PAR LE TEXTE", fontsize=10, color=MUTED, fontweight="bold", va="top")
    y -= 0.034
    for e in es:
        p = e["properties"]
        nom = p["nom"] + (" — hors carte" if p["hors_carte"] else "") + (" — localisation à confirmer"
                                                                       if p["a_confirmer"] else "")
        lignes = textwrap.wrap(nom, 50)
        fig.text(x + 0.018, y, f"{p['ordre']}", fontsize=10.5, color=c, fontweight="bold", va="top", ha="right")
        fig.text(x + 0.026, y, "\n".join(lignes), fontsize=10.5, color=INK, va="top", linespacing=1.25)
        fig.text(0.975, y, p["ref"], fontsize=9.5, color=MUTED, va="top", ha="right")
        y -= 0.0215 * len(lignes) + 0.011
    y -= 0.015
    note = ("Tracé reconstitué : entre deux étapes, le trait suit le plus court chemin sur la voirie actuelle "
            "(fond OpenStreetMap). Le roman nomme les étapes, rarement les rues suivies."
            + (" Itinéraire type composé de plusieurs passages." if pr["nature"] == "composite" else ""))
    fig.text(x, max(y, 0.10), textwrap.fill(note, 70), fontsize=9.5, color=MUTED, va="top", style="italic")
    fig.text(0.036, 0.03, CREDIT["photo1950"] + " · Tracé : © les contributeurs OpenStreetMap (ODbL) · "
             "Données : 04_Donnees/itineraires.yaml", fontsize=9, color=MUTED)
    nom = f"itineraire_{pr['id'][2:]}.png"
    (CARTES / "itineraires").mkdir(exist_ok=True)
    fig.savefig(CARTES / "itineraires" / nom, dpi=100, facecolor=PAPER)
    plt.close(fig)
    print(f"itineraires/{nom} : {len(es)} étapes, zoom {z}, {round(largeur_m)} m de large")


def carte_itineraires():
    data = json.loads((DONNEES / "itineraires.geojson").read_text(encoding="utf-8"))
    its = [f for f in data["features"] if f["properties"]["type"] == "itineraire"]
    etapes = [f for f in data["features"] if f["properties"]["type"] == "etape"]
    for k, it in enumerate(its):
        carte_itineraire(it, etapes, k)
    # Vue d'ensemble : les cinq tracés sur la carte de 1950
    import textwrap
    fig = cadre_figure("Cinq itinéraires", "Étapes attestées par le texte · tracés reconstitués au plus court "
                       "sur la voirie actuelle · carte IGN de 1950", largeur=16, hauteur=12.8)
    axw, axh = 0.63, 0.76
    ax = fig.add_axes([0.036, 0.075, axw, axh])
    pts = [p for it in its for l in lignes_itineraire(it) for p in l]
    x0, y0, x1, y1 = cadrage(pts, (axw * 16) / (axh * 12.8), marge=0.06)
    (lon0, lat0), (lon1, lat1) = inv_merc(x0, y0), inv_merc(x1, y1)
    fond(ax, "carte1950", lon0, lat0, lon1, lat1, 15)
    voile = ax.get_images()[0]
    voile.set_data(Image.blend(adoucir(mosaique("carte1950", lon0, lat0, lon1, lat1, 15)[0], "carte1950"),
                               Image.new("RGB", voile.get_array().shape[1::-1], (247, 242, 232)), 0.35))
    for k, it in enumerate(its):
        tracer(ax, it, ITI_COL[k], fleches=False, lw=3.4)
        for e in etapes_de(etapes, it):
            p = e["properties"]
            if p["hors_carte"]:
                continue
            ex, ey = merc(*e["geometry"]["coordinates"])
            ax.scatter([ex], [ey], s=40, c="white", edgecolors=ITI_COL[k], linewidths=1.6, zorder=6)
    echelle(ax, (lat0 + lat1) / 2, 500, "500 m")
    y = 0.80
    fig.text(0.69, y, "LES CINQ TRAJETS", fontsize=11, color=MUTED, fontweight="bold")
    y -= 0.04
    for k, it in enumerate(its):
        pr = it["properties"]
        fig.add_artist(plt.Line2D([0.69, 0.715], [y - 0.006, y - 0.006], color=ITI_COL[k], lw=4,
                                  transform=fig.transFigure))
        t = textwrap.wrap(f"{pr['id'][2:]} · {pr['titre']}", 40)
        fig.text(0.722, y, "\n".join(t), fontsize=11.5, color=INK, va="top", family=SERIF, linespacing=1.2)
        y -= 0.0185 * len(t)
        fig.text(0.722, y - 0.004, f"{pr['date']} · {round(pr['longueur_m'] / 100) / 10} km tracés"
                 + (" · itinéraire type" if pr["nature"] == "composite" else ""), fontsize=9.5, color=MUTED,
                 va="top")
        y -= 0.05
    fig.text(0.69, y - 0.01, textwrap.fill("Une planche par itinéraire, avec les étapes numérotées et leurs "
             "références, se trouve dans 05_Cartes/itineraires/. Les tracés suivent au plus court la voirie "
             "actuelle entre des étapes nommées par le roman : ce sont des reconstitutions.", 52),
             fontsize=10, color=MUTED, va="top")
    fig.text(0.036, 0.035, CREDIT["carte1950"] + " · Tracés : © les contributeurs OpenStreetMap (ODbL).",
             fontsize=9.5, color=MUTED)
    fig.savefig(CARTES / "itineraires.png", dpi=100, facecolor=PAPER)
    plt.close(fig)
    print("itineraires.png")


ATLAS = """<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Atlas historique — Lyon des Deux Étendards</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
html,body{margin:0;height:100%;background:#f7f2e8;color:#243a3f;font-family:Arial,Helvetica,sans-serif}
header{padding:14px 20px;border-bottom:1px solid #d8d2c6}header h1{font:28px Georgia,serif;margin:2px 0}
header p{margin:0;font-size:13px;color:#687778}#map{position:absolute;top:86px;bottom:0;left:0;right:0}
.leaflet-popup-content{font-size:13px;line-height:1.45;max-width:340px}.leaflet-popup-content h3{font:18px Georgia,serif;margin:0 0 6px}
.tag{font-size:11px;font-weight:bold;text-transform:uppercase;letter-spacing:.04em}
.num{display:flex;align-items:center;justify-content:center;width:24px;height:24px;border-radius:50%;color:#fff;font:bold 11px Arial;border:2px solid #fff;box-shadow:0 0 2px #0006}
.num.probable{border-radius:4px;transform:rotate(45deg)}.num.probable span{transform:rotate(-45deg)}
.num.hypothese{background:#fff!important;border:2px dashed #b45942;color:#b45942}
.etape{display:flex;align-items:center;justify-content:center;width:18px;height:18px;border-radius:50%;background:#fff;font:bold 10px Arial;border:2px solid}
.legend{background:#fffdf8ee;padding:8px 10px;border:1px solid #d8d2c6;border-radius:6px;font-size:12px;line-height:1.7}
</style></head><body>
<header><h1>Lyon des <i>Deux Étendards</i> — atlas sur fonds historiques</h1>
<p>Fonds IGN : carte de 1950, photographies aériennes 1950-1965, carte d'état-major (1820-1866) ; fond actuel OpenStreetMap. Repères de lecture, non cadastraux. Les fiches sont dans le dépôt (liens relatifs).</p></header>
<div id="map"></div>
<script>
const LIEUX = __LIEUX__;
const ITI = __ITI__;
const COL = {atteste:'#235460', probable:'#b07125', hypothese:'#b45942', non_localise:'#7a7772'};
const LIB = {atteste:'Localisation identifiée', probable:'Localisation probable', hypothese:'Hypothèse', non_localise:'Non localisé'};
const ITICOL = ['#7b3f8c','#1f7a63','#c0392b','#2e5fa8','#a0522d'];
function ign(layer, tms, fmt){ return L.tileLayer('https://data.geopf.fr/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER='+layer+'&STYLE=normal&TILEMATRIXSET='+tms+'&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}&FORMAT='+fmt,
  {maxZoom:19, maxNativeZoom: tms==='PM_0_18'?18:15, attribution:'IGN, Géoplateforme — Licence ouverte Etalab 2.0'}); }
const fonds = {
 'Carte IGN 1950': ign('GEOGRAPHICALGRIDSYSTEMS.MAPS.SCAN50.1950','PM_3_15','image/jpeg'),
 'Photographies aériennes 1950-1965': ign('ORTHOIMAGERY.ORTHOPHOTOS.1950-1965','PM_0_18','image/png'),
 "Carte d'état-major (1820-1866)": ign('GEOGRAPHICALGRIDSYSTEMS.ETATMAJOR40','PM_6_15','image/jpeg'),
 'Plan actuel (OpenStreetMap)': L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19, attribution:'© les contributeurs OpenStreetMap'})
};
const map = L.map('map',{layers:[fonds['Carte IGN 1950']]}).setView([45.7585,4.8390],15);
const groupes = {};
for (const s of ['atteste','probable','hypothese']) groupes[s] = L.layerGroup().addTo(map);
function esc(t){return String(t??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}
for (const l of LIEUX){
  if(!l.geometry) continue; const c = COL[l.statut];
  const g = L.geoJSON(l.geometry,{style:{color:c,weight:l.geometry.type==='LineString'?8:1.5,opacity:.45,dashArray:'5 4',fillOpacity:.18}});
  let a = l.ancre; const icon = L.divIcon({className:'',html:'<div class="num '+l.statut+'" style="background:'+c+'"><span>'+l.num+'</span></div>',iconSize:[24,24],iconAnchor:[12,12]});
  const m = L.marker([a[1],a[0]],{icon,title:l.nom});
  if(l.geometry.type==='Point' && l.precision_m) L.circle([a[1],a[0]],{radius:l.precision_m,color:c,weight:1,dashArray:'4 4',fillOpacity:.1}).addTo(groupes[l.statut]);
  const html = '<h3>'+l.num+'. '+esc(l.nom)+'</h3><div class="tag" style="color:'+c+'">'+LIB[l.statut]+(l.code?' · '+esc(l.code):'')+'</div><p>'+esc(l.description)+'</p>'+
    (l.nom_actuel?'<p><b>Aujourd’hui :</b> '+esc(l.nom_actuel)+'</p>':'')+
    (l.refs&&l.refs.length?'<p><b>Texte :</b> '+esc(l.refs.join(' ; '))+'</p>':'')+
    (l.fiche_lieu||l.fiche?'<p>'+(l.fiche_lieu?'<a href="'+esc(l.fiche_lieu)+'">Fiche du lieu</a>':'')+(l.fiche&&l.fiche.indexOf('par_lieu')<0?(l.fiche_lieu?' · ':'')+'<a href="'+esc(l.fiche)+'">Dossier d’argumentation</a>':'')+'</p>':'')+
    (l.sources&&l.sources.length?'<p><b>Sources :</b><br>'+l.sources.map(s=>s.startsWith('http')?'<a href="'+esc(s)+'">'+esc(s.replace(/^https?:\\/\\//,'').slice(0,60))+'</a>':esc(s)).join('<br>')+'</p>':'');
  m.bindPopup(html); if(l.geometry.type!=='Point') g.addTo(groupes[l.statut]); m.addTo(groupes[l.statut]);
}
const itiGroupes = {};
ITI.features.filter(f=>f.properties.type==='itineraire').forEach((f,k)=>{
  const gr = L.layerGroup(); const c = ITICOL[k%ITICOL.length];
  L.geoJSON(f,{style:{color:c,weight:4,opacity:.9}}).bindPopup('<h3>'+esc(f.properties.titre)+'</h3><p>'+esc(f.properties.date)+'</p><p>'+esc(f.properties.resume)+'</p><p><b>Texte :</b> '+esc(f.properties.refs.join(' ; '))+'</p><p><i>Tracé reconstitué au plus court entre les étapes attestées.</i></p>').addTo(gr);
  ITI.features.filter(e=>e.properties.type==='etape'&&e.properties.itineraire===f.properties.id&&!e.properties.hors_carte).forEach(e=>{
    const p=e.properties; L.marker([e.geometry.coordinates[1],e.geometry.coordinates[0]],{icon:L.divIcon({className:'',html:'<div class="etape" style="border-color:'+c+';color:'+c+'">'+p.ordre+'</div>',iconSize:[18,18],iconAnchor:[9,9]})})
      .bindPopup('<b>'+p.ordre+'. '+esc(p.nom)+'</b><br>'+esc(p.ref)+(p.a_confirmer?'<br><i>localisation à confirmer</i>':'')).addTo(gr);});
  itiGroupes['Itinéraire '+f.properties.id.slice(-1)+' — '+f.properties.titre] = gr;
});
const overlays = {'Localisations identifiées':groupes.atteste,'Localisations probables':groupes.probable,'Hypothèses':groupes.hypothese, ...itiGroupes};
L.control.layers(fonds, overlays, {collapsed:false}).addTo(map);
L.control.scale({imperial:false}).addTo(map);
const lg = L.control({position:'bottomleft'}); lg.onAdd=()=>{const d=L.DomUtil.create('div','legend');
 d.innerHTML='<b>Degrés de certitude</b><br>'+['atteste','probable','hypothese'].map(s=>'<span style="color:'+COL[s]+'">●</span> '+LIB[s]).join('<br>')+'<br><i>Zones et segments : marges de recherche, non des adresses.</i>'; return d;}; lg.addTo(map);
</script></body></html>
"""


def atlas_historique():
    lieux = charger_lieux()
    rows = []
    for l in lieux:
        if not l.get("geometry"):
            continue
        rows.append({"num": l["num"], "id": l["id"], "code": l.get("code", ""), "nom": l["nom"],
                     "statut": l["statut"], "geometry": l["geometry"], "ancre": ancre(l),
                     "precision_m": l.get("precision_m"), "description": l.get("description", ""),
                     "nom_actuel": l.get("nom_actuel", ""), "refs": l.get("refs", []),
                     "sources": l.get("sources", []), "fiche": l.get("fiche", ""),
                     "fiche_lieu": "../" + chemin_fiche(l) if l.get("code") else ""})
    iti = json.loads((DONNEES / "itineraires.geojson").read_text(encoding="utf-8"))
    html = ATLAS.replace("__LIEUX__", json.dumps(rows, ensure_ascii=False)).replace(
        "__ITI__", json.dumps(iti, ensure_ascii=False))
    (CARTES / "atlas_historique.html").write_text(html, encoding="utf-8")
    print(f"atlas_historique.html : {len(rows)} lieux")


def main():
    CARTES.mkdir(exist_ok=True)
    seulement = [a.split("=", 1)[1] for a in sys.argv if a.startswith("--seulement=")]
    if seulement:
        for nom in seulement[0].split(","):
            {"atlas": atlas_historique, "itineraires": carte_itineraires}[nom]()
        return
    atlas_historique()
    carte_lieux("lyon_carte_ign_1950.png", "Lyon sur la carte de 1950",
                "Les lieux du roman sur la carte IGN la plus proche de leur temps · centre de Lyon",
                "carte1950", 15, (4.812, 45.739, 4.862, 45.7795), (1000, "1000 m"),
                "La carte de 1950 montre les ponts reconstruits après 1944.")
    carte_lieux("guillotiere_photo_1950.png", "De la place Morand à la Guillotière",
                "Le quartier du trio sur les photographies aériennes de 1950-1965",
                "photo1950", 17, (4.8375, 45.7485, 4.8545, 45.7700), (200, "200 m"),
                "Clichés postérieurs d'une génération au roman.", taille=1.0)
    carte_lieux("environs_ign_1950.png", "Lyon et ses environs",
                "Villas, guinguettes et excursions · carte IGN de 1950",
                "carte1950", 13, (4.62, 45.655, 4.98, 45.905), (5000, "5 km"),
                "Les villas et maisons de famille ne sont pas identifiées à la parcelle.", taille=0.9,
                secteurs={"E"})
    carte_lieux("region_ign_1950.png", "Du Beaujolais au Dauphiné",
                "Brouilly, Mongré, Claveisolles, les villages de Michel · carte IGN de 1950",
                "carte1950", 11, (4.40, 45.25, 5.10, 46.25), (20000, "20 km"),
                "Noms déguisés (l'Épervière, Saint-Chély) : hypothèses biographiques.", taille=0.9,
                secteurs={"R"})
    carte_itineraires()


if __name__ == "__main__":
    main()
