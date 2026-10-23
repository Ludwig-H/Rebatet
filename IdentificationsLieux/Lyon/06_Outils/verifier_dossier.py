#!/usr/bin/env python3
"""Vérifie le corpus, les concordances et les géométries sans accès réseau.

Les exclusions de contexte sont éditoriales : ce contrôle valide les références
retenues, mais ne prétend pas découvrir toutes les omissions possibles.
"""
from pathlib import Path
from html.parser import HTMLParser
from zipfile import ZipFile
import hashlib
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
SHA = '88daa208cc3eeca363f33ddfbf1be4e3bec83a0c0d5ab407d0c1aa34ae7e6e18'


class Paragraphes(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paragraphes = []
        self.buf = None

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.buf = []

    def handle_endtag(self, tag):
        if tag == 'p' and self.buf is not None:
            self.paragraphes.append(' '.join(''.join(self.buf).split()))
            self.buf = None

    def handle_data(self, data):
        if self.buf is not None:
            self.buf.append(data)


def lire_corpus():
    epub = next((REPO / 'DeuxÉtendards').glob('*.epub'))
    assert hashlib.sha256(epub.read_bytes()).hexdigest() == SHA, 'Le témoin EPUB a changé'
    corpus = {}
    with ZipFile(epub) as z:
        for name in z.namelist():
            if name.endswith('.xhtml'):
                parser = Paragraphes()
                parser.feed(z.read(name).decode('utf-8'))
                for i, texte in enumerate(parser.paragraphes, 1):
                    if texte:
                        corpus[(name, i)] = texte
    return corpus


def verifier_geometry(g):
    if g is None:
        return
    assert g['type'] in ('Point', 'LineString', 'Polygon'), g
    pairs = [g['coordinates']] if g['type'] == 'Point' else (
        g['coordinates'] if g['type'] == 'LineString' else [p for ring in g['coordinates'] for p in ring])
    for lon, lat in pairs:
        assert 4.5 < lon < 5.2 and 45.4 < lat < 46.3, (lon, lat)
    if g['type'] == 'Polygon':
        assert all(r[0] == r[-1] and len(r) >= 4 for r in g['coordinates'])


def main():
    corpus = lire_corpus()
    inv = json.loads((ROOT / '04_Donnees/inventaire_corpus.json').read_text())
    assert len({x['id'] for x in inv}) == len(inv), 'IDs inventaire dupliqués'
    ref_count = 0
    for x in inv:
        pat = re.compile(x['regex'], re.I)
        assert x['paragraph_count'] == len(x['refs']), x['id']
        assert x['count'] == sum(r['matches'] for r in x['refs']), x['id']
        for r in x['refs']:
            key = r['file'], r['p']
            assert key in corpus, (x['id'], key)
            assert len(pat.findall(corpus[key])) == r['matches'], (x['id'], key)
            ref_count += 1
        for kind in ('context_refs', 'paratext_refs', 'alias_audit_refs'):
            for r in x.get(kind, []):
                assert (r['file'], r['p']) in corpus, (x['id'], kind, r)
    lieux = json.loads((ROOT / '04_Donnees/lieux.json').read_text())
    assert len({x['id'] for x in lieux}) == len(lieux), 'IDs cartes dupliqués'
    for x in lieux:
        assert x['statut'] in ('atteste', 'probable', 'hypothese', 'non_localise'), x['id']
        verifier_geometry(x['geometry'])
        assert x['refs'] and x['description'], x['id']
        if x['statut'] == 'non_localise':
            assert x['geometry'] is None, x['id']
        if x.get('fiche'):
            target = (ROOT / '05_Cartes' / x['fiche'].split('#')[0]).resolve()
            assert target.is_file(), (x['id'], target)
        for r in x['refs']:
            if '#p' in r:
                f, p = r.rsplit('#p', 1)
                assert (f, int(p)) in corpus, (x['id'], r)
    for svg in (ROOT / '05_Cartes').glob('*.svg'):
        ET.parse(svg)
    print(json.dumps({'corpus_sha256': SHA, 'paragraphes_non_vides': len(corpus),
                      'entrees_inventaire': len(inv), 'references_lexicales_verifiees': ref_count,
                      'notices_cartographiques': len(lieux),
                      'notices_avec_geometrie': sum(x['geometry'] is not None for x in lieux),
                      'controle': 'OK'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
