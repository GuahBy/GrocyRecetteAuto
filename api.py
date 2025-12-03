#!/usr/bin/env python3
"""
API Flask pour importer des recettes dans Grocy
Exposée pour être appelée par l'extension navigateur
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from recipe_extractor import RecipeExtractor
from grocy_client import GrocyClient
import os
import tempfile

app = Flask(__name__)
CORS(app)  # Permet les requêtes cross-origin depuis l'extension

# Configuration depuis variables d'environnement
GROCY_URL = os.getenv('GROCY_URL', 'http://localhost:9283')
GROCY_API_KEY = os.getenv('GROCY_API_KEY', '')

@app.route('/')
def index():
    """Page d'accueil avec interface web"""
    return render_template('index.html')

@app.route('/health', methods=['GET'])
def health():
    """Endpoint de santé pour vérifier que l'API fonctionne"""
    return jsonify({'status': 'ok', 'message': 'Recipe Importer API is running'})

@app.route('/api/import', methods=['POST'])
def import_recipe():
    """
    Importe une recette depuis une URL ou du HTML
    
    Body JSON:
    {
        "url": "https://www.marmiton.org/...",  // OU
        "html": "<html>...</html>",  // HTML de la recette
        "grocy_url": "http://localhost:9283",  // optionnel
        "grocy_api_key": "..."  // optionnel
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Aucune donnée fournie'
            }), 400
        
        # Vérifier qu'on a soit une URL soit du HTML
        if 'url' not in data and 'html' not in data:
            return jsonify({
                'success': False,
                'error': 'URL ou HTML manquant'
            }), 400
        
        grocy_url = data.get('grocy_url', GROCY_URL)
        grocy_api_key = data.get('grocy_api_key', GROCY_API_KEY)
        
        if not grocy_api_key:
            return jsonify({
                'success': False,
                'error': 'Clé API Grocy manquante'
            }), 400
        
        # Étape 1 : Extraction de la recette
        extractor = RecipeExtractor()
        
        if 'url' in data:
            print(f"📥 Import depuis URL: {data['url']}")
            recipe_data = extractor.extract(data['url'])
        else:
            print(f"📥 Import depuis HTML ({len(data['html'])} caractères)")
            # Créer un fichier temporaire avec le HTML
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                f.write(data['html'])
                temp_file = f.name
            
            try:
                recipe_data = extractor.extract(temp_file)
            finally:
                os.unlink(temp_file)
        
        print(f"✓ Recette extraite: {recipe_data['title']}")
        
        # Étape 2 : Connexion à Grocy
        grocy = GrocyClient(grocy_url, grocy_api_key)
        
        if not grocy.test_connection():
            return jsonify({
                'success': False,
                'error': 'Impossible de se connecter à Grocy'
            }), 500
        
        # Étape 3 : Import dans Grocy
        recipe_id = grocy.import_recipe(recipe_data)
        
        print(f"✓ Recette importée: ID {recipe_id}")
        
        return jsonify({
            'success': True,
            'message': f"Recette '{recipe_data['title']}' importée avec succès",
            'data': {
                'recipe_id': recipe_id,
                'title': recipe_data['title'],
                'ingredients_count': len(recipe_data['ingredients']),
                'grocy_url': f"{grocy_url}/#recipe/{recipe_id}"
            }
        })
        
    except Exception as e:
        print(f"✗ Erreur: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/preview', methods=['POST'])
def preview_recipe():
    """
    Prévisualise une recette sans l'importer
    
    Body JSON:
    {
        "url": "https://www.marmiton.org/..."  // OU
        "html": "<html>...</html>"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Aucune donnée fournie'
            }), 400
        
        if 'url' not in data and 'html' not in data:
            return jsonify({
                'success': False,
                'error': 'URL ou HTML manquant'
            }), 400
        
        # Extraction de la recette
        extractor = RecipeExtractor()
        
        if 'url' in data:
            recipe_data = extractor.extract(data['url'])
        else:
            # Créer un fichier temporaire avec le HTML
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                f.write(data['html'])
                temp_file = f.name
            
            try:
                recipe_data = extractor.extract(temp_file)
            finally:
                os.unlink(temp_file)
        
        return jsonify({
            'success': True,
            'data': {
                'title': recipe_data['title'],
                'yields': recipe_data.get('yields', 'N/A'),
                'total_time': recipe_data.get('total_time'),
                'ingredients': recipe_data['ingredients'][:10],  # Max 10 pour preview
                'ingredients_count': len(recipe_data['ingredients']),
                'has_instructions': bool(recipe_data.get('instructions'))
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Vérifier que les variables d'environnement sont définies
    if not GROCY_API_KEY:
        print("⚠️  ATTENTION: GROCY_API_KEY non définie!")
        print("   Définissez-la avec: export GROCY_API_KEY='votre_clé'")
    
    print("=" * 60)
    print("🚀 API Recipe Importer démarrée")
    print(f"   Grocy URL: {GROCY_URL}")
    print(f"   API Key: {'✓ définie' if GROCY_API_KEY else '✗ manquante'}")
    print("=" * 60)
    print()
    
    # Démarrer le serveur
    # En production, utiliser gunicorn ou un autre WSGI server
    app.run(host='0.0.0.0', port=5000, debug=False)