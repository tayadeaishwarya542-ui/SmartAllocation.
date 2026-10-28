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

SETTINGS_JS = r'''// ================================================================
//  Settings Page — Multi-Provider Intelligence & Platform Configuration
// ================================================================

function renderSettingsPage() {
  const currentProvider = API.getProvider();
  const settings = AppState.getSettings();
  const currentModel = API.getModel();

  const providerObj = API.PROVIDERS.find(p => p.id === currentProvider) || API.PROVIDERS[0];

  return `
  <div class="page-view">
    <div class="page-header">
      <div class="page-header-top">
        <div>
          <div class="page-title">Settings & AI Providers <span class="grad-text">✦</span></div>
          <div class="page-desc">Configure multi-provider routing, local NLP engine fallback, and preferences.</div>
        </div>
        <button class="btn btn-primary btn-sm" onclick="SettingsPage.saveAll()">
          <i class="ri-save-line"></i> Save Settings
        </button>
      </div>
    </div>

    <div class="settings-grid">
      <!-- 1. AI Provider Selection Card -->
      <div class="settings-card full-width">
        <div class="settings-card-header">
          <div class="settings-card-title">
            <i class="ri-cpu-line" style="color:var(--accent-primary)"></i> AI Provider & Intelligence Engine
          </div>
          <div class="settings-card-desc">Select which provider powers your content transformations. Local Fallback works offline with zero configuration.</div>
        </div>
        <div class="settings-card-body">
          <div class="provider-cards-grid">
            ${API.PROVIDERS.map(p => `
              <div class="provider-card ${p.id === currentProvider ? 'active' : ''}" onclick="SettingsPage.selectProvider('${p.id}')">
                <div class="flex items-center justify-between mb-2">
                  <span class="provider-card-name">${p.name}</span>
                  <span class="badge ${p.id === 'local' ? 'badge-green' : 'badge-purple'}">${p.badge}</span>
                </div>
                <div class="provider-card-desc">${p.desc}</div>
              </div>
            `).join('')}
          </div>

          <!-- Active Provider Credentials & Models Panel -->
          <div class="provider-config-panel" style="margin-top:20px;padding:20px;background:var(--bg-elevated);border:1px solid var(--border);border-radius:var(--radius-md);">
            <div class="form-title" style="font-size:15px;font-weight:600;margin-bottom:12px;">
              Configuring: <span style="color:var(--accent-primary);">${providerObj.name}</span>
            </div>

            ${currentProvider === 'local' ? `
              <div class="p-3" style="background:rgba(52,211,153,0.1);border:1px solid rgba(52,211,153,0.25);border-radius:var(--radius-sm);color:#6ee7b7;font-size:13px;line-height:1.6;">
                <i class="ri-shield-check-fill" style="font-size:16px;"></i> <strong>Zero-Config Engine Active:</strong> All 8 transformation operations (Summarization, Tone, Polyglot Translation, Formatting, Grammar with Diff, Expansion, Simplification, and Quality Scoring) run directly in your browser. No external API keys or network connection required.
              </div>
            ` : `
              <div class="grid grid-2 gap-4">
                <div class="form-group mb-0">
                  <label class="form-label">${providerObj.name} API Key</label>
                  <div class="input-with-icon">
                    <input type="password" class="form-input" id="providerApiKeyInput"
                      placeholder="Paste your ${providerObj.name} key..."
                      value="${escapeHtml(API.getKey(currentProvider))}" />
                    <button class="icon-toggle" id="apiKeyEyeBtn" onclick="SettingsPage.toggleApiKeyVisibility()">
                      <i class="ri-eye-line"></i>
                    </button>
                  </div>
                  <div class="form-help" style="font-size:11px;color:var(--text-muted);margin-top:4px;">
                    Keys are stored locally in your browser. Never committed to source repositories.
                  </div>
                </div>

                <div class="form-group mb-0">
                  <label class="form-label">Model Selection</label>
                  <select class="form-select" id="providerModelSelect">
                    ${providerObj.models.map(m => `
                      <option value="${m.id}" ${m.id === currentModel ? 'selected' : ''}>${m.label}</option>
                    `).join('')}
                  </select>
                </div>
              </div>

              <div class="flex gap-2 items-center" style="margin-top:14px;">
                <button class="btn btn-secondary btn-sm" onclick="SettingsPage.testCurrentProvider()">
                  <i class="ri-pulse-line"></i> Test Connection
                </button>
                <div id="providerTestResult" style="font-size:12px;font-weight:500;"></div>
              </div>
            `}
          </div>
        </div>
      </div>

      <!-- 2. Preferences & Theme -->
      <div class="settings-card">
        <div class="settings-card-header">
          <div class="settings-card-title">
            <i class="ri-sliders-line" style="color:#67e8f9"></i> Application Preferences
          </div>
          <div class="settings-card-desc">Control runtime streaming, theme aesthetics, and history persistence.</div>
        </div>
        <div class="settings-card-body">
          <div class="toggle-row">
            <div class="toggle-info">
              <div class="toggle-label">Real-time Streaming</div>
              <div class="toggle-desc">Show output word-by-word with typing animation</div>
            </div>
            <div class="toggle-switch ${AppState.getPref('streaming', true) ? 'on' : ''}"
              id="pref-streaming" onclick="SettingsPage.togglePref('streaming')"></div>
          </div>

          <div class="toggle-row">
            <div class="toggle-info">
              <div class="toggle-label">Auto-save History</div>
              <div class="toggle-desc">Save every completed transformation automatically</div>
            </div>
            <div class="toggle-switch ${AppState.getPref('autoSave', true) ? 'on' : ''}"
              id="pref-autoSave" onclick="SettingsPage.togglePref('autoSave')"></div>
          </div>

          <div class="toggle-row">
            <div class="toggle-info">
              <div class="toggle-label">Dark Glassmorphic Theme</div>
              <div class="toggle-desc">Toggle between Sleek Dark and Modern Light mode</div>
            </div>
            <div class="toggle-switch ${document.documentElement.getAttribute('data-theme') !== 'light' ? 'on' : ''}"
              id="pref-theme" onclick="SettingsPage.toggleTheme()"></div>
          </div>
        </div>
      </div>

      <!-- 3. Brand Voice Customization -->
      <div class="settings-card">
        <div class="settings-card-header">
          <div class="settings-card-title">
            <i class="ri-user-voice-line" style="color:#6ee7b7"></i> Custom Brand Voice
          </div>
          <div class="settings-card-desc">Inject custom brand identity into all AI generation prompts.</div>
        </div>
        <div class="settings-card-body">
          <div class="form-group">
            <label class="form-label">Brand / Organization Name</label>
            <input type="text" class="form-input" id="brandNameInput" placeholder="e.g. Acme Corp / TransformAI" value="${escapeHtml(settings.brand?.name || '')}" />
          </div>
          <div class="form-group">
            <label class="form-label">Voice & Tone Directives</label>
            <textarea class="form-textarea" id="brandVoiceInput" placeholder="e.g. Write in a clear, empowering, confident voice. Avoid buzzwords. End with a decisive call to action..." style="min-height:85px;">${escapeHtml(settings.brand?.voice || '')}</textarea>
          </div>
          <button class="btn btn-secondary btn-sm w-full" onclick="SettingsPage.saveBrand()">
            <i class="ri-save-line"></i> Save Brand Voice
          </button>
        </div>
      </div>

      <!-- 4. Data & Local Storage Control -->
      <div class="settings-card full-width">
        <div class="settings-card-header">
          <div class="settings-card-title">
            <i class="ri-database-2-line" style="color:#f87171"></i> Local Data & Storage Management
          </div>
          <div class="settings-card-desc">View storage consumption and clear history or cached configurations.</div>
        </div>
        <div class="settings-card-body">
          <div class="flex items-center justify-between flex-wrap gap-4">
            <div>
              <div style="font-weight:600;font-size:14px;color:var(--text-primary);">Transformation Records: ${AppState.getHistory().length} items</div>
              <div style="font-size:12px;color:var(--text-muted);margin-top:2px;">All information is stored exclusively in your browser localStorage.</div>
            </div>
            <div class="flex gap-2">
              <button class="btn btn-secondary btn-sm" onclick="App.navigate('history')">
                <i class="ri-history-line"></i> View History
              </button>
              <button class="btn btn-danger btn-sm" onclick="SettingsPage.clearAllData()">
                <i class="ri-delete-bin-line"></i> Clear All Data
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>`;
}

const SettingsPage = {
  selectProvider(providerId) {
    API.setProvider(providerId);
    App.updateAPIStatus();
    App.navigate('settings');
    Toast.show('info', 'Provider Changed', `Active provider is now ${providerId.toUpperCase()}.`);
  },

  toggleApiKeyVisibility() {
    const inp = document.getElementById('providerApiKeyInput');
    const btn = document.getElementById('apiKeyEyeBtn');
    if (!inp || !btn) return;
    if (inp.type === 'password') {
      inp.type = 'text';
      btn.innerHTML = '<i class="ri-eye-off-line"></i>';
    } else {
      inp.type = 'password';
      btn.innerHTML = '<i class="ri-eye-line"></i>';
    }
  },

  async testCurrentProvider() {
    const currentProvider = API.getProvider();
    const key = document.getElementById('providerApiKeyInput')?.value?.trim();
    if (currentProvider !== 'local') {
      API.setKey(currentProvider, key);
    }

    const resEl = document.getElementById('providerTestResult');
    if (resEl) {
      resEl.innerHTML = '<span style="color:var(--text-muted);"><i class="ri-loader-4-line spinner"></i> Testing connection...</span>';
    }

    const testRes = await API.testConnection(currentProvider);
    if (resEl) {
      if (testRes.success) {
        resEl.innerHTML = `<span style="color:#34d399;"><i class="ri-check-line"></i> ${testRes.message}</span>`;
        Toast.show('success', 'Connection Verified', testRes.message);
      } else {
        resEl.innerHTML = `<span style="color:#f87171;"><i class="ri-close-line"></i> ${testRes.message}</span>`;
        Toast.show('error', 'Connection Test Failed', testRes.message);
      }
    }
  },

  saveAll() {
    const currentProvider = API.getProvider();
    if (currentProvider !== 'local') {
      const key = document.getElementById('providerApiKeyInput')?.value?.trim();
      const model = document.getElementById('providerModelSelect')?.value;
      if (key !== undefined) API.setKey(currentProvider, key);
      if (model) API.setModel(currentProvider, model);
    }

    const bName = document.getElementById('brandNameInput')?.value?.trim();
    const bVoice = document.getElementById('brandVoiceInput')?.value?.trim();
    AppState.updateSetting('brand', { name: bName, voice: bVoice });

    App.updateAPIStatus();
    Toast.show('success', 'Settings Saved', 'All settings and provider configurations have been persisted.');
  },

  saveBrand() {
    const bName = document.getElementById('brandNameInput')?.value?.trim();
    const bVoice = document.getElementById('brandVoiceInput')?.value?.trim();
    AppState.updateSetting('brand', { name: bName, voice: bVoice });
    Toast.show('success', 'Brand Profile Saved', 'Custom brand voice updated.');
  },

  togglePref(key) {
    const el = document.getElementById(`pref-${key}`);
    const current = AppState.getPref(key, true);
    AppState.updatePref(key, !current);
    if (el) el.classList.toggle('on', !current);
    Toast.show('info', 'Preference Updated', `${key} is now ${!current ? 'Enabled' : 'Disabled'}.`);
  },

  toggleTheme() {
    ThemeManager.toggle();
    const el = document.getElementById('pref-theme');
    if (el) el.classList.toggle('on', document.documentElement.getAttribute('data-theme') !== 'light');
  },

  clearAllData() {
    if (!confirm('Warning: This will permanently delete all your stored history, settings, and cached configurations. Proceed?')) {
      return;
    }
    localStorage.clear();
    Toast.show('success', 'Data Cleared', 'All local storage has been wiped. Reloading...');
    setTimeout(() => location.reload(), 1200);
  }
};
'''

save_file("pages/settings.js", SETTINGS_JS)
