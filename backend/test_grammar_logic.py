import re

def inflect_third_person_singular(verb):
    verb = verb.lower()
    irregular = {
        'have': 'has',
        'be': 'is',
        'do': 'does',
        'go': 'goes',
    }
    if verb in irregular:
        return irregular[verb]
    if re.search(r'(?:s|sh|ch|x|z|o)$', verb):
        return verb + 'es'
    if re.search(r'[^aeiou]y$', verb):
        return verb[:-1] + 'ies'
    return verb + 's'

COMMON_VERBS = {
    'go', 'do', 'come', 'see', 'say', 'make', 'take', 'know', 'think', 'look',
    'want', 'give', 'use', 'find', 'tell', 'ask', 'work', 'seem', 'feel', 'try',
    'leave', 'call', 'play', 'run', 'walk', 'write', 'read', 'speak', 'eat',
    'sing', 'drive', 'like', 'need', 'help', 'live', 'start', 'love', 'listen',
    'watch', 'study', 'talk', 'stay', 'stand', 'sit', 'open', 'close', 'send'
}

COUNT_NOUNS = {
    'girl', 'boy', 'child', 'man', 'woman', 'student', 'teacher', 'doctor', 'nurse',
    'engineer', 'developer', 'book', 'car', 'pen', 'phone', 'computer', 'dog', 'cat',
    'house', 'school', 'college', 'apple', 'orange', 'table', 'chair', 'problem',
    'question', 'game', 'player', 'room', 'friend', 'family', 'song', 'movie'
}

SPELLING_DICT = {
    'teh': 'the',
    'recieve': 'receive',
    'seperate': 'separate',
    'definately': 'definitely',
    'occured': 'occurred',
    'untill': 'until',
    'wich': 'which',
    'accommodate': 'accommodate',
    'embarass': 'embarrass',
    'goverment': 'government',
    'truely': 'truly',
    'wierd': 'weird'
}

