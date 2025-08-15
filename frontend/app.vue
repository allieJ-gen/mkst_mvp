<template>
  <div id="app">
    <!-- 라우팅에 따른 조건부 렌더링 -->
    <div v-if="$route.path === '/'" class="dashboard">
      <!-- 대시보드 내용 -->
      <div class="stats-section">
        <h1 class="text-large-title hidden-title">김엄마 관리형 독서실</h1>
        <p class="text-body">학생 회원 관리 시스템</p>
        
        <div class="grid grid-cols-3">
          <div class="card">
            <h3 class="text-title-3">전체 학생</h3>
            <p class="text-large-title text-blue">0</p>
            <p class="text-caption">등록된 학생 수</p>
          </div>
          <div class="card">
            <h3 class="text-title-3">사물함 사용</h3>
            <p class="text-large-title text-green">0</p>
            <p class="text-caption">사용 중인 사물함</p>
          </div>
          <div class="card">
            <h3 class="text-title-3">오늘 출석</h3>
            <p class="text-large-title text-orange">0</p>
            <p class="text-caption">오늘 출석한 학생</p>
          </div>
        </div>
      </div>
      
      <div class="quick-actions-section">
        <h2 class="text-title-2">빠른 액션</h2>
        <div class="grid grid-cols-2">
          <button @click="goToStudentRegister" class="btn btn-primary">
            학생 등록
          </button>
          <button class="btn btn-secondary">
            학생 목록
          </button>
        </div>
      </div>
      
      <div class="recent-activities-section">
        <h2 class="text-title-2">최근 활동</h2>
        <div class="card">
          <p class="text-body">아직 활동 내역이 없습니다.</p>
        </div>
      </div>
    </div>

    <!-- 학생 등록 페이지 -->
    <div v-else-if="$route.path === '/students/register'" class="student-registration-page">
      <!-- 페이지 헤더 -->
      <div class="page-header">
        <h1 class="text-large-title">학생 등록</h1>
        <p class="text-body text-caption">새로운 학생을 등록합니다</p>
      </div>

      <!-- 등록 폼 -->
      <form @submit.prevent="handleSubmit" class="form-container">
        <!-- 기본 정보 섹션 -->
        <div class="form-section">
          <h2 class="text-title-3 section-title">기본 정보</h2>
          
          <div class="form-grid">
            <!-- 학생명 -->
            <div class="form-group">
              <label class="input-label" for="name">
                학생명 <span class="required">*</span>
              </label>
              <input
                id="name"
                v-model="form.name"
                type="text"
                class="input-field"
                placeholder="학생 이름을 입력하세요"
                required
              />
            </div>

            <!-- 학교명 -->
            <div class="form-group">
              <label class="input-label" for="school">
                학교명 <span class="required">*</span>
              </label>
              <input
                id="school"
                v-model="form.school"
                type="text"
                class="input-field"
                placeholder="서현 (고등학교 접미어 생략)"
                required
              />
              <p class="help-text">예: 서현, 서현고, 서현고등학교 모두 "서현고"로 자동 변환됩니다</p>
            </div>

            <!-- 학년 -->
            <div class="form-group">
              <label class="input-label" for="grade">
                학년 <span class="required">*</span>
              </label>
              <select
                id="grade"
                v-model="form.grade"
                class="input-field"
                required
              >
                <option value="">학년을 선택하세요</option>
                <option value="0">비고등학생</option>
                <option value="1">1학년</option>
                <option value="2">2학년</option>
                <option value="3">3학년</option>
              </select>
            </div>

            <!-- 성별 -->
            <div class="form-group">
              <label class="input-label">성별 <span class="required">*</span></label>
              <div class="radio-group">
                <label class="radio-label">
                  <input
                    type="radio"
                    v-model="form.gender"
                    value="M"
                    required
                  />
                  <span class="radio-text">남</span>
                </label>
                <label class="radio-label">
                  <input
                    type="radio"
                    v-model="form.gender"
                    value="F"
                    required
                  />
                  <span class="radio-text">여</span>
                </label>
              </div>
            </div>
          </div>
        </div>

        <!-- 연락처 정보 섹션 -->
        <div class="form-section">
          <h2 class="text-title-3 section-title">연락처 정보</h2>
          
          <div class="form-grid">
            <!-- 보호자 휴대폰번호 (필수) -->
            <div class="form-group">
              <label class="input-label" for="parentPhone">
                보호자 휴대폰번호 <span class="required">*</span>
              </label>
              <input
                id="parentPhone"
                v-model="form.parentPhone"
                type="tel"
                class="input-field"
                placeholder="12345678"
                required
                @input="formatParentPhoneNumber"
                @focus="handlePhoneFocus"
              />
              <p class="help-text">010- 자동 입력, 숫자만 입력하세요 (예: 12345678)</p>
            </div>

            <!-- 학생 휴대폰번호 (선택) -->
            <div class="form-group">
              <label class="input-label" for="studentPhone">
                학생 휴대폰번호
              </label>
              <input
                id="studentPhone"
                v-model="form.studentPhone"
                type="tel"
                class="input-field"
                placeholder="12345678 (선택사항)"
                @input="formatStudentPhoneNumber"
                @focus="handlePhoneFocus"
              />
              <p class="help-text">010- 자동 입력, 숫자만 입력하세요 (예: 12345678)</p>
            </div>
          </div>
        </div>

        <!-- 등록 정보 섹션 -->
        <div class="form-section">
          <h2 class="text-title-3 section-title">등록 정보</h2>
          
          <div class="form-grid">
            <!-- 등원번호 자동 생성 안내 -->
            <div class="form-group">
              <label class="input-label">등원번호</label>
              <div class="info-display">
                <span class="info-text">자동 생성 예정</span>
                <span class="info-description">등록 완료 후 보호자 휴대폰번호 기반으로 자동 생성됩니다</span>
              </div>
              <p class="help-text">보호자 휴대폰 뒤4자리 + 핀번호(1자리) 자동 생성</p>
            </div>

            <!-- 첫등원일 -->
            <div class="form-group">
              <label class="input-label" for="firstAttendanceDate">
                첫등원일 <span class="required">*</span>
              </label>
              <input
                id="firstAttendanceDate"
                v-model="form.firstAttendanceDate"
                type="date"
                class="input-field"
                required
              />
              <p class="help-text">재등록생의 경우 마지막 재등록일</p>
            </div>

            <!-- 사물함 번호 -->
            <div class="form-group">
              <label class="input-label">
                사물함 번호
              </label>
              <div class="info-display">
                <span class="info-text">자동 배정 예정</span>
                <span class="info-description">등록 완료 후 빈 사물함이 자동으로 배정됩니다</span>
              </div>
              <p class="help-text">1~271번 사물함, 휴대폰보관함과 동일번호</p>
            </div>
          </div>
        </div>

        <!-- 폼 액션 버튼 -->
        <div class="form-actions">
          <button type="button" class="btn btn-secondary" @click="handleCancel">
            취소
          </button>
          <button type="submit" class="btn btn-primary">
            학생 등록
          </button>
        </div>
      </form>
    </div>

    <!-- 기본 페이지 -->
    <div v-else>
      <NuxtPage />
    </div>
  </div>
