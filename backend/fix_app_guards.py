import os

BASE_DIR = r"C:\Users\hp\OneDrive\Desktop\content-transformer"
MIRROR_DIR = r"C:\Users\hp\OneDrive\Desktop\New folder\content-transformer"

def save_file(rel_path, content):
    for base in [BASE_DIR, MIRROR_DIR]:
        full_path = os.path.join(base, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Saved: {full_path} ({len(content)} chars)")

with open(r"C:\Users\hp\OneDrive\Desktop\content-transformer\js\app.js", "r", encoding="utf-8") as f:
    code = f.read()

# Replace document.addEventListener check
code = code.replace(
    "document.addEventListener('DOMContentLoaded', () => App.init());",
    "if (typeof document !== 'undefined') {\n  document.addEventListener('DOMContentLoaded', () => App.init());\n}"
)

# Replace window.location hash check
code = code.replace(
    "const hash = window.location.hash.replace('#', '').trim();",
    "const hash = (typeof window !== 'undefined' && window.location && window.location.hash) ? window.location.hash.replace('#', '').trim() : '';"
)

save_file("js/app.js", code)
print("Updated js/app.js with environment guards.")

