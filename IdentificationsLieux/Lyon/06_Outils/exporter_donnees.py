#!/usr/bin/env python3
"""Dérive GeoJSON et index tabulaire de lieux.json, sans réseau."""
from pathlib import Path
import csv
import json

root = Path(__file__).resolve().parents[1]
folder = root / '04_Donnees'
lieux = json.loads((folder / 'lieux.json').read_text())
features = [{'type': 'Feature', 'id': x['id'], 'geometry': x['geometry'],
             'properties': {k: v for k, v in x.items() if k != 'geometry'}} for x in lieux]
(folder / 'lieux.geojson').write_text(json.dumps({'type': 'FeatureCollection',
    'name': 'Lyon dans Les Deux Étendards — identifications et hypothèses',
    'features': features}, ensure_ascii=False, indent=2) + '\n')
with (folder / 'index_lieux.csv').open('w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['code', 'id', 'nom', 'secteur', 'categorie', 'statut', 'certitude', 'geometrie', 'precision_m',
                'nom_1925', 'nom_actuel', 'references', 'description', 'sources'])
    for x in lieux:
        w.writerow([x.get('code', ''), x['id'], x['nom'], x.get('secteur', ''), x.get('categorie', ''), x['statut'],
                    x.get('certitude', ''), x['geometry']['type'] if x['geometry'] else '', x['precision_m'],
                    x.get('nom_1925', ''), x.get('nom_actuel', ''), ' ; '.join(x.get('refs', [])),
                    x.get('description', ''), ' ; '.join(x.get('sources', []))])
print(f'{len(lieux)} notices exportées ; les géométries nulles restent explicitement non placées.')
