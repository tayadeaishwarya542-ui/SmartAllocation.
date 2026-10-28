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
# 1. Update js/transformations.js (LCS diff + robust rules)
# =====================================================================
with open(os.path.join(BASE_DIR, "js", "transformations.js"), "r", encoding="utf-8") as f:
    trans_content = f.read()

# Replace createWordDiff and grammar
old_diff_grammar_pattern = r"  createWordDiff\(origText, corrText\) \{[\s\S]*?\n  expand\(text,"

new_diff_grammar_code = r'''  createWordDiff(origText, corrText) {
    if (!origText && !corrText) return '';
    if (!origText) return `<ins class="diff-ins">${escapeHtml(corrText)}</ins>`;
    if (!corrText) return `<del class="diff-del">${escapeHtml(origText)}</del>`;

    const origTokens = (origText || '').match(/\S+|\s+/g) || [];
    const corrTokens = (corrText || '').match(/\S+|\s+/g) || [];

    const n = origTokens.length;
    const m = corrTokens.length;

    // LCS dynamic programming table
    const dp = Array.from({ length: n + 1 }, () => new Uint16Array(m + 1));
    for (let i = 0; i < n; i++) {
      for (let j = 0; j < m; j++) {
        if (origTokens[i] === corrTokens[j]) {
          dp[i + 1][j + 1] = dp[i][j] + 1;
        } else {
          dp[i + 1][j + 1] = Math.max(dp[i + 1][j], dp[i][j + 1]);
        }
      }
    }

    // Backtrack to find aligned token operations
    let i = n;
    let j = m;
    const ops = [];
    while (i > 0 || j > 0) {
      if (i > 0 && j > 0 && origTokens[i - 1] === corrTokens[j - 1]) {
        ops.push({ op: 'eq', val: origTokens[i - 1] });
        i--;
        j--;
      } else if (j > 0 && (i === 0 || dp[i][j - 1] >= dp[i - 1][j])) {
        ops.push({ op: 'ins', val: corrTokens[j - 1] });
        j--;
      } else if (i > 0 && (j === 0 || dp[i][j - 1] < dp[i - 1][j])) {
        ops.push({ op: 'del', val: origTokens[i - 1] });
        i--;
      } else {
        break;
      }
    }
    ops.reverse();

    let html = '';
    for (const { op, val } of ops) {
      const esc = escapeHtml(val);
      if (op === 'eq') {
        html += esc;
      } else if (op === 'del') {
        html += val.trim() ? `<del class="diff-del">${esc}</del>` : esc;
      } else if (op === 'ins') {
        html += val.trim() ? `<ins class="diff-ins">${esc}</ins>` : esc;
      }
    }
    return html;
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

trans_content = re.sub(old_diff_grammar_pattern, lambda m: new_diff_grammar_code, trans_content)
save_file("js/transformations.js", trans_content)

# =====================================================================
# 2. Update js/api.js (Hybrid grammar handler & metadata)
# =====================================================================
with open(os.path.join(BASE_DIR, "js", "api.js"), "r", encoding="utf-8") as f:
    api_content = f.read()

# Add _executeGrammarHybrid to API object
grammar_hybrid_method = r'''  // --- Hybrid Grammar Correction Engine ---
  async _executeGrammarHybrid({ input, opts = {}, onChunk, onDone }) {
    const mode = opts.mode || 'hybrid'; // 'hybrid' | 'ai' | 'offline'
    const autoFallback = opts.autoFallback !== 'no' && opts.autoFallback !== false;
    const provider = this._provider;
    const model = this.getModel(provider);

    // Mode B: Offline Grammar Correction (never calls cloud / proxy)
    if (mode === 'offline') {
      const res = LocalNLP.grammar(input, opts);
      const output = res.correctedText;
      const extraMeta = {
        engineUsed: 'offline',
        engineLabel: 'Offline Rule-Based Engine',
        mode: 'offline',
        provider: 'local',
        model: 'local-nlp-v1',
        isFallback: false,
        diffHtml: res.diffHtml
      };
      if (typeof onChunk === 'function') onChunk(output, output);
      onDone?.(output, extraMeta);
      return { output, extraMeta };
    }

    // Mode A or Hybrid: Check AI provider configuration
    const isCloudConfigured = provider !== 'local' && this.isConfigured(provider);

    if (!isCloudConfigured) {
      if (mode === 'ai') {
        const err = new Error(
          provider === 'local'
            ? 'Mode A (AI-Powered) requires a cloud AI provider. Please configure OpenAI, Gemini, or Claude in Settings.'
            : `AI Provider "${provider}" is missing an API key. Please configure credentials in Settings or enable Offline Fallback.`
        );
        err.canRetryAI = false;
        throw err;
      }

      // Hybrid mode: fallback if enabled
      if (autoFallback) {
        const res = LocalNLP.grammar(input, opts);
        const output = res.correctedText;
        const extraMeta = {
          engineUsed: 'offline-fallback',
          engineLabel: `Offline Fallback (${provider === 'local' ? 'Local Provider Selected' : 'No API Key'})`,
          mode: 'hybrid',
          provider,
          model,
          isFallback: true,
          fallbackReason: provider === 'local' ? 'Local provider selected' : `Missing API key for ${provider}`,
          diffHtml: res.diffHtml,
          canRetryAI: true
        };
        Toast.show('info', 'Offline Fallback Used', `Cloud AI not configured for ${provider}. Clean output generated with Offline Rule Engine.`);
        if (typeof onChunk === 'function') onChunk(output, output);
        onDone?.(output, extraMeta);
        return { output, extraMeta };
      } else {
        const err = new Error(`AI Provider "${provider}" is not configured and Automatic Offline Fallback is disabled.`);
        err.canRetryAI = false;
        throw err;
      }
    }

    // Provider is configured: Attempt AI correction with exponential backoff
    const def = TRANSFORMATIONS.grammar;
    const prompt = def.buildPrompt(input, opts);
    const systemPrompt = 'You are TransformAI Grammar Engine. Output ONLY the clean, corrected text with no conversational preamble or markdown commentary.';

    let lastError = null;
    for (let attempt = 1; attempt <= this._maxRetries; attempt++) {
      try {
        let resultText = '';
        if (provider === 'openai') {
          resultText = await this._callOpenAI({ prompt, systemPrompt, model, onChunk });
        } else if (provider === 'gemini') {
          resultText = await this._callGemini({ prompt, systemPrompt, model, onChunk });
        } else if (provider === 'anthropic') {
          resultText = await this._callClaude({ prompt, systemPrompt, model, onChunk });
        }

        resultText = (resultText || '').trim();
        if ((resultText.startsWith('"') && resultText.endsWith('"')) || (resultText.startsWith("'") && resultText.endsWith("'"))) {
          resultText = resultText.slice(1, -1).trim();
        }

        const diffHtml = LocalNLP.createWordDiff(input, resultText);
        const extraMeta = {
          engineUsed: 'ai',
          engineLabel: `AI-Powered (${provider.toUpperCase()}: ${model})`,
          mode,
          provider,
          model,
          isFallback: false,
          diffHtml
        };

        onDone?.(resultText, extraMeta);
        return { output: resultText, extraMeta };
      } catch (err) {
        lastError = err;
        console.warn(`[TransformAI Grammar AI] Attempt ${attempt} failed:`, err.message);

        // Don't retry auth errors
        if (err.status === 401 || err.status === 403 || err.message.includes('API key')) {
          break;
        }

        if (attempt < this._maxRetries) {
          const delay = this._retryDelayMs * Math.pow(2, attempt - 1);
          await new Promise(r => setTimeout(r, delay));
        }
      }
    }

    // AI Call Failed after retries
    if (autoFallback) {
      console.warn(`[TransformAI Grammar] AI failed (${lastError.message}). Safely falling back to Offline Engine.`);
      const res = LocalNLP.grammar(input, opts);
      const output = res.correctedText;
      const extraMeta = {
        engineUsed: 'offline-fallback',
        engineLabel: `Offline Fallback (${lastError.message})`,
        mode,
        provider,
        model,
        isFallback: true,
        fallbackReason: lastError.message,
        diffHtml: res.diffHtml,
        canRetryAI: true
      };
      Toast.show('warning', 'AI Correction Failed', `${lastError.message}. Safely recovered using Offline Rule Engine.`);
      if (typeof onChunk === 'function') onChunk(output, output);
      onDone?.(output, extraMeta);
      return { output, extraMeta };
    } else {
      const err = new Error(`AI Grammar Correction Failed: ${lastError.message}. Automatic Offline Fallback is disabled.`);
      err.canRetryAI = true;
      throw err;
    }
  },

  // --- Core Transform Execution Entry Point ---'''

