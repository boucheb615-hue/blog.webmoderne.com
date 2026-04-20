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

# French month names for date formatting
MOIS_FR = {
    1: "janvier", 2: "février", 3: "mars", 4: "avril",
    5: "mai", 6: "juin", 7: "juillet", 8: "août",
    9: "septembre", 10: "octobre", 11: "novembre", 12: "décembre"
}

def iso_to_french(iso_date):
    """Convert ISO date (2026-04-12) to French format (12 avril 2026)."""
    try:
        dt = datetime.strptime(iso_date, "%Y-%m-%d")
        return f"{dt.day:02d} {MOIS_FR[dt.month]} {dt.year}"
    except (ValueError, KeyError):
        return iso_date

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
    if banner.startswith('http'):
        path_obj = Path(banner.split('blog.webmoderne.com')[-1])
        banner = str(path_obj) if 'blog.webmoderne.com' in banner else banner

    # Date — extract from JSON-LD datePublished (authoritative source)
    pub_iso = None
    mod_iso = None

    dp_match = re.search(r'"datePublished":\s*"([^"]+)"', content)
    if dp_match:
        pub_iso = dp_match.group(1)

    dm_match = re.search(r'"dateModified":\s*"([^"]+)"', content)
    if dm_match:
        mod_iso = dm_match.group(1)

    # Fallback
    if not pub_iso:
        vis_match = re.search(r'Publié le (\d{1,2})\s+(\S+)\s+(\d{4})', content)
        if vis_match:
            pub_iso = vis_match.group(0)

    # Convert ISO to French format
    if pub_iso and re.match(r'\d{4}-\d{2}-\d{2}', pub_iso):
        pub_date = iso_to_french(pub_iso)
    elif pub_iso:
        pub_date = pub_iso
    else:
        pub_date = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime("%d %B %Y")

    if mod_iso and re.match(r'\d{4}-\d{2}-\d{2}', mod_iso):
        mod_date = iso_to_french(mod_iso)
        display_date = f"Mis à jour le {mod_date}"
    else:
        display_date = f"Publié le {pub_date}"

    sort_date = pub_iso if pub_iso and re.match(r'\d{4}-\d{2}-\d{2}', pub_iso) else None

    return {
        "title": title,
        "description": description,
        "banner": banner,
        "pub_date": pub_date,
        "display_date": display_date,
        "link": f"/posts/{filepath.name}",
        "sort_date": sort_date,
        "mtime": os.path.getmtime(filepath)
    }

