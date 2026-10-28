with open(r"C:\Users\hp\OneDrive\Desktop\content-transformer\js\api.js", "r", encoding="utf-8") as f:
    content = f.read()

import re
matches = [m.start() for m in re.finditer(r"_executeGrammarHybrid", content)]
print(f"Occurrences of _executeGrammarHybrid: {len(matches)}")
for idx in matches:
    print(content[max(0, idx-80):min(len(content), idx+120)])
    print("-" * 50)
