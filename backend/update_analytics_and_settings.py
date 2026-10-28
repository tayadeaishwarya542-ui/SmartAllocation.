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

# --- pages/analytics.js ---
ANALYTICS_JS = r'''// ================================================================
//  Analytics Page — Real Metrics & Usage Insights
// ================================================================

function renderAnalyticsPage() {
  const history = AppState.getHistory();
  const stats = AppState.getStats();

  if (history.length === 0) {
    return `
    <div class="page-view">
      <div class="page-header">
        <div class="page-header-top">
          <div>
            <div class="page-title">Analytics & Intelligence Telemetry <span class="grad-text">✦</span></div>
            <div class="page-desc">Comprehensive monitoring of content throughput, operation distribution, and efficiency.</div>
          </div>
          <span class="badge badge-secondary"><i class="ri-pause-circle-line"></i> Awaiting Data</span>
        </div>
      </div>

      <div class="empty-state-box full-width" style="margin-top:20px;">
        <i class="ri-bar-chart-2-line"></i>
        <div class="empty-state-title">No Transformation Analytics Recorded</div>
        <div class="empty-state-desc">Once you execute content transformations or pipelines, live metrics, provider usage distribution, and volume trends will be calculated here in real time.</div>
        <button class="btn btn-primary btn-sm" onclick="App.navigate('transform')" style="margin-top:14px;">
          <i class="ri-magic-line"></i> Launch AI Transformer
        </button>
      </div>
    </div>`;
  }

  // Calculate real metrics from history
  const typeCounts = {};
  const providerCounts = {};
  history.forEach(item => {
    typeCounts[item.type] = (typeCounts[item.type] || 0) + 1;
    const prov = item.provider || item.model || 'local';
    providerCounts[prov] = (providerCounts[prov] || 0) + 1;
  });

  const total = history.length;
  const sortedTypes = Object.entries(typeCounts).sort((a, b) => b[1] - a[1]);

  return `
  <div class="page-view">
    <div class="page-header">
      <div class="page-header-top">
        <div>
          <div class="page-title">Analytics & Intelligence Telemetry <span class="grad-text">✦</span></div>
          <div class="page-desc">Derived strictly from active local transformation records and pipeline executions.</div>
        </div>
        <span class="badge badge-green"><i class="ri-checkbox-circle-fill"></i> Live Real Data</span>
      </div>
    </div>

    <!-- Top Telemetry Stats Grid -->
    <div class="stats-grid" style="margin-bottom:24px">
      <div class="stat-card">
        <div class="stat-icon purple"><i class="ri-bar-chart-2-line"></i></div>
        <div class="stat-value">${stats.totalTransforms}</div>
        <div class="stat-label">Total Transformations</div>
        <div class="stat-subtext"><i class="ri-database-2-line"></i> Executed operations</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon cyan"><i class="ri-file-word-line"></i></div>
        <div class="stat-value">${stats.wordsProcessed.toLocaleString()}</div>
        <div class="stat-label">Words Processed</div>
        <div class="stat-subtext"><i class="ri-speed-up-line"></i> Verified throughput</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon green"><i class="ri-checkbox-circle-line"></i></div>
        <div class="stat-value">${stats.successRate}</div>
        <div class="stat-label">Success Rate</div>
        <div class="stat-subtext">${stats.successfulOperations} success / ${stats.failedOperations} fail</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon orange"><i class="ri-timer-line"></i></div>
        <div class="stat-value">${stats.pipelinesCreated}</div>
        <div class="stat-label">Saved Pipelines</div>
        <div class="stat-subtext"><i class="ri-folder-shared-line"></i> Workflow library</div>
      </div>
    </div>

    <div class="grid grid-2 gap-4" style="margin-bottom:24px;">
      <!-- Most Frequently Used Operations -->
      <div class="settings-card">
        <div class="settings-card-header">
          <div class="settings-card-title"><i class="ri-pie-chart-line" style="color:var(--accent-primary)"></i> Operation Distribution</div>
          <div class="settings-card-desc">Volume of transformations segmented by individual operation.</div>
        </div>
        <div class="settings-card-body">
          <div class="quality-metrics-grid" style="grid-template-columns:1fr;">
            ${sortedTypes.map(([type, count]) => {
              const def = TRANSFORMATIONS[type] || { label: capitalize(type), icon: 'ri-magic-line' };
              const pct = Math.round((count / total) * 100);
              return `
                <div class="metric-row">
                  <div class="metric-label">
                    <span><i class="${def.icon}"></i> ${def.label}</span>
                    <span class="metric-val">${count} (${pct}%)</span>
                  </div>
                  <div class="metric-bar-bg">
                    <div class="metric-bar-fill" style="width:${pct}%;background:var(--accent-primary);"></div>
                  </div>
                </div>
              `;
            }).join('')}
          </div>
        </div>
      </div>

      <!-- Provider Usage Statistics -->
      <div class="settings-card">
        <div class="settings-card-header">
          <div class="settings-card-title"><i class="ri-cpu-line" style="color:#67e8f9"></i> Provider Utilization</div>
          <div class="settings-card-desc">Routing telemetry across configured AI engines.</div>
        </div>
        <div class="settings-card-body">
          <div class="quality-metrics-grid" style="grid-template-columns:1fr;">
            ${Object.entries(providerCounts).map(([prov, count]) => {
              const pct = Math.round((count / total) * 100);
              return `
                <div class="metric-row">
                  <div class="metric-label">
                    <span>${prov.toUpperCase()}</span>
                    <span class="metric-val">${count} (${pct}%)</span>
                  </div>
                  <div class="metric-bar-bg">
                    <div class="metric-bar-fill" style="width:${pct}%;background:#34d399;"></div>
                  </div>
                </div>
              `;
            }).join('')}
          </div>
        </div>
      </div>
    </div>

  </div>`;
}
'''

