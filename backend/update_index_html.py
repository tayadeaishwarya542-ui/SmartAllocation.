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

with open(r"C:\Users\hp\OneDrive\Desktop\content-transformer\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Add script tag for pages/auth.js before js/app.js
if '<script src="pages/auth.js"></script>' not in html:
    html = html.replace(
        '<script src="pages/help.js"></script>\n  <script src="js/app.js"></script>',
        '<script src="pages/help.js"></script>\n  <script src="pages/auth.js"></script>\n  <script src="js/app.js"></script>'
    )

# 2. Add topbarAuthActions before themeToggleBtn if not present
if 'id="topbarAuthActions"' not in html:
    html = html.replace(
        '<!-- Theme Toggle -->\n          <button class="topbar-btn" id="themeToggleBtn"',
        '<!-- Auth Entry Point -->\n          <div class="topbar-auth-actions" id="topbarAuthActions"></div>\n\n          <!-- Theme Toggle -->\n          <button class="topbar-btn" id="themeToggleBtn"'
    )

# 3. Add Account navigation section to sidebar if not present
if 'id="nav-login"' not in html:
    nav_auth_block = '''        <div class="nav-section-label" id="sidebarAuthSection">Account & Security</div>
        <a href="#" class="nav-item" data-page="login" id="nav-login">
          <span class="nav-icon"><i class="ri-login-box-line"></i></span>
          <span class="nav-label">Sign In</span>
        </a>
        <a href="#" class="nav-item" data-page="signup" id="nav-signup">
          <span class="nav-icon"><i class="ri-user-add-line"></i></span>
          <span class="nav-label">Create Account</span>
        </a>
'''
    html = html.replace(
        '        <div class="nav-section-label">Analytics & Preferences</div>',
        nav_auth_block + '        <div class="nav-section-label">Analytics & Preferences</div>'
    )

save_file("index.html", html)
print("Updated index.html successfully")

