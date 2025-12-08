#!/usr/bin/env python3
"""
Script de test complet pour importer un Reel Instagram
Sans passer par l'API, pour tester chaque étape
"""

import sys
from instagram_scraper import InstagramScraper
from audio_transcriber import AudioTranscriber
from recipe_parser import RecipeParser
from grocy_client import GrocyClient
import os

def test_instagram_import(url: str, grocy_url: str, grocy_api_key: str):
    """
    Teste l'import complet d'un Reel Instagram dans Grocy
    
    Args:
        url: URL du Reel Instagram
        grocy_url: URL de Grocy
        grocy_api_key: Clé API Grocy
    """
    print("\n" + "="*60)
    print("🧪 TEST COMPLET - Import Instagram → Grocy")
    print("="*60)
    print(f"URL: {url}")
    print(f"Grocy: {grocy_url}")
    print("="*60 + "\n")
    
    try:
        # Étape 1 : Télécharger le Reel
        print("[1/5] 📥 Téléchargement du Reel Instagram...")
        print("-" * 60)
        
        # Chercher le fichier cookies Instagram
        cookies_file = None
        possible_paths = [
            './cookies/instagram.txt',
            os.path.expanduser('~/cookies/instagram.txt'),
            '/app/cookies/instagram.txt',
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                cookies_file = path
                print(f"  ℹ️ Utilisation des cookies : {cookies_file}")
                break
        
        if not cookies_file:
            print("  ⚠️ Aucun fichier cookies trouvé")
            print("  💡 Instagram peut bloquer sans authentification")
            print("  📖 Voir INSTAGRAM.md section 'Cookies' pour configurer")
        
        scraper = InstagramScraper(cookies_file=cookies_file)
        reel_data = scraper.download_reel(url)
        
        print("\n✅ Reel téléchargé:")
        print(f"  - Créateur: {reel_data['uploader']}")
        print(f"  - Durée: {reel_data['duration']}s")
        print(f"  - Vidéo: {reel_data['video_path']}")
        print(f"  - Audio: {reel_data['audio_path']}")
        print(f"\n  📝 Description COMPLÈTE:")
        print("  " + "-" * 58)
        print(f"  {reel_data['description']}")
        print("  " + "-" * 58)
        print(f"  (Longueur: {len(reel_data['description'])} caractères)")
        
        input("\n⏸️  Appuie sur Entrée pour continuer vers la transcription...")
        
        # Étape 2 : Transcrire l'audio
        print("\n[2/5] 🎤 Transcription de l'audio avec Whisper...")
        print("-" * 60)
        print("⏱️  Cela va prendre 2-3 minutes avec le modèle 'medium'...")
        transcriber = AudioTranscriber(model_name="medium")
        transcription_result = transcriber.transcribe(reel_data['audio_path'], language="fr")
        transcription_text = transcription_result['text']
        
        print("\n✅ Transcription terminée:")
        print(f"  - Langue: {transcription_result['language']}")
        print(f"  - Longueur: {len(transcription_text)} caractères")
        print(f"\n📝 Texte transcrit:")
        print("  " + "-" * 58)
        print(f"  {transcription_text}")
        print("  " + "-" * 58)
        
        input("\n⏸️  Appuie sur Entrée pour continuer vers le parsing...")
        
        # Étape 3 : Parser la recette
        print("\n[3/5] 🔍 Parsing de la recette...")
        print("-" * 60)
        parser = RecipeParser()
        recipe_data = parser.parse_recipe(
            description=reel_data['description'],
            transcription=transcription_text
        )
        
        print("\n✅ Recette parsée:")
        print(f"  - Titre: {recipe_data['title']}")
        print(f"  - Portions: {recipe_data['yields']}")
        if recipe_data.get('total_time'):
            print(f"  - Temps: {recipe_data['total_time']} min")
        
        print(f"\n📋 Ingrédients ({len(recipe_data['ingredients'])}):")
        for i, ing in enumerate(recipe_data['ingredients'], 1):
            print(f"    {i}. {ing}")
        
        print(f"\n📖 Instructions:")
        instructions = recipe_data['instructions']
        if len(instructions) > 200:
            print(f"    {instructions[:200]}...")
            print(f"    (+ {len(instructions) - 200} caractères)")
        else:
            print(f"    {instructions}")
        
        # Demander confirmation avant import
        print("\n" + "="*60)
        response = input("🤔 Veux-tu importer cette recette dans Grocy ? (y/n): ")
        
        if response.lower() != 'y':
            print("\n❌ Import annulé")
            # Nettoyage
            scraper.cleanup_files(
                video_path=reel_data['video_path'],
                audio_path=reel_data['audio_path']
            )
            return
        
        # Étape 4 : Connexion à Grocy
        print("\n[4/5] 🔗 Connexion à Grocy...")
        print("-" * 60)
        grocy = GrocyClient(grocy_url, grocy_api_key)
        
        if not grocy.test_connection():
            print("❌ Impossible de se connecter à Grocy")
            return
        
        print("✅ Connecté à Grocy")
        
        # Étape 5 : Import dans Grocy
        print("\n[5/5] 📤 Import dans Grocy...")
        print("-" * 60)
        recipe_data['image_url'] = reel_data.get('thumbnail', '')
        recipe_id = grocy.import_recipe(recipe_data)
        
        # Nettoyage
        print("\n🧹 Nettoyage des fichiers temporaires...")
        scraper.cleanup_files(
            video_path=reel_data['video_path'],
            audio_path=reel_data['audio_path']
        )
        
        # Résultat final
        print("\n" + "="*60)
        print("✅ IMPORT TERMINÉ AVEC SUCCÈS !")
        print("="*60)
        print(f"📋 Recette: {recipe_data['title']}")
        print(f"🆔 ID Grocy: {recipe_id}")
        print(f"🔗 URL: {grocy_url}/#recipe/{recipe_id}")
        print(f"🥘 Ingrédients: {len(recipe_data['ingredients'])}")
        print("="*60 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    # Vérifier les arguments
    if len(sys.argv) < 2:
        print("Usage: python3 test_instagram_full.py <URL_INSTAGRAM_REEL>")
        print("\nExemple:")
        print("  python3 test_instagram_full.py https://www.instagram.com/reel/ABC123/")
        print("\nVariables d'environnement requises:")
        print("  export GROCY_URL='http://100.83.155.21:9283'")
        print("  export GROCY_API_KEY='ta_clé'")
        sys.exit(1)
    
    # Récupérer les paramètres
    url = sys.argv[1]
    grocy_url = os.getenv('GROCY_URL', 'http://100.83.155.21:9283')
    grocy_api_key = os.getenv('GROCY_API_KEY', '')
    
    if not grocy_api_key:
        print("❌ Erreur: GROCY_API_KEY non définie")
        print("Exécute: export GROCY_API_KEY='ta_clé'")
        sys.exit(1)
    
    # Lancer le test
    test_instagram_import(url, grocy_url, grocy_api_key)
