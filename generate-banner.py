#!/usr/bin/env python3
"""
generate-banner.py - Génère une bannière texte style terminal pour un article
Usage: python generate-banner.py "Titre" "output.png"
"""

import sys
import os
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=False):
    """Get a monospace font from common system paths."""
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/Monaco.ttf",
        "C:\\Windows\\Fonts\\consola.ttf",
        "C:\\Windows\\Fonts\\lucon.ttf",
    ]
    for path in paths:
        try:
            return ImageFont.truetype(path, size)
        except:
            continue
    return ImageFont.load_default()

def create_banner(title, subtitle, output_path, width=1200, height=630):
    # Couleurs WebModerne
    BG_COLOR = "#090935"  # Deep Midnight Blue
    TEXT_COLOR = "#ffffff"
    ACCENT_COLOR = "#db1a1a"  # Strong Red
    
    # Créer l'image
    img = Image.new('RGB', (width, height), color=BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Police monospace avec fallback
    font_title = get_font(48, bold=True)
    font_subtitle = get_font(28, bold=False)
    
    # Titre principal
    title_text = f"> {title}"
    bbox = draw.textbbox((0, 0), title_text, font=font_title)
    title_w = bbox[2] - bbox[0]
    title_h = bbox[3] - bbox[1]
    title_x = (width - title_w) // 2
    title_y = (height - title_h) // 2 - 30
    draw.text((title_x, title_y), title_text, fill=TEXT_COLOR, font=font_title)
    
    # Sous-titre
    subtitle_text = f"# {subtitle}"
    bbox = draw.textbbox((0, 0), subtitle_text, font=font_subtitle)
    subtitle_w = bbox[2] - bbox[0]
    subtitle_h = bbox[3] - bbox[1]
    subtitle_x = (width - subtitle_w) // 2
    subtitle_y = (height - subtitle_h) // 2 + 30
    draw.text((subtitle_x, subtitle_y), subtitle_text, fill=ACCENT_COLOR, font=font_subtitle)
    
    # Ligne décorative en bas
    draw.rectangle([(50, height - 80), (width - 50, height - 78)], fill=ACCENT_COLOR)
    
    # Sauvegarder
    img.save(output_path, 'PNG')
    print(f"✅ Bannière générée : {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate-banner.py 'Titre' 'output.png'")
        sys.exit(1)
    
    title = sys.argv[1]
    output = sys.argv[2]
    
    # Validate output path
    if not output.endswith('.png'):
        print("❌ Erreur: le fichier de sortie doit être un .png")
        sys.exit(1)
    
    # Ensure output directory exists
    output_dir = os.path.dirname(output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    subtitle = "WebModerne - arXiv décrypté"
    
    create_banner(title, subtitle, output)
