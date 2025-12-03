# Roadmap & Idées d'Améliorations

## 🎯 Version Actuelle : 1.0.0

### ✅ Fonctionnalités actuelles
- Extraction depuis URL ou fichier HTML
- Support de 250+ sites via recipe-scrapers
- Import dans Grocy via API REST
- CLI avec affichage coloré (rich)
- Mode dry-run
- Gestion des erreurs
- Docker ready

## 🚀 Améliorations Prioritaires

### 1. Mapping automatique des ingrédients → Produits Grocy
**Problème actuel** : Les ingrédients sont juste dans la description
**Amélioration** : 
- Récupérer la liste des produits existants dans Grocy
- Faire du fuzzy matching pour associer ingrédients → produits
- Demander confirmation en mode interactif
- Créer automatiquement les produits manquants

**Implémentation** :
```python
# Pseudo-code
def map_ingredient_to_product(ingredient: str, grocy_products: list):
    # Normaliser l'ingrédient (enlever quantités, unités)
    clean_ingredient = normalize(ingredient)
    
    # Chercher correspondance exacte
    exact_match = find_exact(clean_ingredient, grocy_products)
    if exact_match:
        return exact_match
    
    # Fuzzy matching (fuzzywuzzy)
    fuzzy_matches = get_fuzzy_matches(clean_ingredient, grocy_products)
    if fuzzy_matches:
        # Demander confirmation à l'utilisateur
        return ask_user_choice(fuzzy_matches)
    
    # Proposer création nouveau produit
    return create_new_product(clean_ingredient)
```

### 2. Import d'images
**Problème actuel** : Les images ne sont pas importées
**Amélioration** :
- Télécharger l'image de la recette
- L'uploader dans Grocy via l'API files
- Associer à la recette

### 3. Mode batch (import multiple)
```bash
# Fichier avec plusieurs URLs
python main.py --batch recettes.txt --grocy-url ... --api-key ...
```

Contenu de `recettes.txt` :
```
https://marmiton.org/recette1
https://750g.com/recette2
https://cuisineaz.com/recette3
```

### 4. Interface web simple
- Mini serveur Flask
- Upload de fichier HTML
- Ou paste d'URL
- Prévisualisation avant import
- Configuration persistante (URL Grocy, API key)

**Stack technique** :
- Flask pour le backend
- Tailwind CSS pour le frontend
- HTMX pour l'interactivité sans JS lourd

### 5. Gestion intelligente des unités
**Problème** : "2 tasses" → besoin de convertir en unités métriques
**Solution** : Bibliothèque de conversion d'unités
```python
from pint import UnitRegistry
ureg = UnitRegistry()

# Conversion automatique
quantity = ureg("2 cups")
ml_quantity = quantity.to("milliliters")
```

### 6. Mode interactif amélioré
```bash
python main.py --interactive "URL"

# Affichage :
# ┌─────────────────────────────────┐
# │ Recette extraite : Poulet curry │
# ├─────────────────────────────────┤
# │ ✓ Titre : Poulet au curry       │
# │ ✓ 8 ingrédients trouvés         │
# │ ✓ Instructions OK               │
# │ ⚠ Temps manquant                │
# └─────────────────────────────────┘
#
# Voulez-vous :
# 1. Éditer le titre
# 2. Ajouter/modifier ingrédients
# 3. Ajouter temps manuellement
# 4. Importer tel quel
# 5. Annuler
```

### 7. Plugin Grocy
Intégrer directement dans l'interface Grocy :
- Bouton "Import depuis URL" dans Grocy
- Pas besoin de CLI

### 8. Support OCR pour recettes scannées
```bash
python main.py photo-recette.jpg --ocr --grocy-url ... --api-key ...
```
Avec Tesseract ou API cloud (Google Vision, AWS Textract)

### 9. Notifications & Logs
- Historique des imports
- Notification quand import réussi
- Webhook vers Discord/Slack/Telegram

### 10. API REST
Exposer l'outil comme API :
```bash
POST /api/import
{
  "url": "https://marmiton.org/...",
  "grocy_url": "http://localhost:9283",
  "grocy_api_key": "..."
}
```

## 🐛 Bugs Connus

Aucun pour le moment ! Signalez-en si vous en trouvez.

## 💡 Idées Communautaires

Tu as une idée ? Ajoute-la ici ou crée une issue !

### Template d'idée
```markdown
### [TITRE DE L'IDÉE]
**Problème** : Description du problème actuel
**Solution proposée** : Comment le résoudre
**Complexité** : 🟢 Facile | 🟡 Moyen | 🔴 Complexe
**Priorité** : ⭐ Nice to have | ⭐⭐ Important | ⭐⭐⭐ Critique
```

## 📊 Priorisation

| Fonctionnalité | Priorité | Complexité | Valeur |
|----------------|----------|------------|--------|
| Mapping ingrédients | ⭐⭐⭐ | 🟡 | Haute |
| Import images | ⭐⭐ | 🟡 | Moyenne |
| Mode batch | ⭐⭐ | 🟢 | Haute |
| Interface web | ⭐⭐ | 🔴 | Haute |
| Conversion unités | ⭐ | 🟡 | Moyenne |
| Mode interactif | ⭐⭐ | 🟡 | Moyenne |
| Plugin Grocy | ⭐ | 🔴 | Haute |
| OCR | ⭐ | 🔴 | Faible |
| Notifications | ⭐ | 🟢 | Faible |
| API REST | ⭐ | 🟡 | Moyenne |

## 🎓 Améliorations Techniques

### Code Quality
- [ ] Ajouter des tests unitaires (pytest)
- [ ] Type hints complets
- [ ] Docstrings Google style
- [ ] CI/CD avec GitHub Actions
- [ ] Coverage >80%

### Performance
- [ ] Cache des produits Grocy
- [ ] Parallel processing pour batch
- [ ] Async requests

### Sécurité
- [ ] Ne jamais logger les API keys
- [ ] Validation des URLs
- [ ] Sanitization du HTML

## 🤝 Comment Contribuer

Si tu veux implémenter une de ces fonctionnalités :

1. Fork le projet
2. Crée une branche : `git checkout -b feature/mapping-ingredients`
3. Code & teste
4. Commit : `git commit -m "feat: add ingredient mapping"`
5. Push : `git push origin feature/mapping-ingredients`
6. Ouvre une PR

Merci ! 🙏
