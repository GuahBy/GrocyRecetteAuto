# 📚 Documentation - Par où commencer ?

Bienvenue ! Voici un guide pour naviguer dans la documentation.

## 🚀 Je veux juste tester rapidement !

1. **[TEST_LOCAL.md](TEST_LOCAL.md)** ← Commence ici !
   - Guide de test en 3 minutes
   - Script automatique inclus
   - Vérification que tout fonctionne

2. **[COMMANDES.md](COMMANDES.md)**
   - Commandes prêtes à copier-coller
   - Exemples concrets
   - One-liners utiles

## 📖 Je veux comprendre l'outil

1. **[README.md](README.md)**
   - Documentation complète
   - Toutes les fonctionnalités
   - Exemples détaillés

2. **[QUICKSTART.md](QUICKSTART.md)**
   - Installation en 3 étapes
   - Utilisation basique
   - Problèmes courants

## 🐳 Je veux l'intégrer dans Docker

**[DOCKER_INTEGRATION.md](DOCKER_INTEGRATION.md)**
- Ajout au docker-compose.yml
- Configuration Docker
- Utilisation avec conteneurs

## 🇫🇷 Quels sites sont supportés ?

**[SITES_SUPPORTES.md](SITES_SUPPORTES.md)**
- Liste sites français testés
- Sites internationaux
- Comment vérifier la compatibilité

## 🔮 Futures améliorations

**[ROADMAP.md](ROADMAP.md)**
- Fonctionnalités prévues
- Comment contribuer
- Idées d'améliorations

---

## 📂 Fichiers du projet

### Fichiers principaux (code)
- `main.py` - Point d'entrée CLI
- `recipe_extractor.py` - Extraction de recettes
- `grocy_client.py` - Communication avec Grocy
- `requirements.txt` - Dépendances Python

### Fichiers utilitaires
- `test.py` - Tests automatisés
- `test-complet.sh` - Script de test bash
- `import-recette.sh` - Script wrapper simplifié
- `exemple-recette.html` - Fichier de test

### Configuration
- `.env.example` - Template de configuration
- `Dockerfile` - Pour Docker
- `.gitignore` - Fichiers à ignorer

---

## 🎯 Workflow recommandé

### Première utilisation

1. **Teste en local** → [TEST_LOCAL.md](TEST_LOCAL.md)
   ```bash
   pip3 install -r requirements.txt
   ./test-complet.sh
   ```

2. **Essaye quelques imports** → [COMMANDES.md](COMMANDES.md)
   ```bash
   python3 main.py "URL" --grocy-url ... --api-key ... --dry-run
   ```

3. **Configure pour usage régulier** → [QUICKSTART.md](QUICKSTART.md)
   ```bash
   cp .env.example .env
   nano .env  # Configure tes paramètres
   ```

4. **Intègre dans Docker** → [DOCKER_INTEGRATION.md](DOCKER_INTEGRATION.md)
   ```yaml
   # Ajoute dans docker-compose.yml
   grocy-recipe-importer:
     build: ./grocy-recipe-importer
     ...
   ```

### Usage quotidien

Une fois configuré, c'est simple :

```bash
# Avec variables d'environnement
source .env
./import-recette.sh "https://marmiton.org/recette..."

# Ou avec Docker
docker-compose run --rm grocy-recipe-importer "URL"

# Ou avec ton alias perso
import-recette "URL"
```

---

## ❓ FAQ Rapide

**Q: Ça marche avec quels sites ?**  
A: 250+ sites incluant Marmiton, 750g, Cuisine AZ → [SITES_SUPPORTES.md](SITES_SUPPORTES.md)

**Q: Comment je teste sans rien casser ?**  
A: Utilise `--dry-run` → [TEST_LOCAL.md](TEST_LOCAL.md)

**Q: Je veux l'utiliser en ligne de commande simple**  
A: Configure `.env` puis utilise `import-recette.sh` → [QUICKSTART.md](QUICKSTART.md)

**Q: Je veux l'intégrer à mon serveur Docker**  
A: Suis le guide → [DOCKER_INTEGRATION.md](DOCKER_INTEGRATION.md)

**Q: Ça ne marche pas, help !**  
A: Lance `./test-complet.sh` pour diagnostiquer

**Q: Je veux améliorer l'outil**  
A: Check les idées → [ROADMAP.md](ROADMAP.md)

---

## 🆘 Besoin d'aide ?

1. **Consulte la FAQ** dans README.md
2. **Lance le diagnostic** : `./test-complet.sh`
3. **Vérifie les commandes** dans COMMANDES.md
4. **Lis le dépannage** dans TEST_LOCAL.md

---

## 🎉 Prêt à commencer ?

```bash
# Installation et test en 2 commandes
pip3 install -r requirements.txt
./test-complet.sh

# Si tout est vert, tu es prêt ! 🚀
```

Bon appétit ! 👨‍🍳