</template>

<script setup>
// 반응형 데이터
const form = ref({
  name: '',
  school: '',
  grade: '',
  gender: '',
  status: 'active', // 자동으로 "재원생" 설정
  studentPhone: '',
  parentPhone: '',
  firstAttendanceDate: new Date().toISOString().split('T')[0]
  // 등원번호와 사물함 번호는 백엔드에서 자동 생성/배정
})

// 등원번호는 백엔드에서 자동 생성 (PRD 규칙: 보호자휴대폰 뒤4자리 + 핀번호 1자리)

// 사물함 자동 배정은 백엔드에서 처리
// 프론트엔드에서는 사물함 번호를 입력하지 않음

// 휴대폰번호 입력 필드 포커스 시 자동 "010-" 추가
const handlePhoneFocus = (event) => {
  const input = event.target
  if (!input.value.startsWith('010-')) {
    input.value = '010-' + input.value
  }
}

// 보호자 휴대폰번호 형식 자동 변환 (010- 자동 추가)
const formatParentPhoneNumber = (event) => {
  const input = event.target
  let value = input.value.replace(/\D/g, '') // 숫자만 추출
  
  // 010- 자동 추가
  if (!value.startsWith('010')) {
    value = '010' + value
  }
  
  // 010 이후 숫자만 추출 (제한 없음)
  const remainingDigits = value.slice(3)
  
  // 형식 변환: 010-1234-5678
  let formattedValue = '010-'
  if (remainingDigits.length > 0) {
    formattedValue += remainingDigits.slice(0, 4)
  }
  if (remainingDigits.length > 4) {
    formattedValue += '-' + remainingDigits.slice(4, 8)
  }
  
  input.value = formattedValue
  form.value.parentPhone = formattedValue
}

