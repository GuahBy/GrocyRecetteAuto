#!/bin/bash
# Script de démarrage rapide de l'API

echo "🚀 Démarrage de l'API Recipe Importer"
echo "======================================"
echo ""

# Vérifier les dépendances
if ! python3 -c "import flask" 2>/dev/null; then
    echo "📦 Installation de Flask..."
    pip3 install flask flask-cors
fi

# Vérifier les variables d'environnement
if [ -z "$GROCY_API_KEY" ]; then
    echo "⚠️  GROCY_API_KEY non définie!"
    echo ""
    echo "Définissez-la avec:"
    echo "  export GROCY_API_KEY='votre_clé'"
    echo ""
    echo "Ou créez un fichier .env avec:"
    echo "  GROCY_URL=http://100.83.155.21:9283"
    echo "  GROCY_API_KEY=votre_clé"
    echo ""
    read -p "Voulez-vous la définir maintenant? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "URL Grocy [http://100.83.155.21:9283]: " grocy_url
        grocy_url=${grocy_url:-http://100.83.155.21:9283}
        read -p "Clé API Grocy: " grocy_key
        
        export GROCY_URL="$grocy_url"
        export GROCY_API_KEY="$grocy_key"
        
        echo ""
        echo "✓ Variables d'environnement définies"
    else
        echo "❌ Annulé"
        exit 1
    fi
fi

echo ""
echo "Configuration:"
echo "  Grocy URL: ${GROCY_URL:-http://localhost:9283}"
echo "  API Key: ${GROCY_API_KEY:0:10}..."
echo ""
echo "L'API sera accessible sur: http://localhost:5000"
echo ""
echo "Utilisez Ctrl+C pour arrêter"
echo ""
echo "======================================"
echo ""

# Démarrer l'API
python3 api.py
