import os
import re

def fix_html(file_path):
    print(f"Processing {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Structure Change: Move header out of container
    # Find the header block
    header_match = re.search(r'(<header.*?</header>)', content, re.DOTALL)
    if header_match:
        header_html = header_match.group(1)
        # Remove it from current position
        content = content.replace(header_html, '')
        # Ensure it is at the start of body
        content = re.sub(r'(<body.*?>)', r'\1\n' + header_html, content)

    # 2. Structure Change: Move footer out of container
    footer_match = re.search(r'(<footer.*?</footer>)', content, re.DOTALL)
    if footer_match:
        footer_html = footer_match.group(1)
        content = content.replace(footer_html, '')
        content = content.replace('</body>', footer_html + '\n</body>')

    # 3. Clean up the container/main
    # If the container still wraps everything, let's fix it.
    # Usually it looks like: <body> <div class="container"> ... </body>
    # We want: <body> <header> <main class="container"> ... </main> <footer> </body>
    
    # Replace <div class="container"> with <main class="container"> if it's the main wrapper
    content = content.replace('<div class="container">', '<main class="container">')
    content = content.replace('</div>\n    <footer', '</main>\n    <footer')
    # If footer was already moved, we might need a different closing
    if '</main>' not in content and '<main class="container">' in content:
        content = content.replace('</body>', '</main>\n</body>')

    # 4. Remove redundant inline styles
    content = re.sub(r'style="display: flex; gap: 20px; flex-wrap: wrap; margin: 40px 0;"', '', content)
    content = re.sub(r'style="flex: 1 1 250px; background: var\(--code-bg\); padding: 20px; border-radius: 8px; border: 1px solid var\(--border-color\);"', '', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

# Process all html files
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".html") and "_snippets" not in root:
            fix_html(os.path.join(root, file))
