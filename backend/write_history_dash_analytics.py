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

# --- pages/history.js ---
HISTORY_JS = r'''// ================================================================
//  History Page — Filter, Search, Reopen, and Export
// ================================================================

let _historyFilterType = '';
let _historySearchQuery = '';

function renderHistoryPage() {
  const history = AppState.getHistory();

  return `
  <div class="page-view">
    <div class="page-header">
      <div class="page-header-top">
        <div>
          <div class="page-title">Transformation History <span class="grad-text">✦</span></div>
          <div class="page-desc">Every transformation and pipeline result is securely persisted in your browser.</div>
        </div>
        <div class="flex gap-2 items-center flex-wrap">
          <button class="btn btn-secondary btn-sm" onclick="HistoryPage.exportCSV()">
            <i class="ri-file-excel-2-line"></i> Export CSV
          </button>
          <button class="btn btn-secondary btn-sm" onclick="HistoryPage.exportJSON()">
            <i class="ri-code-s-slash-line"></i> Export JSON
          </button>
          <button class="btn btn-danger btn-sm" onclick="HistoryPage.clearAll()">
            <i class="ri-delete-bin-line"></i> Clear All History
          </button>
        </div>
      </div>
    </div>

    <!-- Filter & Search Bar -->
    <div class="history-filter-bar">
      <div class="search-bar" style="flex:1;min-width:240px;">
        <i class="ri-search-line"></i>
        <input type="text" placeholder="Search inputs, outputs, models..." id="historySearchInput" oninput="HistoryPage.onSearch(this.value)" />
      </div>
      <select class="form-select" id="historyTypeFilter" onchange="HistoryPage.onFilter(this.value)" style="width:auto;min-width:180px;">
        <option value="">All Transformation Types</option>
        ${Object.keys(TRANSFORMATIONS).map(k => `
          <option value="${k}">${TRANSFORMATIONS[k].label}</option>
        `).join('')}
        <option value="pipeline">Sequential Pipeline</option>
      </select>
    </div>

    <!-- History Items Container -->
    <div class="history-list" id="historyListContainer">
      ${renderHistoryItemsHtml()}
    </div>
  </div>`;
}

function renderHistoryItemsHtml() {
  let items = AppState.getHistory();

  if (_historyFilterType) {
    items = items.filter(i => i.type === _historyFilterType);
  }
  if (_historySearchQuery) {
    const q = _historySearchQuery.toLowerCase();
    items = items.filter(i =>
      (i.input && i.input.toLowerCase().includes(q)) ||
      (i.output && i.output.toLowerCase().includes(q)) ||
      (i.type && i.type.toLowerCase().includes(q)) ||
      (i.model && i.model.toLowerCase().includes(q))
    );
  }

  if (items.length === 0) {
    return `
      <div class="empty-history-box">
        <i class="ri-history-line"></i>
        <div>No history records found</div>
        <div style="font-size:12px;color:var(--text-muted);margin-top:4px;">Transformations you execute will appear here automatically.</div>
      </div>
    `;
  }

  return items.map((item, idx) => {
    const def = TRANSFORMATIONS[item.type] || { label: capitalize(item.type), icon: 'ri-magic-line' };
    const dateStr = new Date(item.timestamp).toLocaleString();
    const inWords = wordCount(item.input);
    const outWords = wordCount(item.output);

    return `
      <div class="history-item-card">
        <div class="history-card-header">
          <div class="flex items-center gap-2">
            <span class="badge badge-purple"><i class="${def.icon}"></i> ${def.label}</span>
            <span class="history-meta-tag"><i class="ri-time-line"></i> ${dateStr}</span>
            <span class="history-meta-tag">${item.model || 'local'}</span>
            <span class="history-meta-tag">${inWords} → ${outWords} words</span>
          </div>
          <div class="history-item-actions">
            <button class="icon-btn-sm" onclick="HistoryPage.reopen(${idx})" title="Open in Transform Studio"><i class="ri-external-link-line"></i> Reopen</button>
            <button class="icon-btn-sm" onclick="HistoryPage.copyItem(${idx})" title="Copy output"><i class="ri-file-copy-line"></i></button>
            <button class="icon-btn-sm btn-delete" onclick="HistoryPage.deleteItem(${idx})" title="Delete"><i class="ri-delete-bin-line"></i></button>
          </div>
        </div>

        <div class="history-card-body">
          <div class="history-snippet input-snip">
            <strong>Input:</strong> ${escapeHtml(item.input ? item.input.slice(0, 160) : '')}${item.input && item.input.length > 160 ? '...' : ''}
          </div>
          <div class="history-snippet output-snip">
            <strong>Output:</strong> ${escapeHtml(item.output ? item.output.slice(0, 200) : '')}${item.output && item.output.length > 200 ? '...' : ''}
          </div>
        </div>
      </div>
    `;
  }).join('');
}

const HistoryPage = {
  onSearch(query) {
    _historySearchQuery = query;
    const c = document.getElementById('historyListContainer');
    if (c) c.innerHTML = renderHistoryItemsHtml();
  },

  onFilter(type) {
    _historyFilterType = type;
    const c = document.getElementById('historyListContainer');
    if (c) c.innerHTML = renderHistoryItemsHtml();
  },

  reopen(idx) {
    const items = AppState.getHistory();
    const item = items[idx];
    if (!item) return;

    if (item.type === 'pipeline') {
      App.navigate('pipelines');
      setTimeout(() => {
        const inp = document.getElementById('pipelineInputText');
        if (inp) {
          inp.value = item.input || '';
          PipelinesPage.updateInputWC();
          Toast.show('info', 'Loaded Pipeline', 'History item loaded into Pipeline Initial Content.');
        }
      }, 200);
      return;
    }

    App.navigate('transform', { type: item.type });
    setTimeout(() => {
      const inp = document.getElementById('inputContent');
      if (inp) {
        inp.value = item.input || '';
        TransformPage.updateWordCount();
      }
      if (item.output) {
        TransformPage.renderFormattedOutput(item.output);
        _outputText = item.output;
        const act = document.getElementById('outputActions');
        if (act) act.style.display = 'flex';
        const pl = document.getElementById('outputPlaceholder');
        if (pl) pl.style.display = 'none';
        const ot = document.getElementById('outputText');
        if (ot) ot.style.display = 'block';
      }
      Toast.show('info', 'Record Restored', `Restored ${TRANSFORMATIONS[item.type]?.label || item.type} session.`);
    }, 250);
  },

  async copyItem(idx) {
    const items = AppState.getHistory();
    const item = items[idx];
    if (!item || !item.output) return;
    try {
      await navigator.clipboard.writeText(item.output);
      Toast.show('success', 'Copied!', 'Item output copied to clipboard.');
    } catch {
      Toast.show('error', 'Copy Failed', 'Unable to write to clipboard.');
    }
  },

  deleteItem(idx) {
    AppState.deleteHistoryItem(idx);
    const c = document.getElementById('historyListContainer');
    if (c) c.innerHTML = renderHistoryItemsHtml();
    Toast.show('success', 'Item Deleted', 'History record removed.');
  },

  clearAll() {
    if (!confirm('Are you sure you want to delete all transformation history?')) return;
    AppState.clearHistory();
    const c = document.getElementById('historyListContainer');
    if (c) c.innerHTML = renderHistoryItemsHtml();
    Toast.show('success', 'History Cleared', 'All transformation history has been cleared.');
  },

  exportCSV() {
    const items = AppState.getHistory();
    if (items.length === 0) {
      Toast.show('warning', 'No Records', 'History is empty.');
      return;
    }

    let csv = 'ID,Timestamp,Type,Model,InputWordCount,OutputWordCount,Input,Output\n';
    items.forEach((item, idx) => {
      const date = new Date(item.timestamp).toISOString();
      const inW = wordCount(item.input);
      const outW = wordCount(item.output);
      const cleanIn = (item.input || '').replace(/"/g, '""').replace(/\n/g, ' ');
      const cleanOut = (item.output || '').replace(/"/g, '""').replace(/\n/g, ' ');
      csv += `"${idx + 1}","${date}","${item.type}","${item.model || 'local'}","${inW}","${outW}","${cleanIn}","${cleanOut}"\n`;
    });

    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `transformai-history-${Date.now()}.csv`;
    a.click();
    Toast.show('success', 'CSV Exported', 'Downloaded transformation history as CSV.');
  },

  exportJSON() {
    const items = AppState.getHistory();
    if (items.length === 0) {
      Toast.show('warning', 'No Records', 'History is empty.');
      return;
    }

    const blob = new Blob([JSON.stringify(items, null, 2)], { type: 'application/json;charset=utf-8' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `transformai-history-${Date.now()}.json`;
    a.click();
    Toast.show('success', 'JSON Exported', 'Downloaded transformation history as JSON.');
  }
};
'''

