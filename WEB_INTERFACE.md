# 🌐 Interface Web - Guide d'Utilisation

## 🎯 Accès

Une fois l'API démarrée, accède à l'interface web :

- **En local :** `http://localhost:5000`
- **Via ton serveur :** `http://ton-ip:5000`

## ✨ Fonctionnalités

L'interface web offre **3 méthodes d'import** :

### 1️⃣ Import par URL

1. Va sur l'onglet **"🔗 URL"**
2. Colle l'URL de la recette (Marmiton, 750g, etc.)
3. **"Prévisualiser"** pour voir la recette extraite
4. **"Importer dans Grocy"** pour l'ajouter

**Exemple :**
```
https://www.marmiton.org/recettes/recette_pate-a-crepes_12372.aspx
```

### 2️⃣ Import par Fichier

1. Va sur l'onglet **"📁 Fichier"**
2. Glisse-dépose un fichier HTML, Markdown ou TXT
3. Ou clique pour sélectionner
4. **"Importer dans Grocy"**

**Formats supportés :**
- `.html` / `.htm` - Page web sauvegardée
- `.md` - Markdown
- `.txt` - Texte brut

### 3️⃣ Import par Texte

1. Va sur l'onglet **"📝 Texte"**
2. Colle le code HTML de la page
3. **"Importer dans Grocy"**

**Comment obtenir le HTML :**
- Sur la page de recette → Clic droit → "Inspecter" ou F12
- Copie l'élément `<html>` complet
- Ou Ctrl+U pour voir le code source, puis copie tout

## 🎨 Captures d'écran

### Page d'accueil
```
┌─────────────────────────────────────┐
│   🍳 Grocy Recipe Importer          │
│   Importez des recettes en quelques │
│   clics                              │
│                                      │
│   🔗 URL  📁 Fichier  📝 Texte      │
│  ────────                            │
│                                      │
│   URL de la recette                  │
│   ┌──────────────────────────────┐  │
│   │ https://...                  │  │
│   └──────────────────────────────┘  │
│                                      │
│   👁️ Prévisualiser                  │
│   📥 Importer dans Grocy             │
│                                      │
└─────────────────────────────────────┘
```

## 🚀 Workflow Recommandé

### Pour une nouvelle recette web

1. **Sur le site de recette** : Copie l'URL
2. **Interface web** : Colle l'URL
3. **Prévisualise** pour vérifier
4. **Importe** en un clic
5. **Succès !** Lien direct vers Grocy

### Pour une recette sauvegardée

1. **Sur le site** : Ctrl+S → Sauvegarder la page
2. **Interface web** : Glisse-dépose le fichier
3. **Importe**
4. **Done !**

### Pour une recette sur un site non supporté

1. **Sur le site** : F12 → Copie le HTML
2. **Interface web** : Onglet "Texte"
3. **Colle le HTML**
4. **Importe**

## 💡 Astuces

### Raccourci navigateur

Ajoute l'interface web en signet :
- **Nom :** "Grocy Recipes"
- **URL :** `http://ton-serveur:5000`
- Ajoute à la barre de favoris

### Batch import

Ouvre plusieurs onglets de l'interface et importe plusieurs recettes en parallèle !

### Mobile friendly

L'interface est responsive, tu peux l'utiliser depuis ton smartphone !

## 🔒 Sécurité

⚠️ **Important :** L'interface web n'a pas d'authentification par défaut.

Si tu l'exposes sur Internet :
- Ajoute un reverse proxy avec authentification (Nginx, Traefik)
- Utilise Tailscale (sécurité intégrée)
- Ou ajoute une authentification basique dans l'API

## 🐛 Dépannage

### "Erreur de connexion"

- ✅ Vérifie que l'API tourne : `docker compose logs recipe-api`
- ✅ Vérifie l'URL dans ton navigateur
- ✅ Teste : `curl http://localhost:5000/health`

### "Clé API Grocy manquante"

L'API n'a pas la clé configurée. Dans `docker-compose.yml` :
```yaml
environment:
  - GROCY_API_KEY=ta_clé
```

### "Impossible d'extraire la recette"

- ✅ Le site n'est peut-être pas supporté
- ✅ Essaie avec un fichier HTML sauvegardé
- ✅ Ou utilise l'onglet "Texte" avec le HTML complet

## 🎉 Profite !

Tu as maintenant une interface web complète pour importer toutes tes recettes ! 

Plus besoin de ligne de commande, tout est visuel et intuitif 🚀
