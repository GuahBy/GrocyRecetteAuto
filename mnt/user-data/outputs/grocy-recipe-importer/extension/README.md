# Extension Navigateur Grocy Recipe Importer

## Installation rapide

### 1. Créer les icônes
```bash
python3 create_icons.py
```

### 2. Installer dans Brave/Chrome

1. Ouvre `brave://extensions` (ou `chrome://extensions`)
2. Active "Mode développeur"
3. Clique "Charger l'extension non empaquetée"
4. Sélectionne ce dossier (`extension/`)

### 3. Configurer

1. Clique sur l'icône de l'extension
2. Clique "⚙️ Configuration"
3. Remplis :
   - URL API : `http://localhost:5000`
   - URL Grocy : `http://100.83.155.21:9283`
   - Clé API : ta clé Grocy

### 4. Utiliser

Va sur une page de recette et clique sur l'extension !

## Fichiers

- `manifest.json` - Configuration de l'extension
- `popup.html` - Interface utilisateur
- `popup.js` - Logique
- `icon*.png` - Icônes (à générer)

## Besoin d'aide ?

Voir [EXTENSION_GUIDE.md](../EXTENSION_GUIDE.md) pour le guide complet.
