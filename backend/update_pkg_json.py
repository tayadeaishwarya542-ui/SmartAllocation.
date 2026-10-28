import os
import json

BASE_DIR = r"C:\Users\hp\OneDrive\Desktop\content-transformer"
MIRROR_DIR = r"C:\Users\hp\OneDrive\Desktop\New folder\content-transformer"

def save_file(rel_path, content):
    for base in [BASE_DIR, MIRROR_DIR]:
        full_path = os.path.join(base, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Saved: {full_path} ({len(content)} chars)")

PACKAGE_JSON = """{
  "name": "transformai-platform",
  "version": "1.0.0",
  "description": "Gen AI SaaS Platform for Content Transformation, Quiz Generation & Multi-Tenant SQLite Auth",
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "test": "node tests/test_suite.js && node tests/test_grammar_hybrid.js && node tests/test_quiz_generator.js && node tests/test_auth_system.js",
    "test:auth": "node tests/test_auth_system.js",
    "test:quiz": "node tests/test_quiz_generator.js",
    "test:grammar": "node tests/test_grammar_hybrid.js",
    "test:regression": "node tests/test_suite.js"
  },
  "keywords": [
    "genai",
    "content-transformation",
    "pipelines",
    "hybrid-nlp",
    "authentication",
    "sqlite-multitenancy"
  ],
  "author": "TransformAI Team",
  "license": "MIT"
}
"""

save_file("package.json", PACKAGE_JSON)
print("Updated package.json")