# In api_content, inject grammar dispatch in executeTransform
old_exec_entry = r"  async executeTransform\(\{ type, input, opts = \{\}, onChunk, onDone \}\) \{"
new_exec_entry = r'''  async executeTransform({ type, input, opts = {}, onChunk, onDone }) {
    if (!input || !input.trim()) {
      throw new Error('Please enter content to transform.');
    }

    // Specialized handling for Grammar & Spell Check Hybrid Engine
    if (type === 'grammar') {
      return this._executeGrammarHybrid({ input, opts, onChunk, onDone });
    }'''

api_content = re.sub(old_exec_entry, lambda m: new_exec_entry, api_content)

# Add _executeGrammarHybrid right before executeTransform
api_content = api_content.replace(
  "  // --- Core Transform Execution Entry Point ---",
  grammar_hybrid_method
)

save_file("js/api.js", api_content)

# =====================================================================
# 3. Update pages/transform.js (Honest Engine Badge, Retry with AI, UI Tabs)
# =====================================================================
with open(os.path.join(BASE_DIR, "pages", "transform.js"), "r", encoding="utf-8") as f:
    tf_content = f.read()

# Enhance renderFormattedOutput in transform.js
old_render_start = r"    if \(_currentTransformType === 'quality'\) \{"
new_render_start = r'''    // Grammar engine attribution & badge handling
    if (_currentTransformType === 'grammar') {
      const modelBadge = document.getElementById('outputModelBadge');
      if (modelBadge && extraMeta) {
        modelBadge.style.display = 'inline-flex';
        if (extraMeta.engineUsed === 'ai') {
          modelBadge.className = 'badge badge-green';
          modelBadge.innerHTML = `<i class="ri-sparkling-fill"></i> ${extraMeta.engineLabel || 'AI-Powered'}`;
        } else if (extraMeta.engineUsed === 'offline-fallback') {
          modelBadge.className = 'badge badge-amber';
          modelBadge.innerHTML = `<i class="ri-alert-line"></i> ${extraMeta.engineLabel || 'Offline Fallback'} <button class="retry-ai-btn" onclick="TransformPage.retryWithAI()" title="Retry with AI"><i class="ri-restart-line"></i> Retry AI</button>`;
        } else {
          modelBadge.className = 'badge badge-gray';
          modelBadge.innerHTML = `<i class="ri-cpu-line"></i> ${extraMeta.engineLabel || 'Offline Rule-Based'}`;
        }
      }
    }

    if (_currentTransformType === 'quality') {'''

