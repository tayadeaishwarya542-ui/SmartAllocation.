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

with open(r"C:\Users\hp\OneDrive\Desktop\content-transformer\pages\dashboard.js", "r", encoding="utf-8") as f:
    code = f.read()

old_welcome = """    <!-- 1. Welcome Section -->
    <div class="dashboard-hero-card">
      <div class="hero-content">
        <div class="hero-badge">
          <i class="ri-sparkling-fill"></i> Next-Gen AI Productivity Suite
        </div>
        <h1 class="hero-title">Welcome to TransformAI</h1>
        <p class="hero-subtitle">
          Transform your content intelligently, automate repetitive writing tasks, and build powerful AI workflows.
        </p>
        <div class="hero-actions">
          <button class="btn btn-primary" onclick="App.navigate('transform')">
            <i class="ri-add-line"></i> + New Transformation
          </button>
          <button class="btn btn-secondary" onclick="App.navigate('practice')">
            <i class="ri-questionnaire-line"></i> My Practice & Quizzes
          </button>
          <button class="btn btn-secondary" onclick="App.navigate('pipelines')">
            <i class="ri-flow-chart"></i> Create Pipeline
          </button>
        </div>
      </div>
    </div>"""

new_welcome = """    <!-- 1. Welcome Section (Personalized by Auth State) -->
    <div class="dashboard-hero-card">
      <div class="hero-content">
        ${isAuth && user ? `
          <div class="hero-badge" style="background:rgba(16, 185, 129, 0.15);border-color:rgba(16, 185, 129, 0.35);color:#34d399;">
            <i class="ri-shield-check-fill"></i> Authenticated Workspace · ${escapeHtml(user.full_name)}
          </div>
          <h1 class="hero-title">Welcome back, <span class="grad-text">${escapeHtml(user.full_name)}</span></h1>
          <p class="hero-subtitle">
            Your personal workspace is active. Access your transformation history, AI practice sets, and custom pipeline workflows.
          </p>
          <div class="hero-actions">
            <button class="btn btn-primary" onclick="App.navigate('transform')">
              <i class="ri-magic-line"></i> Open Transformer
            </button>
            <button class="btn btn-secondary" onclick="App.navigate('practice')">
              <i class="ri-questionnaire-line"></i> My Practice & Quizzes
            </button>
            <button class="btn btn-secondary" onclick="App.navigate('pipelines')">
              <i class="ri-flow-chart"></i> Pipeline Studio
            </button>
            <button class="btn btn-ghost text-danger" onclick="AuthManager.logout()" title="Sign Out of Account">
              <i class="ri-logout-box-r-line"></i> Sign Out
            </button>
          </div>
        ` : `
          <div class="hero-badge">
            <i class="ri-sparkling-fill"></i> Enterprise Gen AI Content Platform
          </div>
          <h1 class="hero-title">Welcome to <span class="grad-text">TransformAI</span></h1>
          <p class="hero-subtitle">
            Transform your content intelligently, automate repetitive writing tasks, and build powerful AI workflows. Sign in or create an account to unlock your personalized transformation records and AI quizzes.
          </p>
          <div class="hero-actions">
            <button class="btn btn-primary" onclick="App.navigate('signup')">
              <i class="ri-user-add-line"></i> Get Started Free
            </button>
            <button class="btn btn-secondary" onclick="App.navigate('login')">
              <i class="ri-login-box-line"></i> Sign In to Account
            </button>
            <button class="btn btn-ghost" onclick="App.navigate('help')">
              <i class="ri-book-open-line"></i> Documentation & Guide
            </button>
          </div>
        `}
      </div>
    </div>"""

# Insert user check at top of function
target_top = """function renderDashboard() {
  const stats = AppState.getStats();
  const history = AppState.getHistory();
  const savedPipelines = AppState.getSavedPipelines();"""

replacement_top = """function renderDashboard() {
  const stats = AppState.getStats();
  const history = AppState.getHistory();
  const savedPipelines = AppState.getSavedPipelines();
  const user = (typeof AuthManager !== 'undefined') ? AuthManager.getUser() : null;
  const isAuth = (typeof AuthManager !== 'undefined') ? AuthManager.isAuthenticated() : false;"""

code = code.replace(target_top, replacement_top)
code = code.replace(old_welcome, new_welcome)

save_file("pages/dashboard.js", code)
print("Updated dashboard.js with auth personalization")