def offline_grammar(text, opts=None):
    if not text or not text.strip():
        return {'correctedText': '', 'diffHtml': ''}
    
    corrected = text.strip()

    # Pass 1: Spacing around punctuation
    corrected = re.sub(r'\s+([.,!?;:])', r'\1', corrected)
    corrected = re.sub(r'([.,!?;:])(?=[A-Za-z0-9])', r'\1 ', corrected)

    # Pass 2: Salutations
    corrected = re.sub(
        r'\b(hello|hi|hey)\s+(how|what|who|where|why|when|are|is|can|could|would|should|do|does|did)\b',
        r'\1, \2',
        corrected,
        flags=re.IGNORECASE
    )

    # Pass 3: Demonstrative agreement
    corrected = re.sub(r'\b(this)\s+(are|were)\b', r'these \2', corrected, flags=re.IGNORECASE)
    corrected = re.sub(r'\b(that)\s+(are|were)\b', r'those \2', corrected, flags=re.IGNORECASE)
    corrected = re.sub(r'\b(these)\s+(is|was)\b', r'these are', corrected, flags=re.IGNORECASE)
    corrected = re.sub(r'\b(those)\s+(is|was)\b', r'those are', corrected, flags=re.IGNORECASE)

    # Pass 4: Subject-Verb Agreement (Be & Have & Do)
    # 3rd person singular pronouns with am/are -> is, have -> has, were -> was
    corrected = re.sub(r'\b(he|she|it)\s+(am|are)\b', r'\1 is', corrected, flags=re.IGNORECASE)
    corrected = re.sub(r'\b(he|she|it)\s+were\b', r'\1 was', corrected, flags=re.IGNORECASE)
    corrected = re.sub(r'\b(he|she|it)\s+have\b', r'\1 has', corrected, flags=re.IGNORECASE)
    corrected = re.sub(r'\b(he|she|it)\s+do\b', r'\1 does', corrected, flags=re.IGNORECASE)

    # Plural pronouns with is/am -> are, has -> have, was -> were
    corrected = re.sub(r'\b(they|we|you)\s+(is|am)\b', r'\1 are', corrected, flags=re.IGNORECASE)
    corrected = re.sub(r'\b(they|we|you)\s+was\b', r'\1 were', corrected, flags=re.IGNORECASE)
    corrected = re.sub(r'\b(they|we|you)\s+has\b', r'\1 have', corrected, flags=re.IGNORECASE)
    corrected = re.sub(r'\b(they|we|you)\s+does\b', r'\1 do', corrected, flags=re.IGNORECASE)

    # First person pronoun I with is/are -> am, has -> have
    corrected = re.sub(r'\b(i)\s+(is|are)\b', r'\1 am', corrected, flags=re.IGNORECASE)
    corrected = re.sub(r'\b(i)\s+has\b', r'\1 have', corrected, flags=re.IGNORECASE)

    # Pass 5: 3rd person singular present inflection for common verbs
    def replace_third_person_verb(match):
        subj = match.group(1)
        verb = match.group(2)
        lower_verb = verb.lower()
        if lower_verb in COMMON_VERBS:
            inflected = inflect_third_person_singular(lower_verb)
            return f"{subj} {inflected}"
        return match.group(0)

    corrected = re.sub(r'\b(he|she|it)\s+([a-zA-Z]+)\b', replace_third_person_verb, corrected, flags=re.IGNORECASE)

    # Pass 6: Missing count noun article after copula verbs (is|am|are|was|were)
    # "she is girl" -> "she is a girl"
    def insert_article(match):
        copula = match.group(1)
        noun = match.group(2)
        lower_noun = noun.lower()
        if lower_noun in COUNT_NOUNS:
            article = 'an' if lower_noun[0] in 'aeiou' else 'a'
            return f"{copula} {article} {noun}"
        return match.group(0)

    # Match linking verb directly followed by singular count noun (not already preceded by a/an/the/my etc)
    corrected = re.sub(
        r'\b(is|am|are|was|were)\s+([a-zA-Z]+)\b',
        insert_article,
        corrected,
        flags=re.IGNORECASE
    )

    # Pass 7: Pronoun "I" and Capitalization
    corrected = re.sub(r'\b(i)\b', 'I', corrected)
    # Capitalize after start of string or sentence boundary (. ! ?)
    corrected = re.sub(r'(^|[.?!]\s+)([a-z])', lambda m: m.group(1) + m.group(2).upper(), corrected)

    # Pass 8: Spelling dictionary
    for typo, fix in SPELLING_DICT.items():
        pattern = re.compile(rf'\b{typo}\b', re.IGNORECASE)
        def replace_spelling(m, f=fix):
            if m.group(0)[0].isupper():
                return f.capitalize()
            return f
        corrected = pattern.sub(replace_spelling, corrected)

    # Pass 9: Terminal Punctuation & Question Mark
    trimmed = corrected.strip()
    if trimmed:
        if not re.search(r'[.?!]$', trimmed):
            # Check if sentence is a question
            if re.search(r'^(?:hello,\s+|hi,\s+|hey,\s+)?(?:how|what|why|who|where|when|which|can|could|would|should|will|is|are|am|do|does|did)\b', trimmed, re.IGNORECASE):
                trimmed += '?'
            else:
                trimmed += '.'
        corrected = trimmed

    return corrected

# Verification against test cases
test_cases = [
    ("she am girl", "She is a girl."),
    ("he are happy", "He is happy."),
    ("they is playing", "They are playing."),
    ("i has a book", "I have a book."),
    ("she go to school", "She goes to school."),
    ("i am going to college", "I am going to college."),
    ("this are my books", "These are my books."),
    ("hello how are you", "Hello, how are you?"),
    ("She is a girl.", "She is a girl.")
]

all_passed = True
for inp, expected in test_cases:
    actual = offline_grammar(inp)
    status = "PASS" if actual == expected else "FAIL"
    if status == "FAIL":
        all_passed = False
    print(f"[{status}] Input: '{inp}' -> Actual: '{actual}' | Expected: '{expected}'")

if all_passed:
    print("\nALL 9 TEST CASES PASSED PERFECTLY!")
