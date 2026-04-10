#!/bin/bash
# Update all existing HTML posts with new header/footer template

BLOG_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
POSTS_DIR="$BLOG_DIR/posts"

# New header (up to </nav>)
NEW_HEADER='<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PLACEHOLDER_TITLE</title>
  <meta name="description" content="PLACEHOLDER_DESC">
  <meta name="author" content="WebModerne">
  <link rel="icon" type="image/png" href="/favicon.ico">
  
  <style>
    :root {
      --bg-color: #090935;
      --accent-color: #db1a1a;
      --text-color: #ffffff;
      --code-bg: #0a0a4a;
      --border-color: #1a1a5a;
    }
    * { box-sizing: border-box; }
    body {
      background-color: var(--bg-color);
      color: var(--text-color);
      font-family: '"'"'Courier New'"'"', '"'"'Consolas'"'"', '"'"'Monaco'"'"', monospace;
      line-height: 1.6;
      margin: 0;
      padding: 0;
    }
    .container { max-width: 900px; margin: 0 auto; padding: 20px; }
    .header {
      border-bottom: 2px solid var(--accent-color);
      padding: 30px 0;
      margin-bottom: 40px;
    }
    .header-content {
      display: flex;
      align-items: center;
      gap: 20px;
    }
    .logo {
      height: 60px;
      width: auto;
    }
    .header h1 {
      color: var(--accent-color);
      font-size: 2.5em;
      margin: 0;
      text-transform: uppercase;
      letter-spacing: 2px;
    }
    .header .subtitle {
      color: #aaa;
      font-size: 1.1em;
      margin-top: 10px;
    }
    .nav-toggle {
      display: none;
      background: none;
      border: 1px solid var(--accent-color);
      color: var(--text-color);
      padding: 8px 12px;
      cursor: pointer;
      font-family: inherit;
      font-size: 1.2em;
    }
    .nav { margin: 20px 0; }
    .nav a {
      color: var(--text-color);
      text-decoration: none;
      margin-right: 20px;
      padding: 8px 16px;
      border: 1px solid var(--accent-color);
      border-radius: 4px;
      transition: all 0.3s ease;
      display: inline-block;
    }
    .nav a:hover {
      background-color: var(--accent-color);
      color: var(--bg-color);
    }
    @media (max-width: 768px) {
      .nav-toggle {
        display: block;
        position: absolute;
        top: 20px;
        right: 20px;
      }
      .nav {
        display: none;
        flex-direction: column;
        margin-top: 20px;
      }
      .nav.active {
        display: flex;
      }
      .nav a {
        margin-bottom: 10px;
        margin-right: 0;
      }
      .header-content {
        flex-wrap: wrap;
      }
      .logo {
        height: 40px;
      }
      .header h1 {
        font-size: 1.5em;
      }
    }
    .terminal-box {
      background: var(--code-bg);
      border: 1px solid var(--border-color);
      border-left: 4px solid var(--accent-color);
      padding: 20px;
      margin: 20px 0;
      border-radius: 0 8px 8px 0;
    }
    .terminal-box h3 {
      color: var(--accent-color);
      margin-top: 0;
    }
    .post-content {
      background: var(--code-bg);
      padding: 30px;
      border-radius: 8px;
      border: 1px solid var(--border-color);
    }
    .post-content h1 {
      color: var(--accent-color);
      border-bottom: 2px solid var(--accent-color);
      padding-bottom: 15px;
      margin-top: 0;
    }
    .post-content h2 {
      color: var(--accent-color);
      margin-top: 30px;
    }
    .post-content h3 {
      color: var(--accent-color);
      margin-top: 25px;
    }
    .post-content .date {
      color: #888;
      margin-bottom: 20px;
    }
    .post-content p {
      color: #ddd;
    }
    .cli-illustration {
      background: #000;
      border: 1px solid var(--accent-color);
      padding: 15px;
      margin: 20px 0;
      border-radius: 4px;
      font-family: '"'"'Courier New'"'"', monospace;
      font-size: 0.9em;
    }
    .cli-illustration .prompt { color: #00ff00; }
    .cli-illustration .output { color: #ccc; margin-left: 20px; }
    .cli-illustration .agent { color: var(--accent-color); font-weight: bold; }
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 20px 0;
    }
    th, td {
      border: 1px solid var(--border-color);
      padding: 10px;
      text-align: left;
    }
    th {
      background: var(--code-bg);
      color: var(--accent-color);
    }
    .footer {
      margin-top: 60px;
      padding-top: 20px;
      border-top: 1px solid var(--border-color);
      text-align: center;
      color: #666;
      font-size: 0.9em;
    }
    a { color: var(--accent-color); text-decoration: none; }
    a:hover { text-decoration: underline; }
    @media (max-width: 768px) {
      .container { padding: 15px; }
      .header h1 { font-size: 1.8em; }
      .nav a { display: block; margin-bottom: 10px; }
      .post-content { padding: 20px; }
    }
  </style>
</head>
<body>
  <div class="container">
    <header class="header">
      <div class="header-content">
        <img src="/static/logo.png" alt="WebModerne Logo" class="logo">
        <div>
          <h1>WebModerne</h1>
          <div class="subtitle">L'"'"'IA expliquée simplement aux non-techniques</div>
        </div>
      </div>
      <button class="nav-toggle" onclick="document.querySelector('"'"'.nav'"'"').classList.toggle('"'"'active'"'"')">☰</button>
    </header>
    
    <nav class="nav">
      <a href="/">Accueil</a>
      <a href="/about.html">À Propos</a>
      <a href="/posts/">Articles</a>
      <a href="https://youtube.com/@WebModerne" target="_blank" rel="noopener">YouTube</a>
    </nav>
    
    <main>'

# New footer
NEW_FOOTER='    </main>
    
    <footer class="footer">
      <p>&copy; 2026 WebModerne - Tous droits réservés</p>
      <p><a href="https://youtube.com/@WebModerne" style="color: #db1a1a;">YouTube</a></p>
    </footer>
  </div>
</body>
</html>'

echo "Updating existing posts..."

for file in "$POSTS_DIR"/*.html; do
    if [ -f "$file" ]; then
        fname=$(basename "$file")
        echo "Processing $fname..."
        
        # Extract title from existing file
        title=$(grep "<title>" "$file" | sed 's/.*<title>\(.*\)<\/title>.*/\1/')
        desc=$(grep "<meta name=\"description\"" "$file" | sed 's/.*content="\([^"]*\)".*/\1/')
        
        # Extract main content (between </nav> and </main>)
        content=$(sed -n '/<\/nav>/,/<\/main>/p' "$file" | sed '1d;$d')
        
        # Build new file
        header="$NEW_HEADER"
        header="${header//PLACEHOLDER_TITLE/$title}"
        header="${header//PLACEHOLDER_DESC/$desc}"
        
        echo "$header" > "$file"
        echo "$content" >> "$file"
        echo "$NEW_FOOTER" >> "$file"
        
        echo "  ✓ Updated $fname"
    fi
done

echo ""
echo "All posts updated!"
