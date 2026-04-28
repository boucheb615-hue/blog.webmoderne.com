import os
import re

def fix_html_v2(file_path):
    print(f"Processing {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix double <main>
    # If we have <main class="container"> and then <main>, remove the inner <main>
    content = content.replace('<main class="container">\n    \n    \n    <main>', '<main class="container">')
    content = content.replace('</main>\n    </main>', '</main>')

    # 2. Fix the stripped divs in value-prop
    # <div class="value-prop" > <div >
    # Replace with <div class="value-prop"> <div class="card">
    content = content.replace('<div class="value-prop" >', '<div class="value-prop">')
    # Use regex to find empty divs inside value-prop or feature-cards
    content = re.sub(r'<div >', r'<div class="card">', content)

    # 3. Ensure footer is correct
    if '</footer>\n</body>' not in content:
        content = content.replace('</footer>', '</footer>\n</body>')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

# Process all html files
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".html") and "_snippets" not in root and "view_logo" not in file:
            fix_html_v2(os.path.join(root, file))
