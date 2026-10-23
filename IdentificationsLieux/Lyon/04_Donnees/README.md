# Données de l'enquête

- **`inventaire_corpus.json`** : 132 entrées lexicales et contextuelles, avec motifs Python et références. Ce ne sont pas 132 identifications historiques.
- **`lieux.json`** : registre éditorial des notices cartographiques, incluant les lieux laissés sans coordonnées.
- **`lieux.geojson`** : export WGS84, utilisable dans un SIG ; une géométrie `null` ne doit pas être remplacée par `[0,0]`.
- **`index_lieux.csv`** : export tabulaire de ce même registre, UTF-8.
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
| `refs` | Passages du roman, format fichier XHTML#p ou chapitre § |
| `sources` | URLs des pièces historiques utilisées ; liste vide lorsque le résultat repose uniquement sur le texte et le repérage géographique |
| `fiche` | Dossier d'argumentation, chemin relatif depuis `05_Cartes` |
| `georeferencement` | Provenance des coordonnées quand disponible |

Le statut du lieu et la forme de sa géométrie ne sont pas interchangeables : une rue explicitement donnée peut être certaine, tandis que le secteur où chercher un appartement sur cette rue reste hypothétique. Les cartes doivent toujours conserver la description et la précision.

Les comptes de l'inventaire lexical excluent les faux positifs explicitement contrôlés ; ils comptent les expressions retenues, non les visites. Les reprises elliptiques du Café des Alpes sont conservées dans une concordance manuelle séparée. Les notes annexes sont séparées du texte narratif.
