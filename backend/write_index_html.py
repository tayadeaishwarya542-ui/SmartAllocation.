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

INDEX_HTML = r'''<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>TransformAI — Gen AI Content Transformation Platform</title>
  <meta name="description" content="Transform any content into any format using state-of-the-art Gen AI. Summarize, translate, rewrite, repurpose — at scale." />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet" />
  <link href="https://cdn.jsdelivr.net/npm/remixicon@4.2.0/fonts/remixicon.css" rel="stylesheet" />
  <link rel="stylesheet" href="css/styles.css" />
</head>
<body>
  <!-- Ambient background glow blobs -->
  <div class="ambient-bg">
    <div class="blob blob-1"></div>
    <div class="blob blob-2"></div>
    <div class="blob blob-3"></div>
  </div>

  <!-- App Shell -->
  <div class="app-shell" id="appShell">

    <!-- ── Sidebar ── -->
    <aside class="sidebar" id="sidebar">
      <div class="sidebar-header">
        <div class="logo">
          <div class="logo-icon">
            <i class="ri-sparkling-2-fill"></i>
          </div>
          <div class="logo-text">
            <span class="logo-name">TransformAI</span>
            <span class="logo-tag">Gen AI Platform</span>
          </div>
        </div>
        <button class="sidebar-toggle" id="sidebarToggle" title="Toggle Sidebar">
          <i class="ri-layout-left-line"></i>
        </button>
      </div>

      <nav class="sidebar-nav">
        <div class="nav-section-label">Main</div>
        <a href="#" class="nav-item active" data-page="dashboard" id="nav-dashboard">
          <span class="nav-icon"><i class="ri-dashboard-3-line"></i></span>
          <span class="nav-label">Dashboard</span>
        </a>
        <a href="#" class="nav-item" data-page="transform" id="nav-transform">
          <span class="nav-icon"><i class="ri-magic-line"></i></span>
          <span class="nav-label">Transform</span>
          <span class="nav-badge new">8 Engines</span>
        </a>
        <a href="#" class="nav-item" data-page="pipelines" id="nav-pipelines">
          <span class="nav-icon"><i class="ri-flow-chart"></i></span>
          <span class="nav-label">Pipelines</span>
          <span class="nav-badge">Studio</span>
        </a>

        <div class="nav-section-label">Workspace</div>
        <a href="#" class="nav-item" data-page="history" id="nav-history">
          <span class="nav-icon"><i class="ri-history-line"></i></span>
          <span class="nav-label">History</span>
        </a>
        <a href="#" class="nav-item" data-page="analytics" id="nav-analytics">
          <span class="nav-icon"><i class="ri-bar-chart-2-line"></i></span>
          <span class="nav-label">Analytics</span>
        </a>

        <div class="nav-section-label">System</div>
        <a href="#" class="nav-item" data-page="settings" id="nav-settings">
          <span class="nav-icon"><i class="ri-settings-4-line"></i></span>
          <span class="nav-label">Settings</span>
        </a>
      </nav>

      <div class="sidebar-footer">
        <div class="api-status" id="apiStatus" onclick="App.navigate('settings')" style="cursor:pointer;" title="Click to configure providers">
          <span class="status-dot online" id="statusDot"></span>
          <span class="status-text" id="statusText">Local Engine (Active)</span>
        </div>
        <div class="plan-badge">v1.0.0 Ready</div>
      </div>
    </aside>

    <!-- ── Main Content ── -->
    <main class="main-content" id="mainContent">

      <!-- Top Bar -->
      <header class="topbar">
        <div class="topbar-left">
          <button class="mobile-menu-btn" id="mobileMenuBtn">
            <i class="ri-menu-3-line"></i>
          </button>
          <div class="breadcrumb" id="breadcrumb">
            <span class="breadcrumb-icon"><i class="ri-dashboard-3-line"></i></span>
            <span class="breadcrumb-label" id="breadcrumbLabel">Dashboard</span>
          </div>
        </div>
        <div class="topbar-right">
          <div class="search-bar">
            <i class="ri-search-line"></i>
            <input type="text" placeholder="Search operations or history (Enter)..." id="globalSearch" />
            <span class="search-shortcut">⌘K</span>
          </div>
          <button class="topbar-btn" id="themeToggleBtn" onclick="ThemeManager.toggle()" title="Toggle Dark/Light Theme">
            <i class="ri-sun-line" id="themeToggleIcon"></i>
          </button>
          <button class="topbar-btn" title="System Telemetry" id="notifBtn">
            <i class="ri-notification-3-line"></i>
            <span class="notif-dot"></span>
          </button>
          <div class="user-avatar" title="TransformAI User" onclick="App.navigate('settings')" style="cursor:pointer;">
            <span>AI</span>
          </div>
        </div>
      </header>

      <!-- Page Content Container -->
      <div class="page-container" id="pageContainer">
        <!-- Rendered dynamically -->
      </div>

    </main>
  </div>

  <!-- Toast Notifications Container -->
  <div class="toast-container" id="toastContainer"></div>

  <!-- Scripts -->
  <script src="js/transformations.js"></script>
  <script src="js/api.js"></script>
  <script src="pages/dashboard.js"></script>
  <script src="pages/transform.js"></script>
  <script src="pages/pipelines.js"></script>
  <script src="pages/history.js"></script>
  <script src="pages/analytics.js"></script>
  <script src="pages/settings.js"></script>
  <script src="js/app.js"></script>
</body>
</html>
'''

save_file("index.html", INDEX_HTML)
