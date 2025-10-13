# Spécifications - Script d'impression de l'affiche de présentation

## Vue d'ensemble

Script Python permettant de générer une affiche A3 de présentation du jeu "Mobiles en Perspective" pour les ateliers. L'affiche contient le titre, la présentation du jeu, le logo et des QR codes pour faciliter l'engagement des participants.

## Format et dimensions

- **Format** : A3 (297 mm × 420 mm)
- **Orientation** : Portrait
- **Marges** : 20 mm de chaque côté
- **Zone de contenu** : 257 mm × 380 mm

## Contenu de l'affiche

### 1. En-tête (haut de page)

**Logo**
- Téléchargé depuis : `https://avatars.githubusercontent.com/u/228016686?s=200&v=4`
- Sauvegardé localement dans : `images/logo.png` (à télécharger automatiquement si absent)
- Dimensions : 80 mm × 80 mm (ou proportionnel)
- Position : Centré horizontalement, en haut de page

**Titre principal**
- Texte : "Mobiles en Perspective"
- Police : Roboto-Bold
- Taille : 28 pt
- Couleur : Noir
- Position : Sous le logo, centré

**Sous-titre**
- Texte : "Quels impacts sociaux et environnementaux ont nos smartphones ?"
- Police : Roboto-Regular
- Taille : 18 pt
- Couleur : Gris foncé (#333333)
- Position : Sous le titre, centré

### 2. Section présentation (milieu de page)

**Texte de présentation**
- Source : Section "Présentation du jeu" du fichier `README.md`
- Texte complet à inclure depuis "Il était une fois..." jusqu'à "...numérique plus responsable !"
- Police : Roboto-Regular
- Taille : 12 pt
- Couleur : Noir
- Interligne : 1.4
- Alignement : Justifié avec marges internes de 15 mm
- Largeur maximale : 227 mm (zone de contenu - marges internes)

### 3. Section QR Codes (bas de page)

Disposition en grille 2×2 avec labels :

**Ligne 1 (gauche à droite)**

1. **QR Code Feedback**
   - URL : `https://openfeedback.io/devfestnantes2025/2025-10-16/mobilesenperspectivequelsimpactssociauxetenvironnementauxontnoss`
   - Label : "Donnez-nous votre feedback !"
   - Taille QR : 60 mm × 60 mm
   - Police label : Roboto-Bold, 11 pt
   - Couleur label : #1976d2 (bleu)

2. **QR Code GitHub Repo**
   - URL : `https://github.com/Mobiles-en-Perspective/mobiles-en-perspective-jeu-de-cartes`
   - Label : "Consulter le code source"
   - Taille QR : 60 mm × 60 mm
   - Police label : Roboto-Bold, 11 pt
   - Couleur label : #388e3c (vert)

**Ligne 2 (gauche à droite)**

3. **QR Code Contribution**
   - URL : `https://framaforms.org/contribuer-au-jeu-de-cartes-mobiles-en-perspective-1757966394`
   - Label : "Contribuer au projet"
   - Taille QR : 60 mm × 60 mm
   - Police label : Roboto-Bold, 11 pt
   - Couleur label : #f57c00 (orange)

4. **QR Code Téléchargement**
   - URL : `https://github.com/Mobiles-en-Perspective/mobiles-en-perspective-jeu-de-cartes/releases/latest`
   - Label : "Télécharger le jeu"
   - Taille QR : 60 mm × 60 mm
   - Police label : Roboto-Bold, 11 pt
   - Couleur label : #7b1fa2 (violet)

**Espacement**
- Espacement horizontal entre QR codes : 20 mm
- Espacement vertical entre les deux lignes : 20 mm
- Espacement entre QR code et son label : 5 mm
- Labels centrés sous chaque QR code

### 4. Pied de page

**Licence**
- Logo CC BY 4.0 : Téléchargé depuis `https://i.creativecommons.org/l/by/4.0/88x31.png`
- Sauvegardé localement dans : `images/cc-by.png` (à télécharger automatiquement si absent)
- Dimensions du logo : 22 mm × 7.75 mm (88×31 pixels à 300 DPI)
- Texte : "Ce jeu est sous licence CC BY 4.0"
- Police : Roboto-Regular
- Taille : 9 pt
- Couleur : Gris (#666666)
- Position : Logo et texte centrés horizontalement, tout en bas (8 mm du bord inférieur)
- Disposition : Logo à gauche du texte, avec 3 mm d'espacement

## Dépendances techniques

### Bibliothèques Python requises

```python
reportlab>=4.0.0  # Génération PDF (déjà dans requirements.txt)
qrcode>=7.4.0     # Génération QR codes
pillow>=10.0.0    # Manipulation images (déjà requis par reportlab)
pyyaml>=6.0       # Lecture YAML (déjà dans requirements.txt)
requests>=2.31.0  # Téléchargement du logo si nécessaire
```

### Polices

- Utilisation des polices Roboto existantes dans `src/fonts/`
- Roboto-Regular.ttf
- Roboto-Bold.ttf

## Structure du script

### Fichier : `src/impression_affiche.py`

**Fonctions principales**

1. `setup_fonts()` : Enregistrement des polices Roboto (réutilisé de impression_cartes.py)
2. `download_image(url, path)` : Télécharge une image (logo ou licence) si absente
3. `read_presentation()` : Lit et extrait la section "Présentation du jeu" du README.md
4. `generate_qr_code(url, size)` : Génère un QR code pour une URL donnée
5. `draw_header(c, y_position)` : Dessine logo, titre et sous-titre
6. `draw_presentation(c, y_position, text)` : Dessine le texte de présentation avec word wrap
7. `draw_qr_codes(c, y_position)` : Dessine la grille de 4 QR codes avec labels
8. `draw_footer(c)` : Dessine le logo CC BY 4.0 et le texte de licence en pied de page
9. `generate_affiche(output_path)` : Fonction principale orchestrant la génération

**Gestion des erreurs**

- Vérification de l'existence des polices
- Téléchargement automatique du logo et du logo de licence avec gestion d'erreur
- Validation des URLs pour les QR codes
- Messages d'erreur clairs si génération impossible

## Utilisation du script

### Ligne de commande

```bash
python src/impression_affiche.py -o affiche-presentation.pdf
```

**Arguments**
- `-o, --output` : Chemin du fichier PDF de sortie (défaut : `affiche-presentation.pdf`)

### Exemple avec environnement virtuel

```bash
# Activation de l'environnement virtuel
source .venv/bin/activate

# Installation des dépendances (si nécessaire)
pip install -r src/requirements.txt

# Génération de l'affiche
python src/impression_affiche.py -o affiche-presentation.pdf
```

## Mise à jour des dépendances

Le fichier `src/requirements.txt` devra être mis à jour pour inclure :

```
qrcode[pil]>=7.4.0
requests>=2.31.0
```

## Contraintes de design

1. **Lisibilité** : Tous les textes doivent être clairement lisibles à 1 mètre de distance
2. **Équilibre visuel** : Répartition harmonieuse des éléments sur la page
3. **Hiérarchie** : Le titre et le logo doivent attirer l'œil en premier
4. **Scannabilité** : Les QR codes doivent être suffisamment grands pour être scannés facilement (60 mm minimum)
5. **Cohérence** : Utilisation des mêmes couleurs que les groupes de cartes pour créer une cohérence visuelle
6. **Aération** : Espaces blancs suffisants pour ne pas surcharger l'affiche

## Tests de validation

Avant de considérer le script comme finalisé :

1. ✅ Le PDF généré est bien au format A3
2. ✅ Le logo du projet est téléchargé et affiché correctement
3. ✅ Le texte de présentation est complet et correctement formaté
4. ✅ Les 4 QR codes sont générés et scannables
5. ✅ Les URLs des QR codes sont correctes
6. ✅ Les couleurs et polices correspondent aux spécifications
7. ✅ L'ensemble tient sur une seule page
8. ✅ Le rendu est esthétique et aéré
9. ✅ Le logo de licence CC BY 4.0 et le texte sont affichés en pied de page

## Évolutions futures possibles

- Paramétrage des URLs via un fichier de configuration
- Support de plusieurs langues
- Variantes de mise en page (mode sombre, etc.)
- Export en format PNG haute résolution pour impression professionnelle
- Ajout d'éléments graphiques décoratifs

## Notes d'implémentation

- Utiliser `reportlab.lib.pagesizes.A3` pour les dimensions
- Les QR codes doivent avoir un niveau de correction d'erreur élevé (ERROR_CORRECT_H) pour résister aux conditions d'impression
- Le texte de présentation utilise la même fonction `wrap_text()` que dans `impression_cartes.py`
- Prévoir une marge de sécurité de 5 mm minimum par rapport aux bords pour l'impression