// 학생 휴대폰번호 형식 자동 변환 (010- 자동 추가)
const formatStudentPhoneNumber = (event) => {
  const input = event.target
  let value = input.value.replace(/\D/g, '') // 숫자만 추출
  
  // 010- 자동 추가
  if (!value.startsWith('010')) {
    value = '010' + value
  }
  
  // 010 이후 숫자만 추출 (제한 없음)
  const remainingDigits = value.slice(3)
  
  // 형식 변환: 010-1234-5678
  let formattedValue = '010-'
  if (remainingDigits.length > 0) {
    formattedValue += remainingDigits.slice(0, 4)
  }
  if (remainingDigits.length > 4) {
    formattedValue += '-' + remainingDigits.slice(4, 8)
  }
  
  input.value = formattedValue
  form.value.studentPhone = formattedValue
}

// 학생 등록 페이지로 이동
const goToStudentRegister = () => {
  window.location.href = '/students/register'
}

// 폼 제출 처리
const handleSubmit = async () => {
  if (validateForm()) {
    try {
      // 구분을 자동으로 "재원생"으로 설정
      form.value.status = 'active'
      
      // API 호출을 위한 데이터 준비
      const studentData = {
        name: form.value.name,
        school: form.value.school,
        grade: parseInt(form.value.grade),
        gender: form.value.gender,
        status: form.value.status,
        student_phone: form.value.studentPhone || null,
        parent_phone: form.value.parentPhone,
        first_attendance_date: form.value.firstAttendanceDate
        // locker_number는 백엔드에서 자동 배정
      }
      
      console.log('학생 등록 데이터:', studentData)
      
      // Django API 호출
      const response = await fetch('http://localhost:8000/api/students/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // TODO: 인증 토큰 추가 필요
          // 'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(studentData)
      })
      
      if (response.ok) {
        const result = await response.json()
        console.log('학생 등록 성공:', result)
        alert('학생이 성공적으로 등록되었습니다!')
        
        // 폼 초기화
        resetForm()
        
        // 대시보드로 돌아가기
        window.location.href = '/'
      } else {
        const errorData = await response.json()
        console.error('학생 등록 실패:', errorData)
        
        // 에러 메시지 표시
        let errorMessage = '학생 등록에 실패했습니다.'
        if (errorData.message) {
          errorMessage = errorData.message
        } else if (errorData.errors) {
          const fieldErrors = Object.entries(errorData.errors)
            .map(([field, errors]) => `${field}: ${errors.join(', ')}`)
            .join('\n')
          errorMessage = `입력 오류:\n${fieldErrors}`
        }
        
        alert(errorMessage)
      }
    } catch (error) {
      console.error('학생 등록 중 오류 발생:', error)
      alert('네트워크 오류가 발생했습니다. 다시 시도해주세요.')
    }
  }
}

// 폼 유효성 검사 (PRD 필수 필드 기준)
const validateForm = () => {
  if (!form.value.name) {
    alert('학생명을 입력해주세요.')
    return false
  }
  if (!form.value.school) {
    alert('학교명을 입력해주세요.')
    return false
  }
  if (!form.value.grade) {
    alert('학년을 선택해주세요.')
    return false
  }
  if (!form.value.gender) {
    alert('성별을 선택해주세요.')
    return false
  }
  if (!form.value.parentPhone) {
    alert('보호자 휴대폰번호를 입력해주세요.')
    return false
  }
  if (!form.value.firstAttendanceDate) {
    alert('첫등원일을 입력해주세요.')
    return false
  }
  
  // 휴대폰번호 형식 검증
  const phoneRegex = /^010-\d{4}-\d{4}$/
  if (!phoneRegex.test(form.value.parentPhone)) {
    alert('보호자 휴대폰번호 형식이 올바르지 않습니다. (010-0000-0000)')
    return false
  }
  if (form.value.studentPhone && !phoneRegex.test(form.value.studentPhone)) {
    alert('학생 휴대폰번호 형식이 올바르지 않습니다. (010-0000-0000)')
    return false
  }
  
  return true
}

