#!/bin/bash
# ============================================================
# WebModerne - Générateur de bannières pour articles
# Usage: ./generate-banner.sh --title "Titre" --subtitle "Sous-titre" --stats "stat1,stat2,stat3" --output "slug-banner.png"
# ============================================================

set -e

# Couleurs
BG_COLOR="9,9,53"        # #090935 - Deep Midnight Blue
ACCENT_COLOR="219,26,26" # #db1a1a - Strong Red
TEXT_COLOR="255,255,255" # White
DIM_COLOR="100,100,130"  # Dimmed
GREEN_COLOR="0,255,100"  # Terminal green

# Dimensions
WIDTH=1200
HEIGHT=630

# Valeurs par défaut
TITLE=""
SUBTITLE=""
STATS=""
OUTPUT=""
BRAND="WebModerne"
URL="blog.webmoderne.com"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --title) TITLE="$2"; shift 2 ;;
        --subtitle) SUBTITLE="$2"; shift 2 ;;
        --stats) STATS="$2"; shift 2 ;;
        --output) OUTPUT="$2"; shift 2 ;;
        --brand) BRAND="$2"; shift 2 ;;
        --url) URL="$2"; shift 2 ;;
        -h|--help)
            echo "Usage: $0 --title 'Titre' --subtitle 'Sous-titre' --stats 'stat1,stat2,stat3' --output 'slug-banner.png'"
            echo ""
            echo "Options:"
            echo "  --title     Titre principal (obligatoire)"
            echo "  --subtitle  Sous-titre explicatif (obligatoire)"
            echo "  --stats     Statistiques séparées par virgules (optionnel)"
            echo "  --output    Nom du fichier de sortie (obligatoire)"
            echo "  --brand     Nom de la marque (défaut: WebModerne)"
            echo "  --url       URL du site (défaut: blog.webmoderne.com)"
            exit 0
            ;;
        *) echo "Erreur: option inconnue $1"; exit 1 ;;
    esac
done

# Validation
if [[ -z "$TITLE" || -z "$OUTPUT" ]]; then
    echo "❌ Erreur: --title et --output sont obligatoires"
    echo "   Utilise --help pour l'aide"
    exit 1
fi

# Output path
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_PATH="${SCRIPT_DIR}/static/images/${OUTPUT}"

# Generate banner with Python
python3 << PYTHON_SCRIPT
from PIL import Image, ImageDraw, ImageFont
import os

# Config
BG_COLOR = (${BG_COLOR})
ACCENT_COLOR = (${ACCENT_COLOR})
TEXT_COLOR = (${TEXT_COLOR})
DIM_COLOR = (${DIM_COLOR})
GREEN_COLOR = (${GREEN_COLOR})

WIDTH = ${WIDTH}
HEIGHT = ${HEIGHT}
MARGIN = 80

# Create image
img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(img)

# Fonts
try:
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 52)
    subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 26)
    code_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 22)
    small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 16)
except:
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()
    code_font = ImageFont.load_default()
    small_font = ImageFont.load_default()

# === HEADER ===
draw.text((MARGIN, 30), "${BRAND}", fill=DIM_COLOR, font=small_font)

# Titre (centré)
title = "${TITLE}"
tb = draw.textbbox((0, 0), title, font=title_font)
draw.text(((WIDTH - tb[2]) // 2, 80), title, fill=ACCENT_COLOR, font=title_font)

# Sous-titre (centré)
subtitle = "${SUBTITLE}"
sb = draw.textbbox((0, 0), subtitle, font=subtitle_font)
draw.text(((WIDTH - sb[2]) // 2, 145), subtitle, fill=TEXT_COLOR, font=subtitle_font)

# Séparateur
draw.line([(MARGIN, 190), (WIDTH - MARGIN, 190)], fill=ACCENT_COLOR, width=2)

# === TERMINAL BOX ===
term_x = MARGIN
term_y = 230
term_w = WIDTH - (MARGIN * 2)
term_h = 320

# Bordure
draw.rectangle([(term_x, term_y), (term_x + term_w, term_y + term_h)], outline=ACCENT_COLOR, width=2)

# Header terminal
draw.rectangle([(term_x, term_y), (term_x + term_w, term_y + 28)], fill=ACCENT_COLOR)
draw.text((term_x + 12, term_y + 6), "terminal", fill=BG_COLOR, font=small_font)

# Contenu terminal
code_y = term_y + 55
line_h = 40

# Stats parsing
stats_list = "${STATS}".split(",") if "${STATS}" else []

lines = [
    ("$ analyse --target article", TEXT_COLOR),
    ("", None),
]

# Add stats dynamically
for stat in stats_list[:4]:  # Max 4 stats
    stat = stat.strip()
    if stat:
        lines.append((f"[✓] {stat}", DIM_COLOR))

lines.extend([
    ("", None),
    (">> ARTICLE DISPONIBLE", ACCENT_COLOR),
    (">> blog.webmoderne.com", GREEN_COLOR),
])

for i, (txt, col) in enumerate(lines):
    if col:
        draw.text((term_x + 25, code_y + (i * line_h)), txt, fill=col, font=code_font)

# === FOOTER ===
footer_y = HEIGHT - 25
draw.text((MARGIN, footer_y), "${URL}", fill=DIM_COLOR, font=small_font)

# Save
os.makedirs(os.path.dirname("${OUTPUT_PATH}"), exist_ok=True)
img.save("${OUTPUT_PATH}", 'PNG')

print(f"✅ Bannière générée : ${OUTPUT_PATH}")
print(f"   Dimensions : {WIDTH}x{HEIGHT}px")
print(f"   Taille : ~{os.path.getsize('${OUTPUT_PATH}')/1024:.1f}KB")
PYTHON_SCRIPT

echo ""
echo "🎉 Bannière prête !"
echo "   Fichier : ${OUTPUT_PATH}"
