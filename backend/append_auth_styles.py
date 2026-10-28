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

AUTH_CSS = """
/* ════════════════════════════════════════════════════════════════
   TransformAI — Authentication, User Session & Security Styles
   ════════════════════════════════════════════════════════════════ */

/* ── 1. Topbar & Header Auth Actions ── */
.topbar-auth-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-avatar.auth-logged-in {
  background: var(--accent-grad);
  color: #fff;
  font-weight: 700;
  border: 1px solid rgba(255, 255, 255, 0.25);
  box-shadow: 0 0 16px rgba(124, 58, 237, 0.4);
}

.user-avatar.auth-guest {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  color: var(--text-secondary);
}

.profile-badge-pill {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  margin-top: 6px;
  padding: 3px 8px;
  background: rgba(16, 185, 129, 0.12);
  border: 1px solid rgba(16, 185, 129, 0.25);
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  color: #6ee7b7;
}

.profile-logout-link {
  color: #f87171 !important;
  font-weight: 600;
}
.profile-logout-link:hover {
  background: rgba(239, 68, 68, 0.15) !important;
  color: #fca5a5 !important;
}

/* ── 2. Sidebar User Pill ── */
.sidebar-user-pill {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  margin-bottom: 12px;
}

.sidebar-user-info {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.sidebar-user-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sidebar-user-role {
  font-size: 11px;
  color: var(--text-secondary);
}

.sidebar-logout-btn, .sidebar-login-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  color: var(--text-secondary);
  transition: all 0.2s ease;
}

.sidebar-logout-btn:hover {
  background: rgba(239, 68, 68, 0.2);
  border-color: rgba(239, 68, 68, 0.4);
  color: #fca5a5;
}

.sidebar-login-btn:hover {
  background: var(--accent-1);
  color: #fff;
}

/* ── 3. Auth Page Container & Layout ── */
.auth-page-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 120px);
  padding: 40px 20px;
}

.auth-container {
  width: 100%;
  max-width: 480px;
  display: flex;
  flex-direction: column;
  align-items: center;
  animation: authFadeIn 0.35s ease-out;
}

@keyframes authFadeIn {
  from { opacity: 0; transform: translateY(16px); }
  to { opacity: 1; transform: translateY(0); }
}

.auth-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
  text-align: center;
}

.auth-brand-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: var(--accent-grad);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: #fff;
  box-shadow: 0 4px 20px rgba(124, 58, 237, 0.5);
}

.auth-brand-text {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.auth-brand-name {
  font-size: 22px;
  font-weight: 800;
  letter-spacing: -0.5px;
  background: var(--accent-grad);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.auth-brand-badge {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.8px;
}

/* ── 4. Main Auth Card ── */
.auth-card {
  width: 100%;
  background: rgba(15, 23, 42, 0.75);
  backdrop-filter: blur(28px);
  -webkit-backdrop-filter: blur(28px);
  border: 1px solid var(--border-strong);
  border-radius: var(--radius-lg);
  padding: 34px 30px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.6), 0 0 40px rgba(124, 58, 237, 0.15);
}

[data-theme="light"] .auth-card {
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.08), 0 0 30px rgba(124, 58, 237, 0.1);
}

/* Tab Segment Switcher */
.auth-tabs {
  display: flex;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 4px;
  margin-bottom: 24px;
}

.auth-tab {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 9px 14px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
  background: transparent;
  transition: all 0.2s ease;
}

.auth-tab.active {
  background: var(--accent-grad);
  color: #fff;
  box-shadow: 0 2px 10px rgba(124, 58, 237, 0.35);
}

.auth-tab:not(.active):hover {
  color: var(--text-primary);
  background: var(--bg-hover);
}

.auth-card-header {
  margin-bottom: 22px;
  text-align: left;
}

.auth-title {
  font-size: 22px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.3px;
  margin-bottom: 6px;
}

.auth-subtitle {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
}

/* ── 5. Form Elements & Inputs ── */
.auth-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.auth-input-icon {
  position: absolute;
  left: 14px;
  font-size: 18px;
  color: var(--text-muted);
  pointer-events: none;
  transition: color 0.2s;
}

.auth-input {
  padding-left: 42px !important;
  padding-right: 44px !important;
  height: 46px;
  font-size: 14px;
}

.auth-input:focus + .auth-input-icon,
.auth-input-wrapper:focus-within .auth-input-icon {
  color: var(--accent-1);
}

.auth-input-toggle {
  position: absolute;
  right: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 6px;
  color: var(--text-muted);
  background: transparent;
  transition: all 0.2s;
}

.auth-input-toggle:hover {
  color: var(--text-primary);
  background: var(--bg-hover);
}

.form-label-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.auth-link-sm {
  font-size: 12px;
  color: var(--accent-2);
  transition: color 0.15s;
}

.auth-link-sm:hover {
  text-decoration: underline;
  color: #fff;
}

.auth-remember-row {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.auth-checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--text-secondary);
  cursor: pointer;
  user-select: none;
}

.auth-checkbox-label input[type="checkbox"] {
  accent-color: var(--accent-1);
  width: 16px;
  height: 16px;
  cursor: pointer;
}

.auth-submit-btn {
  width: 100%;
  margin-top: 10px;
}

/* ── 6. Password Strength Meter ── */
.password-meter-container {
  margin-top: 10px;
  padding: 12px 14px;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
}

.meter-bar-track {
  width: 100%;
  height: 6px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 8px;
}

.meter-bar-fill {
  height: 100%;
  width: 0%;
  transition: width 0.3s ease, background-color 0.3s ease;
  border-radius: 3px;
}

.meter-status-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  margin-bottom: 10px;
}

.meter-label {
  color: var(--text-secondary);
}

.meter-value {
  font-weight: 700;
  text-transform: capitalize;
}

.meter-requirements {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
}

.req-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  color: var(--text-muted);
  transition: color 0.2s;
}

.req-item.met {
  color: #34d399;
  font-weight: 600;
}

.confirm-match-status {
  font-size: 12px;
  margin-top: 6px;
  min-height: 18px;
}

.auth-terms-note {
  font-size: 11px;
  color: var(--text-muted);
  line-height: 1.45;
  margin: 14px 0 18px 0;
}

/* ── 7. Alerts & Messages ── */
.auth-alert {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px 14px;
  border-radius: var(--radius-sm);
  margin-bottom: 18px;
  font-size: 13px;
  line-height: 1.4;
  animation: authAlertSlide 0.2s ease-out;
}

@keyframes authAlertSlide {
  from { opacity: 0; transform: translateY(-8px); }
  to { opacity: 1; transform: translateY(0); }
}

.auth-alert.error {
  background: rgba(239, 68, 68, 0.15);
  border: 1px solid rgba(239, 68, 68, 0.35);
  color: #fca5a5;
}

.auth-alert.success {
  background: rgba(16, 185, 129, 0.15);
  border: 1px solid rgba(16, 185, 129, 0.35);
  color: #6ee7b7;
}

.auth-alert-text {
  flex: 1;
}

.auth-alert-close {
  color: inherit;
  opacity: 0.7;
  transition: opacity 0.15s;
  font-size: 16px;
  background: none;
  border: none;
  cursor: pointer;
}
.auth-alert-close:hover { opacity: 1; }

/* ── 8. Demo Helper & Security Badges ── */
.auth-demo-box {
  margin-top: 18px;
  padding: 10px 14px;
  background: rgba(245, 158, 11, 0.08);
  border: 1px dashed rgba(245, 158, 11, 0.3);
  border-radius: var(--radius-sm);
}

.demo-box-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  font-weight: 600;
  color: #fcd34d;
}

.btn-text-xs {
  font-size: 11px;
  font-weight: 700;
  color: var(--accent-2);
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 2px 6px;
  border-radius: 4px;
  transition: all 0.15s;
}
.btn-text-xs:hover {
  background: rgba(6, 182, 212, 0.15);
  text-decoration: underline;
}

.demo-box-sub {
  font-size: 11px;
  color: var(--text-secondary);
  margin-top: 3px;
}

.auth-footer-link {
  margin-top: 22px;
  text-align: center;
  font-size: 13px;
  color: var(--text-secondary);
}

.auth-footer-link a {
  color: var(--accent-1);
  font-weight: 600;
  transition: color 0.15s;
}

.auth-footer-link a:hover {
  color: #a78bfa;
  text-decoration: underline;
}

.auth-security-badges {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 16px;
  margin-top: 24px;
  font-size: 11px;
  color: var(--text-muted);
}

.auth-security-badges span {
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

/* ── 9. Access Gate (Protected Routes Interceptor) ── */
.access-gate-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 160px);
  padding: 40px 20px;
}

.access-gate-card {
  max-width: 540px;
  background: rgba(15, 23, 42, 0.75);
  backdrop-filter: blur(28px);
  border: 1px solid var(--border-strong);
  border-radius: var(--radius-xl);
  padding: 44px 38px;
  text-align: center;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.6), 0 0 40px rgba(124, 58, 237, 0.2);
  animation: authFadeIn 0.35s ease-out;
}

.access-gate-icon {
  width: 64px;
  height: 64px;
  border-radius: 20px;
  background: var(--accent-grad);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  color: #fff;
  margin-bottom: 20px;
  box-shadow: 0 8px 28px rgba(124, 58, 237, 0.5);
}

.access-gate-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  background: rgba(245, 158, 11, 0.15);
  border: 1px solid rgba(245, 158, 11, 0.3);
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  color: #fbbf24;
  margin-bottom: 16px;
}

.access-gate-title {
  font-size: 24px;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.4px;
  margin-bottom: 12px;
}

.access-gate-desc {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 24px;
}

.access-gate-features {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 16px;
  margin-bottom: 28px;
  text-align: left;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.gate-feat-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  color: var(--text-primary);
}

.access-gate-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

.access-gate-footer a {
  font-size: 13px;
  color: var(--text-muted);
  transition: color 0.15s;
}

.access-gate-footer a:hover {
  color: var(--text-primary);
}

/* ── 10. Responsive Breakpoints ── */
@media (max-width: 640px) {
  .auth-card {
    padding: 24px 18px;
  }
  .access-gate-card {
    padding: 30px 20px;
  }
  .meter-requirements {
    grid-template-columns: 1fr;
  }
  .topbar-auth-actions span {
    display: none;
  }
}
"""

with open(r"C:\Users\hp\OneDrive\Desktop\content-transformer\css\styles.css", "r", encoding="utf-8") as f:
    css = f.read()

if "/* ── 1. Topbar & Header Auth Actions ── */" not in css:
    css += AUTH_CSS

save_file("css/styles.css", css)
print("Updated styles.css with auth styles")

