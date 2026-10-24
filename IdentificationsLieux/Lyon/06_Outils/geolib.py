"""Géocodage des notices : outils communs.

Méthodes (dictionnaire `geo` passé à `resoudre`) :
  latlon   coordonnées relevées à la main (lat, lon)
  ban      adresse actuelle géocodée par la Base Adresse Nationale (Géoplateforme IGN)
  voie     axe d'une voie du référentiel Grand Lyon (point de l'axe le plus
           proche de son centre)
  inter    carrefour de deux voies du référentiel Grand Lyon (intersection
           calculée ; à défaut, point le plus proche entre les deux axes)
`geometrie_voie(nom)` renvoie l'axe complet d'une voie (LineString des notices de rue).
Les réponses des services sont mises en cache dans 06_Outils/_cache/ (non versionné).
Exemple : python3 -c "import geolib; print(geolib.resoudre({'inter': ('Rue de Créqui', 'Rue Rabelais')}))"
"""
import json
import os
import re
import ssl
import unicodedata
import urllib.parse
import urllib.request

from shapely.geometry import shape
from shapely.ops import nearest_points, unary_union

ICI = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(ICI, "_cache")
CA = "/root/.ccr/ca-bundle.crt"
WFS = ("https://data.grandlyon.com/geoserver/metropole-de-lyon/ows?SERVICE=WFS"
       "&VERSION=1.0.0&REQUEST=GetFeature&TYPENAME=metropole-de-lyon:{couche}"
       "&OUTPUTFORMAT=application/json&SRSNAME=EPSG:4326&BBOX={bbox},EPSG:4326")
BBOX_LYON = "4.76,45.70,4.92,45.81"


def _ctx():
    return ssl.create_default_context(cafile=CA) if os.path.exists(CA) else None


def telecharger(url, chemin):
    """Télécharge `url` vers `chemin` si le fichier n'existe pas déjà."""
    if not os.path.exists(chemin):
        os.makedirs(os.path.dirname(chemin), exist_ok=True)
        req = urllib.request.Request(url, headers={"User-Agent": "Rebatet-IdentificationsLieux/1.0"})
        with urllib.request.urlopen(req, context=_ctx(), timeout=600) as r, open(chemin, "wb") as f:
            f.write(r.read())
    return chemin


def couche_grandlyon(couche, bbox=BBOX_LYON):
    chemin = os.path.join(CACHE, "grandlyon", couche + ".geojson")
    telecharger(WFS.format(couche=couche, bbox=bbox), chemin)
    with open(chemin, encoding="utf-8") as f:
        return json.load(f)


def normaliser(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


_VOIES = None


def voies():
    global _VOIES
    if _VOIES is None:
        _VOIES = {}
        for f in couche_grandlyon("adr_voie_lieu.adrlineairevoie")["features"]:
            p = f["properties"]
            _VOIES.setdefault((normaliser(p["nom"]), p["commune"]), []).append(shape(f["geometry"]))
        _VOIES = {k: unary_union(v) for k, v in _VOIES.items()}
    return _VOIES


def geometrie_voie(nom, commune=None):
    n = normaliser(nom)
    geoms = [g for (k, c), g in voies().items()
             if k == n and (commune is None or c.startswith(commune))]
    if not geoms:
        geoms = [g for (k, c), g in voies().items() if k == n]
    if not geoms:
        raise KeyError(f"voie introuvable : {nom} ({commune})")
    return unary_union(geoms)


def point_voie(nom, commune=None):
    g = geometrie_voie(nom, commune)
    p, _ = nearest_points(g, g.centroid)
    return p.y, p.x


def carrefour(a, b, commune=None):
    ga, gb = geometrie_voie(a, commune), geometrie_voie(b, commune)
    i = ga.intersection(gb)
    if not i.is_empty:
        c = i.centroid
        return c.y, c.x
    p, q = nearest_points(ga, gb)
    return (p.y + q.y) / 2, (p.x + q.x) / 2


def _cache_json(nom):
    chemin = os.path.join(CACHE, nom)
    if os.path.exists(chemin):
        with open(chemin, encoding="utf-8") as f:
            return chemin, json.load(f)
    return chemin, {}


def ban(adresse):
    chemin, cache = _cache_json("ban.json")
    if adresse not in cache:
        url = "https://data.geopf.fr/geocodage/search?" + urllib.parse.urlencode({"q": adresse, "limit": 1})
        with urllib.request.urlopen(url, context=_ctx(), timeout=60) as r:
            f = json.load(r)["features"][0]
        cache[adresse] = {"lat": f["geometry"]["coordinates"][1], "lon": f["geometry"]["coordinates"][0],
                          "label": f["properties"]["label"], "score": f["properties"]["score"]}
        os.makedirs(CACHE, exist_ok=True)
        with open(chemin, "w", encoding="utf-8") as fh:
            json.dump(cache, fh, ensure_ascii=False, indent=1)
    c = cache[adresse]
    return c["lat"], c["lon"]


def resoudre(geo):
    """Renvoie (lat, lon, description de la méthode)."""
    if "latlon" in geo:
        lat, lon = geo["latlon"]
        return lat, lon, "coordonnées relevées"
    if "ban" in geo:
        lat, lon = ban(geo["ban"])
        return lat, lon, f"adresse BAN : {geo['ban']}"
    if "inter" in geo:
        a, b = geo["inter"]
        lat, lon = carrefour(a, b, geo.get("commune"))
        return lat, lon, f"carrefour calculé : {a} × {b}"
    if "voie" in geo:
        lat, lon = point_voie(geo["voie"], geo.get("commune"))
        return lat, lon, f"axe de voie : {geo['voie']}"
    raise ValueError(geo)
