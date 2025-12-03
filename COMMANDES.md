# 📋 Commandes à Copier-Coller

## Installation et test (à lancer dans l'ordre)

### 1. Installation
```bash
cd grocy-recipe-importer
pip3 install -r requirements.txt
```

### 2. Test automatique complet
```bash
./test-complet.sh
```

### 3. Test extraction basique (sans Grocy)
```bash
python3 -c "
from recipe_extractor import RecipeExtractor
extractor = RecipeExtractor()
recipe = extractor.extract('exemple-recette.html')
print(f'✅ Titre: {recipe[\"title\"]}')
print(f'✅ Ingrédients: {len(recipe[\"ingredients\"])}')
print(f'✅ Portions: {recipe[\"yields\"]}')
"
```

---

## Test avec Grocy (remplace les valeurs)

### Configuration
```bash
# Définis tes variables (REMPLACE LES VALEURS!)
export GROCY_URL="http://localhost:9283"
export GROCY_API_KEY="ta_clé_api_ici"
```

### Test dry-run (fichier exemple)
```bash
python3 main.py exemple-recette.html \
  --grocy-url $GROCY_URL \
  --api-key $GROCY_API_KEY \
  --dry-run
```

### Test dry-run (URL Marmiton)
```bash
python3 main.py "https://www.marmiton.org/recettes/recette_crepes-faciles_24622.aspx" \
  --grocy-url $GROCY_URL \
  --api-key $GROCY_API_KEY \
  --dry-run
```

### Import RÉEL (sans dry-run)
```bash
python3 main.py exemple-recette.html \
  --grocy-url $GROCY_URL \
  --api-key $GROCY_API_KEY
```

---

## Exemples de sites français

### Marmiton - Crêpes
```bash
python3 main.py "https://www.marmiton.org/recettes/recette_crepes-faciles_24622.aspx" \
  --grocy-url $GROCY_URL \
  --api-key $GROCY_API_KEY \
  --dry-run
```

### 750g - Tarte aux pommes
```bash
python3 main.py "https://www.750g.com/tarte-aux-pommes-r13223.htm" \
  --grocy-url $GROCY_URL \
  --api-key $GROCY_API_KEY \
  --dry-run
```

### Cuisine AZ - Gratin dauphinois
```bash
python3 main.py "https://www.cuisineaz.com/recettes/gratin-dauphinois-11978.aspx" \
  --grocy-url $GROCY_URL \
  --api-key $GROCY_API_KEY \
  --dry-run
```

---

## Utilisation avec le script wrapper

### Configuration permanente
```bash
# Créer ton fichier .env
cp .env.example .env

# Éditer avec tes valeurs
nano .env
# Modifier GROCY_URL et GROCY_API_KEY

# Charger la config
source .env
```

### Utilisation simplifiée
```bash
# Une fois .env chargé, c'est ultra simple :
./import-recette.sh "https://www.marmiton.org/recettes/recette_poulet-curry.aspx"
```

---

## Test de connexion Grocy

### Vérifier que Grocy est accessible
```bash
curl http://localhost:9283/api/system/info
# ou avec ton IP
curl http://192.168.1.X:9283/api/system/info
```

### Test avec authentification
```bash
curl -H "GROCY-API-KEY: ta_clé" http://localhost:9283/api/system/info
```

Si tu vois du JSON → Grocy est accessible ✅

---

## Commandes de débogage

### Voir la version de Python
```bash
python3 --version
```

### Lister les modules installés
```bash
pip3 list | grep -E "recipe-scrapers|requests|rich"
```

### Tester l'import des modules
```bash
python3 -c "import recipe_scrapers; import requests; from rich.console import Console; print('✅ Tous les modules OK')"
```

### Voir les logs détaillés
```bash
# Ajoute -v ou --verbose (à implémenter si besoin)
python3 main.py "URL" --grocy-url ... --api-key ... -v
```

---

## Raccourcis pratiques

### Créer un alias
Ajoute dans ton `~/.bashrc` ou `~/.zshrc` :

```bash
alias import-recette='cd /chemin/vers/grocy-recipe-importer && source .env && ./import-recette.sh'
```

Puis :
```bash
source ~/.bashrc  # ou ~/.zshrc
import-recette "https://recette.com/..."
```

### Fonction bash avancée
```bash
# Ajoute dans ~/.bashrc
function grocy-import() {
    cd /chemin/vers/grocy-recipe-importer
    source .env
    python3 main.py "$1" --grocy-url $GROCY_URL --api-key $GROCY_API_KEY "${@:2}"
}
```

Utilisation :
```bash
grocy-import "https://marmiton.org/..." --dry-run
```

---

## One-liners utiles

### Installation + test en une ligne
```bash
pip3 install -r requirements.txt && python3 test.py
```

### Test extraction simple
```bash
python3 -c "from recipe_extractor import RecipeExtractor; print(RecipeExtractor().extract('exemple-recette.html')['title'])"
```

### Vérifier connexion Grocy
```bash
python3 -c "from grocy_client import GrocyClient; c = GrocyClient('http://localhost:9283', 'ta_clé'); print('✅ OK' if c.test_connection() else '❌ FAIL')"
```

---

## Batch import (pour plus tard)

### Créer un fichier avec plusieurs URLs
```bash
cat > recettes.txt <<EOF
https://www.marmiton.org/recettes/recette_crepes-faciles_24622.aspx
https://www.750g.com/tarte-aux-pommes-r13223.htm
https://www.cuisineaz.com/recettes/gratin-dauphinois-11978.aspx
EOF
```

### Importer toutes les recettes
```bash
while read url; do
    python3 main.py "$url" --grocy-url $GROCY_URL --api-key $GROCY_API_KEY
    sleep 2  # Pause de 2 secondes entre chaque import
done < recettes.txt
```

---

## Besoin d'aide ?

1. Vérifie TEST_LOCAL.md pour le guide détaillé
2. Lance `./test-complet.sh` pour diagnostiquer
3. Consulte la section dépannage dans README.md
