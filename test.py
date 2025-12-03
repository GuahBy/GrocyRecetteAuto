#!/usr/bin/env python3
"""
Script de test pour vérifier que l'outil fonctionne correctement
"""

import sys
from pathlib import Path

def test_imports():
    """Test des imports"""
    print("🔍 Test des imports...")
    try:
        from recipe_extractor import RecipeExtractor
        from grocy_client import GrocyClient
        print("✅ Tous les modules importés avec succès")
        return True
    except ImportError as e:
        print(f"❌ Erreur d'import : {e}")
        print("\nInstallez les dépendances avec : pip install -r requirements.txt")
        return False

def test_extraction():
    """Test de l'extraction depuis le fichier exemple"""
    print("\n🔍 Test de l'extraction de recette...")
    try:
        from recipe_extractor import RecipeExtractor
        
        example_file = Path(__file__).parent / "exemple-recette.html"
        if not example_file.exists():
            print("❌ Fichier exemple-recette.html introuvable")
            return False
        
        extractor = RecipeExtractor()
        recipe = extractor.extract(str(example_file))
        
        print(f"✅ Recette extraite : {recipe['title']}")
        print(f"   - Ingrédients : {len(recipe['ingredients'])}")
        print(f"   - Portions : {recipe['yields']}")
        print(f"   - Temps total : {recipe.get('total_time', 'N/A')} min")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de l'extraction : {e}")
        return False

def test_grocy_connection():
    """Test de connexion à Grocy (optionnel)"""
    print("\n🔍 Test de connexion Grocy...")
    
    grocy_url = input("URL Grocy (ou Entrée pour skip) : ").strip()
    if not grocy_url:
        print("⏭️  Test de connexion Grocy ignoré")
        return True
    
    api_key = input("Clé API Grocy : ").strip()
    if not api_key:
        print("⏭️  Test de connexion Grocy ignoré")
        return True
    
    try:
        from grocy_client import GrocyClient
        
        client = GrocyClient(grocy_url, api_key)
        if client.test_connection():
            print("✅ Connexion à Grocy réussie")
            return True
        else:
            print("❌ Impossible de se connecter à Grocy")
            return False
    except Exception as e:
        print(f"❌ Erreur de connexion : {e}")
        return False

def main():
    print("=" * 60)
    print("🧪 Test de Grocy Recipe Importer")
    print("=" * 60)
    
    results = []
    
    # Test 1 : Imports
    results.append(test_imports())
    
    # Test 2 : Extraction
    if results[0]:
        results.append(test_extraction())
    
    # Test 3 : Connexion Grocy (optionnel)
    if all(results):
        print("\n" + "=" * 60)
        print("Tests optionnels")
        print("=" * 60)
        test_grocy_connection()
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 Résumé des tests")
    print("=" * 60)
    
    if all(results):
        print("✅ Tous les tests obligatoires ont réussi !")
        print("\nVous pouvez maintenant utiliser l'outil avec :")
        print("  python main.py <URL_ou_fichier> --grocy-url <URL> --api-key <KEY>")
    else:
        print("❌ Certains tests ont échoué")
        print("\nVérifiez les erreurs ci-dessus et installez les dépendances :")
        print("  pip install -r requirements.txt")
        sys.exit(1)

if __name__ == "__main__":
    main()
