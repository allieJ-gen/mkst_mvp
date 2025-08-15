<template>
  <div class="dashboard">
    <!-- 통계 카드 섹션 -->
    <div class="stats-section">
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">👥</div>
          <div class="stat-content">
            <h3 class="stat-value">{{ stats.totalStudents }}</h3>
            <p class="stat-label">전체 학생</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">✅</div>
          <div class="stat-content">
            <h3 class="stat-value">{{ stats.activeStudents }}</h3>
            <p class="stat-label">재원생</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">🗄️</div>
          <div class="stat-content">
            <h3 class="stat-value">{{ stats.occupiedLockers }}</h3>
            <p class="stat-label">사용중인 사물함</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">📊</div>
          <div class="stat-content">
            <h3 class="stat-value">{{ stats.lockerUsageRate }}%</h3>
            <p class="stat-label">사물함 이용률</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 빠른 액션 섹션 -->
    <div class="quick-actions-section">
      <h2 class="section-title">빠른 액션</h2>
      <div class="actions-grid">
        <NuxtLink to="/students/register" class="action-card">
          <div class="action-icon">➕</div>
          <h3 class="action-title">학생 등록</h3>
          <p class="action-description">새로운 학생을 등록합니다</p>
        </NuxtLink>
        
        <NuxtLink to="/students" class="action-card">
          <div class="action-icon">🔍</div>
          <h3 class="action-title">학생 검색</h3>
          <p class="action-description">학생 정보를 검색하고 조회합니다</p>
        </NuxtLink>
        
        <NuxtLink to="/lockers" class="action-card">
          <div class="action-icon">🗄️</div>
          <h3 class="action-title">사물함 관리</h3>
          <p class="action-description">사물함 배정 및 해제를 관리합니다</p>
        </NuxtLink>
        
        <NuxtLink to="/reports" class="action-card">
          <div class="action-icon">📈</div>
          <h3 class="action-title">통계 보고서</h3>
          <p class="action-description">학생 및 사물함 통계를 확인합니다</p>
        </NuxtLink>
      </div>
    </div>

    <!-- 최근 활동 섹션 -->
    <div class="recent-activities-section">
      <h2 class="section-title">최근 활동</h2>
      <div class="activities-list">
        <div v-for="activity in recentActivities" :key="activity.id" class="activity-item">
          <div class="activity-icon">{{ activity.icon }}</div>
          <div class="activity-content">
            <h4 class="activity-title">{{ activity.title }}</h4>
            <p class="activity-description">{{ activity.description }}</p>
            <span class="activity-time">{{ formatTime(activity.timestamp) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// 페이지 메타데이터
definePageMeta({
  title: '대시보드',
  layout: false // AppLayout을 사용하지 않음
})

// 통계 데이터
const stats = ref({
  totalStudents: 0,
  activeStudents: 0,
  occupiedLockers: 0,
  lockerUsageRate: 0
})

// 최근 활동 데이터
const recentActivities = ref([
  {
    id: 1,
    icon: '👤',
    title: '새 학생 등록',
    description: '김철수 학생이 등록되었습니다',
    timestamp: new Date(Date.now() - 1000 * 60 * 30) // 30분 전
  },
  {
    id: 2,
    icon: '🗄️',
    title: '사물함 배정',
    description: '15번 사물함이 배정되었습니다',
    timestamp: new Date(Date.now() - 1000 * 60 * 60) // 1시간 전
  },
  {
    id: 3,
    icon: '📝',
    title: '학생 정보 수정',
    description: '이영희 학생 정보가 수정되었습니다',
    timestamp: new Date(Date.now() - 1000 * 60 * 60 * 2) // 2시간 전
  },
  {
    id: 4,
    icon: '✅',
    title: '사물함 해제',
    description: '23번 사물함이 해제되었습니다',
    timestamp: new Date(Date.now() - 1000 * 60 * 60 * 3) // 3시간 전
  }
])

// 시간 포맷팅
const formatTime = (timestamp) => {
  const now = new Date()
  const diff = now - timestamp
  const minutes = Math.floor(diff / (1000 * 60))
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (minutes < 60) {
    return `${minutes}분 전`
  } else if (hours < 24) {
    return `${hours}시간 전`
  } else {
    return `${days}일 전`
  }
}

// 데이터 로드
const loadDashboardData = async () => {
  try {
    // 학생 통계 API 호출
    const studentsResponse = await fetch('/api/students/statistics/')
    if (studentsResponse.ok) {
      const studentsData = await studentsResponse.json()
      stats.value.totalStudents = studentsData.total_students || 0
      stats.value.activeStudents = studentsData.active_students || 0
    }
    
    // 사물함 통계 API 호출
    const lockersResponse = await fetch('/api/lockers/statistics/')
    if (lockersResponse.ok) {
      const lockersData = await lockersResponse.json()
      stats.value.occupiedLockers = lockersData.occupied_lockers || 0
      const totalLockers = lockersData.total_lockers || 271
      stats.value.lockerUsageRate = Math.round((stats.value.occupiedLockers / totalLockers) * 100)
    }
  } catch (error) {
    console.error('대시보드 데이터 로드 실패:', error)
    // 임시 데이터로 표시
    stats.value = {
      totalStudents: 8,
      activeStudents: 6,
      occupiedLockers: 6,
      lockerUsageRate: 2
    }
  }
}

// 컴포넌트 마운트 시 데이터 로드
onMounted(() => {
  loadDashboardData()
})
</script>

<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
}

/* ===== 통계 카드 섹션 ===== */
.stats-section {
  margin-bottom: var(--spacing-2xl);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-lg);
}

