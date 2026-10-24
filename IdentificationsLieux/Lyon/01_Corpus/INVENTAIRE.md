# Inventaire de travail des lieux lyonnais dans le corpus EPUB

État du 23 octobre 2026. Dépouillement lexical contrôlé et classement narratif, préparatoire aux identifications historiques.

## Source et convention de référence

- Corpus fourni dans le dépôt : `DeuxÉtendards/Les deux étendards (Lucien Rebatet).epub`.
- SHA-256 : `88daa208cc3eeca363f33ddfbf1be4e3bec83a0c0d5ab407d0c1aa34ae7e6e18`.
- Extraction de 8 001 paragraphes non vides. Le numéro § compte tous les éléments HTML `p` du fichier XHTML, y compris les paragraphes vides, puis seuls les paragraphes non vides sont conservés. Il faut donc utiliser le même fichier et la même procédure, non renuméroter le texte affiché.
- Exemple : `X_christ_est_ressuscite.xhtml`, §149. Cette référence est vérifiable dans cet EPUB ; ce n’est pas une pagination de l’édition imprimée.

## Étendue et limites

**132 entrées de travail**, dont 54 classées principales, 69 secondaires, 6 extérieures au périmètre central et 3 exclusions parisiennes. Il ne s’agit ni de 132 bâtiments distincts, ni de 132 identifications historiques acquises : une place, son quartier, un café et une voie peuvent se recouvrir. Le choix « principal » indique un rôle narratif ou une articulation spatiale, non un seuil de fréquence.

Le JSON conserve le motif Python, les références de toutes les correspondances retenues, le nombre de correspondances et de paragraphes. Les références sont triées selon l’ordre de lecture (`spine`) de l’EPUB. Les notes annexées sont isolées dans `paratext_refs` et exclues des comptes narratifs. Les décomptes sont ceux de la formule recherchée, pas toujours ceux de toutes les reprises du lieu. Par exemple, le motif « café des Alpes » ne prétend pas compter chaque « Alpes » elliptique : une recherche globale capterait aussi le massif montagneux. Une concordance manuelle complémentaire `alias_audit_refs`, contrôlée avec le dossier Café des Alpes, retient 25 paragraphes nommant le café ou utilisant une ellipse, dont deux évocations depuis la Savoie (XVIII §101,119). Les `context_refs` signalent des passages utiles qui ne satisfont pas le motif et ne gonflent pas son compte.

Le champ `narrative_mode` indique l’usage dominant de l’entrée : il ne classe pas automatiquement chaque occurrence comme une visite. Les souvenirs peuvent être aussi nombreux que les scènes. Le dépouillement croise les désignations de voies et d’établissements, les noms propres, puis les contextes. Il couvre les principaux pôles urbains et de nombreuses mentions secondaires. Une relecture suivie reste nécessaire pour les lieux sans nom, les pronoms et les transitions implicites. Ne pas publier une garantie d’exhaustivité absolue.

## Conclusions textuelles solides

