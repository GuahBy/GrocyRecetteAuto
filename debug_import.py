#!/usr/bin/env python3
"""
Script de debug pour comprendre pourquoi l'import ne fonctionne pas
"""

import sys
import json
import requests
from recipe_extractor import RecipeExtractor
from grocy_client import GrocyClient

def main():
    if len(sys.argv) < 4:
        print("Usage: python3 debug_import.py <source> <grocy_url> <api_key>")
        print("Example: python3 debug_import.py exemple-recette.html http://localhost:9283 ta_clé")
        sys.exit(1)
    
    source = sys.argv[1]
    grocy_url = sys.argv[2]
    api_key = sys.argv[3]
    
    print("=" * 60)
    print("🔍 DEBUG IMPORT GROCY")
    print("=" * 60)
    print(f"Source: {source}")
    print(f"Grocy URL: {grocy_url}")
    print(f"API Key: {api_key[:10]}...{api_key[-4:]}")
    print()
    
    # Test 1 : Extraction
    print("=" * 60)
    print("Test 1 : Extraction de la recette")
    print("=" * 60)
    try:
        extractor = RecipeExtractor()
        recipe_data = extractor.extract(source)
        print(f"✅ Extraction réussie")
        print(f"   Titre: {recipe_data['title']}")
        print(f"   Ingrédients: {len(recipe_data['ingredients'])}")
        print(f"   Instructions: {len(recipe_data['instructions'])} caractères")
        print()
    except Exception as e:
        print(f"❌ Erreur extraction: {e}")
        sys.exit(1)
    
    # Test 2 : Connexion Grocy
    print("=" * 60)
    print("Test 2 : Connexion à Grocy")
    print("=" * 60)
    try:
        response = requests.get(
            f"{grocy_url}/api/system/info",
            headers={'GROCY-API-KEY': api_key},
            timeout=5
        )
        print(f"Status code: {response.status_code}")
        if response.status_code == 200:
            info = response.json()
            print(f"✅ Connexion réussie")
            print(f"   Version Grocy: {info.get('grocy_version', {}).get('Version', 'N/A')}")
        else:
            print(f"❌ Erreur de connexion")
            print(f"   Response: {response.text}")
            sys.exit(1)
        print()
    except Exception as e:
        print(f"❌ Erreur connexion: {e}")
        sys.exit(1)
    
    # Test 3 : Création de la recette
    print("=" * 60)
    print("Test 3 : Création de la recette dans Grocy")
    print("=" * 60)
    
    # Préparer le payload
    from grocy_client import GrocyClient
    client = GrocyClient(grocy_url, api_key)
    
    recipe_payload = {
        'name': recipe_data['title'],
        'description': client._format_description(recipe_data),
        'base_servings': client._extract_servings_number(recipe_data['yields']),
        'desired_servings': client._extract_servings_number(recipe_data['yields']),
        'not_check_shoppinglist': 0
    }
    
    print("Payload à envoyer:")
    print(json.dumps(recipe_payload, indent=2, ensure_ascii=False)[:500] + "...")
    print()
    
    try:
        response = requests.post(
            f"{grocy_url}/api/objects/recipes",
            headers={
                'GROCY-API-KEY': api_key,
                'Content-Type': 'application/json'
            },
            json=recipe_payload,
            timeout=10
        )
        
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
        print()
        
        if response.status_code in [200, 201]:
            result = response.json()
            recipe_id = result.get('created_object_id')
            print(f"✅ Recette créée avec succès!")
            print(f"   ID: {recipe_id}")
            print(f"   Lien: {grocy_url}/#recipe/{recipe_id}")
        else:
            print(f"❌ Erreur lors de la création")
            print(f"   Code: {response.status_code}")
            print(f"   Message: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Test 4 : Vérification dans Grocy
    print()
    print("=" * 60)
    print("Test 4 : Vérification dans Grocy")
    print("=" * 60)
    try:
        response = requests.get(
            f"{grocy_url}/api/objects/recipes",
            headers={'GROCY-API-KEY': api_key},
            timeout=5
        )
        if response.status_code == 200:
            recipes = response.json()
            print(f"✅ {len(recipes)} recette(s) totale(s) dans Grocy:")
            for r in recipes[-5:]:  # Afficher les 5 dernières
                print(f"   - [{r['id']}] {r['name']}")
        else:
            print(f"⚠️ Impossible de lister les recettes")
    except Exception as e:
        print(f"⚠️ Erreur: {e}")
    
    print()
    print("=" * 60)
    print("🎉 Debug terminé")
    print("=" * 60)

if __name__ == "__main__":
    main()