// 폼 초기화
const resetForm = () => {
  form.value = {
    name: '',
    school: '',
    grade: '',
    gender: '',
    status: 'active', // 항상 "재원생"으로 초기화
    studentPhone: '',
    parentPhone: '',
    firstAttendanceDate: new Date().toISOString().split('T')[0]
    // 등원번호와 사물함 번호는 백엔드에서 자동 생성/배정
  }
}

// 취소 처리
const handleCancel = () => {
  if (confirm('입력한 내용이 사라집니다. 정말 취소하시겠습니까?')) {
    resetForm()
    // 대시보드로 돌아가기
    window.location.href = '/'
  }
}

// 페이지 로드 시 초기화
onMounted(() => {
  // 등원번호와 사물함 번호는 백엔드에서 자동 생성/배정
})
</script>

<style>
/* Apple Human Interface Guidelines 기반 디자인 시스템 */

:root {
  /* ===== 색상 팔레트 ===== */
  
  /* Apple 시스템 색상 */
  --color-blue: #007AFF;           /* Primary Blue */
  --color-blue-dark: #0056CC;      /* Darker Blue for hover */
  --color-green: #34C759;          /* Success Green */
  --color-orange: #FF9500;         /* Warning Orange */
  --color-red: #FF3B30;            /* Error Red */
  --color-gray: #8E8E93;           /* Secondary Gray */
  
  /* 배경 색상 */
  --color-background: #F2F2F7;     /* System Gray 6 */
  --color-surface: #FFFFFF;         /* White */
  --color-secondary-surface: #F2F2F7;
  --color-tertiary-surface: #E5E5EA;
  
  /* 텍스트 색상 */
  --color-text-primary: #000000;    /* Black */
  --color-text-secondary: #8E8E93;  /* System Gray */
  --color-text-tertiary: #C7C7CC;   /* System Gray 3 */
  --color-text-inverse: #FFFFFF;    /* White text on dark */
  
  /* 테두리 색상 */
  --color-border: #C7C7CC;          /* System Gray 3 */
  --color-border-light: #E5E5EA;    /* System Gray 4 */
  
  /* ===== 타이포그래피 ===== */
  
  /* Apple SF Pro Display 기반 폰트 스택 */
  --font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
  --font-family-mono: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace;
  
  /* 폰트 크기 (Apple 표준) */
  --font-size-large-title: 34px;
  --font-size-title-1: 28px;
  --font-size-title-2: 22px;
  --font-size-title-3: 20px;
  --font-size-headline: 17px;
  --font-size-body: 17px;
  --font-size-callout: 16px;
  --font-size-subhead: 15px;
  --font-size-footnote: 13px;
  --font-size-caption-1: 12px;
  --font-size-caption-2: 11px;
  
  /* 폰트 굵기 */
  --font-weight-regular: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
  
  /* ===== 간격 및 레이아웃 ===== */
  
  /* Apple 표준 간격 (8pt 기반) */
  --spacing-xs: 4px;    /* 4pt */
  --spacing-sm: 8px;    /* 8pt */
  --spacing-md: 16px;   /* 16pt */
  --spacing-lg: 24px;   /* 24pt */
  --spacing-xl: 32px;   /* 32pt */
  --spacing-2xl: 48px;  /* 48pt */
  --spacing-3xl: 64px;  /* 64pt */
  
  /* 테두리 반경 */
  --border-radius-sm: 6px;
  --border-radius-md: 8px;
  --border-radius-lg: 12px;
  --border-radius-xl: 16px;
  --border-radius-2xl: 24px;
  
  /* 그림자 */
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1);
  --shadow-md: 0 4px 8px rgba(0, 0, 0, 0.12);
  --shadow-lg: 0 8px 16px rgba(0, 0, 0, 0.14);
  --shadow-xl: 0 12px 24px rgba(0, 0, 0, 0.16);
  
  /* ===== 애니메이션 ===== */
  
  /* Apple 표준 전환 시간 */
  --transition-fast: 0.15s ease;
  --transition-normal: 0.25s ease;
  --transition-slow: 0.35s ease;
  
  /* ===== 컴포넌트 높이 ===== */
  
  /* Apple 표준 컴포넌트 높이 */
  --height-button: 44px;      /* 터치 친화적 */
  --height-input: 44px;       /* 터치 친화적 */
  --height-navbar: 44px;      /* iOS 표준 */
  --height-tabbar: 49px;      /* iOS 표준 */
}

