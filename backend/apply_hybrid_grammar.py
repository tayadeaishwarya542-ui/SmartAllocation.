import os
import re

BASE_DIR = r"C:\Users\hp\OneDrive\Desktop\content-transformer"
MIRROR_DIR = r"C:\Users\hp\OneDrive\Desktop\New folder\content-transformer"

def save_file(rel_path, content):
    for base in [BASE_DIR, MIRROR_DIR]:
        full_path = os.path.join(base, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Saved: {full_path} ({len(content)} chars)")

# =====================================================================
# 1. Update js/transformations.js
# =====================================================================
with open(os.path.join(BASE_DIR, "js", "transformations.js"), "r", encoding="utf-8") as f:
    trans_content = f.read()

# Replace grammar method in LocalNLP
old_grammar_pattern = r"  grammar\(text, opts = \{\}\) \{[\s\S]*?\n  expand\(text,"

new_grammar_code = r'''  createWordDiff(origText, corrText) {
    const origWords = (origText || '').split(/(\s+)/);
    const corrWords = (corrText || '').split(/(\s+)/);
    let diffHtml = '';
    const maxLen = Math.max(origWords.length, corrWords.length);
    for (let i = 0; i < maxLen; i++) {
      const ow = origWords[i] || '';
      const cw = corrWords[i] || '';
      if (ow === cw) {
        diffHtml += escapeHtml(cw);
      } else {
        if (ow.trim()) diffHtml += `<del class="diff-del">${escapeHtml(ow)}</del>`;
        if (cw.trim()) diffHtml += `<ins class="diff-ins">${escapeHtml(cw)}</ins>`;
        if (!ow.trim() && !cw.trim()) diffHtml += cw;
      }
    }
    return diffHtml;
  },

  inflectThirdPerson(verb) {
    verb = (verb || '').toLowerCase();
    const irregular = { have: 'has', be: 'is', do: 'does', go: 'goes' };
    if (irregular[verb]) return irregular[verb];
    if (/(?:s|sh|ch|x|z|o)$/.test(verb)) return verb + 'es';
    if (/[^aeiou]y$/.test(verb)) return verb.slice(0, -1) + 'ies';
    return verb + 's';
  },

  grammar(text, opts = {}) {
    if (!text || !text.trim()) {
      return { correctedText: '', diffHtml: '' };
    }

    let corrected = text.trim();

    // Pass 1: Spacing around punctuation
    corrected = corrected.replace(/\s+([.,!?;:])/g, '$1');
    corrected = corrected.replace(/([.,!?;:])(?=[A-Za-z0-9])/g, '$1 ');

    // Pass 2: Salutations & Greeting openers
    corrected = corrected.replace(
      /\b(hello|hi|hey)\s+(how|what|who|where|why|when|are|is|can|could|would|should|do|does|did)\b/gi,
      '$1, $2'
    );

    // Pass 3: Demonstrative agreement
    corrected = corrected.replace(/\b(this)\s+(are|were)\b/gi, 'these $2');
    corrected = corrected.replace(/\b(that)\s+(are|were)\b/gi, 'those $2');
    corrected = corrected.replace(/\b(these)\s+(is|was)\b/gi, 'these are');
    corrected = corrected.replace(/\b(those)\s+(is|was)\b/gi, 'those are');

    // Pass 4: Subject-Verb Agreement (Be, Have, Do)
    corrected = corrected.replace(/\b(he|she|it)\s+(am|are)\b/gi, '$1 is');
    corrected = corrected.replace(/\b(he|she|it)\s+were\b/gi, '$1 was');
    corrected = corrected.replace(/\b(he|she|it)\s+have\b/gi, '$1 has');
    corrected = corrected.replace(/\b(he|she|it)\s+do\b/gi, '$1 does');

    corrected = corrected.replace(/\b(they|we|you)\s+(is|am)\b/gi, '$1 are');
    corrected = corrected.replace(/\b(they|we|you)\s+was\b/gi, '$1 were');
    corrected = corrected.replace(/\b(they|we|you)\s+has\b/gi, '$1 have');
    corrected = corrected.replace(/\b(they|we|you)\s+does\b/gi, '$1 do');

    corrected = corrected.replace(/\b(i)\s+(is|are)\b/gi, '$1 am');
    corrected = corrected.replace(/\b(i)\s+has\b/gi, '$1 have');

    // Pass 5: 3rd person singular present inflection for common verbs
    const commonVerbs = new Set([
      'go', 'do', 'come', 'see', 'say', 'make', 'take', 'know', 'think', 'look',
      'want', 'give', 'use', 'find', 'tell', 'ask', 'work', 'seem', 'feel', 'try',
      'leave', 'call', 'play', 'run', 'walk', 'write', 'read', 'speak', 'eat',
      'sing', 'drive', 'like', 'need', 'help', 'live', 'start', 'love', 'listen',
      'watch', 'study', 'talk', 'stay', 'stand', 'sit', 'open', 'close', 'send'
    ]);

    corrected = corrected.replace(/\b(he|she|it)\s+([a-zA-Z]+)\b/gi, (match, subj, verb) => {
      const lowerVerb = verb.toLowerCase();
      if (commonVerbs.has(lowerVerb)) {
        const inflected = this.inflectThirdPerson(lowerVerb);
        return `${subj} ${inflected}`;
      }
      return match;
    });

    // Pass 6: Missing count noun article after copula verbs (is|am|are|was|were)
    const countNouns = new Set([
      'girl', 'boy', 'child', 'man', 'woman', 'student', 'teacher', 'doctor', 'nurse',
      'engineer', 'developer', 'book', 'car', 'pen', 'phone', 'computer', 'dog', 'cat',
      'house', 'school', 'college', 'apple', 'orange', 'table', 'chair', 'problem',
      'question', 'game', 'player', 'room', 'friend', 'family', 'song', 'movie'
    ]);

    corrected = corrected.replace(/\b(is|am|are|was|were)\s+([a-zA-Z]+)\b/gi, (match, copula, noun) => {
      const lowerNoun = noun.toLowerCase();
      if (countNouns.has(lowerNoun)) {
        const article = /^[aeiou]/i.test(lowerNoun) ? 'an' : 'a';
        return `${copula} ${article} ${noun}`;
      }
      return match;
    });

    // Pass 7: Pronoun "I" and Capitalization
    corrected = corrected.replace(/\b(i)\b/g, 'I');
    corrected = corrected.replace(/(^|[.?!]\s+)([a-z])/g, (m, p1, p2) => p1 + p2.toUpperCase());

    // Pass 8: Spelling dictionary
    Object.keys(this.spellingDict).forEach(typo => {
      const regex = new RegExp(`\\b${typo}\\b`, 'gi');
      corrected = corrected.replace(regex, (m) => {
        const fix = this.spellingDict[typo];
        if (m[0] === m[0].toUpperCase()) {
          return fix.charAt(0).toUpperCase() + fix.slice(1);
        }
        return fix;
      });
    });

    // Pass 9: Terminal Punctuation & Question Detection
    let trimmed = corrected.trim();
    if (trimmed.length > 0) {
      if (!/[.?!]$/.test(trimmed)) {
        if (/^(?:hello,\s+|hi,\s+|hey,\s+)?(?:how|what|why|who|where|when|which|can|could|would|should|will|is|are|am|do|does|did)\b/i.test(trimmed)) {
          trimmed += '?';
        } else {
          trimmed += '.';
        }
      }
      corrected = trimmed;
    }

    // Pass 10: Accurate Word-level Visual Diff
    const diffHtml = this.createWordDiff(text, corrected);

    return {
      correctedText: corrected,
      diffHtml
    };
  },

  expand(text,'''

trans_content = re.sub(old_grammar_pattern, lambda m: new_grammar_code, trans_content)

# Update TRANSFORMATIONS.grammar definition
old_trans_grammar = r"  grammar: \{[\s\S]*?\n  \},"
new_trans_grammar = r'''  grammar: {
    id: 'grammar',
    label: 'Grammar & Spell Check',
    icon: 'ri-spell-check-line',
    color: 'purple',
    desc: 'Hybrid grammar correction: AI-powered with automatic offline fallback & visual diff',
    buildPrompt(input, opts = {}) {
      return `You are an expert grammar and copy editor. Correct all grammatical errors, subject-verb disagreement, verb tense/form errors, missing articles, spelling mistakes, typos, and punctuation faults in the following text.
Strict Requirements:
1. Preserve the intended meaning, factual information, personal names, and author voice.
2. Return ONLY the clean corrected text. Do NOT add preamble, conversational notes, or explanations unless explicitly asked.

Text to correct:
${input}`;
    },
    extraOptions: [
      { id: 'mode', label: 'Correction Mode', type: 'select', choices: [
        { value: 'hybrid', label: 'Hybrid (AI with Auto Fallback)' },
        { value: 'ai', label: 'Mode A: AI-Powered' },
        { value: 'offline', label: 'Mode B: Offline Local Engine' }
      ], default: 'hybrid' },
      { id: 'autoFallback', label: 'Automatic Offline Fallback', type: 'select', choices: [
        { value: 'yes', label: 'Enabled (Fallback to Local on AI Error)' },
        { value: 'no', label: 'Disabled (Show AI Error)' }
      ], default: 'yes' },
      { id: 'showDiff', label: 'Display Comparison', type: 'select', choices: [
        { value: 'yes', label: 'Show Visual Diff' },
        { value: 'no', label: 'Clean Corrected Text Only' }
      ], default: 'yes' }
    ]
  },'''

trans_content = re.sub(old_trans_grammar, lambda m: new_trans_grammar, trans_content)
save_file("js/transformations.js", trans_content)

print("Updated js/transformations.js successfully.")
