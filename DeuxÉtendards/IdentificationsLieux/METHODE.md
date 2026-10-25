# Méthode

## Question et périmètre

L'enquête cherche quels lieux lyonnais structurent les rencontres, les promenades, les études, la vie religieuse et les sociabilités des personnages, et avec quelle précision on peut les restituer. Elle porte sur Lyon et sa proche périphérie. Le Beaujolais et les excursions sont gardés comme contexte, dans les secteurs E et R. Une mention parisienne n'est jamais reportée sur Lyon à la faveur d'une homonymie.

Un lieu est *principal* s'il remplit au moins l'une de ces fonctions : accueillir une scène décisive, revenir comme rendez-vous, organiser les déplacements ou matérialiser une opposition. Les comparaisons, les souvenirs et les paysages aperçus restent distingués des lieux visités.

## Le témoin et la convention de référence

Le témoin est le fichier [`../Les deux étendards (Lucien Rebatet).epub`](<../Les deux étendards (Lucien Rebatet).epub>). Son empreinte SHA-256, contrôlée par `outils/verifier.py`, est `88daa208cc3eeca363f33ddfbf1be4e3bec83a0c0d5ab407d0c1aa34ae7e6e18`.

Ses métadonnées portent l'ISBN 978-2-07-072467-3. C'est celui de l'édition Gallimard en un volume de 1991 (1312 p.). Comme ces métadonnées sont passées par Calibre, elles orientent vers ce texte sans prouver que l'EPUB le reproduit. Le fichier n'est pas un fac-similé : il garde des traces de conversion, et il lui manque l'avertissement liminaire de l'édition originale (voir [SOURCES](SOURCES.md)).

**Convention P.** « XII §124 » désigne le 124e élément `<p>` du fichier XHTML du chapitre XII, sans compter les titres. Trois parties hors chapitres ont leur propre nom : *Intermèdes*, *Récit de Guitte* et *Notes*, ces dernières étant les notes de l'auteur. Pour cette empreinte, les numéros sont reproductibles.

On ne déduit aucune pagination imprimée d'un écran de liseuse. Une pagination tirée de la critique garde la référence de son édition. Pour lire ou chercher dans le témoin : `python3 outils/corpus.py show XII 124 126` et `python3 outils/corpus.py grep "rue de Jarente"`.

## Trois preuves indépendantes

1. **Attestation textuelle** : forme exacte, contexte, chapitre et paragraphe. Les variantes typographiques sont regroupées pour la recherche, mais elles ne sont pas corrigées dans les citations.
2. **Identification historique** : une source extérieure qui donne une enseigne, une adresse, un changement de nom ou une date compatible avec la scène. Une notice actuelle établit la continuité d'un édifice ; elle ne prouve pas l'existence d'un commerce en 1925.
3. **Localisation géographique** : un point, un segment ou une zone, selon la précision réellement acquise. Ce sont des repères de lecture, jamais des relevés cadastraux.

Un lieu peut être certain sur le premier plan et ouvert sur le deuxième. C'est le cas du café des Alpes. Le texte le place avenue de Saxe, à un angle situé « un peu après le cours La Fayette » (X §149 ; XXII §34-35). Il ne donne ni l'exploitant ni le numéro.

## Statuts et degrés de certitude

| Statut | Certitude | Sens | Représentation |
|---|---|---|---|
| identifié (`atteste`) | A | Le texte concorde explicitement avec un lieu repérable. | Point pour un édifice, un carrefour ou une petite place ; ligne pour une rue ; aire pour une grande place ; point avec halo pour un parc ou une colline. |
| probable (`probable`) | B ou C | B : faisceau d'indices convergents, sans concurrent sérieux. C : indices convergents, mais une pièce manque. | Zone ou segment. Un point n'est que le centre d'une zone signalée. |
| hypothèse (`hypothese`) | D | La proposition est compatible, mais ses concurrents ne sont pas éliminés. | Segment ou aire large. Aucune géométrie si aucun secteur n'est défendable. |
| non localisé (`non_localise`) | E | Le lieu est attesté sans localisation défendable, ou il est inventé. | Hors carte, sans coordonnées fictives. |

