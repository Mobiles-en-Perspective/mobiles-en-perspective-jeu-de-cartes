# Spécifications pour le script d’impression du jeu de cartes

## Format général
- Générer un PDF au format A4 paysage (orientation landscape).
- Chaque page contient 4 cartes (2 colonnes × 2 lignes), format paysage.
- Les cartes sont rectangulaires, format paysage, et font exactement la moitié de la hauteur et la moitié de la largeur de la page (toutes de taille égale).
- Une ligne horizontale et une ligne verticale séparent le PDF en 4 cartes (guides de découpe).
- Marges extérieures et espacement entre les cartes et les contenus.
- Générer un PDF au format A4 paysage (orientation landscape).
- Chaque page contient 4 cartes (2 colonnes × 2 lignes), format paysage.
- Les cartes sont rectangulaires, format paysage, et font exactement la moitié de la hauteur et la moitié de la largeur de la page (toutes de taille égale).
- Marges extérieures et espacement entre les cartes et les contenus.

## Disposition des pages
- Les pages impaires affichent les rectos des cartes, les pages paires affichent les versos correspondants.

### Disposition recto-verso (pour retournement petit côté)

Pour chaque groupe de 4 cartes :

- **Page impaire (recto)**
	- carte 1 recto | carte 2 recto
	- carte 3 recto | carte 4 recto

- **Page paire (verso)**
	- carte 2 recto | carte 1 recto
	- carte 4 recto | carte 3 recto

Ensuite, on passe au groupe de 4 cartes suivant (cartes 5 à 8, etc.).

Ce placement permet, lors de l'impression recto-verso avec retournement sur le petit côté, d'obtenir un alignement parfait des cartes recto et verso après découpe.

## Types de cartes

Chaque carte possède un attribut `type` :
- `type: jeu`
- `type: reponse`
- `type: question` (carte question, règles inchangées)


## Contenu des cartes

### Cartes d'action


### Cartes de type `jeu` ou `reponse`

#### Attributs spécifiques

- Les cartes de type `jeu` ou `reponse` peuvent avoir un attribut optionnel `sources` (chaîne ou liste de chaînes). Cet attribut permet de documenter les sources d'une carte, mais **son contenu n'est jamais affiché sur les cartes du PDF**.

#### Recto (pages impaires)
- En haut et centré : le **titre** (gras, police Roboto, couleur selon le groupe).
- Au centre : l'image (centrée, retaillée pour une hauteur uniforme de 65% de la hauteur de la carte, aspect ratio conservé, rognage latéral possible).
- En bas et centré : le **groupe** (gras, police Roboto, couleur selon le groupe).

#### Verso (pages paires)
- En haut et centré : le **titre** (gras, police Roboto, couleur selon le groupe).
- En dessous : la **description** (police Roboto, texte aligné à gauche, centrée verticalement dans la carte, gestion automatique des retours à la ligne pour rester dans le cadre).

#### Exemple de carte `jeu` ou `reponse` dans cartes.yml :

```yaml
- type: jeu
	titre: "Application"
	image: "application.png"
	groupe: "Groupe 1"
	description: "**Les utilisateurs de Smartphone  utilisateurs en moyenne 9 à 10 apps par jour. 30 par mois.**\nhttps://techjury.net/blog/app-usage-statistics/"
	export: true
```
```yaml
- type: reponse
	titre: "Réponse à la question X"
	image: "reponse.png"
	groupe: "Groupe 2"
	description: "Voici la réponse détaillée à la question X."
	export: true
```

### Cartes question

