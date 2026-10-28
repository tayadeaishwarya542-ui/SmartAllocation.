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

PACKAGE_JSON = r'''{
  "name": "transformai-platform",
  "version": "1.0.0",
  "description": "Gen AI Platform for Automated Content Transformation — Hybrid Grammar Engine",
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "test": "node tests/test_suite.js && node tests/test_grammar_hybrid.js",
    "test:grammar": "node tests/test_grammar_hybrid.js",
    "test:regression": "node tests/test_suite.js"
  },
  "keywords": ["genai", "content-transformation", "pipelines", "hybrid-nlp", "grammar-engine"],
  "author": "TransformAI Team",
  "license": "MIT"
}
'''

save_file("package.json", PACKAGE_JSON)