Le statut qualifie la localisation proposée. La certitude qualifie l'identification du lieu réel. La correspondance entre les deux n'est pas mécanique : un lieu certain (A) peut n'être tracé que par un segment si le roman donne la rue sans numéro.

**Règle des voies.** Un lieu situé sur une voie nommée, sans immeuble identifié, est `atteste` pour la voie. Sa certitude mesure alors sa restriction au tronçon ou au point retenu. Sept notices relèvent de cette règle : B02, B09, B12, G32 et G42 (certitude B), G06 et G33 (certitude C).

Le rayon de précision (`precision_m`) est une convention graphique prudente, non un intervalle statistique.

## Critique du texte

- Les noms affectifs, comme « rue du Six-Janvier » ou « place Antique », sont des actes de nomination des personnages. On ne les cherche pas comme des noms de voies dans un annuaire.
- Une enseigne romanesque peut être exacte, transformée ou composite. Les patronymes, les intérieurs et les clientèles peuvent aussi être transposés.
- Un adjectif polémique ne décrit pas l'état d'un lieu. On distingue le jugement de Michel, celui d'un autre personnage et la voix du narrateur.

## Critique historique

Le récit donne ses propres repères chronologiques :

| Repère | Référence |
|---|---|
| Pâques 1920 | I §3 |
| automne 1923 | II §1 |
| 6 janvier 1925 | Notes §21 |
| avril 1925 | X §227 |
| 31 octobre 1925 | XXI §1 |
| 1926 | XXIV §194 |
| 1927 | XXXVII §5 |

La nuit de Brouilly et la scène du quai Perrache tombent à la fin de septembre 1923 (III §51 ; XII §172). Le noyau lyonnais va de l'automne 1924 (III) à l'été 1926 (XXXII-XXXIII). Le *Récit de Guitte* rapporte ensuite un retour à Lyon, du 20 décembre 1926 au début de 1927. L'épilogue se situe en novembre 1927 (XXXVII §1-6). Les établissements sont donc vérifiés pour la période 1923-1927, en priorité pour 1925-1926.

Ces repères concordent avec la biographie publiée par les *Études rebatiennes* : nuit de Brouilly le 28 septembre 1923, rencontre du 6 janvier 1925, noviciat de Varillon en novembre 1927. Cette concordance ne vaut pas preuve topographique.

Les contrôles suivent cet ordre :

1. Relever toutes les contraintes du passage, y compris le sens de marche et le point de départ.
2. Retrouver la voie dans la liste des voies anciennes et sur les plans de la période.
3. Chercher l'établissement dans les indicateurs Henry et Fournier, par rue, profession et patronyme.
4. Recouper avec la presse, la publicité, le registre du commerce, les permis de construire, les cartes postales et les recensements.
5. Vérifier que l'établissement et la numérotation existaient à la date de la scène.

Les indicateurs Henry et Fournier ne sont pas numérisés (BmL, Guichet du Savoir, 18 mars 2026). Les volumes non consultés restent des pièces à demander. Un échec de recherche sur le web ne prouve pas qu'un café n'a pas existé.

## Témoignages et archives

Le roman est à clef. Michel Croz doit beaucoup à Rebatet, Régis Lanthelme à François Varillon, Anne-Marie Villars à Simone Chevallier. Les témoignages, les biographies et les archives nominatives éclairent le modèle d'un lieu. Ils ne prouvent jamais à eux seuls la topographie du roman.

Chaque témoignage est qualifié selon quatre degrés :

- **primaire contemporain** : document de l'époque (recensement, acte, annuaire) ;
- **primaire tardif** : souvenir publié des années plus tard ;
- **secondaire documenté** : étude qui cite ses pièces ;
- **secondaire non sourcé** : affirmation sans pièce.

Une concordance entre le roman et un témoignage renforce une identification, mais elle ne transforme pas un surnom en toponyme. Une discordance signale une transposition.

Les listes nominatives des recensements (Archives du Rhône, série 6 M, 1906-1936) et l'état civil (série 4E) sont lus en deux temps :

1. Un premier lecteur transcrit chaque ménage retenu, avec sa cote, sa vue et sa page.
2. Un second relit les mêmes images sans connaître la conclusion attendue.

Une trouvaille n'entre au registre qu'avec sa cote et son image. Les personnes réelles ne sont citées que dans les limites de ce qu'établissent les sources publiées et les archives. Un voisin n'est nommé que s'il prouve la continuité d'une maison.

