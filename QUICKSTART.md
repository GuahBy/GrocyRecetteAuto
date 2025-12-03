# 🚀 Démarrage Rapide

## Installation en 3 étapes

### 1. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 2. Configurer votre clé API Grocy
```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer .env avec vos paramètres
nano .env
# ou
vim .env
```

### 3. Tester l'installation
```bash
python test.py
```

## Utilisation basique

### Méthode 1 : Avec le script wrapper (recommandé)
```bash
# Charger la config
source .env

# Importer une recette
./import-recette.sh "https://www.marmiton.org/recettes/recette_poulet-curry.aspx"
```

### Méthode 2 : Directement avec Python
```bash
python main.py \
  "https://www.750g.com/recette-tarte-aux-pommes.htm" \
  --grocy-url http://localhost:9283 \
  --api-key VOTRE_CLE_API
```

### Méthode 3 : Depuis un fichier HTML
```bash
# Sauvegarder une page web (Ctrl+S dans le navigateur)
# Puis l'importer
python main.py ~/Downloads/recette.html --grocy-url http://localhost:9283 --api-key VOTRE_CLE
```

## Test avec l'exemple fourni
```bash
# Un fichier exemple est fourni pour tester
python main.py exemple-recette.html \
  --grocy-url http://localhost:9283 \
  --api-key VOTRE_CLE \
  --dry-run  # Mode prévisualisation, sans import réel
```

## Problèmes courants

**"ModuleNotFoundError: No module named 'recipe_scrapers'"**
→ Vous n'avez pas installé les dépendances : `pip install -r requirements.txt`

**"Impossible de se connecter à Grocy"**
→ Vérifiez l'URL et que Grocy est accessible
→ Testez dans votre navigateur : http://localhost:9283/api/system/info

**"Erreur lors de l'extraction"**
→ Le site n'est peut-être pas supporté
→ Essayez en sauvegardant la page HTML localement d'abord

## Intégration à votre docker-compose

Ajoutez dans votre docker-compose.yml existant :

```yaml
  grocy-recipe-importer:
    build: ./grocy-recipe-importer
    container_name: grocy-recipe-importer
    environment:
      - GROCY_URL=http://app:80
      - GROCY_API_KEY=${GROCY_API_KEY}
    volumes:
      - ./recettes:/recettes
    restart: "no"
```

Puis utilisez :
```bash
docker-compose run grocy-recipe-importer "https://recette.com/..."
```

Pour plus de détails, consultez le README.md !
