#!/usr/bin/env python3
"""Trace les itinéraires de donnees/itineraires.yaml sur la voirie actuelle.

Entre deux étapes attestées par le roman, le tracé retenu est le plus court
chemin sur le réseau des rues du fond OpenStreetMap conservé dans
donnees/fond_osm.geojson (pas de requête réseau). C'est une reconstitution
schématique : le texte nomme des étapes, rarement les rues suivies entre elles.

Sortie : donnees/itineraires.geojson (une ligne par itinéraire, un point
par étape non technique).

Dépendances : pyyaml, networkx.
"""
import json
import math
from pathlib import Path

import networkx as nx
import yaml

ROOT = Path(__file__).resolve().parents[1]
DONNEES = ROOT / "donnees"
EXCLUS = {"motorway", "motorway_link", "trunk"}


def distance(a, b):
    """Distance en mètres entre deux points (lon, lat)."""
    lat = math.radians((a[1] + b[1]) / 2)
    dx = math.radians(b[0] - a[0]) * math.cos(lat) * 6371000
    dy = math.radians(b[1] - a[1]) * 6371000
    return math.hypot(dx, dy)


def reseau():
    fond = json.loads((DONNEES / "fond_osm.geojson").read_text(encoding="utf-8"))
    g = nx.Graph()
    for f in fond["features"]:
        p = f["properties"]
        if p.get("kind") != "road" or p.get("highway") in EXCLUS:
            continue
        coords = [tuple(round(c, 7) for c in pt) for pt in f["geometry"]["coordinates"]]
        for a, b in zip(coords, coords[1:]):
            g.add_edge(a, b, weight=distance(a, b))
    # On ne garde que la plus grande composante connexe
    return g.subgraph(max(nx.connected_components(g), key=len)).copy()


def noeud_proche(g, lon, lat, noeuds):
    return min(noeuds, key=lambda n: (n[0] - lon) ** 2 + ((n[1] - lat) * 1.43) ** 2)


def main():
    data = yaml.safe_load((DONNEES / "itineraires.yaml").read_text(encoding="utf-8"))
    g = reseau()
    noeuds = list(g.nodes)
    features = []
    for it in data["itineraires"]:
        troncons, courant, longueur = [], [], 0.0
        etapes = it["etapes"]
        for a, b in zip(etapes, etapes[1:]):
            if a.get("hors_carte") or b.get("hors_carte"):
                if courant:
                    troncons.append(courant)
                courant = []
                continue
            na = noeud_proche(g, a["lon"], a["lat"], noeuds)
            nb = noeud_proche(g, b["lon"], b["lat"], noeuds)
            chemin = nx.shortest_path(g, na, nb, weight="weight")
            longueur += nx.path_weight(g, chemin, weight="weight")
            segment = [[a["lon"], a["lat"]]] + [list(n) for n in chemin] + [[b["lon"], b["lat"]]]
            courant.extend(segment if not courant else segment[1:])
        if courant:
            troncons.append(courant)
        geom = ({"type": "LineString", "coordinates": troncons[0]} if len(troncons) == 1
                else {"type": "MultiLineString", "coordinates": troncons})
        features.append({"type": "Feature", "geometry": geom, "properties": {
            "type": "itineraire", "id": it["id"], "titre": it["titre"], "date": it["date"],
            "nature": it["nature"], "resume": it["resume"].strip(), "refs": it["refs"],
            "longueur_m": round(longueur), "trace": "reconstitué (plus court chemin, voirie actuelle)"}})
        ordre = 0
        for e in etapes:
            if e.get("via"):
                continue
            ordre += 1
            features.append({"type": "Feature",
                             "geometry": {"type": "Point", "coordinates": [e["lon"], e["lat"]]},
                             "properties": {"type": "etape", "itineraire": it["id"], "ordre": ordre,
                                            "nom": e["nom"], "ref": e.get("ref", ""),
                                            "lieu": e.get("lieu", ""), "hors_carte": bool(e.get("hors_carte")),
                                            "a_confirmer": bool(e.get("a_confirmer"))}})
        print(f"{it['id']} : {len(etapes)} étapes, {round(longueur)} m tracés, {len(troncons)} tronçon(s)")
    sortie = {"type": "FeatureCollection",
              "name": "Itinéraires des Deux Étendards (tracés reconstitués)",
              "license": "Tracés dérivés du fond OpenStreetMap (ODbL 1.0, © les contributeurs OpenStreetMap)",
              "features": features}
    (DONNEES / "itineraires.geojson").write_text(json.dumps(sortie, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
