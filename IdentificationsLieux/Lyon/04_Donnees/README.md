# Données de l'enquête

## Fichiers

- **`lieux.json`** : registre unique des 162 lieux, dont 146 cartographiés. Il fusionne le registre de la première enquête (51 notices, dont les identifiants sont conservés) et le répertoire de la lecture intégrale. Les notices ont été arbitrées secteur par secteur, puis soumises à un contrôleur adverse ; les corrections ont été appliquées et relues (voir le [journal du 24 octobre](../07_Journal/2026-10-24.md)).
- **`lieux.geojson`** : export WGS84 du registre, utilisable dans un SIG ; une géométrie `null` ne doit pas être remplacée par `[0,0]`.
- **`index_lieux.csv`** : export tabulaire (UTF-8), une ligne par notice dans l'ordre du registre. Colonnes : code, identifiant, nom, secteur, catégorie, statut, certitude, type de géométrie, `precision_m`, nom de 1925, nom actuel, références, description, sources. Pour les coordonnées, prendre `lieux.json` ou `lieux.geojson`.
- **`itineraires.yaml`** et **`itineraires.geojson`** : cinq itinéraires reconstitués. Le YAML donne les étapes attestées, avec leur référence ; le GeoJSON, calculé par `06_Outils/itineraires.py`, ajoute les tracés au plus court sur la voirie actuelle. Voir [08_itineraires](../03_Fiches/08_itineraires.md).
- **`inventaire_corpus.json`** : 132 entrées lexicales et contextuelles, avec motifs Python et références. Ce sont des mentions, non 132 identifications historiques.
- **`fond_osm.geojson`** et **`fond_osm_provenance.json`** : fond contemporain conservé (ODbL), avec son origine et ses empreintes. Il ne représente pas la voirie de 1925.
- **`geocodage_*.json`** : réponses de la Base Adresse Nationale pour certains repères. L'adresse historique est justifiée dans les notices ; l'API n'en constitue pas la preuve.

## Champs du registre

| Champ | Sens |
|---|---|
| `id` | Identifiant stable ; celui de la première enquête quand il existait |
| `code` | Code de secteur : G Guillotière, B 3e nord et Brotteaux, P Presqu'île, D rive droite de la Saône, E environs, R région ; il nomme la fiche du lieu et l'étiquette des cartes |
| `nom` | Désignation lisible |
| `secteur`, `categorie` | Secteur (lettre du code) ; type de lieu (domicile, café, voie, église, etc.) |
| `statut_nom` | Nature du nom dans le roman : `reel`, `surnom` (place Antique), `deguise`, `fictif`, `implicite` (lieu désigné sans être nommé) |
| `statut` | Statut cartographique : `atteste` (identification retenue), `probable`, `hypothese`, `non_localise` (aucune géométrie) |
| `certitude` | Degré de certitude de l'identification, de A (certaine) à E (fictive ou non localisable) ; voir le [protocole](../00_Methode/PROTOCOLE.md) |
| `geometry` | Point, ligne ou zone en WGS84 [longitude, latitude] ; `null` si aucune proposition n'est défendable |
| `precision_m` | Marge graphique indicative, ni statistique ni cadastrale. Pour un lieu situé sur une voie sans immeuble identifié, elle mesure l'incertitude le long de la voie |
| `georeferencement` | `{methode}` : origine des coordonnées (axe de voie Grand Lyon, nœud ou fond OSM, point d'adresse BAN, zone tracée) ; `null` sans géométrie |
| `description` | Résultat, portée et réserves, en une à trois phrases |
| `identification` | Ce qu'était le lieu en 1925 et ce qu'il est devenu |
| `nom_1925`, `nom_actuel` | Nom au temps du récit et équivalent actuel (liste des voies anciennes des Archives de Lyon) |
| `refs` | Passages du roman, au format `XII §124` ou `XII §124-127` (numérotation P, voir [NOTICE](../01_Corpus/NOTICE.md)) ; tous contrôlés par `verifier_dossier.py` |
| `cle` | Citation-clé de 30 mots au plus, avec sa référence |
| `arguments` | Raisonnement d'identification, preuves et réserves |
| `motifs` | Expressions régulières de la concordance (insensibles à la casse ; préfixe `CS:` pour une recherche sensible à la casse) ; elles alimentent l'[index des occurrences](../01_Corpus/index_occurrences.md) |
| `sources` | Pièces historiques et géographiques utilisées (URL ou référence complète) |
| `temoignages` | Apports des sources extérieures (témoins, biographes, archives nominatives), chacun avec sa référence et son degré de fiabilité |
| `fiche` | Dossier d'argumentation (dossier thématique de `03_Fiches`, ou `01_Corpus/INVENTAIRE.md` pour six notices ; chemin relatif depuis `05_Cartes`), pour les notices de la première enquête |

Le statut du lieu et la forme de sa géométrie ne sont pas interchangeables. Un lieu que le texte situe sur une voie nommée, sans immeuble identifié, est `atteste` pour la voie ; sa géométrie est alors la voie ou le tronçon désigné, et sa certitude mesure la restriction au tronçon : A quand la voie entière est retenue, B ou C quand la notice n'en retient qu'un tronçon. La description le dit chaque fois. Un point déduit (une porte, un angle) suit au contraire la certitude de la déduction.

## Inventaire lexical

Les comptes de l'inventaire excluent les faux positifs explicitement contrôlés ; ils comptent les expressions retenues, non les visites. Les mentions du café des Alpes font l'objet d'une concordance manuelle distincte du motif littéral : le champ `alias_audit_refs` de l'entrée `cafe_alpes` d'`inventaire_corpus.json`. Elle compte 25 paragraphes qui nomment le café en entier ou par ellipse (« les Alpes », « aux Alpes ») : les 9 paragraphes du motif « café des Alpes » et 16 paragraphes de reprises elliptiques seules, dont les deux évocations du chapitre XVIII (§101 et 119). Les sens géographiques d'« Alpes » en sont exclus. Les reprises sans le nom (X §§190–229, XXIV §137) ne sont pas dénombrées.