1. **Café des Alpes**, non « café des Deux Alpes », au chapitre X §149 : avenue de Saxe, tenue par un couple savoyard, salle de sociétés. Au chapitre XXII §34-35, le couple part de la grande porte du cours Boudier, près de la place Morand, passe le cours La Fayette, oblique à droite et « s’arrêta à l’angle de l’avenue de Saxe, au café des Alpes ». Le café occupe donc un angle de l’avenue de Saxe, un peu au-delà du cours La Fayette en venant de la place Morand. Aucun numéro n’est donné.
2. **Rue du Six-Janvier** est une désignation affective. Le chapitre XII §124 situe le lieu de pèlerinage à l’angle des rues Créqui et Rabelais. Conserver la distinction entre surnom intime et dénomination administrative.
3. **Place Antique** est un nom textuel extrêmement récurrent et, comme « rue du Six-Janvier », un surnom privé : il vient de l’épithète de Michel, « cette antique place » (VI §8), adoptée par le couple (IX §84). Aucune dénomination administrative n’est donc à chercher. La place apparaît sans nom dès IV §116-118, « à moins de deux cents pas des artères bourgeoises de la Guillotière ». Elle se situe par IX §84 (cinquante mètres de la rue de Marseille, deux cents de chez Régis, trois cents de chez Anne-Marie), IX §85 (école neuve, lanterne), XXIII §228 (« la petite rue Saint-Michel ») et XIX §133 (chambre de Michel « à deux cents pas »). Sa correspondance réelle doit être démontrée par ces trajets et par les archives.
4. **Café des femmes** est expressément un surnom donné par Michel et Anne-Marie (XXV §2) ; la devanture jaune est un peu en retrait avenue Jean-Jaurès (XXV §1). Le numéro « 257 » du même paragraphe qualifie une concierge parmi plusieurs silhouettes du quartier : il n’est pas présenté comme l’adresse du café.
5. **Cours Boudier** désigne un enseignement privé et son établissement ; ce n’est pas automatiquement une voie. Le même mot « cours » a ailleurs le sens d’artère (Gambetta, Lafayette, etc.).
6. **Rue Créqui** désigne le lieu de rencontre ; aucune adresse de domicile ne découle de ce seul toponyme. La porte des **Lanthelme** donne sur le cours Gambetta lui-même, où Anne-Marie et Régis habitent « à deux cents mètres l’un de l’autre » (Notes §11, note appelée en XIX §133 ; « mon cours Gambetta », XI §24). On passe devant elle « sous la mesquine marquise du bazar des « Galeries Modernes » », et Régis y dit « nous sommes en bas de ma chambre » (XXXVII §160-161). Le circuit de XXXVII §150 (la porte, « l’avenue » traversée, le tour du pâté « derrière l’Eldorado », l’angle de la place du Pont) la place sur le trottoir opposé à ce pâté : c’est une inférence. Aucun numéro n’est donné.
7. **Vinatier** est un secteur d’excursion et de guinguette (XXII §86 ; XXVI §140). « Chez Carreau » n’est pas situé dans l’hôpital par le texte.
8. **Brouilly, Claveisolles et Mongré** sont essentiels à l’action et aux souvenirs, mais appellent une carte régionale distincte du Lyon central.

## Principaux pièges écartés

- **Rue de Fleurus** : Paris, explicitement près du Luxembourg et du collège Bouhours (III §72,78).
- **Cinéma Marivaux** : passage parisien (XIV §201), non cinéma lyonnais établi.
- **Petite-Chaumière** : séquence parisienne du chapitre XIV.
- **Chauve-Souris** : surnom d’une femme, pas un cabaret à pointer.
- **Royal** : l’adjectif, Port-Royal et Palais-Royal sont exclus du compte de l’établissement lyonnais.
- **Bourse** : les emplois désignant argent personnel, spéculation ou Paris sont exclus ; seuls quatre passages lyonnais pertinents sont retenus.
- **Quai Perrache** : IV §7 désigne le quai de gare, retiré du compte du quai urbain ; XII §172 expose la confusion puis sa résolution.
- **Institut catholique** : I §51 concerne Paris et est retiré du compte lyonnais.
- **Charité** : seuls les quatre emplois du nom de l’édifice avec majuscule sont retenus ; la vertu théologale et les ventes de charité sont exclues.
- **Saint-Sacrement** : l’exposition liturgique XVI §50 est exclue de la fiche d’église.
- **Eldorado** : la métaphore VII §71 est exclue de la fiche du théâtre.
- **Briguais / Brignais** : deux occurrences `Briguais` XV §265,271 entourent des occurrences `Brignais`. Conserver la variante et vérifier sur édition imprimée ; ne pas créer deux communes. Le motif est sensible à la casse : XVI §3 (« des emplois que je briguais », verbe briguer) est exclu ; restent 9 occurrences.
- Les **marronniers** de l’air des Noces (VIII §213-214), les noms de compositeurs, le « 257 » de la concierge (XXV §1), la chambre d’hôtel « 348 » (ch. XXXIII, §272) et les comparaisons architecturales ne constituent pas des adresses lyonnaises. Le roman ne donne que deux adresses numérotées : 13 rue de Jarente (XI §98) et 3 bis cours Gambetta (XXIX §106).

## Dossiers supplémentaires de lieux anonymes ou privés

