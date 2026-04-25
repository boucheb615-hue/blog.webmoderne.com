import sqlite3
import sys
import json
from datetime import datetime

DB_PATH = "/home/agentic/blog.webmoderne.com/social_analytics.db"

def log_post(fb_id, content, image_url):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO fb_posts (fb_id, content, image_url, last_updated)
            VALUES (?, ?, ?, ?)
        ''', (fb_id, content, image_url, datetime.now()))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def update_stats(fb_id, likes, comments, shares):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        UPDATE fb_posts 
        SET likes = ?, comments = ?, shares = ?, last_updated = ?
        WHERE fb_id = ?
    ''', (likes, comments, shares, datetime.now(), fb_id))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Simple CLI for the agent to use
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "log":
            # python log_manager.py log <id> <content> <url>
            log_post(sys.argv[2], sys.argv[3], sys.argv[4])
        elif cmd == "update":
            # python log_manager.py update <id> <likes> <comments> <shares>
            update_stats(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