tf_content = re.sub(old_render_start, lambda m: new_render_start, tf_content)

# Add helper methods on TransformPage
helpers = r'''  retryWithAI() {
    Toast.show('info', 'Retrying AI', 'Re-attempting AI-powered grammar correction...');
    this.run();
  },

  fallbackToOffline() {
    Toast.show('info', 'Offline Mode', 'Executing with Offline Rule-Based Grammar Engine...');
    const input = document.getElementById('inputContent')?.value || '';
    const res = LocalNLP.grammar(input, {});
    this.renderFormattedOutput(res.correctedText, {
      engineUsed: 'offline',
      engineLabel: 'Offline Rule-Based Engine',
      diffHtml: res.diffHtml
    });
    const outputText = document.getElementById('outputText');
    if (outputText) outputText.textContent = res.correctedText;
    const diffView = document.getElementById('outputDiffView');
    if (diffView) diffView.innerHTML = res.diffHtml.replace(/\n/g, '<br>');
    const tabsBar = document.getElementById('outputTabsBar');
    if (tabsBar) tabsBar.style.display = 'flex';
    const tabDiff = document.getElementById('tabBtnDiff');
    if (tabDiff) tabDiff.style.display = 'inline-block';
  },

  buildQualityCardHtml(scoreData) {'''

tf_content = tf_content.replace("  buildQualityCardHtml(scoreData) {", helpers)

