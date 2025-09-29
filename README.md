# Mobiles en Perspective: quels impacts sociaux et environnementaux ont nos smartphones ? - Jeu de cartes

## Présentation du jeu

Il était une fois, en 2007, une révolution qui a changé nos vies : l'arrivée du smartphone. Mais comme dans tous les contes, cette innovation cache des faces moins reluisantes...

Cet atelier collaboratif et ludique vous invite à explorer ensemble l'écosystème complexe des technologies mobiles et leurs impacts sur notre société et notre environnement. Inspiré de la Fresque du Climat, ce jeu de cartes vous permettra de découvrir les enjeux cachés derrière nos appareils du quotidien.

Ce que vous vivrez :

  * Un moment d'échange détendu et enrichissant (aucun prérequis technique !)
  * Une approche ludique pour comprendre des enjeux complexes
  * Des discussions stimulantes avec d'autres participant·e·s
  * Une réflexion collective sur les solutions à notre portée
  * Déroulé : Réparti·e·s en petites tables de 4 à 8 personnes, vous manipulerez des cartes pour construire une vision partagée de l'impact des smartphones, des mines de cobalt jusqu'aux data centers, en passant par nos usages quotidiens.

Venez découvrir comment, nous pouvons contribuer à un numérique plus responsable !

## Règles du jeu

Les règles du jeu sont détaillées dans le fichier [regles.md](regles.md)

## Base de données

Les donneés des cartes sont dans le fichier [cartes.yml](cartes.yml)

## Script d'impression

### Spécifications

Les spécifications sont dans le fichier [specs-impression.md](specs-impression.md)

### Exemple d'utilisation

Pour générer le PDF d'impression des cartes :

#### Installation des dépendances

```sh
pip install -r src/requirements.txt
```

#### (Optionnel) Utilisation d'un environnement virtuel Python

Pour isoler les dépendances du projet, vous pouvez utiliser un environnement virtuel :

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r src/requirements.txt
```

Pour quitter l'environnement virtuel :

```sh
deactivate
```

#### Génération du PDF

```sh
python src/impression_cartes.py -o cartes-impression.pdf
```

- Le PDF sera généré dans le fichier indiqué (par défaut `cartes-impression.pdf`).
- Les cartes sont disposées pour une impression recto-verso et un découpage manuel.
- Les polices et couleurs sont gérées automatiquement.

## Contribuer au projet

Vous souhaitez améliorer le jeu en ajoutant de nouvelles cartes, en corrigeant des données ou en proposant des améliorations ? Consultez notre [guide de contribution](CONTRIBUTING.md) pour savoir comment procéder.

Toutes les contributions sont les bienvenues :
- 🃏 Ajout de nouvelles cartes dans `cartes.yml`
- 📊 Amélioration des ordres de grandeur dans `ordres-de-grandeur.md`
- 📋 Amélioration des règles du jeu
- 🛠️ Améliorations techniques du script d'impression

# License

[![CC BY 4.0][cc-by-shield]][cc-by]

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

Les fichiers de police Roboto (présents dans `src/fonts`) sont distribués sous licence Apache 2.0.
Voir https://www.apache.org/licenses/LICENSE-2.0

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