/* ===== 기본 스타일 ===== */

* {
  box-sizing: border-box;
}

html {
  font-family: var(--font-family);
  font-size: 16px;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  margin: 0;
  padding: 0;
  background-color: var(--color-background);
  color: var(--color-text-primary);
  font-size: var(--font-size-body);
  font-weight: var(--font-weight-regular);
}

/* ===== 타이포그래피 유틸리티 ===== */

.text-large-title {
  font-size: var(--font-size-large-title);
  font-weight: var(--font-weight-bold);
  line-height: 1.2;
}

.text-title-1 {
  font-size: var(--font-size-title-1);
  font-weight: var(--font-weight-bold);
  line-height: 1.3;
}

.text-title-2 {
  font-size: var(--font-size-title-2);
  font-weight: var(--font-weight-semibold);
  line-height: 1.3;
}

.text-title-3 {
  font-size: var(--font-size-title-3);
  font-weight: var(--font-weight-semibold);
  line-height: 1.4;
}

.text-headline {
  font-size: var(--font-size-headline);
  font-weight: var(--font-weight-semibold);
  line-height: 1.4;
}

.text-body {
  font-size: var(--font-size-body);
  font-weight: var(--font-weight-regular);
  line-height: 1.5;
}

.text-caption {
  font-size: var(--font-size-caption-1);
  font-weight: var(--font-weight-regular);
  line-height: 1.4;
  color: var(--color-text-secondary);
}

/* ===== 간격 유틸리티 ===== */

.p-xs { padding: var(--spacing-xs); }
.p-sm { padding: var(--spacing-sm); }
.p-md { padding: var(--spacing-md); }
.p-lg { padding: var(--spacing-lg); }
.p-xl { padding: var(--spacing-xl); }

.m-xs { margin: var(--spacing-xs); }
.m-sm { margin: var(--spacing-sm); }
.m-md { margin: var(--spacing-md); }
.m-lg { margin: var(--spacing-lg); }
.m-xl { margin: var(--spacing-xl); }

/* ===== Apple HIG 기반 컴포넌트 스타일 ===== */

/* 카드 컴포넌트 */
.card {
  background-color: var(--color-surface);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-sm);
  padding: var(--spacing-xl);
  margin-bottom: var(--spacing-lg);
}

/* 입력 필드 */
.input-field {
  width: 100%;
  height: var(--height-input);
  padding: var(--spacing-sm) var(--spacing-md);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-md);
  font-size: var(--font-size-body);
  font-family: var(--font-family);
  background-color: var(--color-surface);
  transition: border-color var(--transition-normal), box-shadow var(--transition-normal);
}

.input-field:focus {
  outline: none;
  border-color: var(--color-blue);
  box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.1);
}

.input-field::placeholder {
  color: var(--color-text-tertiary);
}

/* 버튼 컴포넌트 */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: var(--height-button);
  padding: var(--spacing-sm) var(--spacing-xl);
  border: none;
  border-radius: var(--border-radius-md);
  font-size: var(--font-size-body);
  font-weight: var(--font-weight-semibold);
  font-family: var(--font-family);
  cursor: pointer;
  transition: all var(--transition-normal);
  text-decoration: none;
}

.btn-primary {
  background-color: var(--color-blue);
  color: var(--color-text-inverse);
}

.btn-primary:hover {
  background-color: var(--color-blue-dark);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.btn-secondary {
  background-color: var(--color-surface);
  color: var(--color-blue);
  border: 1px solid var(--color-blue);
}

.btn-secondary:hover {
  background-color: var(--color-blue);
  color: var(--color-text-inverse);
}

/* 라벨 */
.input-label {
  display: block;
  font-size: var(--font-size-subhead);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-sm);
}

/* 섹션 구분선 */
.section-divider {
  height: 1px;
  background-color: var(--color-border-light);
  margin: var(--spacing-xl) 0;
}

