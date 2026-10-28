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

with open(r"C:\Users\hp\OneDrive\Desktop\content-transformer\server.js", "r", encoding="utf-8") as f:
    code = f.read()

# Replace url.parse with WHATWG URL API
code = code.replace(
    "const parsedUrl = url.parse(req.url, true);\n  const pathname = parsedUrl.pathname;",
    "const parsedUrl = new URL(req.url, `http://${req.headers.host || 'localhost'}`);\n  const pathname = parsedUrl.pathname;"
)

save_file("server.js", code)
print("Updated server.js to use WHATWG URL API")

