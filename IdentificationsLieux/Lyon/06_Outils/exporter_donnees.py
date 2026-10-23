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
    w.writerow(['id', 'nom', 'statut', 'geometrie', 'precision_m', 'references', 'description', 'sources'])
    for x in lieux:
        w.writerow([x['id'], x['nom'], x['statut'], x['geometry']['type'] if x['geometry'] else '',
                    x['precision_m'], ' ; '.join(x['refs']), x['description'], ' ; '.join(x['sources'])])
print(f'{len(lieux)} notices exportées ; les géométries nulles restent explicitement non placées.')
