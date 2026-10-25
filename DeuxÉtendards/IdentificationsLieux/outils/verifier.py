#!/usr/bin/env python3
"""Vérifie le corpus, le registre, les géométries et les liens du dossier, sans accès réseau.

Les exclusions de contexte sont éditoriales : ce contrôle valide les références
retenues, mais ne prétend pas découvrir toutes les omissions possibles.
"""
from pathlib import Path
from html.parser import HTMLParser
from zipfile import ZipFile
import hashlib
import json
import re
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]  # DeuxÉtendards/IdentificationsLieux
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
    epub = next(ROOT.parent.glob('*.epub'))
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


ROMAINS = r'(XXXVII|XXXVI|XXXV|XXXIV|XXXIII|XXXII|XXXI|XXX|XXIX|XXVIII|XXVII|XXVI|XXV|XXIV|XXIII|XXII|XXI|XX|XIX|XVIII|XVII|XVI|XV|XIV|XIII|XII|XI|X|IX|VIII|VII|VI|V|IV|III|II|I|Intermèdes|Récit de Guitte|Notes)'
REF = re.compile(ROMAINS + r',? §§?(\d+)(?:\s*[-–]\s*(\d+))?')


def etiquette(nom):
    base = nom.rsplit('/', 1)[-1].replace('.xhtml', '')
    m = re.match(r'([IVXL]+)(_|$)', base)
    if m:
        return m.group(1)
    return {'intermedes': 'Intermèdes', 'recit_de_guitte': 'Récit de Guitte', 'notes': 'Notes'}.get(base)


def verifier_geometry(g):
    if g is None:
        return
    assert g['type'] in ('Point', 'LineString', 'Polygon'), g
    pairs = [g['coordinates']] if g['type'] == 'Point' else (
        g['coordinates'] if g['type'] == 'LineString' else [p for ring in g['coordinates'] for p in ring])
    for lon, lat in pairs:
        assert 4.3 < lon < 5.3 and 45.2 < lat < 46.3, (lon, lat)  # Lyon et région (Moras, Brouilly)
    if g['type'] == 'Polygon':
        assert all(r[0] == r[-1] and len(r) >= 4 for r in g['coordinates'])


LIEN = re.compile(r'\]\((<[^>]+>|[^)\s]+)\)')


def verifier_liens():
    """Liens relatifs des fichiers Markdown du dossier et du README du roman, ancres comprises."""
    n = 0
    for md in sorted(ROOT.rglob('*.md')) + [ROOT.parent / 'README.md']:
        if not md.exists():
            continue
        for cible in LIEN.findall(md.read_text(encoding='utf-8')):
            cible = unquote(cible.strip('<>'))
            if re.match(r'[a-z]+:', cible) or cible.startswith('#'):
                continue
            chemin, _, frag = cible.partition('#')
            fichier = md.parent / chemin
            assert fichier.exists(), ('lien cassé', str(md.relative_to(ROOT.parent)), cible)
            if frag and fichier.suffix == '.md':
                assert f'id="{frag}"' in fichier.read_text(encoding='utf-8'), ('ancre absente', str(md.relative_to(ROOT.parent)), cible)
            n += 1
    return n


def main():
    corpus = lire_corpus()
    inv = json.loads((ROOT / 'donnees/inventaire.json').read_text())
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
        for kind in ('context_refs', 'paratext_refs', 'alias_refs'):
            for r in x.get(kind, []):
                assert (r['file'], r['p']) in corpus, (x['id'], kind, r)
    lieux = json.loads((ROOT / 'donnees/lieux.json').read_text())
    chapitres = {(etiquette(f), p) for f, p in corpus}
    ref_chapitre = 0
    assert len({x['id'] for x in lieux}) == len(lieux), 'IDs cartes dupliqués'
    for x in lieux:
        assert x['statut'] in ('atteste', 'probable', 'hypothese', 'non_localise'), x['id']
        verifier_geometry(x['geometry'])
        assert x['refs'] and x['description'], x['id']
        if x['statut'] == 'non_localise':
            assert x['geometry'] is None, x['id']
        if x.get('fiche'):
            target = ROOT / x['fiche'].split('#')[0]
            assert target.is_file(), (x['id'], target)
        for r in x['refs']:
            if '#p' in r:
                f, p = r.rsplit('#p', 1)
                assert (f, int(p)) in corpus, (x['id'], r)
            else:
                # forme « XII §124 », « XII §124-127 », « Notes §21 » (convention P, cf. METHODE.md)
                trouve = False
                for m in REF.finditer(r):
                    ch, a, b = m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))
                    assert (ch, a) in chapitres and (ch, b) in chapitres, (x['id'], r)
                    trouve = True
                    ref_chapitre += 1
                assert trouve or 'titre' in r, (x['id'], 'référence non reconnue', r)
    liens = verifier_liens()
    print(json.dumps({'corpus_sha256': SHA, 'paragraphes_non_vides': len(corpus),
                      'entrees_inventaire': len(inv), 'references_lexicales_verifiees': ref_count,
                      'notices_cartographiques': len(lieux),
                      'notices_avec_geometrie': sum(x['geometry'] is not None for x in lieux),
                      'references_chapitre_verifiees': ref_chapitre,
                      'liens_markdown_verifies': liens,
                      'controle': 'OK'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
