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

with open(r"C:\Users\hp\OneDrive\Desktop\content-transformer\pages\settings.js", "r", encoding="utf-8") as f:
    code = f.read()

# Add user and isAuth variables to renderSettingsPage
code = code.replace(
    "function renderSettingsPage() {\n  const settings = AppState.getSettings();",
    "function renderSettingsPage() {\n  const settings = AppState.getSettings();\n  const user = (typeof AuthManager !== 'undefined') ? AuthManager.getUser() : null;\n  const isAuth = (typeof AuthManager !== 'undefined') ? AuthManager.isAuthenticated() : false;"
)

# Add Account & Security Profile card before 1. Appearance Section
account_card = """      <!-- 0. Account Profile & Security -->
      <div class="settings-card" style="grid-column: 1 / -1;">
        <div class="settings-card-header">
          <div class="settings-card-title"><i class="ri-shield-user-line" style="color:#a855f7;"></i> Account Profile & Authentication</div>
          <div class="settings-card-desc">Active session credentials, security safeguards, and account management.</div>
        </div>
        <div class="settings-card-body">
          ${isAuth && user ? `
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px;">
              <div>
                <div style="font-size:16px; font-weight:700; color:var(--text-primary); margin-bottom:4px;">
                  ${escapeHtml(user.full_name)}
                </div>
                <div style="font-size:13px; color:var(--text-secondary); margin-bottom:8px;">
                  <i class="ri-mail-line"></i> ${escapeHtml(user.email)}
                </div>
                <div style="display:flex; gap:8px; flex-wrap:wrap;">
                  <span class="badge badge-green"><i class="ri-shield-check-fill"></i> Scrypt Salted Encryption</span>
                  <span class="badge badge-cyan"><i class="ri-database-2-line"></i> Isolated User SQLite Database</span>
                </div>
              </div>
              <button class="btn btn-danger btn-sm" onclick="AuthManager.logout()">
                <i class="ri-logout-box-r-line"></i> Sign Out of Account
              </button>
            </div>
          ` : `
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px;">
              <div>
                <div style="font-size:14px; font-weight:600; color:var(--text-primary); margin-bottom:4px;">Guest Workspace</div>
                <div style="font-size:13px; color:var(--text-secondary);">Sign in to enable cloud session persistence and personal quiz history.</div>
              </div>
              <div style="display:flex; gap:8px;">
                <button class="btn btn-secondary btn-sm" onclick="App.navigate('login')"><i class="ri-login-box-line"></i> Sign In</button>
                <button class="btn btn-primary btn-sm" onclick="App.navigate('signup')"><i class="ri-user-add-line"></i> Create Account</button>
              </div>
            </div>
          `}
        </div>
      </div>

"""

code = code.replace(
    '    <div class="settings-grid">\n      <!-- 1. Appearance Section -->',
    '    <div class="settings-grid">\n' + account_card + '      <!-- 1. Appearance Section -->'
)

save_file("pages/settings.js", code)
print("Updated settings.js with account profile card")

