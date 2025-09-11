# Jeu de cartes Mobiles en Perspective

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