#### Recto (pages impaires)
- Au centre : le **titre** (gras, police Roboto, taille de police supérieure à celle des cartes d'action, texte centré, gestion des retours à la ligne).
- En bas et centré : le **groupe** (gras, police Roboto, couleur selon le groupe).
- Bordure extérieure épaisse de la couleur du groupe associé (largeur 12 points).
- Marge interne de 6 points pour éviter le débordement de la bordure sur les cartes adjacentes.

#### Verso (pages paires)
- Un large point d'interrogation `?` est affiché en gras, au centre de la carte et de la couleur du groupe associé.
- Bordure extérieure épaisse de la couleur du groupe associé (largeur 12 points).
- Marge interne de 6 points pour éviter le débordement de la bordure sur les cartes adjacentes.

Les cartes question sont imprimées avec les autres cartes.

#### Exemple de carte question dans cartes.yml :

```yaml
- type: question
	titre: "Quels usages du smartphone sont les plus énergivores ?"
	groupe: "Groupe 2"
	export: true
```


## Marges et espacement
- Les descriptions peuvent contenir des balises **texte en gras** (syntaxe Markdown) : tout texte entouré de doubles astérisques sera affiché en gras dans le PDF, même si le texte à mettre en gras s'étale sur plusieurs lignes (le gras est propagé jusqu'à la fermeture des balises **).
- Marges extérieures sur chaque page pour faciliter la découpe.
- Espacement entre les cartes pour éviter les chevauchements lors de la découpe.
- Espacement entre les éléments (titre, image, groupe/description) à l’intérieur de chaque carte.
- Tous les textes (titre, description, question, réponse) sont automatiquement coupés en plusieurs lignes si besoin : ils restent à l'intérieur de la carte, sans débordement ni ellipsis, grâce à un retour à la ligne dynamique (word wrap).
	- Aucun texte ne doit être tronqué ou sortir du cadre de la carte.

## Données d’entrée
- Inclure uniquement les cartes du fichier `cartes.yml` avec `export: true`.
- Les images sont présentes dans le dossier `images/`.
- Chaque carte doit avoir un attribut `type` (`action` ou `question`).

## Contraintes techniques
- PDF prêt à imprimer, compatible recto-verso (retournement petit côté).
- Orientation paysage pour toutes les pages et cartes.
- Police utilisée : Roboto.
- Titres et groupes en gras.
- Chaque groupe utilise une couleur différente (palette à définir dans le script).
- Images centrées et retaillées pour une hauteur uniforme, aspect ratio conservé, rognage latéral possible.
- Pas de numérotation des cartes ou des pages.

## Exclusions
- Pas de page de garde ni de page spéciale.
- Pas de numérotation.

## Génération d'un PDF des sources

- Le script doit générer un second PDF listant toutes les cartes disposant d'un attribut `sources`.
- Ce PDF est au format A4, orientation portrait.
- Le nom du PDF est le même que le PDF principal, suffixé par `_sources` (ex: `cartes-impression_sources.pdf`).
- En haut du PDF, afficher le titre : "Jeu de cartes Mobiles en Perspective - Sources".
- Pour chaque carte ayant un attribut `sources`, afficher :
	- le titre de la carte (avec retour à la ligne automatique si trop long)
	- le type (avec retour à la ligne automatique si trop long)
	- le groupe (avec retour à la ligne automatique si trop long)
	- la liste des sources, chaque source sur une ou plusieurs lignes selon la longueur
	- **Spécificité pour les URLs** :
		- Toute URL (débutant par http:// ou https://) est automatiquement affichée sur une nouvelle ligne, même si elle est collée à du texte.
		- Les URLs trop longues sont coupées automatiquement (word wrap) pour ne pas dépasser la largeur de la page.
	- Les retours à la ligne présents dans le YAML sont respectés dans le PDF.
- Séparer chaque bloc de carte par une ligne de tirets : `---------------------------`.
- Sauter une ligne entre chaque bloc pour l'aération.

Ce PDF sert uniquement à la documentation des sources et n'est pas destiné à l'impression des cartes.

---

**Palette de couleurs par groupe** (à définir dans le script, exemple) :
- Groupe 1 : Bleu
- Groupe 2 : Vert
- Groupe 3 : Orange
- Groupe 4 : Violet

**Remarque** : Adapter la palette selon les besoins ou la charte graphique.

---


