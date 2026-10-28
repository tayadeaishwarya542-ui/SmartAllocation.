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

APP_JS = r'''// ================================================================
//  TransformAI — Core SaaS Application Router & State Manager
// ================================================================

const AppState = {
  _key: 'transformai_saas_state_v3',

  _defaults() {
    return {
      provider: 'local',
      keys: { openai: '', gemini: '', anthropic: '' },
      models: { openai: 'gpt-4o-mini', gemini: 'gemini-1.5-flash', anthropic: 'claude-3-5-sonnet-20241022', local: 'local-nlp-v1' },
      brand: { name: 'TransformAI Enterprise', voice: 'Clear, direct, and outcome-focused.' },
      prefs: {
        streaming: true,
        autoSave: true,
        theme: 'dark',
        defaultType: 'summarize',
        defaultLang: 'hi',
        defaultTone: 'professional',
        defaultLength: 'medium'
      },
      history: [],
      notifications: [
        {
          id: 'notif_welcome',
          title: 'TransformAI Initialized',
          message: 'The zero-config Local Fallback NLP Engine is active and ready for transformations.',
          time: Date.now() - 1000 * 60 * 15,
          read: false
        }
      ],
      savedPipelines: [
        {
          id: 'pipe_blog_social',
          name: 'Blog → Social Media Kit',
          desc: 'Turn long-form content into polished social media takeaways.',
          stages: [
            { type: 'grammar', opts: { showDiff: 'no' }, enabled: true },
            { type: 'tone', opts: { targetTone: 'professional' }, enabled: true },
            { type: 'summarize', opts: { length: 'short' }, enabled: true },
            { type: 'convert', opts: { targetFormat: 'bullets' }, enabled: true }
          ],
          lastExecuted: Date.now() - 1000 * 60 * 60 * 2,
          status: 'Ready'
        },
        {
          id: 'pipe_exec_brief',
          name: 'Report → Executive Briefing',
          desc: 'Condense complex technical reports into formal briefings.',
          stages: [
            { type: 'summarize', opts: { length: 'detailed' }, enabled: true },
            { type: 'tone', opts: { targetTone: 'formal' }, enabled: true },
            { type: 'convert', opts: { targetFormat: 'report' }, enabled: true },
            { type: 'quality', opts: { evaluationStandard: 'business' }, enabled: true }
          ],
          lastExecuted: null,
          status: 'Ready'
        },
        {
          id: 'pipe_multilang',
          name: 'Global Dispatch (EN → HI)',
          desc: 'Proofread and translate English text into regional Hindi.',
          stages: [
            { type: 'grammar', opts: { showDiff: 'no' }, enabled: true },
            { type: 'tone', opts: { targetTone: 'friendly' }, enabled: true },
            { type: 'translate', opts: { sourceLang: 'en', targetLang: 'hi' }, enabled: true }
          ],
          lastExecuted: null,
          status: 'Ready'
        }
      ],
      stats: {
        successfulOperations: 0,
        failedOperations: 0,
        totalTransforms: 0,
        wordsProcessed: 0,
        usageByType: {}
      }
    };
  },

  _load() {
    try {
      const data = localStorage.getItem(this._key);
      if (!data) return this._defaults();
      const parsed = JSON.parse(data);
      return {
        ...this._defaults(),
        ...parsed,
        stats: { ...this._defaults().stats, ...(parsed.stats || {}) },
        prefs: { ...this._defaults().prefs, ...(parsed.prefs || {}) },
        savedPipelines: parsed.savedPipelines && parsed.savedPipelines.length ? parsed.savedPipelines : this._defaults().savedPipelines
      };
    } catch {
      return this._defaults();
    }
  },

  _save(state) {
    try {
      localStorage.setItem(this._key, JSON.stringify(state));
    } catch (e) {
      console.warn('[AppState] Failed to save state to localStorage:', e);
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

  // --- History Records ---
  getHistory() {
    return (this._load().history || []).slice().reverse();
  },

  addHistory(item) {
    const s = this._load();
    if (!s.history) s.history = [];
    s.history.push(item);

    // Compute metrics
    if (!s.stats) s.stats = this._defaults().stats;
    s.stats.totalTransforms = (s.stats.totalTransforms || 0) + 1;
    s.stats.successfulOperations = (s.stats.successfulOperations || 0) + 1;

    const wc = item.input ? item.input.trim().split(/\s+/).filter(Boolean).length : 0;
    s.stats.wordsProcessed = (s.stats.wordsProcessed || 0) + wc;

    if (!s.stats.usageByType) s.stats.usageByType = {};
    s.stats.usageByType[item.type] = (s.stats.usageByType[item.type] || 0) + 1;

    this._save(s);

    // Trigger Notification
    const def = TRANSFORMATIONS[item.type];
    this.addNotification(
      'Transformation Completed',
      `${def ? def.label : item.type} finished successfully (${wc} words).`,
      'success'
    );
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
  },

  // --- Notifications ---
  getNotifications() {
    return (this._load().notifications || []).slice().reverse();
  },

  addNotification(title, message, type = 'info') {
    const s = this._load();
    if (!s.notifications) s.notifications = [];
    s.notifications.push({
      id: `notif_${Date.now()}`,
      title,
      message,
      type,
      time: Date.now(),
      read: false
    });
    if (s.notifications.length > 50) s.notifications.shift();
    this._save(s);
    App.updateNotificationBadge();
  },

  markNotificationsRead() {
    const s = this._load();
    if (!s.notifications) return;
    s.notifications.forEach(n => { n.read = true; });
    this._save(s);
    App.updateNotificationBadge();
  },

  clearNotifications() {
    const s = this._load();
    s.notifications = [];
    this._save(s);
    App.updateNotificationBadge();
  },

  getUnreadNotificationCount() {
    const notifs = this._load().notifications || [];
    return notifs.filter(n => !n.read).length;
  },

  // --- Saved Pipelines ---
  getSavedPipelines() {
    return (this._load().savedPipelines || []).slice();
  },

  savePipeline(pipeline) {
    const s = this._load();
    if (!s.savedPipelines) s.savedPipelines = [];
    const existingIdx = s.savedPipelines.findIndex(p => p.id === pipeline.id);
    if (existingIdx !== -1) {
      s.savedPipelines[existingIdx] = pipeline;
    } else {
      s.savedPipelines.push(pipeline);
    }
    this._save(s);
    this.addNotification('Pipeline Saved', `Pipeline "${pipeline.name}" saved to library.`, 'success');
  },

  duplicateSavedPipeline(id) {
    const s = this._load();
    const orig = (s.savedPipelines || []).find(p => p.id === id);
    if (!orig) return null;
    const copy = {
      ...JSON.parse(JSON.stringify(orig)),
      id: `pipe_${Date.now()}`,
      name: `${orig.name} (Copy)`,
      lastExecuted: null,
      status: 'Ready'
    };
    s.savedPipelines.push(copy);
    this._save(s);
    this.addNotification('Pipeline Duplicated', `Created copy "${copy.name}".`, 'info');
    return copy;
  },

  deleteSavedPipeline(id) {
    const s = this._load();
    s.savedPipelines = (s.savedPipelines || []).filter(p => p.id !== id);
    this._save(s);
    this.addNotification('Pipeline Deleted', 'Pipeline removed from library.', 'info');
  },

  updatePipelineExecution(id, success = true) {
    const s = this._load();
    const p = (s.savedPipelines || []).find(x => x.id === id);
    if (p) {
      p.lastExecuted = Date.now();
      p.status = success ? 'Success' : 'Failed';
      this._save(s);
    }
  },

  // --- Real Stats Helpers ---
  getStats() {
    const s = this._load();
    const history = s.history || [];
    const savedPipelines = s.savedPipelines || [];

    // Calculate live word count sum from history
    let realWords = 0;
    history.forEach(item => {
      if (item.input) {
        realWords += item.input.trim().split(/\s+/).filter(Boolean).length;
      }
    });

    const success = s.stats?.successfulOperations || history.length;
    const failed = s.stats?.failedOperations || 0;
    const totalOps = success + failed;

    let successRateStr = '100%';
    if (totalOps === 0) {
      successRateStr = 'No data yet';
    } else {
      const pct = Math.round((success / totalOps) * 100);
      successRateStr = `${pct}%`;
    }

    return {
      totalTransforms: history.length,
      pipelinesCreated: savedPipelines.length,
      wordsProcessed: realWords,
      successRate: successRateStr,
      successfulOperations: success,
      failedOperations: failed,
      usageByType: s.stats?.usageByType || {}
    };
  },

  recordFailure() {
    const s = this._load();
    if (!s.stats) s.stats = this._defaults().stats;
    s.stats.failedOperations = (s.stats.failedOperations || 0) + 1;
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
    Toast.show('info', 'Theme Switched', `${next === 'dark' ? 'Dark' : 'Light'} mode activated.`);
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
    title: 'AI Transformer',
    icon: 'ri-magic-line',
    render: (opts) => renderTransformPage(opts?.type),
    afterRender: () => {}
  },
  pipelines: {
    title: 'Pipeline Studio',
    icon: 'ri-flow-chart',
    render: (opts) => renderPipelinesPage(opts),
    afterRender: () => {}
  },
  'saved-pipelines': {
    title: 'Saved Pipelines',
    icon: 'ri-folder-shared-line',
    render: () => renderSavedPipelinesPage(),
    afterRender: () => {}
  },
  history: {
    title: 'Transformation History',
    icon: 'ri-history-line',
    render: () => renderHistoryPage(),
    afterRender: () => {}
  },
  providers: {
    title: 'AI Providers',
    icon: 'ri-cpu-line',
    render: () => renderProvidersPage(),
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
  },
  help: {
    title: 'Help & Support',
    icon: 'ri-question-line',
    render: () => renderHelpPage(),
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
    this.updateNotificationBadge();

    // Sidebar collapse toggle
    const toggleBtn = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    const main = document.getElementById('mainContent');
    if (toggleBtn && sidebar && main) {
      toggleBtn.addEventListener('click', () => {
        sidebar.classList.toggle('collapsed');
        main.classList.toggle('sidebar-collapsed');
      });
    }

    // Mobile drawer menu
    const mobileBtn = document.getElementById('mobileMenuBtn');
    if (mobileBtn && sidebar) {
      mobileBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        sidebar.classList.toggle('mobile-open');
      });
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

    // Topbar Notifications Dropdown
    const notifBtn = document.getElementById('notifBtn');
    const notifDropdown = document.getElementById('notifDropdown');
    if (notifBtn && notifDropdown) {
      notifBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        const isShown = notifDropdown.classList.contains('show');
        this.closeAllDropdowns();
        if (!isShown) {
          this.renderNotificationDropdown();
          notifDropdown.classList.add('show');
          AppState.markNotificationsRead();
        }
      });
    }

    // Topbar Profile Dropdown
    const profileBtn = document.getElementById('profileBtn');
    const profileDropdown = document.getElementById('profileDropdown');
    if (profileBtn && profileDropdown) {
      profileBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        const isShown = profileDropdown.classList.contains('show');
        this.closeAllDropdowns();
        if (!isShown) {
          profileDropdown.classList.add('show');
        }
      });
    }

    // Global click dismiss
    document.addEventListener('click', () => {
      this.closeAllDropdowns();
      sidebar?.classList.remove('mobile-open');
    });

    // Prevent clicks inside dropdowns from closing them
    notifDropdown?.addEventListener('click', e => e.stopPropagation());
    profileDropdown?.addEventListener('click', e => e.stopPropagation());

    // Command Search Shortcut (Cmd+K / Ctrl+K)
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
          const matchOp = Object.values(TRANSFORMATIONS).find(t => t.id.includes(val) || t.label.toLowerCase().includes(val));
          if (matchOp) {
            this.navigateToTransform(matchOp.id);
            Toast.show('info', 'Command Search', `Opened ${matchOp.label}.`);
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

    this.navigate('dashboard');
  },

  closeAllDropdowns() {
    document.getElementById('notifDropdown')?.classList.remove('show');
    document.getElementById('profileDropdown')?.classList.remove('show');
  },

  updateNotificationBadge() {
    const badge = document.getElementById('notifBadge');
    if (!badge) return;
    const count = AppState.getUnreadNotificationCount();
    if (count > 0) {
      badge.style.display = 'flex';
      badge.textContent = count > 9 ? '9+' : count;
    } else {
      badge.style.display = 'none';
    }
  },

  renderNotificationDropdown() {
    const listEl = document.getElementById('notifList');
    if (!listEl) return;
    const notifs = AppState.getNotifications();

    if (notifs.length === 0) {
      listEl.innerHTML = `
        <div class="empty-notif-box">
          <i class="ri-notification-off-line"></i>
          <div>No notifications yet</div>
        </div>
      `;
      return;
    }

    listEl.innerHTML = notifs.map(n => {
      const typeIcons = {
        success: 'ri-checkbox-circle-fill text-green',
        error: 'ri-close-circle-fill text-red',
        info: 'ri-information-fill text-blue'
      };
      const timeAgo = formatTimeAgo(n.time);

      return `
        <div class="notif-item ${!n.read ? 'unread' : ''}">
          <div class="notif-icon"><i class="${typeIcons[n.type] || typeIcons.info}"></i></div>
          <div class="notif-content">
            <div class="notif-title">${escapeHtml(n.title)}</div>
            <div class="notif-msg">${escapeHtml(n.message)}</div>
            <div class="notif-time">${timeAgo}</div>
          </div>
        </div>
      `;
    }).join('');
  },

  navigate(pageId, opts = {}) {
    const page = PAGES[pageId];
    if (!page) return;

    this._currentPage = pageId;

    // Update active nav items
    document.querySelectorAll('.nav-item').forEach(el => {
      el.classList.toggle('active', el.dataset.page === pageId);
    });

    // Update topbar breadcrumbs
    const bcIcon = document.querySelector('.breadcrumb-icon i');
    const bcLabel = document.getElementById('breadcrumbLabel');
    if (bcIcon) bcIcon.className = page.icon;
    if (bcLabel) bcLabel.textContent = page.title;

    // Render into page container
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

function formatTimeAgo(timestamp) {
  if (!timestamp) return 'Just now';
  const diffSec = Math.floor((Date.now() - timestamp) / 1000);
  if (diffSec < 60) return 'Just now';
  if (diffSec < 3600) return `${Math.floor(diffSec / 60)}m ago`;
  if (diffSec < 86400) return `${Math.floor(diffSec / 3600)}h ago`;
  return new Date(timestamp).toLocaleDateString([], { month: 'short', day: 'numeric' });
}

document.addEventListener('DOMContentLoaded', () => App.init());
'''

save_file("js/app.js", APP_JS)
