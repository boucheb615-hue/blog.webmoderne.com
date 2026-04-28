import sys
import requests
import json
import os
from pathlib import Path

def get_image_url(image_source):
    """
    Returns the URL if it's a URL. 
    If it's a local path, we can't send it via URL, 
    so we return None or the path (but the user specifically asked for URL only).
    """
    if not image_source:
        return None
        
    if image_source.startswith(('http://', 'https://')):
        return image_source
        
    return None # We don't send local paths as URLs

def send_fb_webhook(webhook_url, text, image_source=None):
    """Envoie une requête POST au webhook configuré avec uniquement l'URL."""
    url = get_image_url(image_source)
    
    payload = {
        "text": text,
        "image": url, # Renamed to 'image' as requested
        "source": "Hermes Agent",
        "agent": "Hermes-WebModerne-Core"
    }
    
    # We stripped b64 and image_data fields as requested.
    
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(webhook_url, data=json.dumps(payload), headers=headers, timeout=15)
        return response.status_code, response.text
    except Exception as e:
        return 500, str(e)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python fb_post.py <webhook_url> <text> [image_url]")
        sys.exit(1)
        
    status, result = send_fb_webhook(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
    print(json.dumps({"status": status, "result": result}))
