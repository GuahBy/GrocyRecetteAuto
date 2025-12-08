# 📸 Import depuis Instagram Reels

## 🎯 Fonctionnalités

Ce module permet d'importer des recettes depuis Instagram Reels en :

1. **Téléchargeant le Reel** avec yt-dlp
2. **Extrayant la description** du post
3. **Transcrivant l'audio** avec Whisper
4. **Parsant les ingrédients** et les étapes
5. **Important dans Grocy** automatiquement

## 🚀 Utilisation

### Via l'interface web

1. Va sur `http://ton-serveur:5000`
2. Clique sur l'onglet **"📸 Instagram"**
3. Colle l'URL du Reel : `https://www.instagram.com/reel/ABC123/`
4. Clique **"Importer depuis Instagram"**
5. Attends 1-2 minutes ⏱️
6. ✅ La recette est dans Grocy !

### Via API

```bash
curl -X POST http://localhost:5000/api/import/instagram \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.instagram.com/reel/ABC123/"
  }'
```

### Via ligne de commande

```bash
# Test de téléchargement
python3 instagram_scraper.py "https://www.instagram.com/reel/ABC123/"

# Test de transcription
python3 audio_transcriber.py chemin/vers/audio.mp3

# Test du parsing
python3 recipe_parser.py
```

## 📋 Prérequis

### Dépendances système

- **ffmpeg** (pour extraire l'audio)
- **yt-dlp** (pour télécharger les Reels)

```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Télécharger depuis https://ffmpeg.org/
```

### Dépendances Python

Toutes installées automatiquement avec Docker, sinon :

```bash
pip install yt-dlp openai-whisper torch
```

## ⚙️ Configuration

### Modèle Whisper

Par défaut, le modèle **"base"** est utilisé (compromis vitesse/qualité).

**Modèles disponibles :**
- `tiny` - ~39M params, très rapide, moins précis (~500MB téléchargement)
- `base` - ~74M params, bon compromis (~500MB)
- `small` - ~244M params, meilleure qualité (~1.5GB)
- `medium` - ~769M params, très précis (~3GB) ✅ **RECOMMANDÉ**
- `large` - ~1550M params, le meilleur (~6GB) ⚠️ Très lent sur CPU

Pour changer le modèle dans `api.py` :

```python
transcriber = AudioTranscriber(model_name="small")  # au lieu de "base"
```

### Performances CPU

**Ton Xeon X3430 (4 cores, 16GB RAM) :**
- Modèle `tiny` : ~15-20 secondes pour 60s audio
- Modèle `base` : ~30-45 secondes pour 60s audio
- Modèle `small` : ~60-90 secondes pour 60s audio
- Modèle `medium` : ~120-180 secondes pour 60s audio ✅

## 🎬 Process complet

```
URL Instagram Reel
    ↓
[1/5] Téléchargement vidéo + métadonnées
    ├─ Vidéo (.mp4)
    ├─ Audio (.mp3, 16kHz mono)
    └─ Description
    ↓
[2/5] Transcription audio avec Whisper
    └─ Texte français transcrit
    ↓
[3/5] Parsing de la recette
    ├─ Fusion description + transcription
    ├─ Extraction ingrédients (regex + patterns)
    └─ Extraction étapes
    ↓
[4/5] Connexion Grocy
    ↓
[5/5] Import dans Grocy
    ├─ Création produits manquants
    ├─ Création unités (g, ml, etc.)
    └─ Ajout de la recette
    ↓
[Nettoyage] Suppression fichiers temporaires
    ↓
✅ Terminé !
```

## 📊 Exemples de Reels supportés

### Format typique qui fonctionne bien

**Description :**
```
🍪 Cookies au chocolat ultra moelleux

Ingrédients :
- 200g de farine
- 100g de beurre
- 150g de sucre
- 2 oeufs
- 200g de chocolat

Préparation :
Mélanger tous les ingrédients.
Former des boules.
Cuire 12min à 180°C.

#recette #cookies #gourmandise
```

**Audio (transcrit) :**
> "Bonjour à tous ! Aujourd'hui on fait des cookies. On commence par mélanger le beurre et le sucre, puis on ajoute les oeufs..."

### Résultat dans Grocy

- ✅ **Titre** : "Cookies au chocolat ultra moelleux"
- ✅ **Ingrédients** : 5 ingrédients créés automatiquement
- ✅ **Instructions** : Étapes fusionnées (description + audio)
- ✅ **Portions** : Détecté automatiquement
- ✅ **Temps** : Extrait (12min)

## 🐛 Dépannage

### "yt-dlp: command not found"

```bash
pip install yt-dlp
```

### "ffmpeg: command not found"

```bash
sudo apt-get install ffmpeg
```

### Transcription trop lente

Utilise le modèle `tiny` :

```python
transcriber = AudioTranscriber(model_name="tiny")
```

### Reel privé ou protégé

Instagram bloque l'accès aux Reels privés. Le Reel doit être public.

### "Login required"

Certains Reels nécessitent une authentification. Solutions :

1. **Copier la description manuellement** et utiliser l'onglet "Texte"
2. **Télécharger le Reel** manuellement et utiliser l'onglet "Fichier"

### Ingrédients mal parsés

Le parsing est basé sur des patterns. Si les ingrédients sont mal détectés :

1. Vérifie que le format est clair (quantité + unité + nom)
2. Utilise des mots-clés : "Ingrédients :", "Il faut :", etc.
3. Corrige manuellement dans Grocy après import

## 🔮 Améliorations futures

- [ ] Support des stories Instagram
- [ ] Support TikTok
- [ ] OCR pour texte affiché dans la vidéo
- [ ] Détection automatique des recettes (ML)
- [ ] Import batch (plusieurs Reels d'un coup)
- [ ] Authentification Instagram pour Reels privés
- [ ] Cache des transcriptions (éviter de re-transcrire)

## 💡 Astuces

### Profils Instagram à suivre

Ces comptes postent souvent des recettes bien formatées :
- @chefclub
- @marmiton_org
- @750grammes
- @cuisineaz

### Format idéal pour l'extraction

Pour maximiser la qualité :
1. **Description claire** avec sections distinctes
2. **Quantités précises** (200g, 2 cuillères, etc.)
3. **Audio clair** sans musique trop forte
4. **Langue française** bien articulée

## 📞 Support

Si tu rencontres des problèmes :

1. Vérifie les logs : `docker compose logs -f recipe-api`
2. Teste chaque module séparément (voir "Via ligne de commande")
3. Ouvre une issue sur GitHub avec :
   - L'URL du Reel
   - Les logs d'erreur
   - La description du problème

Bon appétit ! 🍳
