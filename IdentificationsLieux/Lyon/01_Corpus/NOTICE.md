# Corpus et système de références

## Témoin utilisé

- Fichier du dépôt : `DeuxÉtendards/Les deux étendards (Lucien Rebatet).epub`.
- Commit de départ : `aa38aa3fc2d80ff5e6c9f1dbcff3eed92c829459`.
- Blob Git : `ebf33de718dfac2f89156cc2c9b41a072bceb3e5`.
- SHA-256 : `88daa208cc3eeca363f33ddfbf1be4e3bec83a0c0d5ab407d0c1aa34ae7e6e18`.
- Taille : 1 335 930 octets.
- 8 003 éléments `p` dans l'ensemble des XHTML, paratextes et notes compris, dont deux vides (titre §4, XII §96), soit 8 001 paragraphes non vides. Le vide XII §96 étant compté, toute renumérotation des seuls paragraphes visibles est décalée d'une unité à partir de XII §97.

Le fichier OPF indique Gallimard, l'ISBN `9782070724673`, une date encodée `1950-12-31T23:00:00+00:00`, ainsi que des traces de conversion Calibre et Sigil. La page de copyright porte « © Éditions Gallimard, 1951 ». Ces éléments décrivent le fichier. L'ISBN (978-2-07-072467-3, soit 2-07-072467-0) est celui de la réimpression Gallimard de 1991 en un volume de 1312 p. ([notice BnF cb35472418v](https://catalogue.bnf.fr/ark:/12148/cb35472418v), consultée le 24 octobre 2026). La date encodée correspond au 1er janvier 1951 à 0 h, heure de Paris : c'est l'année 1951 du copyright, enregistrée comme date seule. Le texte dérive donc vraisemblablement de cette réimpression ; ni sa pagination ni une collation typographique ne peuvent lui être attribuées sans examen de l'imprimé.

La [notice d'œuvre de la BnF](https://catalogue.bnf.fr/ark:/12148/cb136141571) donne **1952** comme date de l'œuvre (« Date de l'oeuvre : 1952 »). La [notice bibliographique de l'édition originale](https://catalogue.bnf.fr/ark:/12148/cb357789124) (consultée le 24 octobre 2026) porte en revanche « Paris : Gallimard, 1951 », 2 vol. (496, 519 p.), en accord avec le « © 1951 » du témoin. On distingue donc le millésime de l'impression (1951) de la date retenue pour l'œuvre (1952). Celle-ci renvoie sans doute à la mise en vente, au début de 1952 ; ce point n'a pas été vérifié sur une source datée. On n'attribue à cet EPUB la pagination d'aucune édition imprimée sur la seule foi des métadonnées : ni celle de la réimpression de 1991 que désigne son ISBN, ni celle d'une édition plus récente (l'existence d'éditions de 2007 ou 2009 n'a pas été contrôlée au catalogue).

## Comment retrouver un passage

`X §149` signifie : fichier `OEBPS/Text/X_christ_est_ressuscite.xhtml`, 149e élément `p`. La numérotation compte tous les éléments `p`, même si certains sont vides. Les mots sont rassemblés depuis les nœuds de texte et les espaces normalisés pour la recherche. Les parties sans numéro romain sont désignées par une étiquette courte : « intermedes » (`intermedes.xhtml`), « recit » (`recit_de_guitte.xhtml`), « notes » (`notes.xhtml`, cité aussi « Notes §11 ») ; XXXVII renvoie à `XXXVII.xhtml`.

Un paragraphe HTML peut être long ; il n'est ni une page ni nécessairement une unité choisie par l'auteur. Les fiches donnent un fragment court ou une description pour faciliter la reconnaissance dans un autre exemplaire.

## Limites du dépouillement

L'examen combine reconnaissance de toponymes, lecture de contextes et recherches par variantes. Il couvre les lieux nommés et les principaux lieux anonymes repérés ; il n'équivaut pas à une édition critique collationnée ligne à ligne avec l'imprimé. Les occurrences d'un dictionnaire ne sont pas une découverte automatique de tous les noms propres.

Les recherches `Deux Alpes`/`Deux-Alpes` ne fournissent pas le nom du café lyonnais dans ce témoin. Le nom lu dans le texte est **Café des Alpes**, avec reprises « les Alpes ». Le mot Alpes désigne aussi la montagne : ses occurrences ne doivent pas être comptées indistinctement comme des visites au café.

Les extractions intégrales de travail ne sont pas ajoutées au dépôt. Les nouveaux fichiers publient les analyses, les références et les données d'identification ; le témoin déjà présent est laissé intact.
