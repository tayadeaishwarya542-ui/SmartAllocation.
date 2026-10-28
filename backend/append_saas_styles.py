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

css_path = os.path.join(BASE_DIR, "css", "styles.css")
with open(css_path, "r", encoding="utf-8") as f:
    existing_css = f.read()

SAAS_CSS = r'''

/* ================================================================
   TransformAI SaaS Dashboard Enhancements
   ================================================================ */

/* Hero Banner Card */
.dashboard-hero-card {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.12) 0%, rgba(139, 92, 246, 0.06) 100%), var(--bg-surface);
  border: 1px solid rgba(99, 102, 241, 0.25);
  border-radius: var(--radius-xl);
  padding: 32px 36px;
  margin-bottom: 24px;
  position: relative;
  overflow: hidden;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  background: rgba(99, 102, 241, 0.18);
  border: 1px solid rgba(99, 102, 241, 0.35);
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  color: #818cf8;
  margin-bottom: 12px;
}

.hero-title {
  font-size: 28px;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 8px;
  letter-spacing: -0.02em;
}

.hero-subtitle {
  font-size: 14.5px;
  color: var(--text-secondary);
  max-width: 680px;
  line-height: 1.6;
  margin-bottom: 20px;
}

.hero-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.stat-subtext {
  font-size: 11.5px;
  color: var(--text-muted);
  margin-top: 6px;
  display: flex;
  align-items: center;
  gap: 4px;
}

/* Quick Actions Grid */
.quick-actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 16px;
}

.quick-action-card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 22px;
  cursor: pointer;
  transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
}

.quick-action-card:hover {
  border-color: var(--accent-primary);
  transform: translateY(-2px);
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.2);
}

.qa-icon-box {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  margin-bottom: 14px;
}

.qa-icon-box.purple { background: rgba(124, 58, 237, 0.15); color: #c084fc; }
.qa-icon-box.cyan { background: rgba(6, 182, 212, 0.15); color: #67e8f9; }
.qa-icon-box.green { background: rgba(16, 185, 129, 0.15); color: #6ee7b7; }
.qa-icon-box.orange { background: rgba(245, 158, 11, 0.15); color: #fcd34d; }

.qa-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 6px;
}

.qa-desc {
  font-size: 13px;
  color: var(--text-muted);
  line-height: 1.5;
  flex: 1;
  margin-bottom: 14px;
}

.qa-link {
  font-size: 12.5px;
  font-weight: 600;
  color: var(--accent-primary);
  display: flex;
  align-items: center;
  gap: 4px;
}

/* Pipeline Overview Grid */
.pipeline-overview-grid,
.pipeline-library-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 16px;
}

.dashboard-pipeline-card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 20px;
  display: flex;
  flex-direction: column;
  transition: all 0.2s ease;
}

.dashboard-pipeline-card:hover {
  border-color: rgba(99, 102, 241, 0.4);
}

.dash-pipe-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 14px;
}

.dash-pipe-name {
  font-size: 15px;
  font-weight: 700;
  color: var(--text-primary);
}

.dash-pipe-desc {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 2px;
}

.dash-pipe-sequence {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
  padding: 10px 0;
  border-top: 1px solid var(--border-subtle);
  border-bottom: 1px solid var(--border-subtle);
  margin-bottom: 14px;
}

.pipe-seq-chip {
  font-size: 11.5px;
  font-weight: 500;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 2px 7px;
  color: var(--text-secondary);
}

.pipe-seq-arrow {
  color: var(--text-muted);
  font-size: 13px;
}

.dash-pipe-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: auto;
  gap: 8px;
  flex-wrap: wrap;
}

.dash-pipe-meta {
  font-size: 11.5px;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 4px;
}

.dash-pipe-actions {
  display: flex;
  align-items: center;
  gap: 6px;
}

.icon-btn-xs {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 4px;
  color: var(--text-primary);
  font-size: 13px;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.15s;
}

.icon-btn-xs:hover {
  border-color: var(--accent-primary);
  color: var(--accent-primary);
}

.icon-btn-xs.btn-delete:hover {
  border-color: #f87171;
  color: #f87171;
}

/* Recent Activity SaaS Table Card */
.recent-table-card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.recent-table-header {
  display: grid;
  grid-template-columns: 140px 1fr 140px 100px 90px 110px;
  padding: 12px 18px;
  background: var(--bg-card);
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
  border-bottom: 1px solid var(--border);
}

.recent-table-row {
  display: grid;
  grid-template-columns: 140px 1fr 140px 100px 90px 110px;
  padding: 14px 18px;
  border-bottom: 1px solid var(--border-subtle);
  align-items: center;
  font-size: 13px;
  color: var(--text-primary);
  transition: background 0.15s;
}

.recent-table-row:hover {
  background: rgba(255, 255, 255, 0.02);
}

.input-cell-text {
  color: var(--text-secondary);
  font-size: 12.5px;
}

.provider-pill {
  font-size: 11px;
  background: var(--bg-elevated);
  padding: 2px 7px;
  border-radius: 4px;
  color: var(--text-muted);
}

.status-pill {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 11.5px;
  font-weight: 600;
}

.status-pill.success {
  color: #34d399;
}

/* Empty State Box */
.empty-state-box {
  background: var(--bg-surface);
  border: 1px dashed var(--border);
  border-radius: var(--radius-lg);
  padding: 36px 24px;
  text-align: center;
  color: var(--text-muted);
}

.empty-state-box i {
  font-size: 38px;
  color: var(--accent-primary);
  opacity: 0.8;
  margin-bottom: 8px;
  display: inline-block;
}

.empty-state-title {
  font-size: 15px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.empty-state-desc {
  font-size: 13px;
  color: var(--text-muted);
  max-width: 480px;
  margin: 0 auto;
}

/* Topbar Dropdowns */
.topbar-dropdown-anchor {
  position: relative;
}

.notif-badge-count {
  position: absolute;
  top: -2px;
  right: -2px;
  background: #f43f5e;
  color: #ffffff;
  font-size: 10px;
  font-weight: 800;
  width: 17px;
  height: 17px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid var(--bg-base);
}

.notif-dropdown-menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  width: 320px;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: 0 16px 36px rgba(0, 0, 0, 0.45);
  display: none;
  flex-direction: column;
  z-index: 1000;
}

.notif-dropdown-menu.show {
  display: flex;
  animation: pageIn 0.2s ease;
}

.notif-dropdown-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-bottom: 1px solid var(--border);
  font-size: 13px;
  font-weight: 700;
  color: var(--text-primary);
}

.notif-dropdown-list {
  max-height: 300px;
  overflow-y: auto;
}

.notif-item {
  display: flex;
  gap: 12px;
  padding: 12px 16px;
  border-bottom: 1px solid var(--border-subtle);
  transition: background 0.15s;
}

.notif-item:hover {
  background: var(--bg-card);
}

.notif-item.unread {
  background: rgba(99, 102, 241, 0.05);
}

.notif-icon {
  font-size: 18px;
  margin-top: 1px;
}

.notif-title {
  font-size: 12.5px;
  font-weight: 600;
  color: var(--text-primary);
}

.notif-msg {
  font-size: 11.5px;
  color: var(--text-muted);
  line-height: 1.4;
  margin-top: 2px;
}

.notif-time {
  font-size: 10.5px;
  color: var(--text-muted);
  margin-top: 4px;
}

.empty-notif-box {
  text-align: center;
  padding: 24px;
  color: var(--text-muted);
  font-size: 12px;
}

.profile-dropdown-menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  width: 220px;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: 0 16px 36px rgba(0, 0, 0, 0.45);
  display: none;
  flex-direction: column;
  z-index: 1000;
  padding: 8px 0;
}

.profile-dropdown-menu.show {
  display: flex;
  animation: pageIn 0.2s ease;
}

.profile-menu-header {
  padding: 10px 16px 8px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 4px;
}

.profile-name {
  font-size: 13px;
  font-weight: 700;
  color: var(--text-primary);
}

.profile-sub {
  font-size: 11px;
  color: var(--text-muted);
}

.profile-dropdown-menu a {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  font-size: 13px;
  color: var(--text-secondary);
  text-decoration: none;
  transition: all 0.15s;
}

.profile-dropdown-menu a:hover {
  background: var(--bg-elevated);
  color: var(--text-primary);
}

.dropdown-divider {
  height: 1px;
  background: var(--border);
  margin: 6px 0;
}

.pipeline-meta-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 20px;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  margin-bottom: 18px;
  flex-wrap: wrap;
  gap: 12px;
}

/* Responsive Table */
@media (max-width: 900px) {
  .recent-table-header {
    display: none;
  }
  .recent-table-row {
    grid-template-columns: 1fr;
    gap: 8px;
    padding: 16px;
  }
}
'''

full_css = existing_css + SAAS_CSS
save_file("css/styles.css", full_css)
