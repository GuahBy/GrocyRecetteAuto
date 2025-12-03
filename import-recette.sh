#!/bin/bash
# Script wrapper pour importer facilement des recettes dans Grocy

# Configuration (à modifier selon votre setup)
GROCY_URL="${GROCY_URL:-http://localhost:9283}"
GROCY_API_KEY="${GROCY_API_KEY:-}"

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Vérification des prérequis
if [ -z "$GROCY_API_KEY" ]; then
    echo -e "${RED}Erreur: GROCY_API_KEY n'est pas défini${NC}"
    echo "Définissez-le avec: export GROCY_API_KEY='votre_clé'"
    echo "Ou créez un fichier .env avec vos paramètres"
    exit 1
fi

if [ -z "$1" ]; then
    echo -e "${YELLOW}Usage:${NC} $0 <URL_ou_fichier_HTML> [--dry-run]"
    echo ""
    echo "Examples:"
    echo "  $0 'https://www.marmiton.org/recettes/recette_poulet-curry.aspx'"
    echo "  $0 ~/Downloads/recette.html"
    echo "  $0 'https://750g.com/recette.htm' --dry-run"
    exit 1
fi

# Lancer l'import
echo -e "${GREEN}🍳 Import de recette vers Grocy...${NC}"
python3 main.py "$@" --grocy-url "$GROCY_URL" --api-key "$GROCY_API_KEY"