def generate_post_item_html(post):
    """Génère le HTML d'une carte d'article."""
    return f"""          <li class="post-item">
            <a href="{post['link']}">
              <img src="{post['banner']}" alt="{post['title']}" class="post-banner-thumb" loading="lazy">
            </a>
            <div class="post-item-content">
              <div class="date">{post['display_date']}</div>
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

    newest = posts[0] if posts else None
    if newest:
        content = re.sub(
            r'<div class="flash-alert">\s*<span class="flash-tag">.*?</span>\s*<a href="[^"]+">[^<]*</a>\s*</div>',
            f'<div class="flash-alert">\n          <span class="flash-tag">NOUVEAU</span>\n          <a href="{newest["link"]}">{newest["title"]}</a>\n        </div>',
            content,
            flags=re.DOTALL
        )

    latest_posts_block = f"""      <div class="latest-posts">
        <h3>Derniers Articles</h3>
        <ul class="post-list">
{articles_html}
          <li class="post-item no-hover" style="text-align: center; margin-top: 20px;">
            <a href="/posts/" style="color: var(--accent-color); font-family: var(--font-mono); font-weight: 600;">→ Voir tous les articles</a>
          </li>
        </ul>
      </div>"""

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

    num_pages = (len(posts) + MAX_PER_PAGE - 1) // MAX_PER_PAGE
    
    with open(ARCHIVE_INDEX, 'r', encoding='utf-8') as f:
        template = f.read()

    for i in range(num_pages):
        start = i * MAX_PER_PAGE
        end = start + MAX_PER_PAGE
        page_posts = posts[start:end]
        
        articles_html = "\n".join([generate_post_item_html(p) for p in page_posts])
        
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

        page_content = template
        if i > 0:
            page_content = page_content.replace("<h1>Tous les Décryptages</h1>", f"<h1>Archives - Page {i+1}</h1>")
            page_content = re.sub(r'<!-- ARTICLE EN VEDETTE -->.*?<h3', '<h3', page_content, flags=re.DOTALL)

        list_pattern = r'<ul class="post-list">.*?</ul>\s*(?:<div class="pagination">.*?</div>\s*)?'
        page_content = re.sub(list_pattern, f'<ul class="post-list">\n{articles_html}\n      </ul>\n{pagination_html}', page_content, flags=re.DOTALL)

        filename = ARCHIVE_INDEX if i == 0 else f"posts/page-{i+1}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(page_content)
        print(f"✅ Archive générée : {filename}")

def update_featured(posts):
    """Met à jour l'article vedette (À la Une) sur la page d'archives."""
    if not os.path.exists(ARCHIVE_INDEX):
        return

    newest = posts[0] if posts else None
    if not newest:
        return

    with open(ARCHIVE_INDEX, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract tags from the article for the featured section
    tags_text = ""
    try:
        article_path = os.path.join(POSTS_DIR, newest['link'].split('/')[-1])
        with open(article_path, 'r', encoding='utf-8') as af:
            art_content = af.read()
        tags_match = re.search(r'Tags\s*:\s*(.*?)(?:</p>|$)', art_content)
        if tags_match:
            # Keep the HTML spans as-is
            tags_raw = tags_match.group(1)
            span_match = re.findall(r'<span[^>]*>#[^<]+</span>', tags_raw)
            if span_match:
                tags_text = " ".join(span_match)
            else:
                # Plain text tags like "#IA #Foo"
                tags_text = " ".join([f'<span style="color: #00ff00;">{t.strip()}</span>' for t in tags_raw.split() if t.startswith('#')])
    except Exception as e:
        print(f"⚠️ Could not extract tags: {e}")

    # Build the new featured block — replace everything from <!-- ARTICLE EN VEDETTE --> to the closing </div> before <h3
    new_featured = f"""      <!-- ARTICLE EN VEDETTE -->
      <div class="featured-article" style="background: var(--code-bg); border: 2px solid var(--accent-color); border-radius: 8px; padding: 25px; margin: 30px 0;">
        <span style="color: var(--accent-color); font-family: var(--font-mono); font-size: 0.85em; text-transform: uppercase;">🔥 À la Une</span>
        <h2 style="margin: 10px 0;"><a href="{newest['link']}" style="color: var(--text-color); text-decoration: none;">{newest['title']}</a></h2>
        <p style="color: #aaa; margin: 10px 0;">{newest['description']}</p>
        <div style="display: flex; gap: 15px; align-items: center; margin-top: 15px; flex-wrap: wrap;">
          <span style="color: #888; font-family: var(--font-mono); font-size: 0.85em;">{newest['pub_date']}</span>
          <span style="color: #888; font-family: var(--font-mono); font-size: 0.85em;">•</span>
          <span style="color: var(--accent-color); font-family: var(--font-mono); font-size: 0.85em;">{tags_text}</span>
        </div>
      </div>"""

    # Replace from <!-- ARTICLE EN VEDETTE --> through the closing </div> that ends the featured-article div
    # Pattern: <!-- ARTICLE EN VEDETTE --> ... </div> (the one right before <h3 or whitespace+<h3)
    pattern = r'<!-- ARTICLE EN VEDETTE -->.*?</div>\s*\n(\s*<h3)'
    replacement = new_featured + '\n      \\1'
    
    new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)

    if count > 0:
        with open(ARCHIVE_INDEX, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ Article vedette mis à jour : {newest['title']}")
    else:
        print("⚠️ Impossible de mettre à jour l'article vedette (pattern non trouvé)")

def main():
    print(f"📄 Scan des articles...")
    posts_path = Path(POSTS_DIR)
    html_files = [f for f in posts_path.glob("*.html") if f.name != "index.html" and "page-" not in f.name]
    
    all_posts = []
    for f in html_files:
        meta = extract_metadata(f)
        if meta:
            all_posts.append(meta)
            
    all_posts.sort(key=lambda x: x['sort_date'] or datetime.fromtimestamp(x['mtime']).strftime("%Y-%m-%d"), reverse=True)
    
    if not all_posts:
        print("⚠️ Aucun article trouvé.")
        return

    update_homepage(all_posts)
    update_archives(all_posts)
    update_featured(all_posts)
    print("\nMission accomplie : Structure blog synchronisée.")

if __name__ == "__main__":
    main()
