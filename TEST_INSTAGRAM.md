# 🧪 Test Instagram Import - Guide Rapide

## ⚡ Test en local (avant déploiement)

### 1. Installer les dépendances

```bash
cd /mnt/user-data/outputs/grocy-recipe-importer

# Installer ffmpeg (si pas déjà fait)
sudo apt-get update && sudo apt-get install ffmpeg

# Installer les dépendances Python
pip3 install -r requirements.txt
pip3 install flask flask-cors yt-dlp openai-whisper torch
```

### 2. Tester chaque composant

#### Test 1 : Téléchargement Instagram

```bash
# Trouver un Reel public avec une recette
# Exemple: https://www.instagram.com/reel/ABC123/

python3 instagram_scraper.py "https://www.instagram.com/reel/ABC123/"
```

✅ Tu devrais voir :
- Téléchargement de la vidéo
- Extraction de l'audio
- Description affichée

#### Test 2 : Transcription

```bash
# Utilise l'audio du test précédent
python3 audio_transcriber.py /tmp/instagram_*/audio.mp3
```

✅ Tu devrais voir :
- Chargement du modèle Whisper (première fois = téléchargement)
- Transcription du texte français

**Note** : La première fois, Whisper téléchargera le modèle (~500MB pour "base")

#### Test 3 : Parsing

```bash
# Test intégré dans le fichier
python3 recipe_parser.py
```

✅ Tu devrais voir :
- Parsing d'une recette test
- Ingrédients extraits
- Instructions formatées

### 3. Tester l'API complète

```bash
# Lancer l'API en mode dev
export GROCY_URL="http://ton-serveur:9283"
export GROCY_API_KEY="ta_clé"

python3 api.py
```

Ouvre un autre terminal et teste :

```bash
curl -X POST http://ton-serveur:5000/api/import/instagram \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.instagram.com/reel/ABC123/"
  }'
```

✅ Tu devrais voir :
```json
{
  "success": true,
  "message": "Recette 'Nom de la recette' importée depuis Instagram",
  "data": {
    "recipe_id": 6,
    "title": "Nom de la recette",
    "ingredients_count": 5,
    "grocy_url": "http://ton-serveur:9283/#recipe/6"
  }
}
```

### 4. Tester l'interface web

1. Garde l'API lancée (`python3 api.py`)
2. Va sur `http://ton-serveur:5000`
3. Onglet **"📸 Instagram"**
4. Colle une URL de Reel
5. Clique **"Importer"**

## ⏱️ Temps d'exécution

**Pour un Reel de 60 secondes sur ton Xeon X3430 :**
- Téléchargement : ~5-10s
- Extraction audio : ~2-3s
- Transcription (modèle medium) : ~120-180s
- Parsing + Import : ~5s

**Total : ~2-3 minutes**

## 🚨 Problèmes courants

### "Login required"

Certains Reels nécessitent une connexion. Utilise des Reels publics.

### Timeout

Si le Reel est trop long (>90s), augmente le timeout dans `instagram_scraper.py` :

```python
timeout=120  # → timeout=300
```

### Modèle Whisper trop lent

Change pour `tiny` :

```python
transcriber = AudioTranscriber(model_name="tiny")
```

## ✅ Si tout fonctionne

Tu peux déployer en production ! 🚀

```bash
# Push sur GitHub
git add .
git commit -m "Add Instagram Reels support"
git push

# Sur le serveur
cd ~/docker/grocy-recipe-importer
git pull
cd ..
docker compose build --no-cache recipe-api
docker compose up -d recipe-api
```

## 🎯 Reels de test recommandés

Cherche des Reels avec ces hashtags :
- #recette
- #recipefr
- #recettefacile
- #cuisinefrancaise

Comptes recommandés :
- @chefclub
- @marmiton_org
- @750grammes

Bon test ! 🧪
