import os, subprocess, time, sys

MIN_VALID_SIZE = 10000

def gen_pollinations(prompt, output_path, width=1024, height=1024, max_retries=3):
    for attempt in range(1, max_retries + 1):
        seed = int(time.time() * 1000) % 100000 + attempt
        full_prompt = prompt.replace(' ', '%20')
        url = f"https://image.pollinations.ai/prompt/{full_prompt}?width={width}&height={height}&nologo=true&seed={seed}"
        
        subprocess.run(
            ["curl", "-L", "-s", url, "-o", output_path, "-A", "Mozilla/5.0"],
            check=False
        )
        
        if os.path.exists(output_path) and os.path.getsize(output_path) >= MIN_VALID_SIZE:
            print(f"✅ Généré en {attempt} tentative(s) : {output_path} ({os.path.getsize(output_path)} octets)")
            return True
        
        print(f"⚠️ Tentative {attempt}/{max_retries} échouée (taille {os.path.getsize(output_path) if os.path.exists(output_path) else 0} octets). Retry...")
        time.sleep(1.5)
    
    print(f"✗ Échec définitif après {max_retries} tentatives.")
    return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python gen-pollinations.py '<prompt>' <output_path> [width] [height]")
        sys.exit(1)
    
    prompt = sys.argv[1]
    out = sys.argv[2]
    w = int(sys.argv[3]) if len(sys.argv) > 3 else 1024
    h = int(sys.argv[4]) if len(sys.argv) > 4 else 1024
    
    ok = gen_pollinations(prompt, out, w, h)
    sys.exit(0 if ok else 1)
