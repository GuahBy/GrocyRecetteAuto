# 🔌 Extension Navigateur - Guide d'Installation

## 📦 Ce que tu as maintenant

1. **API Flask** (`api.py`) - Serveur qui gère les imports
2. **Extension Navigateur** (`extension/`) - Bouton dans ton navigateur

## 🚀 Installation en 3 étapes

### Étape 1 : Démarrer l'API

```bash
cd /mnt/user-data/outputs/grocy-recipe-importer

# Installer Flask et Flask-CORS
pip3 install flask flask-cors

# Définir les variables d'environnement
export GROCY_URL="http://ton-serveur:9283"
export GROCY_API_KEY="TA-CLE-API"

# Lancer l'API
python3 api.py
```

L'API sera accessible sur `http://ton-serveur:5000`

**Pour production (avec Docker)** : Voir ci-dessous

### Étape 2 : Créer les icônes

```bash
cd extension

# Option A : Avec Python/PIL
pip3 install pillow
python3 create_icons.py

# Option B : Télécharger des icônes
# Va sur https://www.flaticon.com et cherche "recipe" ou "cooking"
# Télécharge 3 tailles : 16x16, 48x48, 128x128
```

### Étape 3 : Installer l'extension dans Brave

1. **Ouvre Brave**
2. **Va dans** `brave://extensions`
3. **Active** "Mode développeur" (coin supérieur droit)
4. **Clique** sur "Charger l'extension non empaquetée"
5. **Sélectionne** le dossier `extension/`
6. **C'est fait !** L'icône apparaît dans la barre d'outils

## ⚙️ Configuration de l'extension

1. **Clique** sur l'icône de l'extension
2. **Clique** sur "⚙️ Configuration"
3. **Remplis** :
   - **URL de l'API** : `http://localhost:5000` (ou ton IP serveur)
   - **URL Grocy** : `http://100.83.155.21:9283`
   - **Clé API Grocy** : `6GjzdHjcghEXlDkaGmpiC7sn2T2NxwGJzO8OEjYaKFW3FkLxmc`
4. **Sauvegarde**

## 🎯 Utilisation

1. **Va sur une page de recette** (Marmiton, 750g, etc.)
2. **Clique** sur l'icône de l'extension
3. **Choisis** :
   - **"Prévisualiser"** pour voir la recette extraite
   - **"Importer"** pour l'ajouter directement dans Grocy
4. **✅ C'est fait !**

## 🐳 Déploiement avec Docker (Production)

### docker-compose.yml complet

Ajoute ces services à ton docker-compose :

```yaml
  # API Recipe Importer
  recipe-api:
    build:
      context: ./grocy-recipe-importer
      dockerfile: Dockerfile.api
    container_name: recipe-api
    environment:
      - GROCY_URL=http://app:80
      - GROCY_API_KEY=${GROCY_API_KEY}
    ports:
      - 5000:5000
    restart: unless-stopped
    depends_on:
      - app
```

### Dockerfile.api

Crée ce fichier dans `grocy-recipe-importer/` :

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir flask flask-cors gunicorn

COPY *.py ./

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "api:app"]
```

### Lancer

```bash
docker-compose up -d recipe-api

# Tester
curl http://localhost:5000/health
```

## 🌐 Accès depuis Internet

Si tu veux utiliser l'extension depuis n'importe où :

### Option 1 : Tailscale (recommandé)

Tu as déjà Tailscale configuré ! Utilise :
- **URL API** : `http://ton-nom-tailscale:5000`

### Option 2 : Reverse Proxy (Nginx/Traefik)

Expose l'API derrière ton reverse proxy existant avec HTTPS.

### Option 3 : Tunnel Cloudflare

```bash
# Installer cloudflared
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o cloudflared
chmod +x cloudflared

# Créer un tunnel
./cloudflared tunnel --url http://localhost:5000
```

## 🔒 Sécurité

### ⚠️ Important

L'API n'a **pas d'authentification** pour l'instant. Pour la prod :

1. **Ajoute un token** dans l'API
2. **Utilise HTTPS** (pas HTTP)
3. **Rate limiting** pour éviter les abus

### Amélioration rapide (authentification basique)

Dans `api.py`, ajoute :

```python
API_TOKEN = os.getenv('API_TOKEN', 'change-me')

@app.before_request
def check_auth():
    if request.endpoint in ['import_recipe', 'preview_recipe']:
        token = request.headers.get('Authorization')
        if token != f'Bearer {API_TOKEN}':
            return jsonify({'error': 'Unauthorized'}), 401
```

## 🧪 Tester l'API manuellement

```bash
# Test health
curl http://ton-serveur:5000/health

# Test preview
curl -X POST http://localhost:5000/api/preview \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.marmiton.org/recettes/recette_pate-a-crepes_12372.aspx"}'

# Test import
curl -X POST http://localhost:5000/api/import \
  -H "Content-Type: application/json" \
  -d '{
    "url":"https://www.marmiton.org/recettes/recette_pate-a-crepes_12372.aspx",
    "grocy_url":"http://100.83.155.21:9283",
    "grocy_api_key":"ta_clé"
  }'
```

## 🐛 Dépannage

### Extension : "Erreur de connexion"

- ✅ Vérifie que l'API tourne : `curl http://localhost:5000/health`
- ✅ Vérifie l'URL dans la config de l'extension
- ✅ Regarde les logs de l'API

### API : "Impossible de se connecter à Grocy"

- ✅ Vérifie que Grocy est accessible depuis le serveur API
- ✅ Teste manuellement : `curl -H "GROCY-API-KEY: ta_clé" http://URL/api/system/info`

### Extension : L'icône n'apparaît pas

- ✅ Vérifie que les icônes existent (`icon16.png`, `icon48.png`, `icon128.png`)
- ✅ Recharge l'extension dans `brave://extensions`

## 🎨 Personnalisation

### Changer les couleurs de l'extension

Édite `popup.html` et modifie les gradients :

```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
/* Change vers tes couleurs préférées */
```

### Ajouter un raccourci clavier

Dans `manifest.json`, ajoute :

```json
"commands": {
  "_execute_action": {
    "suggested_key": {
      "default": "Ctrl+Shift+G"
    }
  }
}
```

## 📝 Notes

- L'extension fonctionne sur **Chrome, Brave, Edge** (tous les navigateurs Chromium)
- Pour **Firefox**, modifie le `manifest.json` en version 2
- L'API utilise **Flask** (simple) - en prod, utilise **Gunicorn** ou **uWSGI**

## 🚀 Prochaines étapes

- [ ] Ajouter authentification API
- [ ] Support de plusieurs comptes Grocy
- [ ] Historique des imports
- [ ] Bouton "Ouvrir dans Grocy"
- [ ] Stats d'utilisation

Enjoy ! 🎉
