#!/usr/bin/env python3
"""
Script de debug pour tester le parsing d'ingrédients
Permet de tester avec ta propre description et transcription
"""

from recipe_parser import RecipeParser

# Colle ici la DESCRIPTION de ton Reel Instagram
DESCRIPTION = """
Colle ici la description complète de ton Reel Instagram
"""

# Colle ici la TRANSCRIPTION audio de ton Reel
TRANSCRIPTION = """
Colle ici le texte transcrit par Whisper
"""

if __name__ == '__main__':
    print("="*60)
    print("🧪 TEST DE PARSING D'INGRÉDIENTS")
    print("="*60)
    
    # Afficher les entrées
    print("\n📝 DESCRIPTION:")
    print("-"*60)
    print(DESCRIPTION)
    
    print("\n🎤 TRANSCRIPTION:")
    print("-"*60)
    print(TRANSCRIPTION)
    
    # Parser
    print("\n🔍 PARSING EN COURS...")
    print("-"*60)
    
    parser = RecipeParser()
    result = parser.parse_recipe(DESCRIPTION, TRANSCRIPTION)
    
    # Afficher les résultats
    print("\n✅ RÉSULTATS:")
    print("="*60)
    
    print(f"\n📋 Titre: {result['title']}")
    print(f"🍽️  Portions: {result['yields']}")
    if result.get('total_time'):
        print(f"⏱️  Temps: {result['total_time']} min")
    
    print(f"\n🥘 Ingrédients détectés ({len(result['ingredients'])}):")
    print("-"*60)
    if result['ingredients']:
        for i, ing in enumerate(result['ingredients'], 1):
            print(f"  {i}. {ing}")
    else:
        print("  ⚠️ Aucun ingrédient détecté")
    
    print(f"\n📖 Instructions:")
    print("-"*60)
    instructions = result['instructions']
    if instructions:
        if len(instructions) > 300:
            print(f"  {instructions[:300]}...")
            print(f"  (+ {len(instructions) - 300} caractères)")
        else:
            print(f"  {instructions}")
    else:
        print("  ⚠️ Aucune instruction détectée")
    
    print("\n" + "="*60)
    
    # Conseils si peu d'ingrédients
    if len(result['ingredients']) < 3:
        print("\n💡 CONSEILS:")
        print("  - Vérifie que la description/transcription contient bien les ingrédients")
        print("  - Les ingrédients doivent avoir des quantités (200g, 2 carottes, etc.)")
        print("  - Ou mentionner des mots-clés: 'il faut', 'on utilise', 'ajouter', etc.")
        print("  - Essaie d'ajouter une section 'Ingrédients:' dans la description")
