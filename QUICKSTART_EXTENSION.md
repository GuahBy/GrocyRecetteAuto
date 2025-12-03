# 🎯 Quick Start - Extension Navigateur

## En 3 minutes chrono

### 1️⃣ Démarre l'API (1 min)

```bash
cd /mnt/user-data/outputs/grocy-recipe-importer

# Installer Flask
pip3 install flask flask-cors

# Démarrer l'API
export GROCY_URL="http://100.83.155.21:9283"
export GROCY_API_KEY="ta_clé"
./start-api.sh
```

✅ L'API tourne sur `http://localhost:5000`

### 2️⃣ Installe l'extension (1 min)

```bash
# Créer les icônes
cd extension
python3 create_icons.py

# OU télécharge des icônes sur https://www.flaticon.com
```

Puis dans Brave :
1. `brave://extensions`
2. "Mode développeur" → ON
3. "Charger l'extension non empaquetée"
4. Sélectionne le dossier `extension/`

### 3️⃣ Configure (30 sec)

1. Clique sur l'icône de l'extension
2. "⚙️ Configuration"
3. Remplis :
   - API : `http://localhost:5000`
   - Grocy : `http://100.83.155.21:9283`
   - Clé : ta clé Grocy
4. Sauvegarde

### 4️⃣ Teste ! (30 sec)

1. Va sur https://www.marmiton.org/recettes/recette_pate-a-crepes_12372.aspx
2. Clique sur l'extension
3. "Importer cette recette"
4. ✅ C'est dans Grocy !

## 🚀 Mode Production (Docker)

Voir [EXTENSION_GUIDE.md](EXTENSION_GUIDE.md) pour déployer avec Docker.

## 🎉 C'est tout !

Tu peux maintenant importer n'importe quelle recette en un clic depuis ton navigateur !
