#!/bin/bash
# Script pour créer les icônes de l'extension (nécessite ImageMagick)

# Créer une icône SVG simple
cat > icon.svg << 'SVG'
<svg width="128" height="128" xmlns="http://www.w3.org/2000/svg">
  <rect width="128" height="128" rx="20" fill="#667eea"/>
  <text x="64" y="85" font-size="80" text-anchor="middle" fill="white">🍳</text>
</svg>
SVG

# Convertir en PNG (si ImageMagick est installé)
if command -v convert &> /dev/null; then
    convert -background none icon.svg -resize 16x16 icon16.png
    convert -background none icon.svg -resize 48x48 icon48.png
    convert -background none icon.svg -resize 128x128 icon128.png
    echo "✓ Icônes créées"
else
    echo "⚠️  ImageMagick non installé. Créez les icônes manuellement."
    echo "   Vous pouvez utiliser un emoji 🍳 comme icône temporaire."
fi
