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

# 1. Update db.js
with open(r"C:\Users\hp\OneDrive\Desktop\content-transformer\db.js", "r", encoding="utf-8") as f:
    db_code = f.read()

db_code = db_code.replace(
    "INSERT INTO user_practice_attempts (id, user_id, set_id, score, correct_count, total_questions, answers_json, timestamp)",
    "INSERT OR REPLACE INTO user_practice_attempts (id, user_id, set_id, score, correct_count, total_questions, answers_json, timestamp)"
)

db_code = db_code.replace(
    "INSERT INTO user_history (id, user_id, type, input_text, output_text, metrics_json, options_json, created_at)",
    "INSERT OR REPLACE INTO user_history (id, user_id, type, input_text, output_text, metrics_json, options_json, created_at)"
)

save_file("db.js", db_code)

# 2. Update test_auth_system.js
with open(r"C:\Users\hp\OneDrive\Desktop\content-transformer\tests\test_auth_system.js", "r", encoding="utf-8") as f:
    test_code = f.read()

test_code = test_code.replace(
    "attempt: { id: `att_alice_1`, score: 95, correctCount: 1, totalQuestions: 1 }",
    "attempt: { id: `att_alice_1_${Date.now()}`, score: 95, correctCount: 1, totalQuestions: 1 }"
)

save_file("tests/test_auth_system.js", test_code)
print("Updated db.js and test_auth_system.js with INSERT OR REPLACE and dynamic attempt ID.")

