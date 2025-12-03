# Sites de Recettes Français Supportés 🇫🇷

Voici une liste de sites français populaires compatibles avec l'outil :

## ✅ Sites testés et fonctionnels

### Marmiton
- URL type : `https://www.marmiton.org/recettes/recette_[nom-recette]_[id].aspx`
- Exemple : `https://www.marmiton.org/recettes/recette_poulet-au-curry_166854.aspx`
- **Excellent support** - Métadonnées complètes

### 750g
- URL type : `https://www.750g.com/[nom-recette]-r[id].htm`
- Exemple : `https://www.750g.com/tarte-aux-pommes-r12345.htm`
- **Bon support** - Temps et ingrédients bien parsés

### Cuisine AZ
- URL type : `https://www.cuisineaz.com/recettes/[nom-recette]-[id].aspx`
- Exemple : `https://www.cuisineaz.com/recettes/gratin-dauphinois-12345.aspx`
- **Support correct**

### Journal des Femmes Cuisine
- URL type : `https://cuisine.journaldesfemmes.fr/recette/[id]-[nom]`
- Exemple : `https://cuisine.journaldesfemmes.fr/recette/1234567-tiramisu-facile`
- **Bon support**

### Ptitchef
- URL type : `https://www.ptitchef.com/recettes/[categorie]/[nom]-fid-[id]`
- Exemple : `https://www.ptitchef.com/recettes/plat/quiche-lorraine-fid-12345`
- **Support correct**

### Ricardo Cuisine (Québec)
- URL type : `https://www.ricardocuisine.com/recettes/[id]-[nom]`
- Exemple : `https://www.ricardocuisine.com/recettes/1234-poutine-classique`
- **Excellent support**

## 🌍 Sites internationaux populaires (aussi supportés)

- AllRecipes
- BBC Food / BBC Good Food
- Food Network
- Serious Eats
- NYT Cooking
- Bon Appétit
- Epicurious
- Tasty
- Et 200+ autres...

## 🧪 Comment tester si un site est supporté

```bash
# Mode dry-run pour tester sans importer
python main.py "URL_DU_SITE" \
  --grocy-url http://localhost:9283 \
  --api-key VOTRE_CLE \
  --dry-run
```

Si ça affiche les ingrédients et instructions, c'est supporté ! ✅

## 💡 Astuces pour les sites non supportés

Si un site n'est pas directement supporté :

1. **Sauvegardez la page HTML** (Ctrl+S dans votre navigateur)
2. **Importez le fichier local** :
   ```bash
   python main.py ~/Downloads/recette.html --grocy-url ... --api-key ...
   ```
3. Le parser essaiera d'extraire les données même sans support spécifique (mode "wild")

## 📝 Signaler un site non supporté

Si un site français populaire ne fonctionne pas, vous pouvez :
- Créer une issue sur le repo recipe-scrapers : https://github.com/hhursev/recipe-scrapers
- Ou me le signaler pour que j'ajoute un parser custom

## 🔍 Vérifier le support d'un site

La bibliothèque recipe-scrapers utilise les métadonnées **Schema.org**. 

Pour vérifier si un site les utilise :
1. Allez sur la page de la recette
2. Faites "Voir le code source" (Ctrl+U)
3. Cherchez `"@type": "Recipe"` dans le code
4. Si présent → Le site est supporté ✅

## 📊 Qualité de l'extraction

| Site | Ingrédients | Instructions | Temps | Image | Note |
|------|------------|--------------|-------|-------|------|
| Marmiton | ✅ | ✅ | ✅ | ✅ | Excellent |
| 750g | ✅ | ✅ | ✅ | ✅ | Excellent |
| Cuisine AZ | ✅ | ✅ | ⚠️ | ✅ | Bon |
| JDF Cuisine | ✅ | ✅ | ✅ | ✅ | Bon |
| Ptitchef | ✅ | ✅ | ⚠️ | ✅ | Correct |

Légende : ✅ Parfait | ⚠️ Partiel | ❌ Non supporté

## 🚀 Exemples de commandes complètes

### Marmiton - Poulet au curry
```bash
python main.py \
  "https://www.marmiton.org/recettes/recette_poulet-au-curry_166854.aspx" \
  --grocy-url http://localhost:9283 \
  --api-key votre_clé
```

### 750g - Tarte aux pommes
```bash
python main.py \
  "https://www.750g.com/tarte-aux-pommes-r12345.htm" \
  --grocy-url http://localhost:9283 \
  --api-key votre_clé
```

### Cuisine AZ - Gratin dauphinois
```bash
python main.py \
  "https://www.cuisineaz.com/recettes/gratin-dauphinois-12345.aspx" \
  --grocy-url http://localhost:9283 \
  --api-key votre_clé
```

Happy cooking! 👨‍🍳
