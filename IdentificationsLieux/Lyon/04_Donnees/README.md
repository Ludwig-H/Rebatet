# Données de l'enquête

- **`inventaire_corpus.json`** : 132 entrées lexicales et contextuelles, avec motifs Python et références. Ce ne sont pas 132 identifications historiques.
- **`lieux.json`** : registre éditorial des notices cartographiques, incluant les lieux laissés sans coordonnées.
- **`lieux.geojson`** : export WGS84, utilisable dans un SIG ; une géométrie `null` ne doit pas être remplacée par `[0,0]`.
- **`index_lieux.csv`** : export tabulaire simplifié du registre (UTF-8, produit par `06_Outils/exporter_donnees.py`), une ligne par notice dans l'ordre de `lieux.json` : identifiant, nom, statut, type de géométrie (vide si la notice n'est pas placée), `precision_m`, références, description, sources. Les coordonnées, la fiche et le géoréférencement n'y figurent pas : les prendre dans `lieux.json` ou `lieux.geojson`.
- **`fond_osm.geojson`** et **`fond_osm_provenance.json`** : fond contemporain conservé, origine et empreintes, sous ODbL. Il ne représente pas la voirie de 1925.
- **`geocodage_*.json`** : réponses de la Base Adresse Nationale et requêtes pour certains repères. L'adresse historique est justifiée dans les fiches ; l'API n'en constitue pas la preuve.

## Champs du registre

| Champ | Sens |
|---|---|
| `id` | Identifiant stable de la notice ; peut différer de l'entrée lexicale quand les objets ne coïncident pas |
| `nom` | Désignation lisible, accompagnée de l'hypothèse lorsqu'elle est nécessaire |
| `statut` | `atteste` (identification retenue), `probable`, `hypothese`, `non_localise` |
| `geometry` | Repère WGS84 [longitude, latitude], segment ou zone ; `null` si pas de proposition défendable |
| `precision_m` | Marge graphique indicative ; ni statistique ni cadastrale |
| `description` | Résultat, portée et réserves propres au lieu |
| `refs` | Passages du roman, au format `OEBPS/Text/fichier.xhtml#pN` (existence du paragraphe contrôlée par `verifier_dossier.py`) ou `CHAPITRE §N`, `§§N–M` (non contrôlé automatiquement ; formes hétérogènes, à normaliser). À corriger : `bellecour` cite « XXIII, titre et §1 », alors que XXIII §1 ne nomme pas Bellecour ; hors le titre du chapitre (« Les théologiens de Bellecour »), la première mention est en XXIII §28 |
| `sources` | URLs des pièces historiques utilisées ; liste vide lorsque le résultat repose uniquement sur le texte et le repérage géographique |
| `fiche` | Dossier d'argumentation, chemin relatif depuis `05_Cartes` |
| `georeferencement` | Méthode qui a produit les coordonnées (repérage sur le fond OSM, repère ou géocodage BAN, Wikimedia Commons), avec selon les cas la requête (`adresse_requete`), le libellé renvoyé (`label_retour`) et la `source` ; `null` pour les notices sans géométrie, sauf `maristes_regis`, qui garde la trace d'un géocodage BAN (« 4 montée Saint Barthélemy Lyon ») alors que sa géométrie est nulle (incohérence à résoudre) |

Le statut du lieu et la forme de sa géométrie ne sont pas interchangeables : une rue explicitement donnée peut être certaine, tandis que le secteur où chercher un appartement sur cette rue reste hypothétique. Les cartes doivent toujours conserver la description et la précision.

Les comptes de l'inventaire lexical excluent les faux positifs explicitement contrôlés ; ils comptent les expressions retenues, non les visites. Les mentions du Café des Alpes font l'objet d'une concordance manuelle distincte du motif littéral : le champ `alias_audit_refs` de l'entrée `cafe_alpes` d'`inventaire_corpus.json`. Elle compte 25 paragraphes qui nomment le café en entier ou par ellipse (« les Alpes », « aux Alpes ») : les 9 paragraphes du motif « café des Alpes » et 16 paragraphes de reprises elliptiques seules, dont les deux évocations du chapitre XVIII (§101 et 119). Les sens géographiques d'« Alpes » en sont exclus. Le compte du motif littéral (10 occurrences en 9 paragraphes) n'inclut pas ces reprises. Les reprises sans le nom (X §§190–229, XXIV §137) ne sont pas dénombrées. Les notes annexes sont séparées du texte narratif.
