<template>
  <div class="app-layout">
    <!-- 사이드바 네비게이션 -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <h1 class="sidebar-logo">MKST</h1>
        <p class="sidebar-subtitle">관리형독서실</p>
      </div>
      
      <nav class="sidebar-nav">
        <ul class="nav-list">
          <li class="nav-item">
            <NuxtLink to="/" class="nav-link" active-class="nav-link-active">
              <span class="nav-icon">📊</span>
              <span class="nav-text">대시보드</span>
            </NuxtLink>
          </li>
          <li class="nav-item">
            <NuxtLink to="/students" class="nav-link" active-class="nav-link-active">
              <span class="nav-icon">👥</span>
              <span class="nav-text">학생 관리</span>
            </NuxtLink>
          </li>
          <li class="nav-item">
            <NuxtLink to="/lockers" class="nav-link" active-class="nav-link-active">
              <span class="nav-icon">🗄️</span>
              <span class="nav-text">사물함 관리</span>
            </NuxtLink>
          </li>
          <li class="nav-item">
            <NuxtLink to="/settings" class="nav-link" active-class="nav-link-active">
              <span class="nav-icon">⚙️</span>
              <span class="nav-text">설정</span>
            </NuxtLink>
          </li>
        </ul>
      </nav>
    </aside>

    <!-- 메인 컨텐츠 영역 -->
    <main class="main-content">
      <!-- 헤더 -->
      <header class="header">
        <div class="header-left">
          <h2 class="page-title">{{ pageTitle }}</h2>
        </div>
        <div class="header-right">
          <div class="user-menu">
            <span class="user-name">관리자</span>
            <button class="user-avatar">👤</button>
          </div>
        </div>
      </header>

      <!-- 페이지 컨텐츠 -->
      <div class="page-content">
        <slot />
      </div>
    </main>
  </div>
</template>

<script setup>
// 페이지 제목을 props로 받기
defineProps({
  pageTitle: {
    type: String,
    default: '대시보드'
  }
})
</script>

<style scoped>
.app-layout {
  display: flex;
  min-height: 100vh;
  background-color: var(--color-background);
}

/* ===== 사이드바 스타일 ===== */
.sidebar {
  width: 280px;
  background-color: var(--color-surface);
  border-right: 1px solid var(--color-border-light);
  display: flex;
  flex-direction: column;
  position: fixed;
  height: 100vh;
  z-index: 100;
}

.sidebar-header {
  padding: var(--spacing-xl);
  border-bottom: 1px solid var(--color-border-light);
  text-align: center;
}

.sidebar-logo {
  font-size: var(--font-size-title-2);
  font-weight: var(--font-weight-bold);
  color: var(--color-blue);
  margin: 0 0 var(--spacing-xs) 0;
}

.sidebar-subtitle {
  font-size: var(--font-size-caption-1);
  color: var(--color-text-secondary);
  margin: 0;
}

.sidebar-nav {
  flex: 1;
  padding: var(--spacing-lg) 0;
}

.nav-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav-item {
  margin: 0;
}

.nav-link {
  display: flex;
  align-items: center;
  padding: var(--spacing-md) var(--spacing-xl);
  color: var(--color-text-primary);
  text-decoration: none;
  transition: all var(--transition-normal);
  border-left: 3px solid transparent;
}

.nav-link:hover {
  background-color: var(--color-secondary-surface);
  color: var(--color-blue);
}

.nav-link-active {
  background-color: var(--color-secondary-surface);
  color: var(--color-blue);
  border-left-color: var(--color-blue);
}

.nav-icon {
  font-size: var(--font-size-body);
  margin-right: var(--spacing-md);
  width: 20px;
  text-align: center;
}

.nav-text {
  font-size: var(--font-size-body);
  font-weight: var(--font-weight-medium);
}

/* ===== 메인 컨텐츠 영역 ===== */
.main-content {
  flex: 1;
  margin-left: 280px;
  display: flex;
  flex-direction: column;
}

.header {
  background-color: var(--color-surface);
  border-bottom: 1px solid var(--color-border-light);
  padding: var(--spacing-lg) var(--spacing-xl);
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 50;
}

.page-title {
  font-size: var(--font-size-title-2);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  margin: 0;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.user-name {
  font-size: var(--font-size-subhead);
  color: var(--color-text-secondary);
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 1px solid var(--color-border);
  background-color: var(--color-secondary-surface);
  cursor: pointer;
  transition: all var(--transition-normal);
}

.user-avatar:hover {
  border-color: var(--color-blue);
  transform: scale(1.05);
}

.page-content {
  flex: 1;
  padding: var(--spacing-xl);
}

/* ===== 반응형 디자인 ===== */
@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
    transition: transform var(--transition-normal);
  }
  
  .sidebar.open {
    transform: translateX(0);
  }
  
  .main-content {
    margin-left: 0;
  }
  
  .page-content {
    padding: var(--spacing-lg);
  }
}
</style>
