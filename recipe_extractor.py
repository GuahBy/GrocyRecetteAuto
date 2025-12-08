"""
Module d'extraction de recettes depuis des pages web
Utilise recipe-scrapers pour supporter 250+ sites de recettes
"""

from recipe_scrapers import scrape_me, scrape_html
from pathlib import Path
from typing import Dict, Any


class RecipeExtractor:
    """Extrait les données de recettes depuis URLs ou fichiers HTML"""
    
    def extract(self, source: str) -> Dict[str, Any]:
        """
        Extrait une recette depuis une URL ou un fichier HTML
        
        Args:
            source: URL ou chemin vers fichier HTML local
            
        Returns:
            Dict contenant les données de la recette
        """
        if self._is_file(source):
            return self._extract_from_file(source)
        else:
            return self._extract_from_url(source)
    
    def _is_file(self, source: str) -> bool:
        """Vérifie si la source est un fichier local"""
        return Path(source).exists()
    
    def _extract_from_url(self, url: str) -> Dict[str, Any]:
        """Extrait une recette depuis une URL"""
        try:
            # Essayer avec wild_mode (versions récentes)
            try:
                scraper = scrape_me(url, wild_mode=True)
            except TypeError:
                # Fallback sans wild_mode (versions anciennes)
                scraper = scrape_me(url)
            return self._format_recipe(scraper)
        except Exception as e:
            raise Exception(f"Erreur lors de l'extraction depuis l'URL : {e}")
    
    def _extract_from_file(self, filepath: str) -> Dict[str, Any]:
        """Extrait une recette depuis un fichier HTML local"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # On essaie d'extraire l'URL originale du HTML si disponible
            # Sinon on utilise une URL factice
            # Essayer avec wild_mode (versions récentes)
            try:
                scraper = scrape_html(html_content, org_url="http://localhost", wild_mode=True)
            except TypeError:
                # Fallback sans wild_mode (versions anciennes)
                scraper = scrape_html(html_content, org_url="http://localhost")
            return self._format_recipe(scraper)
        except Exception as e:
            raise Exception(f"Erreur lors de l'extraction depuis le fichier : {e}")
    
    def _format_recipe(self, scraper) -> Dict[str, Any]:
        """
        Formate les données extraites dans un format standard
        
        Args:
            scraper: Instance de recipe-scrapers
            
        Returns:
            Dict avec les données formatées
        """
        recipe_data = {
            'title': scraper.title(),
            'ingredients': scraper.ingredients(),
            'instructions': scraper.instructions(),
            'yields': self._extract_yields(scraper),
            'total_time': self._safe_get_time(scraper, 'total_time'),
            'prep_time': self._safe_get_time(scraper, 'prep_time'),
            'cook_time': self._safe_get_time(scraper, 'cook_time'),
            'image_url': self._safe_get(scraper, 'image'),
            'nutrients': self._safe_get(scraper, 'nutrients'),
            'host': self._safe_get(scraper, 'host')
        }
        
        return recipe_data
    
    def _extract_yields(self, scraper) -> str:
        """Extrait le nombre de portions de manière sécurisée"""
        try:
            yields = scraper.yields()
            return yields
        except:
            return "Non spécifié"
    
    def _safe_get_time(self, scraper, method_name: str):
        """Récupère un temps de manière sécurisée"""
        try:
            method = getattr(scraper, method_name)
            time_value = method()
            return time_value if time_value else None
        except:
            return None
    
    def _safe_get(self, scraper, method_name: str):
        """Récupère une valeur de manière sécurisée"""
        try:
            method = getattr(scraper, method_name)
            return method()
        except:
            return None
