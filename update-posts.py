#!/usr/bin/env python3
"""
update-posts.py - Génère automatiquement la liste des derniers articles
Usage: python update-posts.py
"""

import os
import re
import sys
import html
from pathlib import Path
from datetime import datetime

POSTS_DIR = "posts"
INDEX_FILE = "index.html"
MAX_ARTICLES = 5  # Homepage performance: keeps initial load under 100KB

def extract_metadata(filepath):
    """Extract title, description and date from HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract title
    title_match = re.search(r'<title>([^<]+)</title>', content)
    title = title_match.group(1) if title_match else "Sans titre"
    title = re.sub(r'\s*-\s*WebModerne$', '', title)
    title = html.escape(title)  # Security: prevent XSS
    
    # Extract description
    desc_match = re.search(r'<meta name="description" content="([^"]+)"', content)
    description = desc_match.group(1) if desc_match else ""
    description = html.escape(description)  # Security: prevent XSS
    
    # Extract date from content (div class="date")
    date_match = re.search(r'<div class="date">([^<]+)</div>', content)
    if date_match:
        pub_date = date_match.group(1)
    else:
        # Fallback: use file modification date
        mtime = os.path.getmtime(filepath)
        pub_date = datetime.fromtimestamp(mtime).strftime("%d %B %Y")
    
    return title, description, pub_date

def main():
    print(f"📄 Scan des articles dans {POSTS_DIR}...")
    
    # Get all HTML files except index.html, sorted by modification time (newest first)
    posts_path = Path(POSTS_DIR)
    html_files = [f for f in posts_path.glob("*.html") if f.name != "index.html"]
    html_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    html_files = html_files[:MAX_ARTICLES]
    
    # Generate HTML for each article
    articles_html = ""
    for filepath in html_files:
        title, description, pub_date = extract_metadata(filepath)
        link = f"/posts/{filepath.stem}.html"
        
        articles_html += f"""          <li class="post-item">
            <h4><a href="{link}">{title}</a></h4>
            <div class="date">{pub_date}</div>
            <div class="summary">{description}</div>
          </li>
"""
    
    print(f"✅ {len(html_files)} articles trouvés")
    
    # Read index.html
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Build new latest-posts section
    latest_posts_block = f"""      <div class="latest-posts">
        <h3>Derniers Articles</h3>
        <ul class="post-list">
{articles_html}          <li class="post-item" style="text-align: center; margin-top: 20px;">
            <a href="/posts/" style="color: var(--accent-color); font-family: var(--font-mono); font-weight: 600;">→ Voir tous les articles</a>
          </li>
        </ul>
      </div>"""
    
    # Replace the latest-posts section
    pattern = r'      <div class="latest-posts">.*?</div>\s*</main>'
    replacement = f'{latest_posts_block}\n    </main>'
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Write back with error handling
    try:
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ {INDEX_FILE} mis à jour")
    except Exception as e:
        print(f"❌ Erreur écriture {INDEX_FILE}: {e}")
        sys.exit(1)
    print()
    print("Articles inclus :")
    for filepath in html_files:
        print(f"  - {filepath.name}")

if __name__ == "__main__":
    main()