# Update run() catch error block to display action buttons
old_catch_block = r"      if \(outputText\) \{\s+outputText\.innerHTML = `<div class=\"error-banner\"><i class=\"ri-error-warning-line\"></i> <strong>Error:</strong> \$\{escapeHtml\(err\.message\)\}</div>`;\s+\}"
new_catch_block = r'''      if (outputText) {
        outputText.innerHTML = `
          <div class="error-banner">
            <i class="ri-error-warning-line"></i>
            <div style="flex:1;">
              <strong>Transformation Error:</strong> ${escapeHtml(err.message)}
              <div style="margin-top:10px;display:flex;gap:8px;">
                <button class="btn btn-sm btn-outline" onclick="TransformPage.run()"><i class="ri-restart-line"></i> Retry Request</button>
                ${_currentTransformType === 'grammar' ? '<button class="btn btn-sm btn-primary" onclick="TransformPage.fallbackToOffline()"><i class="ri-cpu-line"></i> Use Offline Fallback</button>' : ''}
              </div>
            </div>
          </div>
        `;
      }'''

tf_content = re.sub(old_catch_block, lambda m: new_catch_block, tf_content)

save_file("pages/transform.js", tf_content)

# =====================================================================
# 4. Update server.js (Secure Node.js proxy with environment keys)
# =====================================================================
with open(os.path.join(BASE_DIR, "server.js"), "r", encoding="utf-8") as f:
    server_content = f.read()

secure_proxy_handler = r'''  // API Route: Server-side secure proxy for transformations
  if (pathname === '/api/transform' && req.method === 'POST') {
    let bodyStr = '';
    req.on('data', chunk => { bodyStr += chunk; });
    req.on('end', async () => {
      try {
        const body = JSON.parse(bodyStr || '{}');
        const { provider, model, prompt, systemPrompt } = body;

        let apiKey = '';
        if (provider === 'openai') apiKey = process.env.OPENAI_API_KEY;
        else if (provider === 'gemini') apiKey = process.env.GEMINI_API_KEY;
        else if (provider === 'anthropic') apiKey = process.env.ANTHROPIC_API_KEY;

        if (!apiKey) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({
            error: `Server-side credentials for "${provider}" not configured. Set ${provider.toUpperCase()}_API_KEY in server environment.`,
            serverProxyActive: false
          }));
          return;
        }

        // Call Provider
        let outputText = '';
        if (provider === 'openai') {
          const https = require('https');
          const postData = JSON.stringify({
            model: model || 'gpt-4o-mini',
            messages: [
              ...(systemPrompt ? [{ role: 'system', content: systemPrompt }] : []),
              { role: 'user', content: prompt }
            ],
            temperature: 0.3
          });

          outputText = await new Promise((resolve, reject) => {
            const clientReq = https.request({
              hostname: 'api.openai.com',
              path: '/v1/chat/completions',
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey}`,
                'Content-Length': Buffer.byteLength(postData)
              }
            }, (clientRes) => {
              let resData = '';
              clientRes.on('data', c => { resData += c; });
              clientRes.on('end', () => {
                try {
                  const parsed = JSON.parse(resData);
                  if (clientRes.statusCode >= 200 && clientRes.statusCode < 300) {
                    resolve(parsed.choices?.[0]?.message?.content || '');
                  } else {
                    reject(new Error(parsed.error?.message || `OpenAI Error: HTTP ${clientRes.statusCode}`));
                  }
                } catch (e) { reject(e); }
              });
            });
            clientReq.on('error', reject);
            clientReq.write(postData);
            clientReq.end();
          });
        }

        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ status: 'success', output: outputText, provider, model }));
      } catch (err) {
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: err.message }));
      }
    });
    return;
  }'''

old_proxy_pattern = r"  // API Route: Server-side secure proxy for transformations[\s\S]*?\n  // Static File Serving"
server_content = re.sub(old_proxy_pattern, lambda m: secure_proxy_handler + "\n\n  // Static File Serving", server_content)
save_file("server.js", server_content)

# =====================================================================
# 5. Write .env.example
# =====================================================================
ENV_EXAMPLE = """# ================================================================
# TransformAI Server Environment Configuration Template
# KEEP SECRET: Never commit real production credentials to Git
# ================================================================

PORT=5174

# AI Provider API Keys (Stored securely on the server)
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
"""

save_file(".env.example", ENV_EXAMPLE)

print("\nAll full hybrid system components generated and saved successfully!")
