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
- L'ordre d'enchaînement est strict : 
	- page 1 : rectos cartes 1, 2, 3, 4
	- page 2 : versos cartes 1, 2, 3, 4
	- page 3 : rectos cartes 5, 6, 7, 8
	- page 4 : versos cartes 5, 6, 7, 8
	- etc.
- Les cartes sont positionnées pour permettre une impression recto-verso (retournement petit côté), afin que recto et verso coïncident lors du découpage manuel.

## Contenu des cartes

### Recto (pages impaires)
- En haut et centré : le **titre** (gras, police Roboto, couleur selon le groupe).
- Au centre : l’image (centrée, retaillée pour une hauteur uniforme, aspect ratio conservé, rognage latéral possible).
- En bas et centré : le **groupe** (gras, police Roboto, couleur selon le groupe).

### Verso (pages paires)
- En haut et centré : le **titre** (gras, police Roboto, couleur selon le groupe).
- En dessous : la **description** (police Roboto, texte centré, gestion des retours à la ligne).

## Marges et espacement
- Marges extérieures sur chaque page pour faciliter la découpe.
- Espacement entre les cartes pour éviter les chevauchements lors de la découpe.
- Espacement entre les éléments (titre, image, groupe/description) à l’intérieur de chaque carte.
- Les textes des descriptions doivent rester dans le cadre de leur carte et ne pas déborder ni se chevaucher.

## Données d’entrée
- Inclure uniquement les cartes du fichier `cartes.yml` avec `export: true`.
- Les images sont présentes dans le dossier `images/`.

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

---

**Palette de couleurs par groupe** (à définir dans le script, exemple) :
- Groupe 1 : Bleu
- Groupe 2 : Vert
- Groupe 3 : Orange
- Groupe 4 : Violet
- Événements : Gris

**Remarque** : Adapter la palette selon les besoins ou la charte graphique.

---


