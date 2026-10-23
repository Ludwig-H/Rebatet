# Lyon dans *Les Deux Étendards*

## Une enquête philologique et historique, avec atlas critique

**État du 23 octobre 2026.** Le dépouillement du roman fourni dans ce dépôt réunit **132 entrées de travail**, dont **54 principales**, et **855 références lexicales contrôlées**. Un registre cartographique de **51 notices** développe les identifications et les questions ouvertes ; **35** disposent d'une géométrie, les autres restent volontairement sans emplacement. Ces nombres comptent des objets de natures différentes et parfois imbriqués : ils ne signifient pas que 132 bâtiments historiques ont été retrouvés.

**Pour commencer :** [carte générale](05_Cartes/lyon_ensemble.svg), [zoom Saxe–Guillotière](05_Cartes/lyon_guillotiere_saxe.svg), puis [atlas interactif](05_Cartes/atlas_lyon.html). Télécharger l'HTML et l'ouvrir dans un navigateur pour utiliser recherche, filtres et notices ; GitHub en affiche le code. Les trois cartes fonctionnent sans service de cartes externe.

![Lyon, une géographie intime](05_Cartes/lyon_ensemble.svg)

## Les résultats qui changent la lecture

| Lieu du roman | Résultat de l'enquête | Certitude et réserve |
|---|---|---|
| **Café des Alpes** | C'est la forme lue dans le roman, et non « Café des Deux Alpes ». Avenue de Saxe explicitement donnée ; la filature du chapitre XXII oriente vers le sud du cours Lafayette. | Avenue certaine dans le texte ; secteur probable ; **aucun numéro historique démontré**. [Dossier](03_Fiches/01_cafe_des_alpes.md) |
| **Rue du Six-Janvier** | Carrefour Créqui/Rabelais, expressément nommé XII §124 ; souvenir du 6 janvier 1925. | Carrefour certain ; trottoir et réverbère exacts inconnus. Nom privé, pas ancienne rue administrative. [Dossier](03_Fiches/02_toponymes_et_adresses.md) |
| **Place Antique** | Carrefour probable de Saint-Michel et de l'ancienne rue de la Vierge, actuelle Gilbert-Dru. La présence d'une école achevée en 1924 recoupe l'école neuve du texte. | Faisceau d'indices fort ; zone probable, sans bâtisse précisément identifiée. [Dossier](03_Fiches/02_toponymes_et_adresses.md) |
| **Banc du « quai Perrache »** | Le paysage décrit la Saône, Fourvière, un pont ferroviaire et un tunnel ; il ne correspond pas au quai Perrache actuel sur le Rhône. | Discordance conservée. Hypothèse Rambaud–Tilsitt/Quarantaine discutée ; **banc non placé**. [Dossier](03_Fiches/02_toponymes_et_adresses.md) |
| **Lugdunum, Brazier, Grand Théâtre, Rameau, Maison Dorée, Cintra, Carlton** | Bâtiments ou établissements identifiables, avec contrôles de chronologie et de transformations. | Distinguer date du bâtiment, ouverture de l'exploitation et état actuel. [Dossiers](03_Fiches/03_etablissements.md) |
| **Bibliothèque au pied de Saint-Jean** | Ancien palais archiépiscopal, où se trouve la bibliothèque centrale en 1912–1972. | Ne pas la déplacer à la Part-Dieu. [Analyse](03_Fiches/04_geographie_critique.md) |
| **Cercle de Rollet** | Rapprochement avec la Maison des étudiants catholiques, ancien Hôtel de la Chanson, 4 rue Montesquieu ; convergence institutionnelle et nom de Jean Roullet. | Modèle probable, pas identité parfaite démontrée. [Dossier](03_Fiches/05_religieux_et_enseignement.md) |
| **Morel et Royal** | Morel à l'angle Bellecour/rue de l'Hôtel-de-Ville ; Royal probablement au 50 rue de la République. | Publicités datées de 1884 et 1929 respectivement : continuité au temps de l'action à recouper. [Dossier](03_Fiches/04_cafes_morel_royal.md) |

