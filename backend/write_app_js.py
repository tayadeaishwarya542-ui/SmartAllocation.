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

# --- js/app.js ---
APP_JS = r'''// ================================================================
//  TransformAI — Core Application Router, State Manager & Theme
// ================================================================

const AppState = {
  _key: 'transformai_state_v2',

  _defaults() {
    return {
      provider: 'local',
      keys: { openai: '', gemini: '', anthropic: '' },
      models: { openai: 'gpt-4o-mini', gemini: 'gemini-1.5-flash', anthropic: 'claude-3-5-sonnet-20241022', local: 'local-nlp-v1' },
      brand: { name: '', voice: '' },
      prefs: { streaming: true, autoSave: true, theme: 'dark' },
      history: [],
      stats: { totalTransforms: 0, wordsProcessed: 0, languagesUsed: 7, timeSaved: 0, usageByType: {} }
    };
  },

  _load() {
    try {
      const data = localStorage.getItem(this._key);
      if (!data) return this._defaults();
      return { ...this._defaults(), ...JSON.parse(data) };
    } catch {
      return this._defaults();
    }
  },

  _save(state) {
    try {
      localStorage.setItem(this._key, JSON.stringify(state));
    } catch (e) {
      console.warn('[AppState] Failed to save to localStorage:', e);
    }
  },

  getAll() { return this._load(); },

  getSettings() {
    const s = this._load();
    return {
      provider: s.provider,
      keys: s.keys,
      models: s.models,
      brand: s.brand,
      prefs: s.prefs
    };
  },

  getSetting(key) {
    const s = this._load();
    return s[key];
  },

  getPref(key, defaultVal) {
    const s = this._load();
    if (!s.prefs) return defaultVal;
    return s.prefs[key] !== undefined ? s.prefs[key] : defaultVal;
  },

  updateSetting(key, val) {
    const s = this._load();
    s[key] = val;
    this._save(s);
  },

  updatePref(key, val) {
    const s = this._load();
    if (!s.prefs) s.prefs = {};
    s.prefs[key] = val;
    this._save(s);
  },

  getHistory() {
    return (this._load().history || []).slice().reverse();
  },

  getStats() {
    return this._load().stats || this._defaults().stats;
  },

  addHistory(item) {
    const s = this._load();
    if (!s.history) s.history = [];
    s.history.push(item);

    if (!s.stats) s.stats = this._defaults().stats;
    s.stats.totalTransforms = (s.stats.totalTransforms || 0) + 1;
    const wc = item.input ? item.input.trim().split(/\s+/).filter(Boolean).length : 0;
    s.stats.wordsProcessed = (s.stats.wordsProcessed || 0) + wc;

    if (!s.stats.usageByType) s.stats.usageByType = {};
    s.stats.usageByType[item.type] = (s.stats.usageByType[item.type] || 0) + 1;
    s.stats.timeSaved = Math.round((s.stats.wordsProcessed / 250) * 0.5 * 10) / 10;

    this._save(s);
  },

  deleteHistoryItem(idx) {
    const s = this._load();
    const reversed = (s.history || []).slice().reverse();
    reversed.splice(idx, 1);
    s.history = reversed.slice().reverse();
    this._save(s);
  },

  clearHistory() {
    const s = this._load();
    s.history = [];
    this._save(s);
  }
};

// --- Theme Controller ---
const ThemeManager = {
  init() {
    const savedTheme = AppState.getPref('theme', 'dark');
    document.documentElement.setAttribute('data-theme', savedTheme);
    this.updateIcon(savedTheme);
  },

  toggle() {
    const current = document.documentElement.getAttribute('data-theme') || 'dark';
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    AppState.updatePref('theme', next);
    this.updateIcon(next);
    Toast.show('info', 'Theme Switched', `Active theme is now ${next.toUpperCase()} mode.`);
  },

  updateIcon(theme) {
    const icon = document.getElementById('themeToggleIcon');
    if (icon) {
      icon.className = theme === 'dark' ? 'ri-sun-line' : 'ri-moon-line';
    }
  }
};

// --- Toast System ---
const Toast = {
  show(type, title, message, duration = 4000) {
    const icons = {
      success: 'ri-checkbox-circle-fill',
      error: 'ri-close-circle-fill',
      info: 'ri-information-fill',
      warning: 'ri-alert-fill'
    };
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
      <i class="toast-icon ${icons[type] || icons.info}"></i>
      <div class="toast-body">
        <div class="toast-title">${title}</div>
        ${message ? `<div class="toast-msg">${message}</div>` : ''}
      </div>
      <i class="toast-close ri-close-line" onclick="this.closest('.toast').remove()"></i>`;

    container.appendChild(toast);
    setTimeout(() => {
      toast.classList.add('removing');
      setTimeout(() => toast.remove(), 300);
    }, duration);
  }
};

// --- Page Declarations ---
const PAGES = {
  dashboard: {
    title: 'Dashboard',
    icon: 'ri-dashboard-3-line',
    render: () => renderDashboard(),
    afterRender: () => {}
  },
  transform: {
    title: 'Transform',
    icon: 'ri-magic-line',
    render: (opts) => renderTransformPage(opts?.type),
    afterRender: () => {}
  },
  pipelines: {
    title: 'Pipelines',
    icon: 'ri-flow-chart',
    render: () => renderPipelinesPage(),
    afterRender: () => {}
  },
  history: {
    title: 'History',
    icon: 'ri-history-line',
    render: () => renderHistoryPage(),
    afterRender: () => {}
  },
  analytics: {
    title: 'Analytics',
    icon: 'ri-bar-chart-2-line',
    render: () => renderAnalyticsPage(),
    afterRender: () => {}
  },
  settings: {
    title: 'Settings',
    icon: 'ri-settings-4-line',
    render: () => renderSettingsPage(),
    afterRender: () => {}
  }
};

// --- Main App Controller ---
const App = {
  _currentPage: 'dashboard',

  init() {
    ThemeManager.init();
    API.initFromStorage();
    this.updateAPIStatus();

    // Sidebar collapse
    const toggleBtn = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    const main = document.getElementById('mainContent');
    if (toggleBtn && sidebar && main) {
      toggleBtn.addEventListener('click', () => {
        sidebar.classList.toggle('collapsed');
        main.classList.toggle('sidebar-collapsed');
      });
    }

    // Mobile menu toggle
    const mobileBtn = document.getElementById('mobileMenuBtn');
    if (mobileBtn && sidebar) {
      mobileBtn.addEventListener('click', () => sidebar.classList.toggle('mobile-open'));
    }

    // Nav clicks
    document.querySelectorAll('.nav-item').forEach(item => {
      item.addEventListener('click', e => {
        e.preventDefault();
        const page = item.dataset.page;
        if (page) this.navigate(page);
        sidebar?.classList.remove('mobile-open');
      });
    });

    // Global Search Shortcut (Cmd+K / Ctrl+K)
    document.addEventListener('keydown', e => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        const s = document.getElementById('globalSearch');
        if (s) { s.focus(); s.select(); }
      }
    });

    const searchInput = document.getElementById('globalSearch');
    if (searchInput) {
      searchInput.addEventListener('keydown', e => {
        if (e.key === 'Enter') {
          const val = searchInput.value.trim().toLowerCase();
          if (!val) return;
          // Check if matches an operation
          const matchOp = Object.values(TRANSFORMATIONS).find(t => t.id.includes(val) || t.label.toLowerCase().includes(val));
          if (matchOp) {
            this.navigateToTransform(matchOp.id);
            Toast.show('info', 'Navigated', `Opened ${matchOp.label}.`);
          } else {
            this.navigate('history');
            setTimeout(() => {
              const hSearch = document.getElementById('historySearchInput');
              if (hSearch) { hSearch.value = val; HistoryPage.onSearch(val); }
            }, 200);
          }
        }
      });
    }

    // Notification button
    const notifBtn = document.getElementById('notifBtn');
    if (notifBtn) {
      notifBtn.addEventListener('click', () => {
        Toast.show('info', 'System Telemetry', 'TransformAI Engine v1.0.0 is operating normally with zero degraded services.');
      });
    }

    this.navigate('dashboard');
  },

  navigate(pageId, opts = {}) {
    const page = PAGES[pageId];
    if (!page) return;

    this._currentPage = pageId;

    document.querySelectorAll('.nav-item').forEach(el => {
      el.classList.toggle('active', el.dataset.page === pageId);
    });

    const bcIcon = document.querySelector('.breadcrumb-icon i');
    const bcLabel = document.getElementById('breadcrumbLabel');
    if (bcIcon) bcIcon.className = page.icon;
    if (bcLabel) bcLabel.textContent = page.title;

    const container = document.getElementById('pageContainer');
    if (container) {
      container.innerHTML = page.render(opts);
      page.afterRender?.();
      container.scrollTo({ top: 0, behavior: 'smooth' });
    }
  },

  navigateToTransform(type) {
    this.navigate('transform', { type });
  },

  updateAPIStatus() {
    const dot = document.getElementById('statusDot');
    const text = document.getElementById('statusText');
    if (!dot || !text) return;

    const provider = API.getProvider();
    const model = API.getModel();

    if (provider === 'local') {
      dot.className = 'status-dot online';
      text.textContent = 'Local Engine (Active)';
    } else if (API.isConfigured(provider)) {
      dot.className = 'status-dot online';
      text.textContent = `${provider.toUpperCase()} (${model})`;
    } else {
      dot.className = 'status-dot offline';
      text.textContent = `${provider.toUpperCase()} (No Key)`;
    }
  }
};

document.addEventListener('DOMContentLoaded', () => App.init());
'''

save_file("js/app.js", APP_JS)
