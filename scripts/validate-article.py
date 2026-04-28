#!/usr/bin/env python3
"""
validate-article.py — Vérifie qu'un article respecte les invariants du blog.
Usage: python validate-article.py posts/YYYY-MM-DD-slug.html
Retourne 0 si valide, exit(1) si invalide (pour CI/pre-commit).
"""

import re
import sys
from pathlib import Path

def validate(filepath):
    content = Path(filepath).read_text(encoding='utf-8')
    errors = []
    name = Path(filepath).name

    # 1. Nom de fichier
    if not re.match(r'^\d{4}-\d{2}-\d{2}-', name):
        errors.append(f"Nom invalide: doit commencer par YYYY-MM-DD-")

    # 2. Header social
    checks = [
        ('og:title', r'<meta property="og:title"'),
        ('og:description', r'<meta property="og:description"'),
        ('og:url', r'<meta property="og:url"'),
        ('og:type', r'<meta property="og:type"'),
        ('og:image absolue', r'<meta property="og:image" content="https://'),
        ('twitter:card', r'<meta name="twitter:card"'),
        ('twitter:image absolue', r'<meta name="twitter:image" content="https://'),
        ('canonical', r'<link rel="canonical"'),
        ('gtag', r'googletagmanager'),
        ('script ld+json', r'<script type="application/ld\+json">'),
    ]
    for label, pattern in checks:
        if not re.search(pattern, content):
            errors.append(f"Header manquant: {label}")

    # 3. Pas d'URL canonique morte (doit pointer vers le bon slug)
    slug = name.replace('.html', '')
    if not f'/posts/{slug}.html' in content:
        errors.append(f"Canonical/og:url ne pointe pas vers /posts/{slug}.html")

    # 4. Sommaire
    if 'nav class="toc-box"' not in content:
        errors.append("Sommaire manquant: nav class=\"toc-box\"")

    # 5. h2 avec id
    h2s = re.findall(r'<h2( id="[^"]+")?>([^<]+)</h2>', content)
    missing_ids = [h2[1] for h2 in h2s if not h2[0]]
    if missing_ids:
        errors.append(f"h2 sans id: {', '.join(missing_ids)}")

    # 6. Footer complet
    if 'footer-social' not in content:
        errors.append("Footer manquant (footer-social)")

    # 7. Pas de style="..." dans les balises meta/link du head
    head = re.search(r'<head>.*?</head>', content, re.DOTALL)
    if head:
        head_inline = re.findall(r'<(meta|link)[^>]* style="[^"]*"[^>]*>', head.group())
        if head_inline:
            errors.append(f"Styles inline dans le head: {len(head_inline)} éléments")

    # Résultat
    if errors:
        print(f"❌ {name} — {len(errors)} erreur(s):")
        for e in errors:
            print(f"    • {e}")
        return False
    else:
        print(f"✅ {name} — Valide")
        return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate-article.py FILE [FILE ...]")
        sys.exit(1)
    files = [f for f in sys.argv[1:] if not f.endswith('index.html') and 'page-' not in Path(f).name]
    if not files:
        print("Aucun article à valider.")
        sys.exit(0)
    all_valid = True
    for f in files:
        if not validate(f):
            all_valid = False
    sys.exit(0 if all_valid else 1)
