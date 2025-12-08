"""
Client pour l'API Grocy
Gère l'import de recettes et la communication avec Grocy
"""

import requests
from typing import Dict, Any, Optional
from urllib.parse import urljoin


class GrocyClient:
    """Client pour interagir avec l'API Grocy"""
    
    def __init__(self, base_url: str, api_key: str):
        """
        Initialise le client Grocy
        
        Args:
            base_url: URL de base de Grocy (ex: http://localhost:9283)
            api_key: Clé API Grocy
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            'GROCY-API-KEY': api_key,
            'Content-Type': 'application/json'
        }
    
    def test_connection(self) -> bool:
        """
        Teste la connexion à Grocy
        
        Returns:
            True si la connexion est OK, False sinon
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/system/info",
                headers=self.headers,
                timeout=5
            )
            return response.status_code == 200
        except Exception:
            return False
    
    def import_recipe(self, recipe_data: Dict[str, Any]) -> int:
        """
        Importe une recette dans Grocy
        
        Args:
            recipe_data: Données de la recette à importer
            
        Returns:
            ID de la recette créée dans Grocy
        """
        # Étape 1 : Créer la recette de base
        recipe_payload = {
            'name': recipe_data['title'],
            'description': self._format_description(recipe_data),
            'base_servings': self._extract_servings_number(recipe_data['yields']),
            'desired_servings': self._extract_servings_number(recipe_data['yields']),
            'not_check_shoppinglist': 0
        }
        
        # Note: Les champs de temps (prep_time_minutes, cook_time_minutes) ne sont pas 
        # supportés dans toutes les versions de Grocy. Ils sont inclus dans la description.
        
        # Créer la recette via l'API
        response = requests.post(
            f"{self.base_url}/api/objects/recipes",
            headers=self.headers,
            json=recipe_payload,
            timeout=10
        )
        
        if response.status_code not in [200, 201]:
            raise Exception(f"Erreur lors de la création de la recette : {response.text}")
        
        recipe_id = response.json()['created_object_id']
        
        # Étape 2 : Ajouter les ingrédients comme recipe positions
        if recipe_data['ingredients']:
            self._add_recipe_ingredients(recipe_id, recipe_data['ingredients'])
        
        # Étape 3 : Ajouter l'image si disponible
        if recipe_data.get('image_url'):
            self._add_recipe_image(recipe_id, recipe_data['image_url'])
        
        return recipe_id
    
    def _add_recipe_ingredients(self, recipe_id: int, ingredients: list) -> bool:
        """
        Ajoute les ingrédients à une recette en créant les produits nécessaires
        
        Args:
            recipe_id: ID de la recette dans Grocy
            ingredients: Liste des ingrédients (texte)
            
        Returns:
            True si succès, False sinon
        """
        success_count = 0
        
        # Récupérer tous les produits existants
        existing_products = self.get_products()
        product_dict = {p['name'].lower(): p for p in existing_products}
        
        for ingredient in ingredients:
            # Parser l'ingrédient pour extraire quantité, unité et nom
            parsed = self._parse_ingredient(ingredient)
            product_name = parsed['product_name']
            amount = parsed['amount']
            unit_name = parsed['unit']
            
            print(f"  📊 {parsed['original']}")
            print(f"     → {amount} {unit_name} de {product_name}")
            
            # Obtenir ou créer l'unité
            unit_id = self._get_or_create_unit(unit_name)
            
            # Vérifier si le produit existe déjà
            product = None
            if product_name.lower() in product_dict:
                product = product_dict[product_name.lower()]
                print(f"     ✓ Produit existant: {product_name}")
            else:
                # Créer le produit avec la bonne unité
                new_product_id = self._create_product(product_name, unit_id)
                if new_product_id:
                    print(f"     + Produit créé: {product_name}")
                    # Récupérer les infos du produit qu'on vient de créer
                    product = self._get_product_by_id(new_product_id)
                    if product:
                        product_dict[product_name.lower()] = product
                else:
                    print(f"     ⚠️ Impossible de créer: {product_name}")
                    continue
            
            # Ajouter l'ingrédient à la recette via recipes_pos
            if product:
                ingredient_payload = {
                    'recipe_id': recipe_id,
                    'product_id': product['id'],
                    'amount': amount,
                    'qu_id': unit_id,
                    'note': parsed['original'],
                    'only_check_single_unit_in_stock': 0,
                    'ingredient_group': '',
                    'variable_amount': '',
                }
                
                try:
                    response = requests.post(
                        f"{self.base_url}/api/objects/recipes_pos",
                        headers=self.headers,
                        json=ingredient_payload,
                        timeout=10
                    )
                    
                    if response.status_code in [200, 201]:
                        success_count += 1
                        print(f"     ✅ Ajouté à la recette")
                    else:
                        print(f"     ⚠️ Erreur liaison (code {response.status_code}): {response.text}")
                except Exception as e:
                    print(f"     ⚠️ Exception liaison: {e}")
        
        print(f"\n✓ {success_count}/{len(ingredients)} ingrédients ajoutés")
        return success_count > 0
    
    def _get_product_by_id(self, product_id: int) -> Optional[Dict]:
        """
        Récupère les informations complètes d'un produit par son ID
        
        Args:
            product_id: ID du produit
            
        Returns:
            Dict avec les infos du produit ou None si erreur
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/objects/products/{product_id}",
                headers=self.headers,
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception:
            return None
    
    def _parse_ingredient(self, ingredient: str) -> Dict[str, Any]:
        """
        Parse un ingrédient pour extraire quantité, unité et nom
        
        Args:
            ingredient: Texte de l'ingrédient (ex: "600g de blanc de poulet")
            
        Returns:
            Dict avec 'amount', 'unit', 'product_name'
        """
        import re
        
        text = ingredient.lower().strip()
        
        # Pattern pour quantité + unité
        # Exemples: 600g, 2kg, 400ml, 2 cuillères à soupe, 1.5 l
        pattern = r'^(\d+[\.,]?\d*)\s*(g|kg|mg|ml|cl|dl|l|cuillère|cuillères|cuillere|cuilleres|tasse|tasses|c\.|cs|cc|pièce|pièces|piece|pieces|gousse|gousses)?s?\s*'
        
        match = re.match(pattern, text)
        
        if match:
            amount_str = match.group(1).replace(',', '.')
            amount = float(amount_str)
            unit = match.group(2) if match.group(2) else 'piece'
            
            # Normaliser l'unité
            unit = self._normalize_unit(unit)
            
            # Retirer la partie quantité+unité du texte pour avoir le nom du produit
            remaining = text[match.end():].strip()
            product_name = self._clean_ingredient_name(remaining if remaining else ingredient)
            
            return {
                'amount': amount,
                'unit': unit,
                'product_name': product_name,
                'original': ingredient
            }
        
        # Pas de quantité détectée - chercher les articles "du", "de la", "des"
        # et assigner des quantités par défaut
        article_patterns = [
            (r'^(?:du|de l\')\s*(beurre)', 10, 'g'),  # du beurre = 10g
            (r'^(?:de la|de l\')\s*(crème|creme)', 10, 'cl'),  # de la crème = 10cl
            (r'^(?:du|de l\')\s*(lait)', 10, 'cl'),  # du lait = 10cl
            (r'^(?:de l\'|de la)\s*(huile)', 5, 'cl'),  # de l'huile = 5cl
            (r'^(?:du|de l\')\s*(sel)', 5, 'g'),  # du sel = 5g
            (r'^(?:du|de l\')\s*(sucre)', 10, 'g'),  # du sucre = 10g
            (r'^(?:du|de l\')\s*(fromage)', 50, 'g'),  # du fromage = 50g
            (r'^(?:de la|de l\')\s*(farine)', 50, 'g'),  # de la farine = 50g
            (r'^(?:des?)\s*(.*)', 1, 'piece'),  # des X = 1 pièce
        ]
        
        for pattern_str, default_amount, default_unit in article_patterns:
            match = re.match(pattern_str, text, re.IGNORECASE)
            if match:
                product_name = match.group(1).strip()
                product_name = self._clean_ingredient_name(product_name)
                return {
                    'amount': default_amount,
                    'unit': default_unit,
                    'product_name': product_name.capitalize(),
                    'original': ingredient
                }
        
        # Ingrédients sans article ni quantité - assigner valeurs par défaut intelligentes
        # Ex: "Huile d'olive", "Fleur de sel", "Laurier", "Poivre"
        default_quantities = {
            'huile': (5, 'cl'),
            'beurre': (10, 'g'),
            'crème': (10, 'cl'),
            'sel': (5, 'g'),
            'poivre': (2, 'g'),
            'laurier': (1, 'piece'),
            'thym': (1, 'piece'),
            'romarin': (1, 'piece'),
            'basilic': (5, 'g'),
            'persil': (5, 'g'),
            'coriandre': (5, 'g'),
            'épice': (2, 'g'),
            'piment': (1, 'piece'),
            'ail': (1, 'piece'),
            'oignon': (1, 'piece'),
        }
        
        text_lower = text.lower()
        for keyword, (amount, unit) in default_quantities.items():
            if keyword in text_lower:
                product_name = self._clean_ingredient_name(text)
                return {
                    'amount': amount,
                    'unit': unit,
                    'product_name': product_name,
                    'original': ingredient
                }
        
        # Aucun pattern détecté, utiliser valeurs par défaut
        return {
            'amount': 1,
            'unit': 'piece',
            'product_name': self._clean_ingredient_name(ingredient),
            'original': ingredient
        }
    
    def _normalize_unit(self, unit: str) -> str:
        """
        Normalise les noms d'unités
        """
        unit_map = {
            'g': 'g',
            'kg': 'kg',
            'mg': 'mg',
            'ml': 'ml',
            'cl': 'cl',
            'dl': 'dl',
            'l': 'l',
            'cuillère': 'cuillère à soupe',
            'cuillères': 'cuillère à soupe',
            'cuillere': 'cuillère à soupe',
            'cuilleres': 'cuillère à soupe',
            'c.': 'cuillère à soupe',
            'cs': 'cuillère à soupe',
            'cc': 'cuillère à café',
            'tasse': 'tasse',
            'tasses': 'tasse',
            'pièce': 'piece',
            'pièces': 'piece',
            'piece': 'piece',
            'pieces': 'piece',
            'gousse': 'piece',  # Gousse = pièce
            'gousses': 'piece',
        }
        
        return unit_map.get(unit.lower(), unit)
    
    def _get_or_create_unit(self, unit_name: str) -> int:
        """
        Récupère l'ID d'une unité ou la crée si elle n'existe pas
        
        Args:
            unit_name: Nom de l'unité (ex: "g", "kg", "ml")
            
        Returns:
            ID de l'unité
        """
        units = self.get_quantity_units()
        
        # Map des noms courts vers les noms complets possibles
        unit_variants = {
            'g': ['gramme', 'grammes', 'g'],
            'kg': ['kilogramme', 'kilogrammes', 'kg'],
            'mg': ['milligramme', 'milligrammes', 'mg'],
            'ml': ['millilitre', 'millilitres', 'ml'],
            'cl': ['centilitre', 'centilitres', 'cl'],
            'dl': ['décilitre', 'décilitres', 'dl'],
            'l': ['litre', 'litres', 'l'],
            'cuillère à soupe': ['cuillère à soupe', 'cuillères à soupe', 'cuillere a soupe'],
            'cuillère à café': ['cuillère à café', 'cuillères à café', 'cuillere a cafe'],
            'tasse': ['tasse', 'tasses'],
            'piece': ['piece', 'pieces', 'pièce', 'pièces'],
        }
        
        # Obtenir les variantes possibles pour cette unité
        variants = unit_variants.get(unit_name.lower(), [unit_name.lower()])
        
        # Chercher si l'unité existe déjà (insensible à la casse et avec variantes)
        for unit in units:
            unit_name_lower = unit['name'].lower()
            unit_plural_lower = unit.get('name_plural', '').lower()
            
            if unit_name_lower in variants or unit_plural_lower in variants:
                return unit['id']
        
        # L'unité n'existe pas, la créer
        unit_names = {
            'g': ('Gramme', 'Grammes'),
            'kg': ('Kilogramme', 'Kilogrammes'),
            'mg': ('Milligramme', 'Milligrammes'),
            'ml': ('Millilitre', 'Millilitres'),
            'cl': ('Centilitre', 'Centilitres'),
            'dl': ('Décilitre', 'Décilitres'),
            'l': ('Litre', 'Litres'),
            'cuillère à soupe': ('Cuillère à soupe', 'Cuillères à soupe'),
            'cuillère à café': ('Cuillère à café', 'Cuillères à café'),
            'tasse': ('Tasse', 'Tasses'),
            'piece': ('Piece', 'Pieces'),
        }
        
        if unit_name in unit_names:
            singular, plural = unit_names[unit_name]
        else:
            singular = unit_name.capitalize()
            plural = unit_name.capitalize() + 's'
        
        unit_payload = {
            'name': singular,
            'name_plural': plural,
            'description': f'Créé automatiquement',
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/objects/quantity_units",
                headers=self.headers,
                json=unit_payload,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                new_unit_id = response.json()['created_object_id']
                print(f"    + Unité '{singular}' créée")
                return new_unit_id
            else:
                print(f"    ⚠️ Impossible de créer l'unité '{singular}': {response.text}")
                # L'unité existe probablement déjà, recharger et chercher à nouveau
                units = self.get_quantity_units()
                for unit in units:
                    unit_name_lower = unit['name'].lower()
                    if unit_name_lower in variants:
                        print(f"    ✓ Unité '{unit['name']}' trouvée après rechargement")
                        return unit['id']
                # Fallback sur la première unité disponible
                return self._get_default_quantity_unit()
        except Exception as e:
            print(f"    ⚠️ Exception création unité: {e}")
            return self._get_default_quantity_unit()
    
    def _clean_ingredient_name(self, ingredient: str) -> str:
        """
        Nettoie le nom d'un ingrédient pour extraire le produit
        Exemple: "blanc de poulet" -> "Poulet Blanc"
        """
        import re
        
        text = ingredient.lower().strip()
        
        # Si le texte est vide ou trop court, retourner l'original
        if len(text) < 2:
            return ingredient
        
        # Retirer "de" ou "d'" SEULEMENT au début
        text = re.sub(r'^(?:de|d\')\s+', '', text)
        
        # Garder les expressions importantes ensemble
        # Ne pas séparer "cuisses de canard", "gousse d'ail", "blanc de poulet"
        # On garde "de" quand il est au milieu
        
        # Retirer les articles uniquement au début
        text = re.sub(r'^(?:la|le|les|un|une|des)\s+', '', text)
        
        # Nettoyer les espaces multiples
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Retirer la ponctuation en début/fin
        text = text.strip('.,;:-\'\"')
        
        # Si le résultat est vide, retourner l'original
        if not text:
            return ingredient
        
        # Capitaliser proprement en gardant les prépositions
        words = text.split()
        result = []
        
        for i, word in enumerate(words):
            # Ne capitaliser "de" et "d'" que s'ils ne sont pas seuls
            if word in ['de', "d'"] and i > 0 and i < len(words) - 1:
                result.append(word)
            elif word in ['et', 'ou', 'à', 'au', 'aux']:
                result.append(word)
            else:
                result.append(word.capitalize())
        
        final = ' '.join(result)
        
        # Si le résultat est trop court, retourner l'original
        if len(final) < 2:
            return ingredient
        
        return final
    
    def _create_product(self, product_name: str, unit_id: int = None) -> Optional[int]:
        """
        Crée un nouveau produit dans Grocy
        
        Args:
            product_name: Nom du produit à créer
            unit_id: ID de l'unité à utiliser (optionnel, sinon utilise unité par défaut)
            
        Returns:
            ID du produit créé ou None si échec
        """
        # Si pas d'unité spécifiée, récupérer l'unité par défaut
        if unit_id is None:
            unit_id = self._get_default_quantity_unit()
        
        # Payload minimal pour créer un produit
        product_payload = {
            'name': product_name,
            'description': 'Créé automatiquement par recipe importer',
            'location_id': 1,  # Location par défaut
            'qu_id_purchase': unit_id,
            'qu_id_stock': unit_id,
            'min_stock_amount': 0,
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/objects/products",
                headers=self.headers,
                json=product_payload,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                product_id = response.json()['created_object_id']
                return product_id
            else:
                print(f"        ❌ ERREUR création produit (code {response.status_code}): {response.text}")
                return None
        except Exception as e:
            print(f"        ❌ EXCEPTION création produit: {e}")
            return None
    
    def _format_description(self, recipe_data: Dict[str, Any]) -> str:
        """
        Formate la description complète de la recette
        Inclut les temps et instructions (les ingrédients sont ajoutés séparément)
        """
        description_parts = []
        
        # Section informations
        info_parts = []
        if recipe_data.get('yields'):
            info_parts.append(f"**Portions :** {recipe_data['yields']}")
        if recipe_data.get('prep_time'):
            info_parts.append(f"**Temps de préparation :** {recipe_data['prep_time']} min")
        if recipe_data.get('cook_time'):
            info_parts.append(f"**Temps de cuisson :** {recipe_data['cook_time']} min")
        if recipe_data.get('total_time'):
            info_parts.append(f"**Temps total :** {recipe_data['total_time']} min")
        
        if info_parts:
            description_parts.append(" | ".join(info_parts))
            description_parts.append("\n")
        
        # Section instructions
        if recipe_data['instructions']:
            description_parts.append("## Instructions\n")
            description_parts.append(recipe_data['instructions'])
        
        # Informations supplémentaires
        if recipe_data.get('host'):
            description_parts.append(f"\n\n---\n*Source: {recipe_data['host']}*")
        
        return "\n".join(description_parts)
    
    def _extract_servings_number(self, yields_str: str) -> int:
        """
        Extrait le nombre de portions depuis une chaîne
        
        Args:
            yields_str: Chaîne décrivant les portions (ex: "4 portions", "6 personnes")
            
        Returns:
            Nombre de portions (défaut: 4)
        """
        if not yields_str or yields_str == "Non spécifié":
            return 4
        
        # Essayer d'extraire le premier nombre de la chaîne
        import re
        numbers = re.findall(r'\d+', str(yields_str))
        return int(numbers[0]) if numbers else 4
    
    def _add_recipe_image(self, recipe_id: int, image_url: str) -> bool:
        """
        Tente d'ajouter une image à la recette
        
        Note: L'API Grocy pour les images peut être complexe,
        cette fonction est optionnelle et peut échouer silencieusement
        """
        try:
            # Télécharger l'image
            img_response = requests.get(image_url, timeout=10)
            if img_response.status_code != 200:
                return False
            
            # Upload vers Grocy (nécessite de gérer les fichiers)
            # Cette partie dépend de la configuration de Grocy
            # Pour l'instant on skip pour simplifier
            return False
        except Exception:
            return False
    
    def get_quantity_units(self) -> list:
        """
        Récupère la liste des unités de quantité disponibles
        
        Returns:
            Liste des unités
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/objects/quantity_units",
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            return []
        except Exception:
            return []
    
    def _get_default_quantity_unit(self) -> int:
        """
        Trouve une unité de quantité par défaut (pièce, piece, unit, etc.)
        
        Returns:
            ID de l'unité par défaut
        """
        units = self.get_quantity_units()
        
        if not units:
            return 1  # Fallback
        
        # Chercher "pièce", "piece", "unit", "pc", etc.
        for unit in units:
            name_lower = unit.get('name', '').lower()
            if name_lower in ['pièce', 'piece', 'unit', 'pc', 'pcs', 'stück', 'stk']:
                return unit['id']
        
        # Si aucune trouvée, prendre la première
        return units[0]['id']
    
    def get_products(self) -> list:
        """
        Récupère la liste des produits Grocy
        Utile pour mapper les ingrédients aux produits existants
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/objects/products",
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            return []
        except Exception:
            return []
