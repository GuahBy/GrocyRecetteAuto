# 🚦 Guide de Test Local (3 minutes)

## Méthode Rapide avec le script automatique

```bash
cd grocy-recipe-importer

# 1. Installer les dépendances
pip3 install -r requirements.txt

# 2. Lancer le test automatique
./test-complet.sh
```

Le script va :
- ✅ Vérifier Python
- ✅ Vérifier les dépendances
- ✅ Tester l'extraction
- ✅ (Optionnel) Tester la connexion à Grocy

---

## Méthode Manuelle (étape par étape)

### 1️⃣ Installer les dépendances (1 minute)

```bash
cd grocy-recipe-importer
pip3 install -r requirements.txt
```

### 2️⃣ Test basique - Extraction uniquement (30 secondes)

```bash
# Teste juste l'extraction, sans toucher à Grocy
python3 -c "
from recipe_extractor import RecipeExtractor
extractor = RecipeExtractor()
recipe = extractor.extract('exemple-recette.html')
print(f'✅ Recette extraite : {recipe[\"title\"]}')
print(f'✅ {len(recipe[\"ingredients\"])} ingrédients trouvés')
print('Test OK!')
"
```

Si tu vois "Test OK!" → **Ça marche !**

### 3️⃣ Test complet avec Grocy (1 minute)

```bash
# Remplace par ton URL et ta clé API
python3 main.py exemple-recette.html \
  --grocy-url http://localhost:9283 \
  --api-key TA_CLE_API_ICI \
  --dry-run
```

Tu devrais voir un affichage coloré avec :
- 🔍 Extraction...
- ✓ Recette extraite
- Liste des ingrédients
- Mode dry-run activé

### 4️⃣ Test avec une vraie URL (30 secondes)

```bash
python3 main.py "https://www.marmiton.org/recettes/recette_crepes-faciles_24622.aspx" \
  --grocy-url http://localhost:9283 \
  --api-key TA_CLE_API \
  --dry-run
```

### 5️⃣ Import réel (test final)

```bash
# SANS --dry-run → va vraiment importer dans Grocy
python3 main.py exemple-recette.html \
  --grocy-url http://localhost:9283 \
  --api-key TA_CLE_API
```

Le script te demandera confirmation avant d'importer.

---

## 🎯 Checklist avant mise en prod

- [ ] Les dépendances s'installent sans erreur
- [ ] Le test automatique passe tous les tests
- [ ] L'extraction fonctionne (exemple-recette.html)
- [ ] La connexion à Grocy fonctionne
- [ ] Un import en dry-run fonctionne
- [ ] Un import réel fonctionne et la recette apparaît dans Grocy

Si tous ces points sont ✅ → **Tu peux passer en prod !**

---

## ⚡ Commandes ultra-rapides

```bash
# Installation complète
pip3 install -r requirements.txt

# Test rapide (tout en une commande)
python3 test.py

# Test extraction simple
python3 -c "from recipe_extractor import RecipeExtractor; print(RecipeExtractor().extract('exemple-recette.html')['title'])"

# Test avec vraie URL (remplace TA_CLE)
python3 main.py "https://www.marmiton.org/recettes/recette_crepes-faciles_24622.aspx" --grocy-url http://localhost:9283 --api-key TA_CLE --dry-run
```

---

## 🐛 Problèmes fréquents

**"ModuleNotFoundError: No module named 'recipe_scrapers'"**
```bash
pip3 install -r requirements.txt
# ou
python3 -m pip install -r requirements.txt
```

**"Impossible de se connecter à Grocy"**
```bash
# Teste manuellement
curl http://localhost:9283/api/system/info

# Vérifie ton URL et ton port (9283 ou 8081 ?)
```

**"Permission denied: ./test-complet.sh"**
```bash
chmod +x test-complet.sh
```

---

## 📱 Où trouver ta clé API Grocy

1. Ouvre Grocy : `http://ton-serveur:9283` (ou 8081)
2. Clique sur l'icône 🔑 (clé) en haut à droite
3. **Manage API keys**
4. **+ Add**
5. Copie la clé générée

---

## ✅ Tout fonctionne ? Passe en prod !

1. Copie le dossier sur ton serveur
2. Intègre dans docker-compose (voir DOCKER_INTEGRATION.md)
3. Enjoy ! 🎉