![Saxe et Guillotière](05_Cartes/lyon_guillotiere_saxe.svg)

## Comment lire ces cartes

Le fond est **moderne** et explicitement crédité. Il permet de retrouver les lieux ; il ne reconstitue pas Lyon en 1925. Les couleurs distinguent identification, probabilité et hypothèse. Les halos et segments expriment une emprise ou une marge de recherche, pas une adresse. Les cartes statiques présentent une sélection ; l'atlas contient les 51 notices du registre, y compris les lieux hors cadre ou non placés.

Les coordonnées des édifices identifiés sont des repères de lecture. Ni la précision des décimales ni un résultat de géocodage n'établissent une parcelle historique. La forme de l'incertitude est conservée dans le [GeoJSON](04_Donnees/lieux.geojson).

## Architecture de l'enquête

| Dossier | Contenu |
|---|---|
| [00_Methode](00_Methode/PROTOCOLE.md) | Critères de preuve, niveaux de certitude, limites et protocole d'archives |
| [01_Corpus](01_Corpus/NOTICE.md) | Témoin EPUB, empreinte, convention de paragraphes ; [inventaire complet](01_Corpus/INVENTAIRE.md) |
| [02_Sources](02_Sources/BIBLIOGRAPHIE.md) | Sources institutionnelles, presse, critique, ouvrages repérés mais non consultés |
| [03_Fiches](03_Fiches/) | Démonstrations, alternatives, objections, lecture littéraire et pièces à chercher |
| [04_Donnees](04_Donnees/README.md) | Concordances JSON, registre, GeoJSON, tableau CSV et provenance géographique |
| [05_Cartes](05_Cartes/README.md) | Deux cartes vectorielles et atlas HTML autonome |
| [06_Outils](06_Outils/) | Contrôle du corpus, export des données, génération des cartes sans réseau |
| [07_Journal](07_Journal/2026-10-23.md) | Recherches négatives, limites d'accès, priorités documentaires et contrôle technique |

## Portée critique

L'enquête distingue le **texte**, l'**histoire du lieu** et la **géographie actuelle**. Elle écarte plusieurs faux amis : la rue de Fleurus et le Marivaux des passages concernés sont parisiens ; la Chauve-Souris est une personne ; le cours Boudier est un enseignement ; un quai ferroviaire n'est pas un quai urbain.

Le récit est traité comme une construction littéraire. Ses noms intimes, détours, impressions nocturnes et jugements sur les lieux ne deviennent pas automatiquement des données cadastrales. La [lecture critique de la géographie](03_Fiches/04_geographie_critique.md) montre pourquoi une école neuve ou une rue de traverse peut être un meilleur indice qu'une évocation pittoresque.

Le dépouillement ne constitue pas encore une collation exhaustive avec une édition imprimée. Il n'existe pas ici de preuve suffisante pour le numéro du Café des Alpes, Modern House, les logis privés ou plusieurs guinguettes. Les annuaires Henry/Fournier des années concernées ne sont pas intégralement accessibles en ligne : ils sont **à consulter**, et non présentés comme déjà dépouillés. La bibliographie signale notamment l'étude de Pascal A. Ifri de 1997 consacrée au Lyon du roman, dont le texte intégral reste à obtenir.

## Reproduire les contrôles

Depuis la racine du dépôt, Python 3.10 ou ultérieur, sans dépendance à installer :

```sh
python IdentificationsLieux/Lyon/06_Outils/verifier_dossier.py
python IdentificationsLieux/Lyon/06_Outils/exporter_donnees.py
python IdentificationsLieux/Lyon/06_Outils/generer_cartes.py
```

Le contrôle vérifie l'empreinte du témoin, l'existence des références retenues, les correspondances lexicales, les comptes, les liens de fiches et les géométries. Il ne remplace pas le jugement philologique ni la vérification des archives. Les cartes conservent les empreintes de leurs entrées et sorties dans leur manifeste.