.stat-card {
  background-color: var(--color-surface);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-xl);
  box-shadow: var(--shadow-sm);
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
  transition: all var(--transition-normal);
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.stat-icon {
  font-size: 32px;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--color-secondary-surface);
  border-radius: var(--border-radius-lg);
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: var(--font-size-title-1);
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-xs) 0;
}

.stat-label {
  font-size: var(--font-size-subhead);
  color: var(--color-text-secondary);
  margin: 0;
}

/* ===== 빠른 액션 섹션 ===== */
.quick-actions-section {
  margin-bottom: var(--spacing-2xl);
}

.section-title {
  font-size: var(--font-size-title-2);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-lg);
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--spacing-lg);
}

.action-card {
  background-color: var(--color-surface);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-xl);
  box-shadow: var(--shadow-sm);
  text-decoration: none;
  color: inherit;
  transition: all var(--transition-normal);
  border: 1px solid var(--color-border-light);
}

.action-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: var(--color-blue);
}

.action-icon {
  font-size: 32px;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--color-secondary-surface);
  border-radius: var(--border-radius-lg);
  margin-bottom: var(--spacing-md);
}

.action-title {
  font-size: var(--font-size-headline);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-sm) 0;
}

.action-description {
  font-size: var(--font-size-body);
  color: var(--color-text-secondary);
  margin: 0;
  line-height: 1.5;
}

/* ===== 최근 활동 섹션 ===== */
.recent-activities-section {
  margin-bottom: var(--spacing-2xl);
}

.activities-list {
  background-color: var(--color-surface);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
}

.activity-item {
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-md);
  padding: var(--spacing-lg);
  border-bottom: 1px solid var(--color-border-light);
  transition: background-color var(--transition-normal);
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-item:hover {
  background-color: var(--color-secondary-surface);
}

.activity-icon {
  font-size: 20px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--color-secondary-surface);
  border-radius: var(--border-radius-md);
  flex-shrink: 0;
}

.activity-content {
  flex: 1;
}

.activity-title {
  font-size: var(--font-size-subhead);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-xs) 0;
}

.activity-description {
  font-size: var(--font-size-body);
  color: var(--color-text-secondary);
  margin: 0 0 var(--spacing-xs) 0;
  line-height: 1.4;
}

.activity-time {
  font-size: var(--font-size-caption-1);
  color: var(--color-text-tertiary);
}

/* ===== 반응형 디자인 ===== */
@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .actions-grid {
    grid-template-columns: 1fr;
  }
  
  .stat-card,
  .action-card {
    padding: var(--spacing-lg);
  }
  
  .activity-item {
    padding: var(--spacing-md);
  }
}
</style>
