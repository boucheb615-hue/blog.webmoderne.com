#!/usr/bin/env python3
"""
add-toc.py — Injecte un sommaire standard dans les articles qui n'en ont pas.
Le sommaire est généré à partir des <h2 id="..."> existants.
Usage: python add-toc.py posts/ARTICLE.html
"""

import re
import sys
from pathlib import Path

def add_toc(filepath):
    content = Path(filepath).read_text(encoding='utf-8')

    # Already has TOC?
    if 'nav class="toc-box"' in content or 'nav class="toc"' in content:
        print(f"✅ Already has TOC: {Path(filepath).name}")
        return

    # Find all h2 with ids
    h2s = re.findall(r'<h2 id="([^"]+)">\s*([^<]+)', content)
    if not h2s:
        print(f"⚠️ No <h2 id=...> found: {Path(filepath).name}")
        return

    # Build TOC HTML
    toc_items = '\n'.join([f'          <li class="toc-item"><a href="#{hid}">{title.strip()}</a></li>' for hid, title in h2s])

    toc_block = f"""        <nav class="toc-box">
          <h4 class="toc-title">📋 Sommaire</h4>
          <ul class="toc-list">
{toc_items}
          </ul>
        </nav>
"""

    # Inject before the first <h2 id=...>
    first_h2 = re.search(r'<h2 id="[^"]+"', content)
    if not first_h2:
        print(f"⚠️ No <h2> found: {Path(filepath).name}")
        return

    pos = first_h2.start()
    new_content = content[:pos] + toc_block + content[pos:]

    Path(filepath).write_text(new_content, encoding='utf-8')
    print(f"✅ TOC added to {Path(filepath).name} ({len(h2s)} entries)")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python add-toc.py FILE [FILE ...]")
        sys.exit(1)
    for f in sys.argv[1:]:
        add_toc(f)
