import html

def escape_html(s):
    return html.escape(s)

def create_word_diff(orig_text, corr_text):
    # Split into word and whitespace/punctuation tokens
    import re
    orig_tokens = re.findall(r'\S+|\s+', orig_text or '')
    corr_tokens = re.findall(r'\S+|\s+', corr_text or '')

    # Compute LCS dynamic programming table
    n = len(orig_tokens)
    m = len(corr_tokens)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n):
        for j in range(m):
            if orig_tokens[i].lower() == corr_tokens[j].lower() and orig_tokens[i] == corr_tokens[j]:
                dp[i + 1][j + 1] = dp[i][j] + 1
            elif orig_tokens[i].lower() == corr_tokens[j].lower():
                dp[i + 1][j + 1] = dp[i][j] + 1
            else:
                dp[i + 1][j + 1] = max(dp[i + 1][j], dp[i][j + 1])

    # Backtrack to build diff ops
    i, j = n, m
    ops = []
    while i > 0 or j > 0:
        if i > 0 and j > 0 and orig_tokens[i - 1].lower() == corr_tokens[j - 1].lower() and (dp[i][j] == dp[i - 1][j - 1] + 1):
            if orig_tokens[i - 1] == corr_tokens[j - 1]:
                ops.append(('eq', orig_tokens[i - 1]))
            else:
                ops.append(('ins', corr_tokens[j - 1]))
                ops.append(('del', orig_tokens[i - 1]))
            i -= 1
            j -= 1
        elif j > 0 and (i == 0 or dp[i][j - 1] >= dp[i - 1][j]):
            ops.append(('ins', corr_tokens[j - 1]))
            j -= 1
        elif i > 0 and (j == 0 or dp[i][j - 1] < dp[i - 1][j]):
            ops.append(('del', orig_tokens[i - 1]))
            i -= 1
        else:
            break

    ops.reverse()

    # Render HTML
    html_out = []
    for op, val in ops:
        escaped = escape_html(val)
        if op == 'eq':
            html_out.append(escaped)
        elif op == 'del':
            if val.strip():
                html_out.append(f'<del class="diff-del">{escaped}</del>')
            else:
                html_out.append(escaped)
        elif op == 'ins':
            if val.strip():
                html_out.append(f'<ins class="diff-ins">{escaped}</ins>')
            else:
                html_out.append(escaped)

    return ''.join(html_out)

res = create_word_diff("she am girl", "She is a girl.")
print("DIFF RESULT:\n", res)
