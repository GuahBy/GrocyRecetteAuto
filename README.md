# Grocy Recipe Importer 🍳

Outil Python pour importer automatiquement des recettes depuis des sites web ou fichiers HTML vers votre instance Grocy.

## Fonctionnalités

- ✅ Support de **250+ sites de recettes** (Marmiton, 750g, Cuisine AZ, etc.)
- ✅ Import depuis **URL** ou **fichier HTML local** ou **Reels instagram** (transcription de l'audio, scraping de la description, extraction des données)
- ✅ Extraction automatique des ingrédients, instructions, temps de préparation
- ✅ Interface CLI simple et colorée
- ✅ Mode dry-run pour prévisualiser avant import
- ✅ 100% en français

## Installation

```bash
# Cloner ou télécharger le projet
cd GrocyRecetteAuto

# Installer les dépendances
pip install -r requirements.txt
```

## Prérequis

1. Une instance Grocy fonctionnelle
2. Une clé API Grocy (à générer dans Grocy → Manage API Keys)

### Générer une clé API Grocy

1. Connectez-vous à votre Grocy
2. Allez dans **Manage API keys** (icône clé en haut à droite)
3. Cliquez sur **Add**
4. Copiez la clé générée

## Prérequis pour les reels instagram: 
1. Connectez-vous sur instagram depuis votre navigateur
2. Exporter les cookies de connexion (Get cookies.txt LOCALLY plugin chrome)
3. Déplacer les cookies (instagram.txt) dans GrocyRecetteAuto/cookies

## Utilisation

### Import depuis une URL

```bash
python main.py \
  "https://www.marmiton.org/recettes/recette_poulet-au-curry_12345.aspx" \
  --grocy-url http://ton-serveur:9283 \
  --api-key VOTRE_CLE_API
```

### Import depuis un fichier HTML local

```bash
python main.py \
  "/chemin/vers/recette.html" \
  --grocy-url http://ton-serveur:9283 \
  --api-key VOTRE_CLE_API
```

### Mode prévisualisation (sans import)

```bash
python main.py \
  "https://www.750g.com/recette-tarte-aux-pommes.htm" \
  --grocy-url http://ton-serveur:9283 \
  --api-key VOTRE_CLE_API \
  --dry-run
```

## Sites supportés

L'outil utilise `recipe-scrapers` qui supporte automatiquement plus de 250 sites, dont :

**Sites français :**
- Marmiton
- 750g
- Cuisine AZ
- Journal des Femmes Cuisine
- Recettes de Cuisine
- Et beaucoup d'autres...

**Sites internationaux :**
- AllRecipes
- BBC Food
- Food Network
- NYT Cooking
- Serious Eats
- Etc.

[Liste complète des sites supportés](https://github.com/hhursev/recipe-scrapers#scrapers-available-for)

## Exemples de workflow

### Scénario 1 : Importer une recette trouvée en ligne

```bash
# Je trouve une recette sur Marmiton
python main.py \
  "https://www.marmiton.org/recettes/recette_blanquette-de-veau_12345.aspx" \
  --grocy-url http://ton-serveur:9283 \
  --api-key ta-cle-api
```

### Scénario 2 : Sauvegarder puis importer

```bash
# 1. Je sauvegarde la page HTML depuis mon navigateur (Ctrl+S)
# 2. J'importe le fichier local
python main.py \
  ~/Downloads/recette-tiramisu.html \
  --grocy-url http://ton-serveur:9283 \
  --api-key ta-cle-api
```

### Scénario 3: Importer une recette depuis un reels instagram: 
```bash
#1. Je trouve une recette sur un reels instagram
#2. J'appuie sur l'enveloppe pour envoyer le reels
#3. Je fait copier le lien

  python3 test_instagram_full.py "https://www.instagram.com/reel/recette-géniale"
```
## Intégration Docker

Vous pouvez ajouter ce service à votre docker-compose pour un accès simplifié :

```yaml
  recipe-api:
   build:
     context: ./GrocyRecetteAuto
     dockerfile: Dockerfile.api
   container_name: recipe-api
   environment:
     - GROCY_URL=http://grocy:80
     - GROCY_API_KEY=ta-clé-api
   ports:
     - 5000:5000
   volumes:
     - ./GrocyRecetteAuto/cookies:/app/cookies
   restart: unless-stopped
   depends_on:
     - grocy
```

Puis :

```bash
docker-compose run recipe-importer python main.py "https://..." --grocy-url $GROCY_URL --api-key $GROCY_API_KEY
```

## Configuration avancée

### Variables d'environnement

Pour éviter de taper l'URL et la clé API à chaque fois :

```bash
export GROCY_URL="http://ton-serveur:9283"
export GROCY_API_KEY="ta-clé-api"

# Puis utilisez :
python main.py "https://recette.com/..."
```

### Script wrapper

Créez un script `import-recette.sh` :

```bash
#!/bin/bash
python /chemin/vers/grocy-recipe-importer/main.py "$1" \
  --grocy-url "http://ton-serveur:9283" \
  --api-key "ta-clé-api"
```

Utilisez-le simplement :

```bash
./import-recette.sh "https://marmiton.org/recette-xyz"
```

## Limitations connues

1. **Images** : L'import d'images n'est pas encore implémenté (complexité API Grocy)
2. **Ingrédients** : Les ingrédients sont ajoutés dans la description, pas comme entités liées
3. **Unités** : La normalisation des unités (g, kg, ml, etc.) n'est pas automatique

## Améliorations futures

- [ ] Import d'images
- [ ] Mapping automatique ingrédients → produits Grocy existants
- [ ] Support de plusieurs recettes en batch
- [ ] Interface web simple
- [ ] Mode interactif pour éditer avant import

## Contribution

N'hésite pas à améliorer le code ! Les PRs sont les bienvenues.

## Dépannage

### Erreur "Impossible de se connecter à Grocy"

- Vérifiez que Grocy est bien accessible à l'URL fournie
- Testez dans votre navigateur : `http://ton-serveur:9283/api/system/info`
- Vérifiez votre clé API

### Erreur lors de l'extraction

- Le site n'est peut-être pas supporté par recipe-scrapers
- Essayez en sauvegardant la page HTML localement d'abord
- Vérifiez que la page contient bien des métadonnées de recette (schema.org)

### La recette est mal formatée

- Les sites ont parfois des formats différents
- Vous pouvez éditer manuellement la recette dans Grocy après import

## Licence

MIT - Fais-en ce que tu veux !
