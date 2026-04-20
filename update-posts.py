#!/usr/bin/env python3
"""
update-posts.py - Génère automatiquement la liste des derniers articles avec bannières et pagination
Usage: python update-posts.py
"""

import os
import re
import sys
import html
from pathlib import Path
from datetime import datetime

# Configuration
POSTS_DIR = "posts"
INDEX_FILE = "index.html"
ARCHIVE_INDEX = "posts/index.html"
MAX_HOME = 5
MAX_PER_PAGE = 10

def extract_metadata(filepath):
    """Extrait le titre, la description, la date et la bannière d'un fichier HTML."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"⚠️ Erreur lors de la lecture de {filepath}: {e}")
        return None

    # Title
    title_match = re.search(r'<title>([^<]+)</title>', content)
    title = title_match.group(1) if title_match else "Sans titre"
    title = re.sub(r'\s*-\s*WebModerne$', '', title)
    title = html.escape(title)

    # Description
    desc_match = re.search(r'<meta name="description" content="([^"]+)"', content)
    description = desc_match.group(1) if desc_match else ""
    description = html.escape(description)

    # Banner
    banner_match = re.search(r'<meta property="og:image" content="([^"]+)"', content)
    banner = banner_match.group(1) if banner_match else "/static/logo.png"
    # Resolve relative paths if needed
    if banner.startswith('http'):
        path_obj = Path(banner.split('blog.webmoderne.com')[-1])
        banner = str(path_obj) if 'blog.webmoderne.com' in banner else banner

    # Date
    date_match = re.search(r'<div class="date">([^<]+)</div>', content)
    pub_date = date_match.group(1) if date_match else datetime.fromtimestamp(os.path.getmtime(filepath)).strftime("%d %B %Y")

    return {
        "title": title,
        "description": description,
        "banner": banner,
        "date": pub_date,
        "link": f"/posts/{filepath.name}",
        "mtime": os.path.getmtime(filepath)
    }

def generate_post_item_html(post):
    """Génère le HTML d'une carte d'article."""
    return f"""          <li class="post-item">
            <a href="{post['link']}">
              <img src="{post['banner']}" alt="{post['title']}" class="post-banner-thumb" loading="lazy">
            </a>
            <div class="post-item-content">
              <div class="date">{post['date']}</div>
              <h4><a href="{post['link']}">{post['title']}</a></h4>
              <div class="summary">{post['description']}</div>
            </div>
          </li>"""

def update_homepage(posts):
    """Met à jour les derniers articles sur la page d'accueil."""
    if not os.path.exists(INDEX_FILE):
        return

    home_posts = posts[:MAX_HOME]
    articles_html = "\n".join([generate_post_item_html(p) for p in home_posts])

    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Block replacement
    latest_posts_block = f"""      <div class="latest-posts">
        <h3>Derniers Articles</h3>
        <ul class="post-list">
{articles_html}
          <li class="post-item" style="text-align: center; margin-top: 20px; border: none; background: none; backdrop-filter: none;">
            <a href="/posts/" style="color: var(--accent-color); font-family: var(--font-mono); font-weight: 600;">→ Voir tous les articles</a>
          </li>
        </ul>
      </div>"""

    # Pattern matches the entire section until </main>
    pattern = r'      <div class="latest-posts">.*?</div>\s*</main>'
    replacement = f'{latest_posts_block}\n    </main>'
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"✅ Page d'accueil mise à jour ({len(home_posts)} articles)")

def update_archives(posts):
    """Génère les pages d'archives paginées."""
    if not os.path.exists(ARCHIVE_INDEX):
        return

    # Total pages
    num_pages = (len(posts) + MAX_PER_PAGE - 1) // MAX_PER_PAGE
    
    with open(ARCHIVE_INDEX, 'r', encoding='utf-8') as f:
        template = f.read()

    for i in range(num_pages):
        start = i * MAX_PER_PAGE
        end = start + MAX_PER_PAGE
        page_posts = posts[start:end]
        
        articles_html = "\n".join([generate_post_item_html(p) for p in page_posts])
        
        # Pagination HTML
        pagination_html = '<div class="pagination">'
        if i > 0:
            prev_link = "index.html" if i == 1 else f"page-{i}.html"
            pagination_html += f'<a href="{prev_link}">Précédent</a>'
        
        for p_idx in range(num_pages):
            p_link = "index.html" if p_idx == 0 else f"page-{p_idx + 1}.html"
            active_class = ' class="active"' if p_idx == i else ''
            pagination_html += f'<a href="{p_link}"{active_class}>{p_idx + 1}</a>'
            
        if i < num_pages - 1:
            next_link = f"page-{i + 2}.html"
            pagination_html += f'<a href="{next_link}">Suivant</a>'
        pagination_html += '</div>'

        # Content replacement
        page_content = template
        
        # Replace intro/title if not on first page
        if i > 0:
            page_content = page_content.replace("<h1>Tous les Décryptages</h1>", f"<h1>Archives - Page {i+1}</h1>")
            # Remove featured article on pages > 1
            page_content = re.sub(r'<!-- ARTICLE EN VEDETTE -->.*?<h3', '<h3', page_content, flags=re.DOTALL)

        # Replace post list and add pagination
        list_pattern = r'<ul class="post-list">.*?</ul>'
        page_content = re.sub(list_pattern, f'<ul class="post-list">\n{articles_html}\n      </ul>\n{pagination_html}', page_content, flags=re.DOTALL)

        # Write file
        filename = ARCHIVE_INDEX if i == 0 else f"posts/page-{i+1}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(page_content)
        print(f"✅ Archive générée : {filename}")

def main():
    print(f"📄 Scan des articles...")
    posts_path = Path(POSTS_DIR)
    html_files = [f for f in posts_path.glob("*.html") if f.name != "index.html" and "page-" not in f.name]
    
    all_posts = []
    for f in html_files:
        meta = extract_metadata(f)
        if meta:
            all_posts.append(meta)
            
    # Sort by date (mtime fallback)
    all_posts.sort(key=lambda x: x['mtime'], reverse=True)
    
    if not all_posts:
        print("⚠️ Aucun article trouvé.")
        return

    update_homepage(all_posts)
    update_archives(all_posts)
    print("\nMission accomplie : Structure blog synchronisée.")

if __name__ == "__main__":
    main()
