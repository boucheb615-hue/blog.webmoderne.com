#!/usr/bin/env python3
"""
Send blog draft preview to Telegram reports channel.
Usage: python3 send_draft_telegram.py <draft_html_path> <title>
"""

import sys
import re
import os
import subprocess

def extract_text_from_html(html_content):
    """Extract plain text from HTML."""
    text = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<nav[^>]*>.*?</nav>', '', text, flags=re.DOTALL)
    text = re.sub(r'<header[^>]*>.*?</header>', '', text, flags=re.DOTALL)
    text = re.sub(r'<footer[^>]*>.*?</footer>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '\n', text)
    
    # HTML entities
    entities = {
        '&agrave;': 'à', '&eacute;': 'é', '&egrave;': 'è', '&ecirc;': 'ê',
        '&iuml;': 'ï', '&ocirc;': 'ô', '&ucirc;': 'û', '&ccedil;': 'ç',
        '&laquo;': '«', '&raquo;': '»', '&amp;': '&', '&nbsp;': ' ',
        '&lt;': '<', '&gt;': '>', '&#39;': "'"
    }
    for entity, char in entities.items():
        text = text.replace(entity, char)
    
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = re.sub(r' +', ' ', text)
    return text.strip()

def send_to_telegram(text_preview, title):
    """Send message to Telegram reports channel."""
    chat_id = "-1003901746884"
    
    # Build message
    message = f"""📝 DRAFT BLOGUEUR

{title}

{text_preview}

[Consulter le fichier complet : /posts/drafts/]

✅ /approve — Publier ce brouillon
❌ /reject — À retravailler
📝 /edit — Proposer des modifications"""
    
    # Use tg-send or curl to Telegram Bot API
    # Assuming you have TELEGRAM_BOT_TOKEN in env
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        print("Error: TELEGRAM_BOT_TOKEN not set")
        return False
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    try:
        result = subprocess.run([
            "curl", "-s", "-X", "POST", url,
            "-d", f"chat_id={chat_id}",
            "-d", f"text={message}",
            "-d", "parse_mode=HTML"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print(f"✅ Draft sent to Telegram: {title}")
            return True
        else:
            print(f"❌ Failed to send: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 send_draft_telegram.py <html_path> <title>")
        sys.exit(1)
    
    html_path = sys.argv[1]
    title = sys.argv[2]
    
    if not os.path.exists(html_path):
        print(f"Error: File not found: {html_path}")
        sys.exit(1)
    
    with open(html_path, 'r') as f:
        html_content = f.read()
    
    text = extract_text_from_html(html_content)
    preview = text[:3000] + "\n\n[...article continue...]\n\nFichier : " + html_path
    
    success = send_to_telegram(preview, title)
    sys.exit(0 if success else 1)