# --- pages/dashboard.js ---
DASHBOARD_JS = r'''// ================================================================
//  Dashboard Page — Operational Metrics & Quick Launch Grid
// ================================================================

function renderDashboard() {
  const stats = AppState.getStats();
  const history = AppState.getHistory();
  const provider = API.getProvider();

  return `
  <div class="page-view">
    <div class="page-header">
      <div class="page-header-top">
        <div>
          <div class="page-title">Welcome to TransformAI <span class="grad-text">✦</span></div>
          <div class="page-desc">Automated content transformation platform with verified multi-provider intelligence.</div>
        </div>
        <div class="flex gap-2">
          <button class="btn btn-secondary btn-sm" onclick="App.navigate('pipelines')">
            <i class="ri-flow-chart"></i> Pipeline Studio
          </button>
          <button class="btn btn-primary btn-sm" onclick="App.navigate('transform')">
            <i class="ri-magic-line"></i> New Transform
          </button>
        </div>
      </div>
    </div>

    <!-- Live Telemetry Stats Grid -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon purple"><i class="ri-magic-line"></i></div>
        <div class="stat-value">${stats.totalTransforms}</div>
        <div class="stat-label">Total Transformations</div>
        <div class="stat-change up"><i class="ri-arrow-up-line"></i> Live Local DB</div>
      </div>

      <div class="stat-card">
        <div class="stat-icon cyan"><i class="ri-file-text-line"></i></div>
        <div class="stat-value">${stats.wordsProcessed.toLocaleString()}</div>
        <div class="stat-label">Words Processed</div>
        <div class="stat-change up"><i class="ri-speed-up-line"></i> High Throughput</div>
      </div>

      <div class="stat-card">
        <div class="stat-icon green"><i class="ri-translate-2"></i></div>
        <div class="stat-value">${stats.languagesUsed || 7}</div>
        <div class="stat-label">Languages Supported</div>
        <div class="stat-change up"><i class="ri-global-line"></i> Multilingual Polyglot</div>
      </div>

      <div class="stat-card">
        <div class="stat-icon orange"><i class="ri-time-line"></i></div>
        <div class="stat-value">${Math.max(stats.timeSaved, 0.5)} hrs</div>
        <div class="stat-label">Estimated Time Saved</div>
        <div class="stat-change up"><i class="ri-sparkling-fill"></i> Accelerated Delivery</div>
      </div>
    </div>

    <!-- 8 Transformation Operations Quick Launch -->
    <div class="section-header" style="margin-top:30px;">
      <div class="section-title"><i class="ri-apps-2-line"></i> 8 Core Transformation Engines</div>
      <button class="btn btn-secondary btn-xs" onclick="App.navigate('transform')">View All</button>
    </div>

    <div class="dashboard-ops-grid">
      ${getTransformationTypes().map(t => `
        <div class="dash-op-card" onclick="App.navigateToTransform('${t.id}')">
          <div class="dash-op-icon"><i class="${t.icon}"></i></div>
          <div class="dash-op-content">
            <div class="dash-op-name">${t.label}</div>
            <div class="dash-op-desc">${t.desc}</div>
          </div>
          <div class="dash-op-arrow"><i class="ri-arrow-right-line"></i></div>
        </div>
      `).join('')}
    </div>

    <!-- Preset Pipelines Showcase -->
    <div class="section-header" style="margin-top:30px;">
      <div class="section-title"><i class="ri-flow-chart"></i> Ready-to-Run Pipelines</div>
      <button class="btn btn-secondary btn-xs" onclick="App.navigate('pipelines')">Open Studio</button>
    </div>

    <div class="presets-row" style="margin-bottom:30px;">
      ${PIPELINE_PRESETS.map(p => `
        <div class="pipeline-card" onclick="App.navigate('pipelines'); setTimeout(() => PipelinesPage.loadPreset('${p.id}'), 200);" style="cursor:pointer;flex:1;min-width:260px;">
          <div class="flex items-center gap-3 mb-2">
            <div class="pipeline-icon" style="background:rgba(124,58,237,0.15);color:#c084fc;">
              <i class="${p.icon}"></i>
            </div>
            <div>
              <div class="pipeline-name">${p.name}</div>
              <div class="pipeline-desc">${p.desc}</div>
            </div>
          </div>
          <div class="pipeline-steps">
            ${p.stages.map(s => `<span class="pipeline-step-chip">${TRANSFORMATIONS[s.type]?.label || s.type}</span>`).join(' <i class="ri-arrow-right-s-line" style="color:var(--text-muted)"></i> ')}
          </div>
        </div>
      `).join('')}
    </div>

    <!-- Recent Activity -->
    <div class="section-header">
      <div class="section-title"><i class="ri-history-line"></i> Recent Activity</div>
      <button class="btn btn-secondary btn-xs" onclick="App.navigate('history')">Full History</button>
    </div>

    <div class="recent-activity-card">
      ${history.length === 0 ? `
        <div class="p-6 text-center text-muted" style="color:var(--text-muted);">
          No transformations executed yet. Click "New Transform" to get started!
        </div>
      ` : `
        <div class="recent-list">
          ${history.slice(0, 5).map(h => `
            <div class="recent-row" onclick="App.navigate('history')" style="cursor:pointer;">
              <div class="flex items-center gap-3">
                <span class="badge badge-purple">${h.type}</span>
                <span style="font-size:13px;color:var(--text-secondary);">${escapeHtml(h.input ? h.input.slice(0, 70) : '')}...</span>
              </div>
              <div class="flex items-center gap-4">
                <span style="font-size:12px;color:var(--text-muted);">${wordCount(h.output)} words</span>
                <span style="font-size:12px;color:var(--text-muted);">${new Date(h.timestamp).toLocaleTimeString([], { hour:'2-digit', minute:'2-digit' })}</span>
              </div>
            </div>
          `).join('')}
        </div>
      `}
    </div>

  </div>`;
}
'''

