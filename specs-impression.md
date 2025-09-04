# Spécifications pour le script d’impression du jeu de cartes

## Format général
- Générer un PDF au format A4.
- Chaque page contient 4 cartes (2 colonnes × 2 lignes).
- Les cartes sont rectangulaires, avec marges extérieures et espacement entre elles et entre les contenus.

## Disposition des pages
- Pages impaires : 4 rectos de cartes.
- Pages paires : 4 versos correspondants.
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

## Données d’entrée
- Inclure uniquement les cartes du fichier `cartes.yml` avec `export: true`.
- Les images sont présentes dans le dossier `images/`.

## Contraintes techniques
- PDF prêt à imprimer, compatible recto-verso (retournement petit côté).
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


