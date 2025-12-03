#!/bin/bash
# Script de test complet pour Grocy Recipe Importer

echo "======================================"
echo "🧪 Test Grocy Recipe Importer"
echo "======================================"
echo ""

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Compteur de tests
TESTS_PASSED=0
TESTS_FAILED=0

# Fonction de test
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    echo -e "${BLUE}Test :${NC} $test_name"
    if eval "$test_command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASS${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC}"
        ((TESTS_FAILED++))
    fi
    echo ""
}

# Test 1 : Python installé
run_test "Python 3 installé" "python3 --version"

# Test 2 : Dépendances
echo -e "${BLUE}Test :${NC} Dépendances Python"
if python3 -c "import recipe_scrapers; import requests; from rich.console import Console" 2>/dev/null; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL - Installez avec: pip3 install -r requirements.txt${NC}"
    ((TESTS_FAILED++))
fi
echo ""

# Test 3 : Fichiers présents
run_test "Fichiers du projet présents" "test -f main.py && test -f recipe_extractor.py && test -f grocy_client.py"

# Test 4 : Extraction depuis fichier exemple
echo -e "${BLUE}Test :${NC} Extraction depuis fichier exemple"
if python3 -c "
from recipe_extractor import RecipeExtractor
extractor = RecipeExtractor()
recipe = extractor.extract('exemple-recette.html')
assert recipe['title'] == 'Poulet au curry maison'
assert len(recipe['ingredients']) == 8
print('OK')
" 2>/dev/null | grep -q "OK"; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((TESTS_FAILED++))
fi
echo ""

# Test 5 : Connexion Grocy (optionnel)
echo -e "${BLUE}Test :${NC} Connexion Grocy (optionnel)"
echo -e "${YELLOW}Entrez l'URL de votre Grocy (ou Entrée pour skip):${NC}"
read -r GROCY_URL

if [ -z "$GROCY_URL" ]; then
    echo -e "${YELLOW}⏭️  Test ignoré${NC}"
else
    echo -e "${YELLOW}Entrez votre clé API Grocy:${NC}"
    read -r GROCY_API_KEY
    
    if curl -s -H "GROCY-API-KEY: $GROCY_API_KEY" "$GROCY_URL/api/system/info" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Connexion Grocy OK${NC}"
        
        # Test dry-run
        echo ""
        echo -e "${BLUE}Test dry-run avec fichier exemple...${NC}"
        python3 main.py exemple-recette.html \
            --grocy-url "$GROCY_URL" \
            --api-key "$GROCY_API_KEY" \
            --dry-run
    else
        echo -e "${RED}✗ Connexion Grocy échouée${NC}"
    fi
fi
echo ""

# Résumé
echo "======================================"
echo "📊 Résumé des tests"
echo "======================================"
echo -e "${GREEN}Tests réussis : $TESTS_PASSED${NC}"
if [ $TESTS_FAILED -gt 0 ]; then
    echo -e "${RED}Tests échoués : $TESTS_FAILED${NC}"
    echo ""
    echo "⚠️  Certains tests ont échoué. Vérifiez les erreurs ci-dessus."
    exit 1
else
    echo -e "${GREEN}Tests échoués : 0${NC}"
    echo ""
    echo "✅ Tous les tests sont passés !"
    echo ""
    echo "🎉 L'outil est prêt à l'emploi !"
    echo ""
    echo "Prochaines étapes :"
    echo "1. Test avec une URL réelle :"
    echo "   python3 main.py 'https://www.marmiton.org/recettes/recette_crepes-faciles_24622.aspx' \\"
    echo "     --grocy-url http://localhost:9283 \\"
    echo "     --api-key VOTRE_CLE \\"
    echo "     --dry-run"
    echo ""
    echo "2. Import réel (sans --dry-run)"
    echo ""
    echo "3. Intégration Docker (voir DOCKER_INTEGRATION.md)"
fi
