# Protocole philologique, historique et cartographique

## Question et périmètre

Quels lieux lyonnais structurent les rencontres, promenades, études, pratiques religieuses et sociabilités des personnages des *Deux Étendards* ? À quelle précision peut-on les restituer ?

Le centre de l'enquête est Lyon et sa proche périphérie. Le Beaujolais et les excursions lointaines sont conservés dans l'inventaire comme contexte, sans les confondre avec Lyon. Les mentions de Paris ne sont pas déplacées sur la carte lyonnaise à la faveur d'une homonymie.

« Principal » ne signifie pas seulement « fréquent ». Un lieu est principal s'il accueille une scène décisive, revient comme rendez-vous, organise les déplacements ou matérialise une opposition structurante. Les simples comparaisons, souvenirs et paysages aperçus restent distingués des lieux visités.

## Deux enquêtes, un registre

Le dossier réunit deux enquêtes conduites indépendamment sur le même témoin : l'une (23 octobre 2026) par dictionnaire lexical et dossiers thématiques ; l'autre par lecture intégrale, chapitre par chapitre, en dix tranches. La seconde a fourni les relevés par chapitre (`01_Corpus/releves_par_chapitre/`) et un répertoire de 110 lieux. Le 24 octobre 2026, chaque affirmation de la première enquête a été contre-vérifiée (journal du jour). Les deux répertoires ont ensuite été fusionnés dans un registre unique de 162 lieux, `04_Donnees/lieux.json`, qui conserve les identifiants de la première enquête et donne à chaque notice un code de secteur (G Guillotière, B 3e nord et Brotteaux, P Presqu'île, D rive droite de la Saône, E environs, R région).

Quand les deux enquêtes divergeaient, la notice retenue est celle que les pièces départagent ; à défaut, la plus prudente. Le désaccord est alors consigné dans la fiche.

## Trois preuves indépendantes

1. **Attestation textuelle** : forme exacte, contexte, chapitre, paragraphe de l'EPUB. Les variantes typographiques sont regroupées pour la recherche, mais pas silencieusement corrigées dans les citations.
2. **Identification historique** : source extérieure donnant une enseigne, une adresse, un changement de nom ou une date compatible avec la scène. Une notice actuelle peut établir la continuité d'un édifice ; elle ne prouve pas à elle seule l'existence d'un commerce en 1925.
3. **Localisation géographique** : point, segment ou zone correspondant à la précision réellement acquise. Les coordonnées sont des repères de lecture, jamais des relevés cadastraux.

Un résultat peut être certain sur le premier axe et ouvert sur le deuxième : c'est le cas du Café des Alpes. Le roman le situe avenue de Saxe (X §149), à un angle de cette avenue « un peu après le cours La Fayette », sur un trajet venu de la place Morand (XXII §§34–35). Il en décrit les tenanciers sans les nommer (« un ménage de grands et gros Savoyards », X §149 ; « le patron moustachu », XXII §196). Le lien entre ces Savoyards et l'enseigne n'est lui-même qu'une conjecture du narrateur (« d'où probablement l'enseigne »). Le texte ne donne ni le nom de l'exploitant ni le numéro.

## Vocabulaire de certitude

| Statut cartographique | Sens | Représentation adaptée |
|---|---|---|
| Identifié (`atteste`) | Concordance explicite du texte avec un lieu géographique identifiable | Point de repérage pour un édifice, un carrefour ou une place de petite emprise ; ligne pour une rue ; aire pour une grande place (Bellecour) ; point conventionnel avec halo pour un parc ou une colline |
| Probable (`probable`) | Plusieurs indices convergent, mais une pièce manque | Zone ou segment ; point seulement comme centre d'une zone signalée |
| Hypothèse (`hypothese`) | Proposition compatible, concurrents non éliminés | Segment ou aire large, avec commentaire des alternatives ; aucune géométrie si aucun secteur n'est défendable |
| Non localisé (`non_localise`) | Attestation textuelle sans localisation défendable | Liste hors carte, sans coordonnées fictives |

Ces statuts qualifient la **localisation proposée**. Ils ne certifient ni une équivalence biographique ni la matérialité de toutes les scènes. Un rayon de précision est une convention graphique prudente, pas un intervalle statistique calculé.

### Degré de certitude et statut cartographique

Le registre conserve, à côté du statut cartographique, le degré de certitude de la lecture intégrale. Ce degré porte sur l'identification du lieu réel, non sur la forme de la géométrie.

| Degré | Sens | Statut cartographique correspondant |
|---|---|---|
| A | identification certaine (nom réel explicite, lieu repérable) | `atteste` |
| B | très probable (faisceau d'indices convergents, aucun concurrent sérieux) | `probable` |
| C | probable (indices convergents, une pièce manque) | `probable` |
| D | hypothèse (proposition compatible, concurrents non éliminés) | `hypothese` |
| E | lieu inventé ou non localisable | `non_localise` (aucune coordonnée) |

La correspondance n'est pas mécanique dans les deux sens : un lieu certain (A) peut n'être cartographié que par un segment, si le roman donne la rue sans le numéro.

## Critique du texte

- Le corpus de travail est l'EPUB déjà fourni dans le dépôt. Il comporte des traces de conversion ; ce n'est pas un fac-similé d'une édition imprimée.
- Les numéros de paragraphes désignent les éléments HTML `p`, dans leur ordre à l'intérieur de chaque fichier XHTML. Ils sont reproductibles pour cette empreinte du corpus.
- Les pages des éditions imprimées ne sont pas inventées à partir des écrans d'une liseuse. Toute pagination trouvée dans la critique conserve la référence de son édition.
- Les noms affectifs sont analysés comme tels : « rue du Six-Janvier » et « Place Antique » sont des actes de nomination des personnages, non des noms de voies administratives à rechercher littéralement dans un annuaire.
- Une enseigne romanesque peut être exacte, transformée ou composite. Le patronyme des propriétaires, l'intérieur et la clientèle peuvent eux aussi être transposés.
- L'adjectif polémique ou impressionniste n'est pas un état des lieux architectural. Le jugement de Michel, celui d'un autre personnage et la voix narrative ne sont pas confondus.

## Deux numérotations, une référence

La référence est la numérotation P, définie ci-dessus : rang de l'élément `<p>` dans le fichier du chapitre, titres non comptés. La lecture intégrale avait d'abord numéroté les lignes non vides du texte extrait (numérotation L) : titre de chapitre compris, une ligne par `<p>`, par `<br/>` interne et par bloc. Ses relevés ont été convertis en P au moyen de la table `01_Corpus/concordance_numerotations.csv`, produite par `06_Outils/concordance_numerotations.py` (aucun texte du roman n'y figure). Les citations ont ensuite été recontrôlées contre le paragraphe P qui les suit. Une référence en L ne doit plus circuler.

## Critique historique

Le récit contient des repères internes explicites : Pâques 1920 (I §3), automne 1923 (II §1), 6 janvier 1925 (Notes §21), avril 1925 (X §227), 31 octobre 1925 (XXI §1), 1926 (XXIV §194) et 1927 dans le dernier chapitre (XXXVII §5). La chronologie relative place la nuit de Brouilly et la scène fondatrice du quai Perrache à la fin de septembre 1923 (III §51 ; XII §172 : « le 30 septembre »). Le noyau lyonnais va de l'automne 1924 (III) à l'été 1926 (XXXII–XXXIII, juillet). Le *Récit de Guitte* rapporte ensuite un retour du couple à Lyon, du 20 décembre 1926 à la rupture du début de 1927 (Récit de Guitte §§15–33), avant l'épilogue lyonnais de novembre 1927 (XXXVII §§1–6). Les vérifications d'établissements doivent donc couvrir 1923–1927, en priorité 1925–1926, et non un vague « Lyon ancien ».

Ces repères concordent avec la [biographie publiée par les *Études rebatiennes*](https://etudesrebatiennes.over-blog.com/pages/BIOGRAPHIE-1027913.html) (consultée le 24 octobre 2026) : nuit de Brouilly le 28 septembre 1923, première rencontre de Rebatet et de Simone Chevallier le 6 janvier 1925, noviciat de Varillon en novembre 1927. Cette concordance ne vaut pas preuve topographique.

Les contrôles suivent cet ordre :

1. relever toutes les contraintes du passage, y compris le sens de marche et le lieu de départ ;
2. retrouver la voie dans le fichier historique des rues et les plans de la période ;
3. chercher l'établissement dans les indicateurs Henry/Fournier, par rue, profession et patronyme ;
4. recouper avec presse, publicité, registre du commerce, permis de construire, carte postale ou recensement ;
5. vérifier que l'établissement et la numérotation existaient à la date de la scène.

La BmL (Guichet du Savoir, réponse du 18 mars 2026) indique que les indicateurs Henry et Fournier ne sont pas numérisés, hormis quelques exemplaires sur Google Livres ou Numelyo. Sa collection, lacunaire (1896–1972), se consulte sur place, à la banque du Silo ; d'autres exemplaires sont conservés aux Archives municipales et aux Archives départementales du Rhône. L'édition 1926 fait partie des volumes dépouillés par le Guichet pour cette réponse. Les annuaires **non consultés** demeurent des pièces à demander, et non des preuves déjà acquises. Un échec de recherche web ne démontre pas l'inexistence d'un café.

## Sources extérieures et témoignages

Le roman est un roman à clef : Michel Croz doit beaucoup à Lucien Rebatet, Régis Lanthelme à François Varillon, Anne-Marie Villars à Simone Chevallier. Les témoignages autobiographiques, les biographies et les archives nominatives peuvent donc éclairer les lieux. Ils ne prouvent pourtant jamais à eux seuls la topographie du roman : un romancier déplace, compose et déguise. Chaque témoignage est qualifié :

- **primaire contemporain** : document de l'époque (lettre de 1925, recensement de 1926, annuaire) ;
- **primaire tardif** : souvenir de l'intéressé publié des décennies plus tard (mémoires, entretiens) ;
- **secondaire documenté** : biographie ou étude qui cite ses pièces ;
- **secondaire non sourcé** : affirmation sans pièce (notice en ligne, article de presse).

Une concordance entre le roman et la biographie (même rue, même établissement) renforce une identification ; elle ne transforme pas un surnom des personnages en toponyme. Une discordance n'invalide pas le roman : elle signale une transposition, à décrire comme telle. Les mentions de personnes réelles se limitent à ce que les sources publiées établissent.

Les archives nominatives (listes nominatives des recensements de 1911 à 1936, Archives départementales du Rhône, série 6 M) sont lues en deux temps. Un premier lecteur parcourt les vues d'une rue, transcrit chaque ménage retenu avec sa cote, sa vue et sa page, et signale ses lectures incertaines. Un second relit ensuite les mêmes images sans connaître la conclusion attendue. Une trouvaille n'entre dans le dossier qu'avec sa cote et son image. Les homonymes écartés sont mentionnés sans autre détail que ce qui justifie l'exclusion.

## Cartes

Les cartes livrées sont des **cartes d'enquête contemporaines sur des lieux du récit**. Le fond moderne sert à se repérer ; il ne reconstitue pas la voirie, les berges, les ponts et les bâtiments de 1925. La source du fond et sa date sont documentées avec les cartes.

Les noms contemporains sont explicités lorsqu'ils aident à retrouver une voie ancienne. Les itinéraires supposés ne sont pas dessinés comme des trajets attestés. Une ligne indiquant un secteur de recherche ne signifie pas que les personnages ont suivi tout ce segment.

### Itinéraires reconstitués

Les itinéraires (`04_Donnees/itineraires.yaml`) ne retiennent comme étapes que des lieux nommés ou désignés sans ambiguïté par le texte, avec leur référence. Entre deux étapes, le tracé est le plus court chemin sur la voirie actuelle (`06_Outils/itineraires.py`). C'est une reconstitution graphique : le roman nomme rarement les rues suivies. Une étape dont la localisation est discutée est marquée « à confirmer ».


### Fonds historiques

Les cartes sur fonds historiques (`06_Outils/cartes_historiques.py`) emploient la carte IGN de 1950 et les photographies aériennes de 1950-1965 (Géoplateforme, Licence ouverte Etalab 2.0). Ces fonds sont plus proches de 1925 qu'un plan actuel, mais postérieurs d'une génération : les ponts du Rhône détruits en 1944 y apparaissent reconstruits, et plusieurs îlots de la Guillotière ont changé. Ils situent, ils ne restituent pas.

## Reproductibilité et révision

Les données séparent inventaire des mentions et sélection cartographiée. Les scripts conservent une empreinte SHA-256 du corpus ; les références du dictionnaire sont contrôlées contre le texte. Les résultats restent révisables au moyen d'une pièce contraire identifiée, datée et décrite. Le journal consigne les recherches négatives, les limites et les pièces manquantes.

## Instruments de recherche

- [Archives de Lyon : plans parcellaires, 1861–1995](https://www.archives-lyon.fr/documents-remarquables/rechercher-dans-les-plans-parcellaires-1861-1995).
- [Archives de Lyon : cartes et plans](https://recherches.archives-lyon.fr/page/cartes-et-plans).
- [BmL, Guichet du Savoir, 18 mars 2026 : indicateurs Henry et Fournier](https://www.guichetdusavoir.org/question/voir/140159) ; consultation sur place à la BmL (banque du Silo), aux Archives de Lyon et aux Archives départementales du Rhône.
- [Archives de Lyon : anciens noms de voies](https://www.archives-lyon.fr/sites/aml/files/2021-03/voies_anciennes.pdf) : dénominations anciennes et dates de changement (par exemple rue de la Vierge, devenue rue Gilbert-Dru en 1945).
- Archives départementales du Rhône : recensements de population, notamment celui de 1926, interrogeable par adresse. Exemple d'usage : [BmL, Guichet du Savoir, 1er septembre 2015 : Simone Chevallier](https://www.guichetdusavoir.org/question/voir/51150) (cours Gambetta, p. 8 du recensement de 1926).

Consultation : 23 octobre 2026 ; 24 octobre 2026 pour les deux derniers liens.

*Révisé le 24 octobre 2026 après contre-vérification : voir [07_Journal/2026-10-24.md](../07_Journal/2026-10-24.md).*
