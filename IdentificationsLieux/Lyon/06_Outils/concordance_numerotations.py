#!/usr/bin/env python3
"""Concordance entre deux numérotations des paragraphes du témoin EPUB.

- P (référence de l'enquête, 01_Corpus/NOTICE.md) : rang de l'élément <p> dans
  le fichier XHTML du chapitre, titres <h1> non comptés.
- L (numérotation de lecture) : rang des lignes non vides du texte extrait,
  titre de chapitre compris (deux lignes : numéro et intitulé), une ligne par
  <p>, par <br/> interne et par bloc <div>. Elle a servi aux relevés de lecture
  intégrale avant leur conversion.

Les lignes L sont rattachées au paragraphe P qui les contient par comparaison
de leur début. Sortie : 01_Corpus/concordance_numerotations.csv (chapitre,
paragraphe_L, paragraphe_P ; P vide pour les lignes de titre). Le fichier ne
reproduit aucun texte du roman. Bibliothèque standard uniquement.
"""
import csv
import html
import re
from html.parser import HTMLParser
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]


class Paragraphes(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paragraphes, self.buf = [], None

    def handle_starttag(self, tag, attrs):
        if tag == "p":
            self.buf = []

    def handle_endtag(self, tag):
        if tag == "p" and self.buf is not None:
            self.paragraphes.append(" ".join("".join(self.buf).split()))
            self.buf = None

    def handle_data(self, data):
        if self.buf is not None:
            self.buf.append(data)


def etiquette(nom):
    base = nom.rsplit("/", 1)[-1].replace(".xhtml", "")
    m = re.match(r"([IVXL]+)(_|$)", base)
    if m:
        return m.group(1)
    return {"intermedes": "Intermèdes", "recit_de_guitte": "Récit de Guitte", "notes": "Notes"}.get(base)


def lignes_lecture(xhtml):
    xhtml = re.sub(r"<head>.*?</head>", "", xhtml, flags=re.S)
    xhtml = re.sub(r"</p>|<br\s*/?>|</h\d>|</div>", "\n", xhtml)
    texte = html.unescape(re.sub(r"<[^>]+>", "", xhtml))
    return [" ".join(l.split()) for l in texte.split("\n") if l.strip()]


def main():
    epub = next((REPO / "DeuxÉtendards").glob("*.epub"))
    lignes = [("chapitre", "paragraphe_L", "paragraphe_P")]
    with ZipFile(epub) as z:
        opf = z.read("OEBPS/content.opf").decode("utf-8")
        for item in re.findall(r'itemref idref="([^"]+)"', opf):
            ch = etiquette(item)
            if not ch:
                continue
            source = z.read("OEBPS/Text/" + item).decode("utf-8")
            parser = Paragraphes()
            parser.feed(source)
            ps = list(enumerate(parser.paragraphes, 1))
            j = 0
            for n, t in enumerate(lignes_lecture(source), 1):
                trouve = ""
                if len(t) >= 12 and not re.fullmatch(r"[A-ZÉÈÀÂÎÔÛÇ’' ,\-]+", t):
                    candidats = range(j, min(len(ps), j + 60))
                    test = lambda p: t[:60] in p
                elif len(t) < 12:
                    candidats = range(j, min(len(ps), j + 3))
                    test = lambda p: p == t or p.startswith(t)
                else:  # intitulé de chapitre en capitales
                    candidats, test = (), None
                for k in candidats:
                    if test(ps[k][1]):
                        trouve, j = ps[k][0], k
                        break
                lignes.append((ch, n, trouve))
    sortie = ROOT / "01_Corpus" / "concordance_numerotations.csv"
    with open(sortie, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(lignes)
    print(f"{len(lignes) - 1} lignes ; {sum(1 for l in lignes[1:] if l[2] == '')} sans paragraphe <p> (titres)")


if __name__ == "__main__":
    main()