# --- pages/analytics.js ---
ANALYTICS_JS = r'''// ================================================================
//  Analytics Page — Transformation Metrics & Volume Insights
// ================================================================

function renderAnalyticsPage() {
  const history = AppState.getHistory();
  const stats   = AppState.getStats();

  const typeCounts = {};
  history.forEach(item => { typeCounts[item.type] = (typeCounts[item.type] || 0) + 1; });

  const total = Math.max(history.length, 1);

  return `
  <div class="page-view">
    <div class="page-header">
      <div class="page-header-top">
        <div>
          <div class="page-title">Analytics & Intelligence Telemetry <span class="grad-text">✦</span></div>
          <div class="page-desc">Comprehensive monitoring of content throughput, operation distribution, and efficiency.</div>
        </div>
        <span class="badge badge-green"><i class="ri-checkbox-circle-fill"></i> Live Local Metrics</span>
      </div>
    </div>

    <!-- Top Stats -->
    <div class="stats-grid" style="margin-bottom:24px">
      <div class="stat-card">
        <div class="stat-icon purple"><i class="ri-bar-chart-2-line"></i></div>
        <div class="stat-value">${history.length}</div>
        <div class="stat-label">Total Records</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon cyan"><i class="ri-file-word-line"></i></div>
        <div class="stat-value">${stats.wordsProcessed.toLocaleString()}</div>
        <div class="stat-label">Total Words Processed</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon green"><i class="ri-dashboard-3-line"></i></div>
        <div class="stat-value">${Object.keys(typeCounts).length}</div>
        <div class="stat-label">Operations Used</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon orange"><i class="ri-timer-line"></i></div>
        <div class="stat-value">${Math.max(stats.timeSaved, 0.5)} hrs</div>
        <div class="stat-label">Production Time Saved</div>
      </div>
    </div>

    <!-- Operation Distribution Breakdown -->
    <div class="settings-card full-width">
      <div class="settings-card-header">
        <div class="settings-card-title"><i class="ri-pie-chart-line" style="color:var(--accent-primary)"></i> Operation Distribution</div>
        <div class="settings-card-desc">Volume of transformations segmented by individual operation.</div>
      </div>
      <div class="settings-card-body">
        <div class="quality-metrics-grid">
          ${getTransformationTypes().map(t => {
            const count = typeCounts[t.id] || 0;
            const pct = Math.round((count / total) * 100);
            return `
              <div class="metric-row">
                <div class="metric-label">
                  <span><i class="${t.icon}"></i> ${t.label}</span>
                  <span class="metric-val">${count} runs (${pct}%)</span>
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

  </div>`;
}
'''

save_file("pages/history.js", HISTORY_JS)
save_file("pages/dashboard.js", DASHBOARD_JS)
save_file("pages/analytics.js", ANALYTICS_JS)