## Cartes et itinéraires

Les cartes sont des cartes d'enquête. Elles reposent sur la carte IGN de 1950 (SCAN 50) et sur les photographies aériennes de 1950-1965, diffusées par la Géoplateforme sous Licence ouverte Etalab 2.0. L'atlas ajoute la carte d'état-major (1820-1866) et un fond OpenStreetMap. Ces fonds situent les lieux ; ils ne restituent pas la ville de 1925.

Chaque repère porte le code de sa notice. Pour chaque géométrie, le registre note la méthode de géoréférencement : point d'adresse de la Base Adresse Nationale, objet OpenStreetMap ou plan parcellaire.

Les itinéraires (`donnees/itineraires.yaml`) ne retiennent comme étapes que des lieux nommés ou désignés par le texte, chacun avec sa référence. Des points de passage (« via » : ponts, angles, quais nommés) orientent le tracé. Entre deux étapes, le tracé suit le plus court chemin sur la voirie actuelle, calculé par `outils/itineraires.py` sur `donnees/fond_osm.geojson`. C'est une reconstitution graphique : elle ne donne pas les rues réellement suivies, que le roman nomme rarement.

## Données

Chaque notice du registre `donnees/lieux.json` comporte les champs suivants :

| Champ | Contenu |
|---|---|
| `id`, `code` | Identifiant stable et code de secteur : G Guillotière, B 3e nord et Brotteaux, P Presqu'île, D rive droite de la Saône, E environs, R région. |
| `nom`, `categorie`, `statut_nom` | Nom de la notice, type de lieu, nature du nom : réel, surnom, déguisé, fictif ou implicite. |
| `statut`, `certitude` | Voir plus haut. |
| `geometry`, `precision_m`, `georeferencement` | Géométrie GeoJSON en WGS84 (point, ligne, polygone, ou `null`), marge en mètres, méthode de géoréférencement. |
| `nom_1925`, `nom_actuel` | Nom vers 1925 et nom actuel. |
| `description`, `identification`, `cle`, `arguments` | Lecture du lieu, identification, citation-clé courte, raisonnement. |
| `refs`, `motifs` | Passages du roman (convention P) ; expressions régulières qui repèrent les occurrences (« CS: » marque un motif sensible à la casse). |
| `sources`, `temoignages` | Sources ; témoignages et archives, avec leur degré. |
| `fiche` | Dossier thématique qui discute le lieu, s'il y en a un. |

Le fichier `donnees/inventaire.json` est l'inventaire lexical. Ses 132 entrées donnent chacune :

- une expression régulière ;
- un classement : principal, secondaire, extérieur ou exclu ;
- les références au paragraphe et le nombre de correspondances ;
- les exclusions de contexte.

Les fichiers `lieux.geojson` et `itineraires.geojson` sont produits par les scripts.

## Contrôles

`outils/verifier.py` effectue ses contrôles sans accès au réseau. Il vérifie :

- l'empreinte du témoin ;
- chaque référence de l'inventaire, avec son paragraphe et son nombre de correspondances ;
- chaque renvoi « chapitre § » du registre ;
- les statuts et les géométries ;
- les liens relatifs et les ancres des fichiers Markdown.

Ces contrôles ne remplacent ni le jugement philologique ni la lecture des archives.

Le registre réunit deux enquêtes indépendantes, conduites sur le même témoin. La première s'appuie sur un dictionnaire lexical et des dossiers thématiques. La seconde procède par lecture intégrale, en dix tranches. Chaque affirmation contrôlable de la première a été contre-vérifiée : 634 en tout, dont 24 sont restées invérifiables. Les deux répertoires ont ensuite été confrontés secteur par secteur, puis fusionnés. En cas de désaccord, la notice retenue est celle que les pièces départagent ; à défaut, c'est la plus prudente.

Les pièces de travail ne figurent plus dans le dossier : relevés par chapitre, journaux de recherche, fiches individuelles, table de concordance avec l'ancienne numérotation par lignes. On les retrouve dans l'historique git, au commit `90e178d` (répertoire `IdentificationsLieux/Lyon/`).

Les résultats restent révisables au vu d'une pièce contraire, identifiée, datée et décrite.
