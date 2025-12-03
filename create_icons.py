#!/usr/bin/env python3
"""
Crée les icônes pour l'extension navigateur
"""

from PIL import Image, ImageDraw, ImageFont

def create_icon(size, filename):
    # Créer une image avec fond violet
    img = Image.new('RGBA', (size, size), (102, 126, 234, 255))
    draw = ImageDraw.Draw(img)
    
    # Dessiner un cercle blanc au centre
    margin = size // 4
    draw.ellipse([margin, margin, size-margin, size-margin], fill=(255, 255, 255, 255))
    
    # Dessiner une "cuillère" simplifiée (rond + bâton)
    if size >= 48:
        # Cuillère
        spoon_x = size // 2
        spoon_y = size // 2 - size // 8
        spoon_r = size // 8
        draw.ellipse([spoon_x-spoon_r, spoon_y-spoon_r, 
                     spoon_x+spoon_r, spoon_y+spoon_r], 
                     fill=(102, 126, 234, 255))
        
        # Manche
        handle_width = size // 16
        handle_start = spoon_y + spoon_r
        handle_end = size - margin - 5
        draw.rectangle([spoon_x - handle_width//2, handle_start,
                       spoon_x + handle_width//2, handle_end],
                      fill=(102, 126, 234, 255))
    
    img.save(filename)
    print(f"✓ Icône créée: {filename}")

if __name__ == '__main__':
    try:
        create_icon(16, 'icon16.png')
        create_icon(48, 'icon48.png')
        create_icon(128, 'icon128.png')
        print("\n✅ Toutes les icônes ont été créées!")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        print("Vous pouvez télécharger des icônes gratuites sur https://www.flaticon.com")
