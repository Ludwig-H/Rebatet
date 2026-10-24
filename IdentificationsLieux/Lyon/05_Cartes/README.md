# Cartes de l'enquête lyonnaise

## Sur fonds historiques (IGN, 1950)

Les fonds de l'IGN (Géoplateforme, Licence ouverte Etalab 2.0) sont plus proches de 1925 qu'un plan actuel, mais postérieurs d'une génération : les ponts du Rhône détruits en 1944 y sont reconstruits, et plusieurs îlots ont changé. Ils situent les lieux sans restituer la ville du roman. Production : `06_Outils/cartes_historiques.py`. Les tuiles sont téléchargées une fois puis gardées en cache.

- **[Vue d'ensemble](lyon_carte_ign_1950.png)**, sur la carte IGN de 1950. Tous les lieux localisés du centre apparaissent, en points colorés selon le statut, sans étiquette. Les rues nommées par le roman sont tracées en filets. Les enveloppes en tirets délimitent les trois planches de détail.
- **Planches de détail**, sur les photographies aériennes de 1950-1965. Chaque lieu est étiqueté par le code de sa notice, et chaque planche a sa légende complète :
  - [la Guillotière et le cours Gambetta](guillotiere_photo_1950.png) (secteur G) ;
  - [de la place Morand aux Brotteaux](brotteaux_photo_1950.png) (secteur B) ;
  - [la Presqu'île et la rive droite](presquile_photo_1950.png) (secteurs P et D).
- **[Lyon et ses environs](environs_ign_1950.png)** (secteur E) et **[du Beaujolais au Dauphiné](region_ign_1950.png)** (secteur R), sur la carte de 1950.
- **[Cinq itinéraires](itineraires.png)**, vue d'ensemble, et une planche par trajet dans [`itineraires/`](itineraires/), avec les étapes attestées et leurs références. Voir [08_itineraires](../03_Fiches/08_itineraires.md).
- **[Atlas historique](atlas_historique.html)**, interactif (Leaflet). Il offre quatre fonds : carte de 1950, photographies de 1950-1965, carte d'état-major de 1820-1866 et plan actuel. Il affiche les 146 lieux cartographiés et les itinéraires en couches. Chaque fenêtre renvoie à la fiche du lieu. Il demande une connexion pour les tuiles.

![Vue d'ensemble](lyon_carte_ign_1950.png)

## Sur fond moderne (OpenStreetMap), sans réseau

Production : `06_Outils/generer_cartes.py`, bibliothèque standard seulement, aucune requête réseau.

- **[Atlas autonome](atlas_lyon.html)** : toutes les notices, avec recherche, filtres de certitude, zoom et déplacement. Télécharger le fichier HTML puis l'ouvrir dans un navigateur ; seuls les liens externes demandent une connexion. GitHub affiche le code, pas l'application.
- **[Lyon, une géographie intime](lyon_ensemble.svg)** : sélection éditoriale de vingt repères du centre.
- **[De Saxe à la Guillotière](lyon_guillotiere_saxe.svg)** : lecture rapprochée de la rue du Six-Janvier, du café des Alpes et de la place Antique, avec les lieux voisins.

## Lire les symboles

| Symbole | Signification |
|---|---|
| Étiquette pleine bleu foncé, arrondie (ou cercle) | Identification retenue (`atteste`) ; la preuve historique est dans la notice |
| Étiquette pleine ocre, carrée (ou losange) | Localisation probable : une inférence reste à contrôler |
| Étiquette blanche à bord rouille en tirets (ou cercle pointillé) | Hypothèse de travail |
| Halo, segment large ou surface translucide | Emprise du lieu ou marge de recherche ; jamais un numéro de voirie |
| Filet de couleur | Rue nommée par le roman |
| Point gris (planches) | Lieu d'une autre planche, pour se repérer |

L'étiquette est le code de la notice (G10, B02…) : elle renvoie au registre ([`04_Donnees/lieux.json`](../04_Donnees/lieux.json)) et à la [fiche du lieu](../03_Fiches/par_lieu/README.md). Les codes ne sont pas des numéros de rue. Un repère placé sur une ligne ou une surface est un renvoi graphique : sa position n'établit aucun bâtiment. Les degrés portent sur l'identification géographique, distincte de l'attestation de l'expression dans le roman. Les 16 lieux non localisés ne figurent sur aucune carte ; ils restent dans le registre et dans l'atlas autonome.

Trois cas méritent d'être lus avec leur notice :
- **Café des Alpes** (B02) : il est représenté par un tronçon de l'avenue de Saxe, celui que le texte désigne, **sans adresse prétendument retrouvée**.
- **Place Antique** (G01) : c'est une zone probable autour du carrefour des rues Gilbert-Dru, Saint-Michel et Béchevelin.
- **« Quai Perrache »** (P23) : le roman le décrit au bord de la Saône, avec Fourvière en face (XII §§166–168), alors que le quai officiel de ce nom longe le Rhône. La zone probable est l'ancien quai d'Occident ; le banc n'est pas localisé.

## Fond moderne et limites

Le fond de l'atlas autonome et des SVG est un **état moderne**, extrait d'OpenStreetMap le 23 octobre 2026. Les ponts, équipements, limites et voies peuvent être postérieurs au roman. Les noms de quartiers et de fleuves sont des étiquettes d'orientation ajoutées par l'enquête. Emprise de la vue générale : longitude 4,810–4,860 ; latitude 45,740–45,780 ; les lieux hors cadre restent dans l'index de l'atlas. Projection locale équirectangulaire, latitude de référence 45,76°, coordonnées d'entrée WGS84.

**Crédit obligatoire du fond : © les contributeurs OpenStreetMap.** Données sous [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/) ; [attribution et conditions](https://www.openstreetmap.org/copyright). Le fond simplifié, avec l'identifiant, la version et la date de chaque objet retenu, est conservé dans `../04_Donnees/fond_osm.geojson`. Les requêtes, leurs empreintes et les versions des trois relations d'eau figurent dans `fond_osm_provenance.json`. Les surfaces principales en eau proviennent des relations OSM 7317123 (Saône), 11696008 (Rhône) et 255155 (lac de la Tête-d'Or).

## Reproduire

Depuis la racine du dépôt :

```sh
python IdentificationsLieux/Lyon/06_Outils/generer_cartes.py       # SVG, atlas autonome, manifest_cartes.json
python IdentificationsLieux/Lyon/06_Outils/cartes_historiques.py   # PNG sur fonds IGN et atlas historique
```

Le premier script écrit dans `manifest_cartes.json` les empreintes SHA-256 de ses entrées et de ses sorties. Le second demande matplotlib, Pillow et shapely, et accepte l'option `--hors-ligne` lorsque les tuiles sont en cache.
