#!/usr/bin/env python3
"""Accès au témoin EPUB selon la convention de référence du dossier.

« XII §124 » désigne le 124e élément <p> du fichier XHTML du chapitre XII
(titres <h1> non comptés ; cf. METHODE.md). Bibliothèque standard
uniquement. Utilisable aussi en ligne de commande :

  python3 outils/corpus.py show XII 124 126    # affiche XII §124 à §126
  python3 outils/corpus.py grep "rue de Jarente" [XI]
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]  # DeuxÉtendards/IdentificationsLieux
LIBELLES = {"intermedes": "Intermèdes", "recit_de_guitte": "Récit de Guitte", "notes": "Notes"}
ALIAS = {"intermedes": "Intermèdes", "intermèdes": "Intermèdes", "recit": "Récit de Guitte",
         "récit": "Récit de Guitte", "récit de guitte": "Récit de Guitte", "notes": "Notes"}


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
    """Nom de fichier XHTML -> étiquette de chapitre (« XII », « Notes »…), ou None."""
    base = nom.rsplit("/", 1)[-1].replace(".xhtml", "")
    m = re.match(r"([IVXL]+)(_|$)", base)
    return m.group(1) if m else LIBELLES.get(base)


def epub():
    return next(ROOT.parent.glob("*.epub"))  # le témoin, dans DeuxÉtendards/


def paragraphes():
    """Liste ordonnée de (chapitre, numéro P, fichier XHTML, texte)."""
    out = []
    with ZipFile(epub()) as z:
        opf = z.read("OEBPS/content.opf").decode("utf-8")
        for item in re.findall(r'itemref idref="([^"]+)"', opf):
            ch = etiquette(item)
            if not ch:
                continue
            p = Paragraphes()
            p.feed(z.read("OEBPS/Text/" + item).decode("utf-8"))
            out += [(ch, i, item, t) for i, t in enumerate(p.paragraphes, 1)]
    return out


def chapitres():
    """Ordre de lecture des étiquettes de chapitre."""
    vus = []
    for ch, *_ in paragraphes():
        if ch not in vus:
            vus.append(ch)
    return vus


def normaliser(ch):
    return ALIAS.get(ch.lower(), ch.upper() if re.fullmatch(r"[ivxlIVXL]+", ch) else ch)


if __name__ == "__main__":
    ps = paragraphes()
    if len(sys.argv) >= 4 and sys.argv[1] == "show":
        ch, a = normaliser(sys.argv[2]), int(sys.argv[3])
        b = int(sys.argv[4]) if len(sys.argv) > 4 else a
        for c, i, _, t in ps:
            if c == ch and a <= i <= b:
                print(f"[{c} §{i}] {t}\n")
    elif len(sys.argv) >= 3 and sys.argv[1] == "grep":
        rx = re.compile(sys.argv[2], re.I)
        ch = normaliser(sys.argv[3]) if len(sys.argv) > 3 else None
        for c, i, _, t in ps:
            if ch and c != ch:
                continue
            m = rx.search(t)
            if m:
                s = max(0, m.start() - 90)
                print(f"{c} §{i} : …{t[s:m.end() + 90]}…")
    else:
        print(__doc__)
