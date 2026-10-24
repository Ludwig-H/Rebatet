#!/usr/bin/env python3
"""Extrait le texte de l'EPUB des *Deux Étendards* en fichiers numérotés par paragraphe.

Chaque chapitre devient un fichier texte dont chaque paragraphe est préfixé par
« [§n] » : c'est le système de référence utilisé dans tout le dossier
(« ch. XIX, § 34 »). Les fichiers produits restent locaux (dossier
`_texte/`, ignoré par git) : le roman est encore protégé par le droit d'auteur,
seules de courtes citations figurent dans le dépôt.

Usage :
    python3 01_extraire_texte.py [chemin_epub] [dossier_sortie]
"""
import html
import os
import re
import sys
import textwrap
import zipfile

ICI = os.path.dirname(os.path.abspath(__file__))
EPUB = os.path.join(ICI, "..", "..", "..", "DeuxÉtendards",
                    "Les deux étendards (Lucien Rebatet).epub")
SORTIE = os.path.join(ICI, "_texte")


def xhtml_vers_paragraphes(xhtml):
    xhtml = re.sub(r"<head>.*?</head>", "", xhtml, flags=re.S)
    xhtml = re.sub(r"</p>|<br\s*/?>|</h\d>|</div>", "\n", xhtml)
    texte = html.unescape(re.sub(r"<[^>]+>", "", xhtml))
    return [p.strip() for p in texte.split("\n") if p.strip()]


def main():
    epub = sys.argv[1] if len(sys.argv) > 1 else EPUB
    sortie = sys.argv[2] if len(sys.argv) > 2 else SORTIE
    os.makedirs(sortie, exist_ok=True)
    with zipfile.ZipFile(epub) as z:
        opf = z.read("OEBPS/content.opf").decode("utf-8")
        spine = re.findall(r'itemref idref="([^"]+)"', opf)
        for i, item in enumerate(spine):
            paras = xhtml_vers_paragraphes(z.read("OEBPS/Text/" + item).decode("utf-8"))
            lignes = []
            for n, p in enumerate(paras, 1):
                morceaux = textwrap.wrap(p, width=170) or [""]
                lignes.append(f"[§{n}] " + morceaux[0])
                lignes.extend("      " + m for m in morceaux[1:])
            nom = f"{i:02d}_{item.replace('.xhtml', '')}.txt"
            with open(os.path.join(sortie, nom), "w", encoding="utf-8") as f:
                f.write("\n".join(lignes) + "\n")
    print(f"{len(spine)} fichiers écrits dans {sortie}")


if __name__ == "__main__":
    main()
