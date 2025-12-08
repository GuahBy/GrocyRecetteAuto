#!/usr/bin/env python3
"""
Module de parsing de recettes depuis texte brut
Extrait ingrédients et étapes depuis description + transcription
"""

import re
from typing import Dict, List, Optional


class RecipeParser:
    def __init__(self):
        """Initialise le parser de recettes"""
        # Mots-clés pour détecter les ingrédients
        self.ingredient_keywords = [
            'ingrédient', 'ingredients', 'il faut', 'vous aurez besoin',
            'pour cette recette', 'liste des courses', 'il vous faut'
        ]
        
        # Mots-clés pour détecter les étapes
        self.step_keywords = [
            'étape', 'étapes', 'préparation', 'instructions', 'recette',
            'procédure', 'réalisation', 'commencez par', 'd\'abord', 'ensuite'
        ]
        
        # Pattern pour détecter des quantités (100g, 2 cuillères, etc.)
        self.quantity_pattern = re.compile(
            r'\b\d+[\.,]?\d*\s*(g|kg|mg|ml|cl|dl|l|cuillère|cuillères|tasse|pièce|pincée)s?\b',
            re.IGNORECASE
        )
    
    def parse_recipe(self, description: str, transcription: str = "") -> Dict:
        """
        Parse une recette depuis description + transcription
        
        Args:
            description: Description du post Instagram
            transcription: Transcription audio de la vidéo
            
        Returns:
            Dict avec:
                - title: Titre de la recette
                - ingredients: Liste des ingrédients
                - instructions: Instructions de préparation
                - yields: Portions
                - total_time: Temps total (si trouvé)
        """
        # Combiner description et transcription
        full_text = f"{description}\n\n{transcription}".strip()
        
        print("📝 Parsing de la recette...")
        
        # Extraire le titre
        title = self._extract_title(description, transcription)
        
        # Extraire les ingrédients
        ingredients = self._extract_ingredients(full_text)
        
        # Extraire les instructions
        instructions = self._extract_instructions(full_text)
        
        # Extraire les portions
        yields = self._extract_yields(full_text)
        
        # Extraire le temps
        total_time = self._extract_time(full_text)
        
        result = {
            'title': title,
            'ingredients': ingredients,
            'instructions': instructions,
            'yields': yields,
            'total_time': total_time,
            'source': 'Instagram Reel',
            'description': description[:500]  # Garder un extrait
        }
        
        print(f"✓ Recette parsée")
        print(f"  Titre : {title}")
        print(f"  Ingrédients : {len(ingredients)}")
        print(f"  Instructions : {len(instructions.split(chr(10))) if instructions else 0} lignes")
        
        return result
    
    def _extract_title(self, description: str, transcription: str) -> str:
        """Extrait le titre de la recette"""
        # Essayer la première ligne de la description
        lines = description.split('\n')
        if lines:
            first_line = lines[0].strip()
            # Si la première ligne est courte et ne contient pas trop de symboles
            if len(first_line) < 100 and first_line.count('#') < 3:
                return first_line
        
        # Chercher "recette de..." dans le texte
        patterns = [
            r'recette\s+de\s+([^.\n]+)',
            r'comment\s+faire\s+([^.\n]+)',
            r'faire\s+des?\s+([^.\n]+)',
        ]
        
        text = description + " " + transcription
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                if len(title) < 100:
                    return title.capitalize()
        
        return "Recette Instagram"
    
    def _extract_ingredients(self, text: str) -> List[str]:
        """Extrait la liste des ingrédients"""
        ingredients = []
        
        # Chercher une section "ingrédients" jusqu'aux vraies sections (préparation, instructions)
        # ou jusqu'aux hashtags/fin
        for keyword in self.ingredient_keywords:
            # Pattern amélioré qui ne s'arrête pas aux sous-sections comme "Purée:", "Garniture:", etc.
            pattern = rf"{keyword}\s*:?\s*(.*?)(?:\n\n|préparation\s*:|recette\s*:|instructions?\s*:|étapes?\s*:|#|\Z)"
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            
            if match:
                ingredient_section = match.group(1).strip()
                
                # Parser toutes les lignes de cette section
                lines = ingredient_section.split('\n')
                
                for line in lines:
                    line_original = line.strip()
                    
                    # Ignorer les lignes vides
                    if not line_original or len(line_original) < 2:
                        continue
                    
                    # Ignorer les sous-titres seuls (Purée:, Garniture:, etc.)
                    if re.match(r'^[A-Za-zÀ-ÿ\s]+\s*:$', line_original):
                        continue
                    
                    # Nettoyer les marques entre parenthèses
                    line_clean = re.sub(r'\([^)]*\)', '', line_original).strip()
                    
                    if not line_clean or len(line_clean) < 2:
                        continue
                    
                    # Vérifier que ce n'est pas une instruction/phrase longue
                    if self._is_instruction(line_clean):
                        # Mais extraire quand même les ingrédients mentionnés
                        # Ex: "Écrasé de potiron, avec..." → extraire "potiron"
                        extracted = self._extract_ingredients_from_instruction(line_clean)
                        ingredients.extend(extracted)
                        continue
                    
                    # Séparer les ingrédients séparés par des virgules
                    if ',' in line_clean:
                        parts = [p.strip() for p in line_clean.split(',')]
                        for part in parts:
                            if part and len(part) > 2:
                                ingredients.append(part)
                    else:
                        # Séparer par "et"
                        if ' et ' in line_clean.lower():
                            parts = re.split(r'\s+et\s+', line_clean, flags=re.IGNORECASE)
                            for part in parts:
                                part = part.strip()
                                if part and len(part) > 2:
                                    ingredients.append(part)
                        else:
                            # Ligne simple
                            ingredients.append(line_clean)
        
        # Si pas d'ingrédients trouvés, essayer de détecter automatiquement
        if not ingredients:
            print("  ⚠️ Section 'Ingrédients' non trouvée, détection automatique...")
            ingredients = self._detect_ingredients_auto(text)
        
        # Nettoyer chaque ingrédient
        cleaned_ingredients = []
        for ing in ingredients:
            clean_ing = self._clean_text(ing)
            if clean_ing and len(clean_ing) > 2:
                # Vérifier que ce n'est pas une phrase complète
                if not self._is_full_sentence(clean_ing):
                    cleaned_ingredients.append(clean_ing)
        
        # Dédupliquer
        cleaned_ingredients = list(dict.fromkeys(cleaned_ingredients))
        
        return cleaned_ingredients[:30]  # Max 30 ingrédients
    
    def _extract_ingredients_from_instruction(self, text: str) -> List[str]:
        """Extrait les ingrédients mentionnés dans une phrase d'instruction"""
        ingredients = []
        
        # Chercher les ingrédients courants mentionnés
        food_items = [
            'potiron', 'citrouille', 'courge', 'pommes de terre', 'patate',
            'carotte', 'oignon', 'ail', 'tomate', 'courgette',
            'huile', 'beurre', 'crème', 'sel', 'poivre',
            'miel', 'sucre', 'chocolat'
        ]
        
        text_lower = text.lower()
        for food in food_items:
            if food in text_lower:
                ingredients.append(food)
        
        return ingredients
    
    def _is_full_sentence(self, text: str) -> bool:
        """Vérifie si c'est une phrase complète plutôt qu'un ingrédient"""
        # Si contient plus de 6 mots, c'est probablement une phrase
        words = text.split()
        if len(words) > 8:
            return True
        
        # Si contient des verbes conjugués
        conjugated_verbs = ['fait', 'fait', 'dois', 'peux', 'vais', 'veux', 'suis', 'sont']
        for verb in conjugated_verbs:
            if f' {verb} ' in f' {text.lower()} ':
                return True
        
        return False
    
    def _is_instruction(self, text: str) -> bool:
        """Vérifie si un texte ressemble à une instruction plutôt qu'un ingrédient"""
        text_lower = text.lower().strip()
        
        # Phrases d'instructions typiques
        instruction_phrases = [
            'dès le début', 'direct sur', 'commencer par', 'faire cuire',
            'mettre au four', 'préchauffer', 'laisser reposer', 'servir avec',
            'à feu', 'pendant', 'jusqu\'à', 'ensuite', 'puis', 'après',
            'une fois', 'quand', 'si besoin'
        ]
        
        for phrase in instruction_phrases:
            if phrase in text_lower:
                return True
        
        # Verbes à l'impératif au début
        if re.match(r'^(faites|mettez|ajoutez|coupez|hachez|mixez|versez|épluchez)', text_lower):
            return True
        
        return False
    
    def _looks_like_ingredient(self, line: str) -> bool:
        """Détermine si une ligne ressemble à un ingrédient"""
        if not line or len(line) < 3 or len(line) > 150:
            return False
        
        line_lower = line.lower().strip()
        
        # Exclure les phrases d'instructions
        # Si ça contient des verbes d'action typiques, c'est une instruction
        instruction_verbs = [
            'faire', 'mettre', 'ajouter', 'mélanger', 'cuire', 'couper',
            'éplucher', 'hacher', 'mixer', 'chauffer', 'verser', 'laisser',
            'préchauffer', 'enfourner', 'sortir', 'retirer', 'prendre',
            'commencer', 'démarrer', 'continuer', 'terminer', 'servir',
            'dès le début', 'direct sur', 'ensuite', 'puis', 'après'
        ]
        
        for verb in instruction_verbs:
            if verb in line_lower:
                return False
        
        # Si ça commence par un verbe à l'impératif, c'est une instruction
        if re.match(r'^(faites|mettez|ajoutez|coupez|hachez|mixez|versez)', line_lower):
            return False
        
        # Doit avoir une quantité
        if self.quantity_pattern.search(line):
            return True
        
        # Ou contenir des mots alimentaires courants
        food_words = [
            # Viandes & poissons
            'poulet', 'canard', 'boeuf', 'porc', 'veau', 'agneau', 'dinde',
            'jambon', 'lardons', 'bacon', 'saucisse', 'merguez',
            'poisson', 'saumon', 'thon', 'cabillaud', 'crevette', 'moule',
            # Légumes
            'carotte', 'oignon', 'ail', 'tomate', 'courgette', 'aubergine',
            'poivron', 'pomme de terre', 'patate', 'navet', 'poireau',
            'champignon', 'salade', 'épinard', 'haricot', 'petit pois',
            'brocoli', 'chou', 'concombre', 'radis', 'betterave',
            'potiron', 'citrouille', 'courge',
            # Produits de base
            'farine', 'sucre', 'sel', 'poivre', 'huile', 'beurre',
            'lait', 'crème', 'fromage', 'yaourt', 'oeuf',
            # Herbes & épices
            'thym', 'romarin', 'persil', 'basilic', 'coriandre',
            'cumin', 'paprika', 'curry', 'gingembre', 'cannelle',
            'laurier', 'origan', 'menthe', 'aneth', 'estragon',
            'safran', 'muscade', 'vanille', 'cardamome',
            # Condiments & assaisonnements
            'fleur de sel', 'gros sel', 'sel fin', 'sel de mer',
            'poivre noir', 'poivre blanc', 'piment',
            "huile d'olive", 'huile de tournesol', 'huile végétale',
            'vinaigre', 'vinaigre balsamique', 'citron', 'lime',
            # Féculents
            'riz', 'pâtes', 'pain', 'semoule', 'quinoa',
            # Fruits
            'pomme', 'banane', 'citron', 'orange', 'fraise',
            # Produits courants
            'chocolat', 'miel', 'confiture', 'sauce', 'bouillon', 'vin',
            'vinaigre', 'moutarde', 'mayonnaise', 'ketchup',
            # Cuissons/parties
            'cuisse', 'filet', 'escalope', 'côte', 'aile', 'blanc',
            # Laitages spécifiques
            "crème d'isigny", 'crème fraiche', 'crème liquide',
            'beurre demi-sel', 'beurre salé',
        ]
        
        # Vérifier les mots alimentaires
        for word in food_words:
            if word in line_lower:
                return True
        
        return False
    
    def _detect_ingredients_auto(self, text: str) -> List[str]:
        """Détection automatique des ingrédients par pattern"""
        ingredients = []
        
        # Pattern 1 : Quantité + unité + "de" + ingrédient
        # Ex: "200g de farine", "2 cuillères de sucre"
        matches = re.finditer(
            r'(\d+[\.,]?\d*\s*(?:g|kg|ml|cl|l|cuillères?|cuillere|tasses?|pincées?)\s+de\s+[^,.\n]{3,60})',
            text,
            re.IGNORECASE
        )
        for match in matches:
            ingredient = match.group(1).strip()
            ingredients.append(self._clean_text(ingredient))
        
        # Pattern 2 : Chiffre + contexte complet (gousse d'ail, cuisse de canard, etc.)
        # Capturer plus de contexte pour garder le type de viande/légume
        matches = re.finditer(
            r'(\d+[\.,]?\d*\s+(?:gousses?|cuisses?|blancs?|filets?|tranches?)\s+(?:d\'|de\s+)?[^,.\n]{3,40})',
            text,
            re.IGNORECASE
        )
        for match in matches:
            ingredient = match.group(1).strip()
            ingredients.append(self._clean_text(ingredient))
        
        # Pattern 3 : Chiffre + nom simple (ex: "3 œufs", "2 carottes")
        matches = re.finditer(
            r'(\d+[\.,]?\d*\s+(?:œufs?|carottes?|oignons?|tomates?|pommes? de terre|patates?|courgettes?|aubergines?))',
            text,
            re.IGNORECASE
        )
        for match in matches:
            ingredient = match.group(1).strip()
            ingredients.append(self._clean_text(ingredient))
        
        # Pattern 4 : Articles "du", "de la", "des" + nom (sans quantité précise)
        # Ex: "du beurre", "de la crème", "des épices"
        matches = re.finditer(
            r'\b((?:du|de la|de l\'|des)\s+[^,.\n]{3,40})',
            text,
            re.IGNORECASE
        )
        for match in matches:
            potential_ingredient = match.group(1).strip()
            # Vérifier que ça ressemble à un ingrédient
            if self._looks_like_ingredient(potential_ingredient):
                ingredients.append(self._clean_text(potential_ingredient))
        
        # Pattern 5 : Phrases avec verbes d'action
        # Ex: "on va utiliser des carottes", "il nous faut du beurre"
        phrases_keywords = [
            r'(?:on va |on |nous allons )?(?:utiliser|prendre|mettre|ajouter|avoir besoin de?)\s+((?:des?|du|de la|de l\'|quelques?|un peu de?)?\s*[^,.\n]{3,40})',
            r'(?:il (?:nous |vous )?faut|faudra)\s+((?:des?|du|de la|de l\'|quelques?|un peu de?)?\s*[^,.\n]{3,40})',
        ]
        
        for pattern in phrases_keywords:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                potential_ingredient = match.group(1).strip()
                # Vérifier que ça ressemble à un ingrédient
                if self._looks_like_ingredient(potential_ingredient):
                    ingredients.append(self._clean_text(potential_ingredient))
        
        return ingredients
    
    def _extract_instructions(self, text: str) -> str:
        """Extrait les instructions de préparation"""
        # Chercher une section "préparation" ou "étapes"
        for keyword in self.step_keywords:
            pattern = rf"{keyword}[:\s]*(.+?)(?:ingrédients?|#|$)"
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            
            if match:
                instructions = match.group(1).strip()
                # Nettoyer
                instructions = self._clean_text(instructions)
                if len(instructions) > 50:  # Au moins 50 caractères
                    return instructions
        
        # Si pas trouvé, prendre tout le texte après nettoyage
        clean_text = self._clean_text(text)
        if len(clean_text) > 100:
            # Prendre les 1000 premiers caractères
            return clean_text[:1000]
        
        return ""
    
    def _extract_yields(self, text: str) -> str:
        """Extrait le nombre de portions"""
        patterns = [
            r'pour\s+(\d+)\s+personnes?',
            r'(\d+)\s+portions?',
            r'(\d+)\s+parts?',
            r'serves?\s+(\d+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return f"{match.group(1)} portions"
        
        return "4 portions"  # Par défaut
    
    def _extract_time(self, text: str) -> Optional[int]:
        """Extrait le temps de préparation (en minutes)"""
        patterns = [
            r'(\d+)\s*min(?:utes?)?',
            r'(\d+)\s*h(?:eure)?(?:s)?\s*(?:(\d+)\s*min)?',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if len(match.groups()) > 1 and match.group(2):
                    # Format "1h30"
                    hours = int(match.group(1))
                    minutes = int(match.group(2))
                    return hours * 60 + minutes
                else:
                    # Format "30min"
                    return int(match.group(1))
        
        return None
    
    def _clean_text(self, text: str) -> str:
        """Nettoie le texte (emojis, hashtags, etc.)"""
        # Retirer les emojis (simplifié)
        text = re.sub(r'[^\w\s\d.,!?;:()\-\'\"àâäéèêëïîôùûüÿç]', '', text)
        
        # Retirer les hashtags
        text = re.sub(r'#\w+', '', text)
        
        # Retirer les mentions
        text = re.sub(r'@\w+', '', text)
        
        # Nettoyer les espaces multiples
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()


# Test du module
if __name__ == '__main__':
    # Exemple de description Instagram
    description = """
    🍰 Gâteau au chocolat facile
    
    Ingrédients :
    - 200g de chocolat noir
    - 100g de beurre
    - 150g de sucre
    - 3 oeufs
    - 50g de farine
    
    Préparation :
    Faire fondre le chocolat avec le beurre.
    Ajouter le sucre et les oeufs.
    Incorporer la farine.
    Cuire 25min à 180°C.
    
    #recette #chocolat #patisserie
    """
    
    transcription = """
    Bonjour tout le monde, aujourd'hui on fait un délicieux gâteau au chocolat.
    C'est super simple. On commence par faire fondre le chocolat avec le beurre au bain-marie.
    Ensuite on ajoute le sucre, on mélange bien. On incorpore les oeufs un par un.
    Pour finir, on ajoute la farine délicatement. On verse dans un moule et hop au four 25 minutes.
    """
    
    parser = RecipeParser()
    result = parser.parse_recipe(description, transcription)
    
    print("\n" + "="*60)
    print("RÉSULTAT DU PARSING")
    print("="*60)
    print(f"\nTitre : {result['title']}")
    print(f"\nIngrédients ({len(result['ingredients'])}) :")
    for ing in result['ingredients']:
        print(f"  - {ing}")
    print(f"\nInstructions :")
    print(f"  {result['instructions'][:200]}...")
    print(f"\nPortions : {result['yields']}")
    if result['total_time']:
        print(f"Temps : {result['total_time']} min")
