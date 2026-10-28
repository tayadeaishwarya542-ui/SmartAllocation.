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

TEST_GRAMMAR_JS = r'''// ================================================================
//  TransformAI — Hybrid Grammar Engine Automated Verification Suite
//  Validates: Mode A (AI), Mode B (Offline Rules), Automatic Fallback
// ================================================================

const fs = require('fs');
const path = require('path');
const vm = require('vm');

// Mock browser globals for Node.js test environment
global.escapeHtml = (str) => (str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
global.wordCount = (text) => text ? text.trim().split(/\s+/).filter(Boolean).length : 0;
global.AppState = {
  _settings: {
    provider: 'openai',
    keys: { openai: '' },
    models: { openai: 'gpt-4o-mini' }
  },
  getSetting(key) { return this._settings[key]; },
  getSettings() { return this._settings; },
  getPref() { return true; },
  updateSetting(k, v) { this._settings[k] = v; },
  addHistory() {}
};
global.Toast = { show: () => {} };

// Load transformations.js into global context
const transCode = fs.readFileSync(path.join(__dirname, '..', 'js', 'transformations.js'), 'utf-8');
vm.runInThisContext(transCode);

// Load api.js into global context
const apiCode = fs.readFileSync(path.join(__dirname, '..', 'js', 'api.js'), 'utf-8');
vm.runInThisContext(apiCode);

let passed = 0;
let failed = 0;

function assertEqual(actual, expected, testName) {
  if (actual === expected) {
    passed++;
    console.log(`  ✓ PASS: ${testName}`);
  } else {
    failed++;
    console.error(`  ✗ FAIL: ${testName}\n     Expected: "${expected}"\n     Actual:   "${actual}"`);
  }
}

function assertTrue(cond, testName, details = '') {
  if (cond) {
    passed++;
    console.log(`  ✓ PASS: ${testName}`);
  } else {
    failed++;
    console.error(`  ✗ FAIL: ${testName} - ${details}`);
  }
}

async function runGrammarTests() {
  console.log('================================================================');
  console.log('  TransformAI — Hybrid Grammar Correction Engine Verification');
  console.log('================================================================\n');

  // -------------------------------------------------------------
  // Test Group 1: The 9 Mandatory Test Cases (Mode B - Offline Rules)
  // -------------------------------------------------------------
  console.log('--- TEST GROUP 1: Mandatory Offline Rule Cases ---');
  const mandatoryCases = [
    { input: "she am girl", expected: "She is a girl." },
    { input: "he are happy", expected: "He is happy." },
    { input: "they is playing", expected: "They are playing." },
    { input: "i has a book", expected: "I have a book." },
    { input: "she go to school", expected: "She goes to school." },
    { input: "i am going to college", expected: "I am going to college." },
    { input: "this are my books", expected: "These are my books." },
    { input: "hello how are you", expected: "Hello, how are you?" },
    { input: "She is a girl.", expected: "She is a girl." }
  ];

  mandatoryCases.forEach(({ input, expected }, idx) => {
    const res = LocalNLP.grammar(input, {});
    assertEqual(res.correctedText, expected, `Rule Case ${idx + 1}: "${input}" -> "${expected}"`);
    assertTrue(res.diffHtml !== undefined, `Rule Case ${idx + 1}: Diff HTML generated`);
  });

  // -------------------------------------------------------------
  // Test Group 2: Generalized Grammatical Rules & Edge Cases
  // -------------------------------------------------------------
  console.log('\n--- TEST GROUP 2: Generalized Rules & Edge Cases ---');
  
  // Demonstrative agreement
  const dem1 = LocalNLP.grammar("that are my keys", {}).correctedText;
  assertEqual(dem1, "Those are my keys.", "Demonstrative: 'that are' -> 'Those are'");

  // 3rd person singular present inflection
  const verb1 = LocalNLP.grammar("he play football", {}).correctedText;
  assertEqual(verb1, "He plays football.", "Verb inflection: 'he play' -> 'He plays'");

  const verb2 = LocalNLP.grammar("she try hard", {}).correctedText;
  assertEqual(verb2, "She tries hard.", "Verb inflection: 'she try' -> 'She tries'");

  const verb3 = LocalNLP.grammar("he watch television", {}).correctedText;
  assertEqual(verb3, "He watches television.", "Verb inflection: 'he watch' -> 'He watches'");

  // Count noun article insertion
  const art1 = LocalNLP.grammar("he is boy", {}).correctedText;
  assertEqual(art1, "He is a boy.", "Missing article: 'he is boy' -> 'He is a boy.'");

  const art2 = LocalNLP.grammar("she is engineer", {}).correctedText;
  assertEqual(art2, "She is an engineer.", "Missing vowel article: 'she is engineer' -> 'She is an engineer.'");

  // Interrogative / Question Mark
  const q1 = LocalNLP.grammar("where do you live", {}).correctedText;
  assertEqual(q1, "Where do you live?", "Interrogative: 'where do you live' ends with '?'");

  const q2 = LocalNLP.grammar("what is your name", {}).correctedText;
  assertEqual(q2, "What is your name?", "Interrogative: 'what is your name' ends with '?'");

  // Idempotency: Correct sentences should remain pristine
  const correctText = "The team delivers high quality software every sprint.";
  const idemRes = LocalNLP.grammar(correctText, {}).correctedText;
  assertEqual(idemRes, correctText, "Idempotency: Pristine sentence remains completely unaltered");

  // -------------------------------------------------------------
  // Test Group 3: Word-Level Visual Diff Inspection
  // -------------------------------------------------------------
  console.log('\n--- TEST GROUP 3: Visual Diff Verification ---');
  const diffTest = LocalNLP.grammar("she am girl", {});
  assertTrue(diffTest.diffHtml.includes('<del class="diff-del">am</del>'), 'Visual diff tags deleted word "am"');
  assertTrue(diffTest.diffHtml.includes('<ins class="diff-ins">is a</ins>'), 'Visual diff tags inserted words "is a"');

  console.log('\n================================================================');
  console.log(`GRAMMAR TEST SUMMARY: ${passed} PASSED, ${failed} FAILED`);
  console.log('================================================================\n');

  if (failed > 0) process.exit(1);
}

runGrammarTests();
'''

save_file("tests/test_grammar_hybrid.js", TEST_GRAMMAR_JS)
print("Saved tests/test_grammar_hybrid.js successfully.")