/* 반응형 그리드 */
.grid {
  display: grid;
  gap: var(--spacing-lg);
}

.grid-cols-1 { grid-template-columns: 1fr; }
.grid-cols-2 { grid-template-columns: repeat(2, 1fr); }
.grid-cols-3 { grid-template-columns: repeat(3, 1fr); }

/* 대시보드 스타일 */
.dashboard {
  padding: var(--spacing-xl);
}

.stats-section {
  margin-bottom: var(--spacing-2xl);
}

.stats-section h1 {
  margin-bottom: var(--spacing-sm);
  color: var(--color-text-primary);
}

.stats-section p {
  margin-bottom: var(--spacing-xl);
  color: var(--color-text-secondary);
}

.quick-actions-section {
  margin-bottom: var(--spacing-2xl);
}

.quick-actions-section h2 {
  margin-bottom: var(--spacing-lg);
  color: var(--color-text-primary);
}

.recent-activities-section h2 {
  margin-bottom: var(--spacing-lg);
  color: var(--color-text-primary);
}

/* 색상 유틸리티 */
.text-blue { color: var(--color-blue); }
.text-green { color: var(--color-green); }
.text-orange { color: var(--color-orange); }
.text-red { color: var(--color-red); }

/* 숨김 타이틀 */
.hidden-title {
  color: #F2F2F7; /* 배경색과 동일하게 직접 설정 */
  user-select: none; /* 텍스트 선택 방지 */
}

/* 학생 등록 페이지 스타일 */
.student-registration-page {
  .info-display {
    background-color: var(--system-gray-6);
    border: 1px solid var(--system-gray-4);
    border-radius: var(--border-radius);
    padding: var(--spacing-3);
    margin-top: var(--spacing-2);
    
    .info-text {
      display: block;
      font-weight: 600;
      color: var(--system-blue);
      margin-bottom: var(--spacing-1);
    }
    
    .info-description {
      display: block;
      font-size: var(--font-size-caption);
      color: var(--system-gray);
    }
  }
  max-width: 1000px;
  margin: 0 auto;
  padding: var(--spacing-xl);
}

.page-header {
  margin-bottom: var(--spacing-2xl);
  text-align: center;
}

.page-header h1 {
  margin-bottom: var(--spacing-sm);
  color: var(--color-text-primary);
}

.page-header p {
  color: var(--color-text-secondary);
}

/* 폼 컨테이너 */
.form-container {
  background-color: var(--color-surface);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-2xl);
  box-shadow: var(--shadow-sm);
}

/* 폼 섹션 */
.form-section {
  margin-bottom: var(--spacing-2xl);
}

.section-title {
  margin-bottom: var(--spacing-lg);
  color: var(--color-text-primary);
  border-bottom: 2px solid var(--color-blue);
  padding-bottom: var(--spacing-sm);
}

/* 폼 그리드 */
.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-lg);
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

/* 입력 필드와 버튼 조합 */
.input-with-button {
  display: flex;
  gap: var(--spacing-sm);
}

.input-with-button .input-field {
  flex: 1;
}

.generate-btn {
  white-space: nowrap;
}

.generate-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 라디오 그룹 */
.radio-group {
  display: flex;
  gap: var(--spacing-lg);
}

.radio-label {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  cursor: pointer;
}

.radio-text {
  font-size: var(--font-size-body);
  color: var(--color-text-primary);
}

/* 체크박스 그룹 */
.checkbox-group {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--spacing-sm);
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  cursor: pointer;
}

.checkbox-text {
  font-size: var(--font-size-body);
  color: var(--color-text-primary);
}

/* 필수 표시 */
.required {
  color: var(--color-red);
}

/* 폼 액션 */
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-md);
  margin-top: var(--spacing-2xl);
  padding-top: var(--spacing-xl);
  border-top: 1px solid var(--color-border-light);
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .grid-cols-2,
  .grid-cols-3 {
    grid-template-columns: 1fr;
  }
  
  .dashboard {
    padding: var(--spacing-lg);
  }
  
  .student-registration-page {
    padding: var(--spacing-lg);
  }
  
  .form-container {
    padding: var(--spacing-lg);
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .checkbox-group {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .form-actions {
    flex-direction: column;
  }
}
</style>
