import sys
import os
import subprocess

def run_revision(draft_path):
    if not os.path.exists(draft_path):
        print(f"Erreur : Le fichier {draft_path} n'existe pas.")
        return

    print(f"🔍 Révision de {draft_path} en cours...")
    
    # On utilise hermes chat -q avec la skill editor pour réviser le fichier
    cmd = [
        "hermes", "chat", "-Q", "-s", "webmoderne-editor-agent",
        "-q", f"Révision complète du fichier suivant selon les règles V2 et le framework AIG. Renvoie directement le code HTML corrigé et complet :\n\n{open(draft_path).read()}"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        new_path = draft_path.replace(".html", "_revised.html")
        with open(new_path, "w") as f:
            f.write(result.stdout)
        print(f"✅ Révision terminée. Fichier sauvegardé sous : {new_path}")
    else:
        print(f"❌ Erreur lors de la révision : {result.stderr}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/auto_editor.py <path_to_draft>")
    else:
        run_revision(sys.argv[1])