| Lieu | Références de départ | Ce que le texte autorise |
|---|---|---|
| Chapelle des Essarts | XXII §210 | Rendez-vous relaté, identification historique à établir. |
| Domicile Villars | XXIX §69, 75, 106, 112 ; XII §202-203 ; XXII §175 ; XXXI §50 ; XXXII §67, 81 ; Notes §11 | Adresse donnée par le texte : « au 3 bis du Cours Gambetta » (XXIX §106 ; « devant le 3 bis », §112). Michel y entre pour déjeuner, invité par Mme Villars (XXIX §69, 75). Immeuble d’angle probable : la chambre et le salon d’Anne-Marie donnent sur une « petite rue » (XII §202 ; XXXI §50), « la première petite rue » après la brasserie de l’Étoile, « à l’entrée du cours Gambetta » (XXII §175). Balcon de la salle à manger et brasserie à violons voisine (XXXII §81). Numérotation de 1925 à contrôler (annuaire Henry ; recensement de 1926). Au recensement de 1926, Simone Chevallier, modèle d’Anne-Marie, réside cours Gambetta ; la réponse publiée ne donne pas de numéro ([Guichet du Savoir BmL, q. 51150](https://www.guichetdusavoir.org/question/voir/51150), consulté le 24 octobre 2026). |
| Domicile Lanthelme | Notes §11 ; I §95, 127 ; XI §24 ; XXI §54 ; XXVII §20-21 ; XXXVII §150, 160-161 | Appartement familial sur le cours Gambetta, à « deux cents mètres » des Villars (Notes §11) ; salle à manger à balcon sur le cours (I §95). Porte sous la marquise du bazar des « Galeries Modernes », « en bas de ma chambre » (XXXVII §160-161). Trottoir opposé au pâté de l’Eldorado, vers la place du Pont : inférence tirée de §150. Aucun numéro ; enseigne du bazar à chercher dans l’annuaire Henry. Concordance extérieure : les parents de Varillon, modèle de Régis, « habitaient cours Gambetta » (Varillon, *Beauté du monde et souffrance des hommes*, 1980 ; [Ifri 2001](https://archive.org/details/lesdeuxetendards0000ifri), extraits plein texte consultés le 24 octobre 2026). |
| Logement chez Mme Mulet | XIX §133, 157 ; XXI §87 ; XXV §147, 177 ; Notes §11 | « Petite chambre » (XIX §133), puis « chambrette » (XXV §177), avenue Jean-Jaurès, « en pleine Guillotière, à deux cents pas de la « place Antique » », chez un conducteur d’imprimerie du Progrès de Lyon (XIX §133). La note de l’auteur appelée sur « avenue Jean-Jaurès » dit : « Avenue populaire, relativement décente » (Notes §11). Logeuse nommée en XIX §157 ; Michel quitte l’avenue en XXV (§147, 177). Aucun numéro. Ne pas géocoder la logeuse comme personne réelle. |
| Garni rue Basse-Combalot | XXVIII §2,5 | Voie ; quatre francs par jour ; numéro absent. |
| Garni voisin rue de Marseille | XXIX §4, 144, 240 ; XXXI §19 | « Petit garni voisin de la rue de Marseille » (XXIX §4), mais Michel le désigne ensuite par la rue même : « J’ai quitté la rue de Marseille pour le Lugdunum » (XXXI §19) ; la logeuse est sans doute « la sorcière de la rue de Marseille » (XXIX §144, 240). Garni sur la rue ou à son débouché immédiat, sur cour, sans électricité ; aucun numéro. |
| Mercière-papetière Mme Mitanchet | XXI §87 | Sur la même avenue que Mulet, à environ deux cents pas ; aucun numéro. |
| Maison de soie Neyratier (leçons de Michel) | XIX §132, 148 ; XX §128 ; XXVII §29 | « Au pied de la Croix-Rousse, une cambuse cariée et charbonneuse » (XIX §132) ; la leçon se donne « dans le magasin de M. Neyratier » (XXVII §29). Secteur du Griffon : après la leçon, Michel « dévalait ensuite du Griffon » vers la maison Rouchouze (XX §128, indice décisif). « Le bureau noir du Griffon » (XIX §148) n’est qu’un indice d’appoint, peut-être une métonymie du métier. Bâtiment non identifié. Ne pas confondre avec la maison des cousins passementiers, « la troisième maison du Griffon » (I §65 ; III §13). |
| Maison Rouchouze (négoce de vins) | XX §102, 103, 107, 128 ; XXI §1 | Maison du « premier négociant en vins de la place », où Michel est commis-auxiliaire (XX §102) jusqu’à son renvoi (XXI §1, 31 octobre 1925). Siège social et entrepôt dans « une ruelle ouvrière », derrière « un portail de bois chocolat » sous une enseigne en fer à cheval (XX §103), « toute proche de la rue Créqui » (XX §107). Le Griffon de XX §128 est le point de départ du trajet, après la leçon chez Neyratier ; ce n’est pas le site de la maison. |
| Villa Lanthelme et maison Marlieux à Bron | III §49 ; IX §142 ; XXVI §154, 167 | Deux propriétés « juste en face » (III §49) ou « presque en face » (IX §142) l’une de l’autre. Le fond du parc de la grand-mère (mur blanc, sapins, petite porte) se voit depuis un chemin entre Bron et Vinatier (XXVI §154, 167). Adresse réelle non fournie. Le voisinage réel des modèles à Bron est attesté par Ifri (2001) : « maison de campagne » de Varillon, Simone « sa voisine de Bron ». |
| Villa Martin-Dumont | XXXIII §2, 52 | Au bout d’Oullins, route de Beaunand (graphie du roman ; graphie actuelle Beaunant, hameau entre Oullins et Sainte-Foy-lès-Lyon) ; parc et intérieur décrits ; villa non identifiée. |
| Villa des cousins | III §2,13 | Saint-Germain-au-Mont-d’Or, près de la Saône ; propriété non identifiée. |
| Café près des Terreaux | XXII §139 | Seulement « tout près » des Terreaux. |
| Brasserie du cours La Fayette | XXII §356-357 | Le 24 décembre, veille de Noël : Michel rentre ensuite « pour réveillonner » (§357). Brasserie sans enseigne nommée, « envahie » ce soir-là par une foule populaire ; voie seule. |
| Bistrot à angle rue Du Guesclin | XXII §388 ; XXIV §4 | Angle nommé sans croisement explicitement établi dans la citation isolée. |
| Restaurant rue des Marronniers | XV §217 | Voie, pas enseigne. |
| Cinéma rue Thomassin | XXIII §180 | Voie et programme décrit ; identification exige presse de spectacles datée. |
| Café-hôtel À la ville d’Oran | XXI §91-104 | Itinéraire depuis centre/Brotteaux vers banlieue au-delà pont ferroviaire ; aucun point précis démontré. |

Ce tableau n’est pas exhaustif. Y manquent notamment le domicile d’Yvonne, rez-de-chaussée de l’avenue de Saxe (XIV §132 ; XV §572), celui de Guitte (Mme Dufaure), sœur d’Anne-Marie, boulevard des Belges (XXX §164 ; XXXIII §184), l’hôtel des « V… D… » sur le même boulevard (XXI §94-95, 137) et la maison des cousines Marlieux à Belleville (XIX §225). Ces lieux relèvent du [registre des lieux](../04_Donnees/lieux.json), refondu séparément.

## Tableau de repérage

Les comptes peuvent se recouper entre entrées ; ne pas les additionner pour mesurer des lieux uniques. Le JSON est la source de toutes les références. Ainsi « Rue de Jarente » reprend le motif et les six références de « Jésuites, 13 rue de Jarente » : c’est un doublon lexical, et le numéro est donné en XI §98.

Les comptes de « Gare Perrache » (3) et de « Parc de la Tête d’Or » (3) ne valent que pour la forme nommée. Une dizaine de mentions absolues « Perrache » désignent la gare (IV §7 ; V §4 ; XI §198 ; XII §162 ; XV §24 ; XVI §23 ; XXII §368 ; XXVIII §3…), et le parc revient souvent comme « le parc » (IV §89-91 ; V §32 ; XXVI §12 ; XXXIII §195-197…). Ces passages figurent en `context_refs`, hors compte. Loyasse, Les Culattes, Craponne, Montessuy (XX §137) et Vénissieux (IX §154 ; XX §137) sont des mentions onomastiques, sans scène ni visite. Chaponost reste un repère d’itinéraire (XV §277) ; sa mention en XX §137 est onomastique.

| Entrée | Classe | Forme recherchée : occurrences | Premiers repères |
|---|---|---:|---|
| Place Antique | principal | 62 | IX §85 ; IX §190 ; X §260 |
| Rue du Six-Janvier | principal | 5 | XI §14 ; XII §155 ; XIII §13 |
| Rue Créqui | principal | 10 | IX §68 ; XII §124 ; XV §265 |
| Rue Rabelais | principal | 3 | XII §124 ; XII §167 ; XXVI §33 |
| Café des Alpes | principal | 10 | X §149 ; X §260 ; XI §14 |
| Quai Perrache | principal | 29 | XII §167 ; XII §172 ; XII §173 |
| Bellecour | principal | 23 | I §95 ; I §127 ; II §3 |
| Cours Gambetta | principal | 34 | I §95 ; I §127 ; IX §124 |
| Place du Pont | principal | 13 | XII §97 ; XXI §68 ; XXII §24 |
| Rue de Marseille | principal | 8 | IX §84 ; XXI §68 ; XXII §278 |
| Avenue Jean-Jaurès | principal | 8 | XIX §133 ; XXII §41 ; XXIV §142 |
| Avenue de Saxe | principal | 10 | X §149 ; XIV §132 ; XV §432 |
| Église Saint-André | principal | 7 | IX §57 ; XI §24 ; XV §428 |
| Église du Saint-Sacrement | principal | 3 | XX §75 ; XX §143 ; XXI §17 |
| Saint-Jean, cathédrale et quartier | principal | 14 | I §65 ; IV §24 ; IX §41 |
| Bibliothèque municipale de Saint-Jean | principal | 3 | I §121 ; XX §117 ; XXI §36 |
| Fourvière | principal | 15 | III §43 ; X §1 ; X §14 |
| Théâtre Eldorado | principal | 12 | XII §136 ; XII §152 ; XII §167 |
| Grand Théâtre | principal | 8 | I §114 ; I §115 ; IV §64 |
| Salle Rameau | principal | 4 | I §96 ; XXIII §242 ; XXV §140 |
| Cours Boudier | principal | 11 | XIV §63 ; XIX §225 ; XIX §235 |
| Café des femmes / petit café jaune | principal | 6 | XXV §2 ; XXV §3 ; XXV §16 |
| Café de la Voûte Saint-Michel | principal | 4 | XXIV §65 ; XXIV §183 ; XXVI §66 |
| Voûte Saint-Michel | principal | 2 | XXIV §5 ; XXIV §65 |
| Pension Modern House | principal | 7 | XXV §145 ; XXV §166 ; XXV §177 |
| Hôtel Lugdunum | principal | 13 | XXXI §15 ; XXXI §19 ; intermedes §15 |
| Hôtel Carlton | principal | 6 | XXX §110 ; XXX §146 ; XXX §155 |
| Bar Cintra | principal | 5 | XX §162 ; XXVII §126 ; XXXI §19 |
| Chez Carreau | principal | 23 | XXII §90 ; XXII §91 ; XXII §101 |
| Maison Dorée | principal | 5 | I §127 ; XV §406 ; XXIII §49 |
| Brasserie de l'Étoile | principal | 2 | X §277 ; XXII §175 |
| Royal | secondaire | 4 | XXI §2 ; XXXVII §43 ; XXXVII §44 |
| Café Morel | secondaire | 1 | XI §82 |
| Brasserie des Archers | secondaire | 1 | XXXVII §35 |
| Chez Brazier / mère Brazier | secondaire | 3 | XX §162 ; XXXIII §296 ; XXXIII §297 |
| Cinéma de la rue Thomassin | secondaire | 1 | XXIII §180 |
| Salle du Conservatoire | secondaire | 3 | XXIX §28 ; XXIX §58 ; XXIX §120 |
| Faculté / Institut catholique | principal | 5 | XIX §109 ; XIX §215 ; XX §102 |
| Collège des Lazaristes | secondaire | 5 | XV §597 ; XVI §4 ; XIX §3 |
| Jésuites rue Sainte-Hélène | secondaire | 2 | XI §93 ; XX §102 |
| Jésuites, 13 rue de Jarente | principal | 6 | XI §91 ; XI §92 ; XI §93 |
| Église Saint-Louis | secondaire | 1 | XXII §99 |
| Église Saint-Bonaventure | secondaire | 1 | XXVII §89 |
| Saint-Nizier | secondaire | 1 | XXI §207 |
| Église / clocher de la Charité | secondaire | 4 | IX §187 ; XI §19 ; XII §200 |
| Église de la rue Bugeaud | secondaire | 1 | XV §587 |
| Parc de la Tête d'Or | principal | 3 | I §65 ; IV §76 ; XXVI §3 |
| Guillotière / la Guille | principal | 38 | III §49 ; IV §116 ; VIII §142 |
| Brotteaux | principal | 13 | X §174 ; XII §172 ; XIV §163 |
| Ainay | secondaire | 5 | XI §91 ; XI §97 ; XVII §194 |
| Griffon | secondaire | 6 | I §65 ; III §13 ; XIX §148 |
| Place des Terreaux / Terreaux | secondaire | 7 | IX §130 ; X §174 ; XXI §90 |
| Cordeliers | secondaire | 2 | XX §150 ; XXX §81 |
| Gare Perrache | principal | 3 | III §4 ; IX §221 ; X §1 |
| Place Carnot | secondaire | 1 | IX §130 |
| Place Morand | principal | 6 | IX §42 ; XXI §93 ; XXII §20 |
| Place de l'Abondance | secondaire | 2 | XXII §99 ; XXII §195 |
| Place Puvis-de-Chavannes | secondaire | 1 | XV §595 |
| Place Le Viste (graphie du roman : « Leviste ») | secondaire | 1 | XXIII §61 |
| Place des Célestins | secondaire | 1 | XXXVII §94 |
| Théâtre / secteur des Célestins | secondaire | 4 | XXX §66 ; XXX §81 ; XXXVII §35 |
| Rue Victor-Hugo / hôtel anonyme | secondaire | 5 | X §1 ; XII §8 ; XV §49 |
| Rue de Jarente | secondaire | 6 | XI §91 ; XI §92 ; XI §93 |
| Rue de la République / rue de la Ré | secondaire | 9 | I §127 ; II §95 ; VIII §9 |
| Rue Saint-Michel | secondaire | 1 | XXIII §228 |
| Rue Du Guesclin / bistrot | secondaire | 2 | XXII §388 ; XXIV §4 |
| Rue de la Barre | secondaire | 2 | XXIX §151 ; XXXVII §141 |
| Rue Garibaldi / hôtel anonyme | secondaire | 2 | XX §108 ; XXI §140 |
| Rue Moncey | secondaire | 2 | XXVI §179 ; XXX §2 |
| Rue Basse-Combalot / garni | principal | 3 | XXVIII §2 ; XXVIII §5 ; XXIX §4 |
| Rue des Marronniers / restaurant | secondaire | 1 | XV §217 |
| Rue Gasparin | secondaire | 1 | XXIII §61 |
| Rue Dubois | secondaire | 1 | XXI §91 |
| Rue Vendôme | secondaire | 1 | XXI §93 |
| Rue de l'Hôtel-de-Ville | secondaire | 1 | XXVIII §34 |
| Rue de la Vierge | secondaire | 1 | XXVI §205 |
| Rue des Archers | secondaire | 1 | XXXIII §117 |
| Rue des Célestins | secondaire | 1 | XXX §81 |
| Rue Chevreul | secondaire | 1 | XI §23 |
| Boulevard des Belges | principal | 7 | XXI §94 ; XXI §119 ; XXI §136 |
| Avenue de Noailles | secondaire | 1 | XXI §93 |
| Avenue du Parc | secondaire | 1 | XXI §95 |
| Avenue Président-Wilson (secteur Bron) | secondaire | 1 | IX §152 |
| Cours La Fayette | principal | 2 | XXII §35 ; XXII §356 |
| Cours Morand | secondaire | 1 | XXIX §151 |
| Cours de la Liberté | principal | 3 | XXI §68 ; XXV §181 ; XXV §206 |
| Cours Charlemagne / voûte Perrache | secondaire | 1 | XXVIII §4 |
| Quai Saint-Clair / cousins | principal | 5 | XXV §203 ; XXVIII §12 ; XXVIII §40 |
| Quai Tilsitt (graphie du roman : « Tilsit ») | secondaire | 2 | XXXI §38 ; recit §3 |
| Quai de Retz | secondaire | 1 | XXI §92 |
| Quai de la Guillotière | secondaire | 1 | XII §112 |
| Quai du Rhône | secondaire | 2 | XI §191 ; XXVII §112 |
| Quai de Saône | secondaire | 2 | VIII §270 ; XXII §233 |
| Pont de la Guillotière / de la Guille | principal | 10 | VIII §142 ; X §147 ; XII §110 |
| Pont La Fayette | secondaire | 3 | XXI §92 ; XXIII §254 ; XXXVII §14 |
| Pont Morand | secondaire | 2 | XIX §232 ; XXI §92 |
| Pont du Midi | principal | 2 | XV §384 ; XXX §109 |
| Pont Tilsit / Tilsitt | principal | 3 | XV §197 ; XXIII §27 ; XXVIII §78 |
| Hôtel-Dieu | secondaire | 1 | XXX §93 |
| Bourse de Lyon | secondaire | 4 | XX §162 ; XXVII §89 ; XXXIII §22 |
| Cercle Saint-Louis-de-Gonzague | secondaire | 1 | XXV §106 |
| À la ville d'Oran (café-hôtel) | secondaire | 1 | XXI §104 |
| Bron | principal | 20 | III §49 ; III §53 ; IX §140 |
| Église de Bron | secondaire | 1 | XIX §42 |
| Vinatier | principal | 3 | XXII §86 ; XXVI §140 ; XXVI §154 |
| Brignais / Briguais | principal | 9 | III §47 ; IV §14 ; X §199 |
| Vaugneray | principal | 16 | XV §77 ; XV §80 ; XV §114 |
| Gare de Saint-Just / ficelle | secondaire | 1 | XV §75 |
| Chaponost | secondaire | 3 | XV §277 ; XX §137 |
| Oullins | principal | 7 | XX §74 ; XXV §268 ; XXX §53 |
| Route de Beaunand | secondaire | 1 | XXXIII §2 |
| Charbonnières | principal | 8 | XII §36 ; XIX §223 ; XXIX §235 |
| Saint-Germain-au-Mont-d'Or | principal | 4 | III §2 ; III §13 ; XV §27 |
| Mont Brouilly | exterieur | 180 | III §51 ; III §53 ; III §64 |
| Claveisolles | exterieur | 15 | X §245 ; XI §25 ; XI §26 |
| Collège de Mongré | exterieur | 4 | XI §28 ; XIX §15 ; XIX §16 |
| Villefranche | exterieur | 5 | III §49 ; III §51 ; VIII §50 |
| Loyasse | secondaire | 1 | XX §137 |
| Les Culattes | secondaire | 1 | XX §137 |
| Craponne | secondaire | 1 | XX §137 |
| Vénissieux | secondaire | 2 | IX §154 ; XX §137 |
| Montessuy | secondaire | 1 | XX §137 |
| Croix-Rousse | secondaire | 1 | XIX §132 |
| Cinéma Marivaux (Paris, exclusion) | exclu | 1 | XIV §201 |
| Rue de Fleurus (Paris, exclusion) | exclu | 8 | III §72 ; III §78 ; V §84 |
| Saint-Chély (hors Lyon) | exterieur | 29 | I §1 ; I §2 ; I §3 |
| Chapelle des Essarts | secondaire | 1 | XXII §210 |
| Cercle des Étudiants catholiques / cercle de Rollet | principal | 4 | XII §64 ; XIX §1 ; XIX §225 |
| Cercle militaire | secondaire | 1 | XXIII §61 |
| Sacré-cœur (établissement pour filles) | secondaire | 1 | XX §102 |
| Belleville (Beaujolais) | exterieur | 6 | IX §34 ; XIX §225 ; XIX §280 |
| Petite-Chaumière (Paris, exclusion) | exclu | 2 | XIV §68 ; XIV §73 |

*Révisé le 24 octobre 2026 après contre-vérification : voir [07_Journal/2026-10-24.md](../07_Journal/2026-10-24.md).*
