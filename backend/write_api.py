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

API_JS = r'''// ================================================================
//  TransformAI — Multi-Provider AI Abstraction Layer
//  Supports: Local Fallback, OpenAI, Google Gemini, Anthropic Claude
//  Features: Exponential backoff retries, JSON validation, streaming
// ================================================================

const API = {
  _provider: 'local', // 'local' | 'openai' | 'gemini' | 'anthropic'
  _keys: {
    openai: '',
    gemini: '',
    anthropic: ''
  },
  _models: {
    openai: 'gpt-4o-mini',
    gemini: 'gemini-1.5-flash',
    anthropic: 'claude-3-5-sonnet-20241022',
    local: 'local-nlp-v1'
  },
  _useProxy: true, // will attempt /api/transform if available
  _maxRetries: 3,
  _retryDelayMs: 1000,

  // --- Configuration Getters/Setters ---
  setProvider(provider) {
    if (['local', 'openai', 'gemini', 'anthropic'].includes(provider)) {
      this._provider = provider;
      AppState.updateSetting('provider', provider);
    }
  },
  getProvider() { return this._provider; },

  setKey(provider, key) {
    if (this._keys.hasOwnProperty(provider)) {
      this._keys[provider] = (key || '').trim();
      const storedKeys = AppState.getSetting('keys') || {};
      storedKeys[provider] = this._keys[provider];
      AppState.updateSetting('keys', storedKeys);
    }
  },
  getKey(provider) {
    return this._keys[provider] || (AppState.getSetting('keys') || {})[provider] || '';
  },

  setModel(provider, model) {
    if (this._models.hasOwnProperty(provider)) {
      this._models[provider] = model;
      const storedModels = AppState.getSetting('models') || {};
      storedModels[provider] = model;
      AppState.updateSetting('models', storedModels);
    }
  },
  getModel(provider = this._provider) {
    return this._models[provider] || (AppState.getSetting('models') || {})[provider] || 'local-nlp-v1';
  },

  isConfigured(provider = this._provider) {
    if (provider === 'local') return true;
    const key = this.getKey(provider);
    return !!key && key.length > 5;
  },

  initFromStorage() {
    const s = AppState.getSettings();
    if (s.provider) this._provider = s.provider;
    if (s.keys) this._keys = { ...this._keys, ...s.keys };
    if (s.models) this._models = { ...this._models, ...s.models };
    // Legacy support
    if (s.apiKey && !this._keys.openai) this._keys.openai = s.apiKey;
    if (s.model && !this._models.openai) this._models.openai = s.model;
  },

  // --- Catalog of Available Providers and Models ---
  PROVIDERS: [
    {
      id: 'local',
      name: 'Local Fallback Engine',
      badge: 'Zero-Config · Offline',
      desc: 'Built-in smart NLP heuristic algorithms. No API key needed, runs 100% locally and privately.',
      models: [{ id: 'local-nlp-v1', label: 'TransformAI Local Engine v1.0' }]
    },
    {
      id: 'openai',
      name: 'OpenAI',
      badge: 'GPT-4o & Mini',
      desc: 'Connect to OpenAI for cutting-edge text generation and multilingual reasoning.',
      models: [
        { id: 'gpt-4o-mini', label: 'GPT-4o Mini (Fast & Cost-Effective — Recommended)' },
        { id: 'gpt-4o', label: 'GPT-4o (State of the Art)' },
        { id: 'gpt-4-turbo', label: 'GPT-4 Turbo' },
        { id: 'gpt-3.5-turbo', label: 'GPT-3.5 Turbo' }
      ]
    },
    {
      id: 'gemini',
      name: 'Google Gemini',
      badge: 'Gemini 1.5 Flash/Pro',
      desc: 'High-speed, long-context Google models with expansive multilingual proficiency.',
      models: [
        { id: 'gemini-1.5-flash', label: 'Gemini 1.5 Flash (Ultra Fast)' },
        { id: 'gemini-1.5-pro', label: 'Gemini 1.5 Pro (Deep Reasoning)' }
      ]
    },
    {
      id: 'anthropic',
      name: 'Anthropic Claude',
      badge: 'Claude 3.5 Sonnet',
      desc: 'Exceptional nuance, nuanced tone shifting, and complex reasoning.',
      models: [
        { id: 'claude-3-5-sonnet-20241022', label: 'Claude 3.5 Sonnet (Most Capable)' },
        { id: 'claude-3-haiku-20240307', label: 'Claude 3 Haiku (Compact & Fast)' }
      ]
    }
  ],

  // --- Main Transformation Entrypoint ---
  async executeTransform({ type, input, opts = {}, onChunk, onDone }) {
    if (!input || !input.trim()) {
      throw new Error('Please enter content to transform.');
    }

    const provider = this._provider;
    const model = this.getModel(provider);
    const brand = AppState.getSetting('brand') || {};
    let systemPrompt = 'You are TransformAI, an expert AI content transformation specialist. Produce strictly accurate, high-quality, professional results.';
    if (brand.name || brand.voice) {
      systemPrompt += ` Incorporate the brand voice of "${brand.name || 'Our Brand'}": ${brand.voice || ''}`;
    }

    const def = TRANSFORMATIONS[type];
    if (!def) throw new Error(`Unknown transformation type: ${type}`);
    const prompt = def.buildPrompt(input, opts);

    // If local provider selected OR cloud provider has no key configured
    if (provider === 'local' || !this.isConfigured(provider)) {
      if (provider !== 'local') {
        Toast.show('info', 'Using Local Engine', `No API key for ${provider}. Executing with Local Fallback Engine.`);
      }
      return this._executeLocal({ type, input, opts, onChunk, onDone });
    }

    // Try cloud provider with exponential backoff retries
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

        // Post-process / validate special types
        let finalOutput = resultText;
        if (type === 'quality') {
          finalOutput = this._cleanAndValidateJSON(resultText);
        } else if (type === 'convert' && opts.targetFormat === 'json') {
          finalOutput = this._cleanAndValidateJSON(resultText);
        }

        onDone?.(finalOutput);
        return finalOutput;
      } catch (err) {
        lastError = err;
        console.warn(`[TransformAI] Attempt ${attempt} failed for ${provider}:`, err.message);

        // Don't retry non-retryable errors (e.g. invalid auth credentials)
        if (err.status === 401 || err.status === 403 || err.message.includes('API key')) {
          break;
        }

        if (attempt < this._maxRetries) {
          const delay = this._retryDelayMs * Math.pow(2, attempt - 1);
          await new Promise(r => setTimeout(r, delay));
        }
      }
    }

    // Cloud provider failed; offer fallback to Local Engine
    console.warn(`[TransformAI] Cloud provider ${provider} failed after retries. Falling back to local engine. Error:`, lastError);
    Toast.show('warning', 'Cloud Request Failed', `${lastError.message}. Recovered via Local Fallback Engine.`);
    return this._executeLocal({ type, input, opts, onChunk, onDone, fallbackNotice: `[Local Fallback: ${lastError.message}]` });
  },

  // --- Local Fallback Engine Execution ---
  async _executeLocal({ type, input, opts = {}, onChunk, onDone, fallbackNotice = '' }) {
    await new Promise(r => setTimeout(r, 60)); // Yield to paint UI spinner

    let result = '';
    let extraMeta = null;

    switch (type) {
      case 'summarize':
        result = LocalNLP.summarize(input, opts);
        break;
      case 'tone':
        result = LocalNLP.tone(input, opts);
        break;
      case 'translate':
        result = LocalNLP.translate(input, opts);
        break;
      case 'convert':
        result = LocalNLP.convert(input, opts);
        break;
      case 'grammar': {
        const res = LocalNLP.grammar(input, opts);
        result = res.correctedText;
        extraMeta = { diffHtml: res.diffHtml };
        break;
      }
      case 'expand':
        result = LocalNLP.expand(input, opts);
        break;
      case 'simplify':
        result = LocalNLP.simplify(input, opts);
        break;
      case 'quality': {
        const scoreData = LocalNLP.scoreQuality(input, opts);
        result = JSON.stringify(scoreData, null, 2);
        extraMeta = { scoreData };
        break;
      }
      default:
        result = input;
    }

    if (fallbackNotice) {
      result = `${fallbackNotice}\n\n${result}`;
    }

    // Simulate streaming for smooth UX if enabled
    const streamingEnabled = AppState.getPref('streaming', true);
    if (streamingEnabled && typeof onChunk === 'function' && result.length > 50) {
      const words = result.split(' ');
      let current = '';
      for (let i = 0; i < words.length; i++) {
        current += (i > 0 ? ' ' : '') + words[i];
        if (i % 4 === 0 || i === words.length - 1) {
          onChunk(words[i] + ' ', current);
          if (i % 12 === 0) await new Promise(r => setTimeout(r, 12));
        }
      }
    } else if (typeof onChunk === 'function') {
      onChunk(result, result);
    }

    onDone?.(result, extraMeta);
    return { output: result, extraMeta };
  },

  // --- Cloud Provider Implementations ---

  // 1. OpenAI
  async _callOpenAI({ prompt, systemPrompt, model, onChunk }) {
    const key = this.getKey('openai');
    if (!key) throw new Error('OpenAI API key missing. Please enter it in Settings.');

    const messages = [];
    if (systemPrompt) messages.push({ role: 'system', content: systemPrompt });
    messages.push({ role: 'user', content: prompt });

    const resp = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${key}`
      },
      body: JSON.stringify({
        model: model || 'gpt-4o-mini',
        messages,
        temperature: 0.7,
        max_tokens: 2500
      })
    });

    if (!resp.ok) {
      const errJson = await resp.json().catch(() => ({}));
      const err = new Error(errJson?.error?.message || `OpenAI API Error: HTTP ${resp.status}`);
      err.status = resp.status;
      throw err;
    }

    const data = await resp.json();
    const content = data.choices?.[0]?.message?.content || '';
    if (typeof onChunk === 'function') onChunk(content, content);
    return content;
  },

  // 2. Google Gemini
  async _callGemini({ prompt, systemPrompt, model, onChunk }) {
    const key = this.getKey('gemini');
    if (!key) throw new Error('Google Gemini API key missing. Please enter it in Settings.');

    const m = model || 'gemini-1.5-flash';
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${m}:generateContent?key=${key}`;

    const contents = [
      {
        role: 'user',
        parts: [{ text: `${systemPrompt}\n\nTask:\n${prompt}` }]
      }
    ];

    const resp = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        contents,
        generationConfig: { temperature: 0.7, maxOutputTokens: 2500 }
      })
    });

    if (!resp.ok) {
      const errJson = await resp.json().catch(() => ({}));
      const err = new Error(errJson?.error?.message || `Gemini API Error: HTTP ${resp.status}`);
      err.status = resp.status;
      throw err;
    }

    const data = await resp.json();
    const content = data.candidates?.[0]?.content?.parts?.[0]?.text || '';
    if (typeof onChunk === 'function') onChunk(content, content);
    return content;
  },

  // 3. Anthropic Claude
  async _callClaude({ prompt, systemPrompt, model, onChunk }) {
    const key = this.getKey('anthropic');
    if (!key) throw new Error('Anthropic Claude API key missing. Please enter it in Settings.');

    const resp = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': key,
        'anthropic-version': '2023-06-01',
        'anthropic-dangerous-direct-browser-access': 'true'
      },
      body: JSON.stringify({
        model: model || 'claude-3-5-sonnet-20241022',
        system: systemPrompt,
        messages: [{ role: 'user', content: prompt }],
        max_tokens: 2500,
        temperature: 0.7
      })
    });

    if (!resp.ok) {
      const errJson = await resp.json().catch(() => ({}));
      const err = new Error(errJson?.error?.message || `Claude API Error: HTTP ${resp.status}`);
      err.status = resp.status;
      throw err;
    }

    const data = await resp.json();
    const content = data.content?.[0]?.text || '';
    if (typeof onChunk === 'function') onChunk(content, content);
    return content;
  },

  // --- Strict JSON Cleaner & Validator ---
  _cleanAndValidateJSON(text) {
    if (!text) return '{}';
    let cleaned = text.trim();
    // Remove markdown code fences if present
    if (cleaned.startsWith('```json')) {
      cleaned = cleaned.replace(/^```json\s*/i, '').replace(/\s*```$/, '');
    } else if (cleaned.startsWith('```')) {
      cleaned = cleaned.replace(/^```\s*/, '').replace(/\s*```$/, '');
    }
    cleaned = cleaned.trim();

    try {
      const parsed = JSON.parse(cleaned);
      return JSON.stringify(parsed, null, 2);
    } catch (e) {
      // Find outermost curly braces
      const first = cleaned.indexOf('{');
      const last = cleaned.lastIndexOf('}');
      if (first !== -1 && last !== -1 && last > first) {
        const sub = cleaned.slice(first, last + 1);
        try {
          const parsed = JSON.parse(sub);
          return JSON.stringify(parsed, null, 2);
        } catch {}
      }
      return cleaned;
    }
  },

  // --- Connection Verification ---
  async testConnection(provider = this._provider) {
    if (provider === 'local') return { success: true, message: 'Local Fallback Engine is active and operational.' };
    const key = this.getKey(provider);
    if (!key) return { success: false, message: `Please enter an API key for ${provider}.` };

    try {
      if (provider === 'openai') {
        const resp = await fetch('https://api.openai.com/v1/models', {
          headers: { 'Authorization': `Bearer ${key}` }
        });
        if (resp.ok) return { success: true, message: 'OpenAI API key verified successfully!' };
        const data = await resp.json().catch(() => ({}));
        return { success: false, message: data?.error?.message || `HTTP ${resp.status}` };
      }
      if (provider === 'gemini') {
        const resp = await fetch(`https://generativelanguage.googleapis.com/v1beta/models?key=${key}`);
        if (resp.ok) return { success: true, message: 'Google Gemini API key verified successfully!' };
        const data = await resp.json().catch(() => ({}));
        return { success: false, message: data?.error?.message || `HTTP ${resp.status}` };
      }
      if (provider === 'anthropic') {
        // Quick 1-token query
        const resp = await fetch('https://api.anthropic.com/v1/messages', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'x-api-key': key,
            'anthropic-version': '2023-06-01',
            'anthropic-dangerous-direct-browser-access': 'true'
          },
          body: JSON.stringify({
            model: 'claude-3-haiku-20240307',
            messages: [{ role: 'user', content: 'hi' }],
            max_tokens: 1
          })
        });
        if (resp.ok) return { success: true, message: 'Anthropic Claude API key verified successfully!' };
        const data = await resp.json().catch(() => ({}));
        return { success: false, message: data?.error?.message || `HTTP ${resp.status}` };
      }
    } catch (err) {
      return { success: false, message: err.message };
    }
  }
};
'''

save_file("js/api.js", API_JS)