# --- pages/settings.js ---
SETTINGS_JS = r'''// ================================================================
//  Settings Page — Full SaaS Preferences, Providers, and Privacy
// ================================================================

function renderSettingsPage() {
  const settings = AppState.getSettings();
  const currentProvider = API.getProvider();
  const prefs = settings.prefs || {};

  return `
  <div class="page-view">
    <div class="page-header">
      <div class="page-header-top">
        <div>
          <div class="page-title">System Settings <span class="grad-text">✦</span></div>
          <div class="page-desc">Manage theme appearance, AI engine preferences, default parameters, and privacy.</div>
        </div>
        <button class="btn btn-primary btn-sm" onclick="SettingsPage.saveAll()">
          <i class="ri-save-line"></i> Save Changes
        </button>
      </div>
    </div>

    <div class="settings-grid">
      <!-- 1. Appearance Section -->
      <div class="settings-card">
        <div class="settings-card-header">
          <div class="settings-card-title"><i class="ri-palette-line" style="color:#67e8f9"></i> Appearance & Theme</div>
          <div class="settings-card-desc">Switch between modern dark glassmorphism and clean light mode.</div>
        </div>
        <div class="settings-card-body">
          <div class="toggle-row">
            <div class="toggle-info">
              <div class="toggle-label">Dark Theme</div>
              <div class="toggle-desc">Charcoal surfaces with deep indigo accents</div>
            </div>
            <div class="toggle-switch ${document.documentElement.getAttribute('data-theme') !== 'light' ? 'on' : ''}"
              id="pref-theme" onclick="SettingsPage.toggleTheme()"></div>
          </div>
          <div class="toggle-row">
            <div class="toggle-info">
              <div class="toggle-label">Real-time Streaming</div>
              <div class="toggle-desc">Show word-by-word streaming generation animation</div>
            </div>
            <div class="toggle-switch ${prefs.streaming !== false ? 'on' : ''}"
              id="pref-streaming" onclick="SettingsPage.togglePref('streaming')"></div>
          </div>
        </div>
      </div>

      <!-- 2. AI Providers Quick Setup -->
      <div class="settings-card">
        <div class="settings-card-header">
          <div class="settings-card-title"><i class="ri-cpu-line" style="color:var(--accent-primary)"></i> AI Provider & Routing</div>
          <div class="settings-card-desc">Current engine: <strong style="color:var(--accent-primary);">${currentProvider.toUpperCase()}</strong></div>
        </div>
        <div class="settings-card-body">
          <p style="font-size:13px;color:var(--text-secondary);line-height:1.5;margin-bottom:14px;">
            TransformAI supports Local Fallback, OpenAI, Google Gemini, and Anthropic Claude with automatic offline resilience.
          </p>
          <button class="btn btn-secondary btn-sm w-full" onclick="App.navigate('providers')">
            <i class="ri-equalizer-line"></i> Open AI Provider Hub
          </button>
        </div>
      </div>

      <!-- 3. Transformation Default Preferences -->
      <div class="settings-card full-width">
        <div class="settings-card-header">
          <div class="settings-card-title"><i class="ri-equalizer-line" style="color:#6ee7b7"></i> Default Transformation Preferences</div>
          <div class="settings-card-desc">Set default parameters applied whenever you start a new transformation.</div>
        </div>
        <div class="settings-card-body">
          <div class="grid grid-2 gap-4">
            <div class="form-group">
              <label class="form-label">Default Transformation Engine</label>
              <select class="form-select" id="prefDefaultType">
                ${Object.keys(TRANSFORMATIONS).map(k => `
                  <option value="${k}" ${prefs.defaultType === k ? 'selected' : ''}>${TRANSFORMATIONS[k].label}</option>
                `).join('')}
              </select>
            </div>

            <div class="form-group">
              <label class="form-label">Default Translation Target Language</label>
              <select class="form-select" id="prefDefaultLang">
                <option value="hi" ${prefs.defaultLang === 'hi' ? 'selected' : ''}>Hindi (हिंदी)</option>
                <option value="mr" ${prefs.defaultLang === 'mr' ? 'selected' : ''}>Marathi (मराठी)</option>
                <option value="es" ${prefs.defaultLang === 'es' ? 'selected' : ''}>Spanish (Español)</option>
                <option value="fr" ${prefs.defaultLang === 'fr' ? 'selected' : ''}>French (Français)</option>
                <option value="de" ${prefs.defaultLang === 'de' ? 'selected' : ''}>German (Deutsch)</option>
                <option value="ja" ${prefs.defaultLang === 'ja' ? 'selected' : ''}>Japanese (日本語)</option>
                <option value="en" ${prefs.defaultLang === 'en' ? 'selected' : ''}>English</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label">Default Target Tone</label>
              <select class="form-select" id="prefDefaultTone">
                <option value="professional" ${prefs.defaultTone === 'professional' ? 'selected' : ''}>Professional</option>
                <option value="formal" ${prefs.defaultTone === 'formal' ? 'selected' : ''}>Formal</option>
                <option value="casual" ${prefs.defaultTone === 'casual' ? 'selected' : ''}>Casual</option>
                <option value="academic" ${prefs.defaultTone === 'academic' ? 'selected' : ''}>Academic</option>
                <option value="persuasive" ${prefs.defaultTone === 'persuasive' ? 'selected' : ''}>Persuasive</option>
                <option value="creative" ${prefs.defaultTone === 'creative' ? 'selected' : ''}>Creative</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label">Default Summary Length</label>
              <select class="form-select" id="prefDefaultLength">
                <option value="short" ${prefs.defaultLength === 'short' ? 'selected' : ''}>Short (Core Takeaways)</option>
                <option value="medium" ${prefs.defaultLength === 'medium' ? 'selected' : ''}>Medium (Executive Overview)</option>
                <option value="detailed" ${prefs.defaultLength === 'detailed' ? 'selected' : ''}>Detailed (Comprehensive Brief)</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <!-- 4. Data & Privacy Management -->
      <div class="settings-card full-width">
        <div class="settings-card-header">
          <div class="settings-card-title"><i class="ri-shield-user-line" style="color:#f87171"></i> Data & Privacy Control</div>
          <div class="settings-card-desc">All user data, history, and preferences are stored locally in your browser.</div>
        </div>
        <div class="settings-card-body">
          <div class="flex items-center justify-between flex-wrap gap-4 p-3" style="background:var(--bg-elevated);border-radius:var(--radius-md);margin-bottom:12px;">
            <div>
              <div style="font-weight:600;font-size:13.5px;color:var(--text-primary);">Transformation History</div>
              <div style="font-size:12px;color:var(--text-muted);">${AppState.getHistory().length} logged operations</div>
            </div>
            <button class="btn btn-secondary btn-sm" onclick="SettingsPage.clearHistoryOnly()">
              <i class="ri-delete-bin-line"></i> Clear History
            </button>
          </div>

          <div class="flex items-center justify-between flex-wrap gap-4 p-3" style="background:var(--bg-elevated);border-radius:var(--radius-md);margin-bottom:12px;">
            <div>
              <div style="font-weight:600;font-size:13.5px;color:var(--text-primary);">Saved Pipelines</div>
              <div style="font-size:12px;color:var(--text-muted);">${AppState.getSavedPipelines().length} workflows in library</div>
            </div>
            <button class="btn btn-secondary btn-sm" onclick="SettingsPage.clearPipelinesOnly()">
              <i class="ri-delete-bin-line"></i> Clear Saved Pipelines
            </button>
          </div>

          <div class="flex items-center justify-between flex-wrap gap-4 p-3" style="background:rgba(248,113,113,0.08);border:1px solid rgba(248,113,113,0.25);border-radius:var(--radius-md);">
            <div>
              <div style="font-weight:600;font-size:13.5px;color:#f87171;">Reset All Application Data</div>
              <div style="font-size:12px;color:var(--text-muted);">Permanently wipes all history, saved workflows, keys, and settings.</div>
            </div>
            <button class="btn btn-danger btn-sm" onclick="SettingsPage.clearAllData()">
              <i class="ri-alert-line"></i> Reset Everything
            </button>
          </div>
        </div>
      </div>

      <!-- 5. General Info & Version -->
      <div class="settings-card full-width">
        <div class="settings-card-header">
          <div class="settings-card-title"><i class="ri-information-line"></i> General Application Information</div>
        </div>
        <div class="settings-card-body" style="font-size:13px;color:var(--text-secondary);line-height:1.6;">
          <div class="flex items-center justify-between flex-wrap gap-2">
            <div>
              <strong>TransformAI Enterprise Platform</strong> · Version 1.0.0<br>
              <span style="font-size:12px;color:var(--text-muted);">Deterministic In-Browser NLP & Multi-Provider Cloud Orchestration Engine</span>
            </div>
            <button class="btn btn-secondary btn-xs" onclick="App.navigate('help')">
              <i class="ri-book-open-line"></i> Documentation & Troubleshooting
            </button>
          </div>
        </div>
      </div>

    </div>
  </div>`;
}

const SettingsPage = {
  toggleTheme() {
    ThemeManager.toggle();
    const el = document.getElementById('pref-theme');
    if (el) el.classList.toggle('on', document.documentElement.getAttribute('data-theme') !== 'light');
  },

  togglePref(key) {
    const el = document.getElementById(`pref-${key}`);
    const current = AppState.getPref(key, true);
    AppState.updatePref(key, !current);
    if (el) el.classList.toggle('on', !current);
    Toast.show('info', 'Preference Updated', `${key} updated.`);
  },

  saveAll() {
    const defaultType = document.getElementById('prefDefaultType')?.value;
    const defaultLang = document.getElementById('prefDefaultLang')?.value;
    const defaultTone = document.getElementById('prefDefaultTone')?.value;
    const defaultLength = document.getElementById('prefDefaultLength')?.value;

    AppState.updatePref('defaultType', defaultType);
    AppState.updatePref('defaultLang', defaultLang);
    AppState.updatePref('defaultTone', defaultTone);
    AppState.updatePref('defaultLength', defaultLength);

    Toast.show('success', 'Settings Saved', 'Default preferences saved successfully.');
  },

  clearHistoryOnly() {
    if (!confirm('Are you sure you want to delete all transformation history?')) return;
    AppState.clearHistory();
    Toast.show('info', 'History Cleared', 'Transformation records removed.');
    App.navigate('settings');
  },

  clearPipelinesOnly() {
    if (!confirm('Are you sure you want to delete all saved pipelines?')) return;
    const s = AppState.getAll();
    s.savedPipelines = [];
    AppState._save(s);
    Toast.show('info', 'Pipelines Cleared', 'Saved pipelines removed.');
    App.navigate('settings');
  },

  clearAllData() {
    if (!confirm('CRITICAL CONFIRMATION: This will delete ALL local history, saved pipelines, preferences, and cached keys. Proceed?')) return;
    localStorage.clear();
    Toast.show('success', 'Reset Complete', 'Local workspace cleared. Reloading...');
    setTimeout(() => location.reload(), 1200);
  }
};
'''

save_file("pages/analytics.js", ANALYTICS_JS)
save_file("pages/settings.js", SETTINGS_JS)
