import os
import re
from pathlib import Path
from datetime import datetime

def update_sitemap():
    root_dir = Path("/home/agentic/blog.webmoderne.com")
    posts_dir = root_dir / "posts"
    sitemap_path = root_dir / "sitemap.xml"
    
    urls = [
        "https://blog.webmoderne.com/",
        "https://blog.webmoderne.com/about.html",
        "https://blog.webmoderne.com/posts/"
    ]
    
    # Add regular posts
    if posts_dir.exists():
        for post in posts_dir.glob("*.html"):
            if post.name == "index.html" or post.name.startswith("page-"):
                continue
            urls.append(f"https://blog.webmoderne.com/posts/{post.name}")
    
    urls.sort()
    
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+00:00")
    
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for url in urls:
        xml_content += f'  <url>\n    <loc>{url}</loc>\n    <lastmod>{now}</lastmod>\n    <priority>{"1.0" if url.endswith("/") else "0.8"}</priority>\n  </url>\n'
    
    xml_content += '</urlset>'
    
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(xml_content)
    
    print(f"✅ Sitemap updated with {len(urls)} URLs")

if __name__ == "__main__":
    update_sitemap()
