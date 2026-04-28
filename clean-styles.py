import os
import re
from pathlib import Path

def clean_articles():
    posts_dir = Path("/home/agentic/blog.webmoderne.com/posts")
    
    # Replacement patterns
    replacements = [
        (r'style="color: #00ff00;"', 'class="post-tag"'),
        (r'<nav class="toc" style="[^"]*">', '<nav class="toc-box">'),
        (r'<h4 style="color: var\(--accent-color\); [^"]*">', '<h4 class="toc-title">'),
        (r'<ul style="margin: 0; padding-left: 20px; color: #ddd;">', '<ul class="toc-list">'),
        (r'<li style="margin-bottom: 8px;">', '<li class="toc-item">'),
        (r'<a href="([^"]+)" style="color: var\(--accent-color\); text-decoration: none;">', r'<a href="\1">')
    ]
    
    for html_file in posts_dir.glob("*.html"):
        if html_file.name == "index.html" or html_file.name.startswith("page-"):
            continue
            
        print(f"Cleaning {html_file.name}...")
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
            
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    clean_articles()
