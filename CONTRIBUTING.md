# Guide de contribution

Merci de votre intérêt pour le projet "Mobiles en Perspective" ! Ce guide vous explique comment contribuer efficacement au jeu de cartes.

## 🚀 Première contribution : Ouvrir une issue

**La façon la plus simple de contribuer est d'ouvrir une issue !** Pas besoin de connaissances techniques avancées en Git ou GitHub.

### Quand ouvrir une issue ?

- 🐛 **Vous avez trouvé une erreur** dans une carte ou une donnée
- 💡 **Vous avez une idée** de nouvelle carte ou fonctionnalité
- 📊 **Vous connaissez un ordre de grandeur** intéressant à ajouter
- ❓ **Vous avez une question** sur les règles du jeu
- 🔗 **Une source ne fonctionne plus** ou est incorrecte
- ✨ **Vous proposez une amélioration** générale

### Comment ouvrir une issue ?

1. Allez sur la [page des issues](https://github.com/Mobiles-en-Perspective/jeu-de-cartes/issues)
2. Cliquez sur "New issue"
3. Choisissez le template qui correspond à votre contribution :
   - 🃏 **Nouvelle carte ou amélioration de contenu**
   - 📊 **Ordre de grandeur**
   - 🛠️ **Amélioration technique**
   - 🐛 **Signaler un problème**
4. Remplissez le template avec vos informations
5. Cliquez sur "Submit new issue"

**C'est tout !** L'équipe du projet pourra alors discuter avec vous et éventuellement implémenter votre suggestion.

## 🛠️ Contribution avancée : Pull Request

Si vous êtes à l'aise avec Git et GitHub, vous pouvez directement proposer vos modifications via une Pull Request.

## Types de contributions

### 🃏 Contribution au contenu des cartes

Le fichier principal contenant les données des cartes est [`cartes.yml`](cartes.yml). Vous pouvez :

- Ajouter de nouvelles cartes avec des données factuelles
- Améliorer les descriptions existantes
- Ajouter ou corriger des sources
- Proposer de nouvelles images (placées dans le dossier `images/`)

**Format d'une carte :**
```yaml
- type: jeu
  titre: "Titre de la carte"
  image: nom_image.png
  groupe: "Groupe X"
  description: "Description factuelle avec sources vérifiées"
  sources:
    - https://source1.com
    - https://source2.com
  export: true
```

### 📊 Contribution aux ordres de grandeur

Le fichier [`ordres-de-grandeur.md`](ordres-de-grandeur.md) contient des données chiffrées sur l'impact environnemental du numérique. Vous pouvez :

- Ajouter de nouveaux ordres de grandeur avec sources
- Mettre à jour les données existantes
- Proposer des comparaisons ou visualisations

### 📋 Contribution aux règles du jeu

Le fichier [`regles.md`](regles.md) peut être amélioré pour :

- Clarifier les règles existantes
- Proposer de nouvelles variantes
- Améliorer la présentation

### 🛠️ Contribution au script d'impression

Le script [`src/impression_cartes.py`](src/impression_cartes.py) peut être amélioré. **Important** : si vous modifiez le script, pensez à mettre à jour le fichier [`specs-impression.md`](specs-impression.md) pour refléter vos changements.

## Comment contribuer par Pull Request (contributeurs expérimentés)

### Prérequis
- Connaissance de base de Git et GitHub
- Compte GitHub
- Git installé sur votre machine

### 1. Fork et clonage

1. Forkez le repository sur GitHub
2. Clonez votre fork localement :
   ```bash
   git clone https://github.com/VOTRE-USERNAME/jeu-de-cartes.git
   cd jeu-de-cartes
   ```

### 2. Création d'une branche

Créez une branche pour votre contribution :
```bash
git checkout -b amelioration-cartes-energie
# ou
git checkout -b correction-regles
# ou
git checkout -b nouvelle-fonctionnalite-script
```

### 3. Modification des fichiers

Effectuez vos modifications en respectant :

- **Pour `cartes.yml`** : Respectez le format YAML existant
- **Pour les scripts** : Testez vos modifications avec :
  ```bash
  python src/impression_cartes.py -o test-impression.pdf
  ```
- **Sources** : Toujours inclure des sources fiables et vérifiables
- **Images** : Utilisez des images libres de droits ou sous licence compatible

### 4. Test de vos modifications

- Vérifiez que le fichier YAML est valide
- Si vous modifiez le script, testez la génération du PDF
- Relisez vos modifications pour éviter les erreurs

### 5. Commit et push

```bash
git add .
git commit -m "Ajout de cartes sur la consommation énergétique"
git push origin nom-de-votre-branche
```

### 6. Création d'une Pull Request

1. Allez sur GitHub et créez une Pull Request
2. Utilisez un titre descriptif
3. Remplissez le template de PR avec les détails de vos modifications

## 💬 Vous préférez discuter d'abord ?

Si vous n'êtes pas sûr de votre idée ou voulez en discuter avant de l'implémenter :
- Ouvrez une issue pour en parler
- Utilisez les [Discussions GitHub](https://github.com/Mobiles-en-Perspective/jeu-de-cartes/discussions) pour les questions générales
- Contactez l'équipe dans votre issue ou Pull Request

## Critères de qualité

### Pour le contenu des cartes

- ✅ Sources fiables et récentes (moins de 5 ans de préférence)
- ✅ Données chiffrées précises
- ✅ Description claire et accessible
- ✅ Respect du format YAML
- ✅ Images de qualité et libres de droits

### Pour les ordres de grandeur

- ✅ Sources scientifiques ou institutionnelles
- ✅ Unités clairement spécifiées
- ✅ Contexte français ou international précisé
- ✅ Comparaisons pertinentes

### Pour les contributions techniques

- ✅ Code fonctionnel et testé
- ✅ Documentation mise à jour
- ✅ Respect des conventions existantes
- ✅ Pas de régression sur les fonctionnalités existantes

## Ressources utiles

- [Format YAML](https://yaml.org/spec/1.2/spec.html)
- [Markdown Guide](https://www.markdownguide.org/)
- [Sources fiables pour l'environnement numérique](https://www.ademe.fr/)
- [Images libres de droits](https://unsplash.com/) ou [Wikimedia Commons](https://commons.wikimedia.org/)

## Besoin d'aide ?

N'hésitez pas à :
- 🐛 **Ouvrir une issue** pour poser des questions ou signaler un problème
- 💬 **Participer aux discussions** pour les questions générales
- 🤝 **Demander de l'aide** dans votre issue ou Pull Request

**Rappel : Ouvrir une issue est souvent le meilleur premier pas !** Même si vous pensez savoir comment résoudre un problème, une issue permet de discuter de la meilleure approche avant de se lancer dans le code.

Merci pour votre contribution ! 🚀
