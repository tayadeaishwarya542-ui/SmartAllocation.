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

# Append complete modern styling to styles.css
css_path = os.path.join(BASE_DIR, "css", "styles.css")
with open(css_path, "r", encoding="utf-8") as f:
    existing_css = f.read()

ADDITIONAL_CSS = r'''

/* ================================================================
   TransformAI — Master Extensions (Light Theme, Diff, Pipelines, Quality)
   ================================================================ */

/* Light Theme Variables */
[data-theme="light"] {
  --bg-base: #f8fafc;
  --bg-surface: #ffffff;
  --bg-card: #f1f5f9;
  --bg-elevated: #e2e8f0;
  --text-primary: #0f172a;
  --text-secondary: #334155;
  --text-muted: #64748b;
  --border: #e2e8f0;
  --border-subtle: #f1f5f9;
  --input-bg: #ffffff;
}

[data-theme="light"] .ambient-bg .blob {
  opacity: 0.15;
}

[data-theme="light"] .sidebar {
  background: #ffffff;
  border-right-color: #e2e8f0;
}

[data-theme="light"] .topbar {
  background: rgba(255, 255, 255, 0.85);
  border-bottom-color: #e2e8f0;
}

[data-theme="light"] .transform-type-btn {
  background: #ffffff;
  border-color: #e2e8f0;
  color: #334155;
}

[data-theme="light"] .transform-type-btn.selected {
  background: rgba(124, 58, 237, 0.08);
  border-color: #7c3aed;
  color: #7c3aed;
}

[data-theme="light"] .editor-panel {
  background: #ffffff;
  border-color: #e2e8f0;
}

[data-theme="light"] .settings-card,
[data-theme="light"] .pipeline-card,
[data-theme="light"] .stat-card {
  background: #ffffff;
  border-color: #e2e8f0;
}

/* Grammar Diff Highlighting */
.diff-view {
  line-height: 1.85;
  font-size: 14.5px;
}

.diff-del {
  background: rgba(239, 68, 68, 0.22);
  color: #f87171;
  text-decoration: line-through;
  padding: 2px 6px;
  border-radius: 4px;
  margin: 0 2px;
  display: inline-block;
}

.diff-ins {
  background: rgba(52, 211, 153, 0.22);
  color: #34d399;
  text-decoration: none;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 4px;
  margin: 0 2px;
  display: inline-block;
}

/* Output Tabs */
.output-tabs-bar {
  display: flex;
  gap: 8px;
  padding: 8px 16px;
  background: var(--bg-card);
  border-bottom: 1px solid var(--border);
}

.output-tab {
  background: none;
  border: none;
  padding: 6px 14px;
  border-radius: var(--radius-sm);
  font-size: 13px;
  font-weight: 500;
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.2s;
}

.output-tab.active {
  background: var(--bg-elevated);
  color: var(--text-primary);
  font-weight: 600;
}

.output-tab:hover {
  color: var(--text-primary);
}

/* Quality Scoring Visual Card */
.quality-report-card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 24px;
}

.quality-top-row {
  display: flex;
  align-items: center;
  gap: 24px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.quality-gauge {
  width: 96px;
  height: 96px;
  border-radius: 50%;
  border: 5px solid var(--accent-primary);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(124, 58, 237, 0.06);
  flex-shrink: 0;
}

.quality-gauge-score {
  font-size: 32px;
  font-weight: 900;
  line-height: 1;
}

.quality-gauge-label {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 2px;
}

.quality-summary-info {
  flex: 1;
  min-width: 240px;
}

.quality-explanation {
  font-size: 13.5px;
  line-height: 1.6;
  color: var(--text-secondary);
  margin-top: 10px;
}

.quality-metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}

.metric-row {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.metric-label {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
}

.metric-bar-bg {
  width: 100%;
  height: 8px;
  background: var(--bg-elevated);
  border-radius: 4px;
  overflow: hidden;
}

.metric-bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s ease;
}

.quality-suggestions {
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 16px;
}

.suggestions-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.quality-suggestions ul {
  margin: 0;
  padding-left: 20px;
  font-size: 13px;
  line-height: 1.6;
  color: var(--text-secondary);
}

/* JSON Badges & Pre */
.json-header-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  background: rgba(52, 211, 153, 0.15);
  border: 1px solid rgba(52, 211, 153, 0.3);
  border-radius: var(--radius-sm);
  color: #34d399;
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 12px;
}

.code-block {
  font-family: 'Fira Code', 'Courier New', monospace;
  font-size: 13px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 16px;
  overflow-x: auto;
  color: var(--text-primary);
}

/* Dropdown Menu */
.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
  min-width: 190px;
  z-index: 100;
  padding: 6px 0;
  margin-top: 6px;
}

.dropdown-menu a {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  color: var(--text-primary);
  text-decoration: none;
  font-size: 13px;
  transition: background 0.15s;
}

.dropdown-menu a:hover {
  background: var(--bg-elevated);
}

/* Pipeline Studio */
.pipeline-presets-bar {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 18px 24px;
  margin-bottom: 20px;
}

.presets-row {
  display: flex;
  gap: 10px;
  overflow-x: auto;
  padding-bottom: 4px;
}

.preset-chip {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 8px 14px;
  color: var(--text-primary);
  font-size: 13px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s;
}

.preset-chip:hover {
  border-color: var(--accent-primary);
  background: rgba(124, 58, 237, 0.1);
}

.pipeline-input-card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 20px 24px;
  margin-bottom: 20px;
}

.pipeline-builder-card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 24px;
  margin-bottom: 24px;
}

.pipeline-builder-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 12px;
}

.builder-title {
  font-size: 17px;
  font-weight: 700;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 8px;
}

.builder-desc {
  font-size: 12.5px;
  color: var(--text-muted);
  margin-top: 3px;
}

.pipeline-stage-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 18px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  margin-bottom: 12px;
  gap: 16px;
  flex-wrap: wrap;
  transition: all 0.2s ease;
}

.pipeline-stage-item.stage-running {
  border-color: #fbbf24;
  box-shadow: 0 0 12px rgba(251, 191, 36, 0.2);
}

.pipeline-stage-item.stage-completed {
  border-color: #34d399;
}

.pipeline-stage-item.stage-failed {
  border-color: #f87171;
  background: rgba(248, 113, 113, 0.05);
}

.pipeline-stage-item.stage-disabled {
  opacity: 0.55;
}

.stage-item-left {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
  min-width: 240px;
}

.stage-index-badge {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  color: var(--text-secondary);
}

.stage-icon-circle {
  width: 34px;
  height: 34px;
  border-radius: 8px;
  background: rgba(124, 58, 237, 0.15);
  color: #c084fc;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}

.stage-main-meta {
  display: flex;
  flex-direction: column;
}

.stage-title-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.stage-type-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.stage-words-tag {
  font-size: 11px;
  color: #34d399;
  background: rgba(52, 211, 153, 0.1);
  padding: 1px 6px;
  border-radius: 4px;
}

.stage-desc-row {
  font-size: 11.5px;
  color: var(--text-muted);
  margin-top: 2px;
}

.stage-options-inline {
  display: flex;
  gap: 8px;
  align-items: center;
}

.stage-item-actions {
  display: flex;
  gap: 6px;
  align-items: center;
}

.pipeline-results-card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 24px;
  margin-bottom: 24px;
}

.pipeline-results-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 10px;
}

.pipeline-output-tabs {
  display: flex;
  gap: 8px;
  border-bottom: 1px solid var(--border);
  padding-bottom: 12px;
  margin-bottom: 16px;
  overflow-x: auto;
}

.formatted-output-box {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 20px;
  font-size: 14px;
  line-height: 1.7;
  color: var(--text-primary);
  max-height: 500px;
  overflow-y: auto;
}

.stage-error-banner {
  width: 100%;
  margin-top: 8px;
  padding: 8px 12px;
  background: rgba(248, 113, 113, 0.1);
  border: 1px solid rgba(248, 113, 113, 0.3);
  border-radius: var(--radius-sm);
  color: #f87171;
  font-size: 12.5px;
  display: flex;
  align-items: center;
  gap: 6px;
}

/* Modals */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(8px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-box {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  width: 90%;
  max-width: 640px;
  padding: 24px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
}

.modal-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
}

.add-stage-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 10px;
  max-height: 420px;
  overflow-y: auto;
}

.add-stage-option {
  display: flex;
  gap: 12px;
  padding: 12px;
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  cursor: pointer;
  background: var(--bg-card);
  transition: all 0.2s;
}

.add-stage-option:hover {
  border-color: var(--accent-primary);
  background: rgba(124, 58, 237, 0.08);
}

.stage-opt-icon {
  font-size: 20px;
  color: var(--accent-primary);
}

.stage-opt-name {
  font-size: 13.5px;
  font-weight: 600;
  color: var(--text-primary);
}

.stage-opt-desc {
  font-size: 11.5px;
  color: var(--text-muted);
  margin-top: 2px;
}

/* Provider Selection Cards */
.provider-cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 14px;
}

.provider-card {
  padding: 16px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s;
}

.provider-card:hover {
  border-color: var(--accent-primary);
}

.provider-card.active {
  border-color: var(--accent-primary);
  background: rgba(124, 58, 237, 0.08);
  box-shadow: 0 0 12px rgba(124, 58, 237, 0.15);
}

.provider-card-name {
  font-size: 14.5px;
  font-weight: 700;
  color: var(--text-primary);
}

.provider-card-desc {
  font-size: 12px;
  color: var(--text-muted);
  line-height: 1.5;
}

/* Dashboard Ops Grid */
.dashboard-ops-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 14px;
}

.dash-op-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s;
}

.dash-op-card:hover {
  border-color: var(--accent-primary);
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.2);
}

.dash-op-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: rgba(124, 58, 237, 0.12);
  color: #c084fc;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
}

.dash-op-content {
  flex: 1;
}

.dash-op-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.dash-op-desc {
  font-size: 11.5px;
  color: var(--text-muted);
  margin-top: 2px;
}

.dash-op-arrow {
  color: var(--text-muted);
  font-size: 16px;
  transition: transform 0.2s;
}

.dash-op-card:hover .dash-op-arrow {
  color: var(--accent-primary);
  transform: translateX(3px);
}

/* History Cards */
.history-filter-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.history-item-card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 16px;
  margin-bottom: 12px;
  transition: all 0.2s;
}

.history-item-card:hover {
  border-color: rgba(124, 58, 237, 0.4);
}

.history-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
  flex-wrap: wrap;
  gap: 8px;
}

.history-meta-tag {
  font-size: 12px;
  color: var(--text-muted);
}

.history-card-body {
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 13px;
  color: var(--text-secondary);
}

.history-snippet {
  line-height: 1.5;
}

.history-snippet.input-snip {
  color: var(--text-muted);
}

.icon-btn-sm {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  color: var(--text-primary);
  font-size: 12px;
  padding: 4px 8px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.icon-btn-sm:hover {
  border-color: var(--accent-primary);
}

.icon-btn-sm.btn-delete:hover {
  border-color: #f87171;
  color: #f87171;
}

.empty-history-box,
.empty-stages-box {
  text-align: center;
  padding: 40px;
  color: var(--text-muted);
  font-size: 14px;
}

.empty-history-box i,
.empty-stages-box i {
  font-size: 36px;
  display: block;
  margin-bottom: 8px;
  opacity: 0.6;
}

.spinner {
  animation: spin 1s linear infinite;
  display: inline-block;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
'''

full_css = existing_css + ADDITIONAL_CSS
save_file("css/styles.css", full_css)
