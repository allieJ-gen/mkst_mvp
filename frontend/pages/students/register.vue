<template>
  <div class="student-registration-page">
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
          <!-- 등원번호 -->
          <div class="form-group">
            <label class="input-label" for="attendanceNumber">
              등원번호 <span class="required">*</span>
            </label>
            <div class="input-with-button">
              <input
                id="attendanceNumber"
                v-model="form.attendanceNumber"
                type="text"
                class="input-field"
                placeholder="자동 생성"
                readonly
              />
              <button 
                type="button" 
                class="btn btn-secondary generate-btn"
                @click="generateAttendanceNumber"
              >
                생성
              </button>
            </div>
          </div>

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
              placeholder="학교명을 입력하세요"
              required
            />
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

          <!-- 생년월일 -->
          <div class="form-group">
            <label class="input-label" for="birthDate">
              생년월일 <span class="required">*</span>
            </label>
            <input
              id="birthDate"
              v-model="form.birthDate"
              type="date"
              class="input-field"
              required
            />
          </div>
        </div>
      </div>

      <!-- 연락처 정보 섹션 -->
      <div class="form-section">
        <h2 class="text-title-3 section-title">연락처 정보</h2>
        
        <div class="form-grid">
          <!-- 전화번호 -->
          <div class="form-group">
            <label class="input-label" for="phone">
              전화번호 <span class="required">*</span>
            </label>
            <input
              id="phone"
              v-model="form.phone"
              type="tel"
              class="input-field"
              placeholder="010-0000-0000"
              required
            />
          </div>

          <!-- 보호자 전화번호 -->
          <div class="form-group">
            <label class="input-label" for="parentPhone">
              보호자 전화번호 <span class="required">*</span>
            </label>
            <input
              id="parentPhone"
              v-model="form.parentPhone"
              type="tel"
              class="input-field"
              placeholder="010-0000-0000"
              required
            />
          </div>

          <!-- 주소 -->
          <div class="form-group full-width">
            <label class="input-label" for="address">
              주소
            </label>
            <input
              id="address"
              v-model="form.address"
              type="text"
              class="input-field"
              placeholder="주소를 입력하세요"
            />
          </div>
        </div>
      </div>

      <!-- 사물함 배정 섹션 -->
      <div class="form-section">
        <h2 class="text-title-3 section-title">사물함 배정</h2>
        
        <div class="form-grid">
          <!-- 사물함 번호 -->
          <div class="form-group">
            <label class="input-label" for="lockerNumber">
              사물함 번호
            </label>
            <input
              id="lockerNumber"
              v-model="form.lockerNumber"
              type="number"
              class="input-field"
              placeholder="자동 배정"
            />
          </div>

          <!-- 등록일 -->
          <div class="form-group">
            <label class="input-label" for="registrationDate">
              등록일 <span class="required">*</span>
            </label>
            <input
              id="registrationDate"
              v-model="form.registrationDate"
              type="date"
              class="input-field"
              required
            />
          </div>

          <!-- 등원 요일 -->
          <div class="form-group">
            <label class="input-label">등원 요일</label>
            <div class="checkbox-group">
              <label class="checkbox-label">
                <input
                  type="checkbox"
                  v-model="form.attendanceDays"
                  value="monday"
                />
                <span class="checkbox-text">월</span>
              </label>
              <label class="checkbox-label">
                <input
                  type="checkbox"
                  v-model="form.attendanceDays"
                  value="tuesday"
                />
                <span class="checkbox-text">화</span>
              </label>
              <label class="checkbox-label">
                <input
                  type="checkbox"
                  v-model="form.attendanceDays"
                  value="wednesday"
                />
                <span class="checkbox-text">수</span>
              </label>
              <label class="checkbox-label">
                <input
                  type="checkbox"
                  v-model="form.attendanceDays"
                  value="thursday"
                />
                <span class="checkbox-text">목</span>
              </label>
              <label class="checkbox-label">
                <input
                  type="checkbox"
                  v-model="form.attendanceDays"
                  value="friday"
                />
                <span class="checkbox-text">금</span>
              </label>
              <label class="checkbox-label">
                <input
                  type="checkbox"
                  v-model="form.attendanceDays"
                  value="saturday"
                />
                <span class="checkbox-text">토</span>
              </label>
              <label class="checkbox-label">
                <input
                  type="checkbox"
                  v-model="form.attendanceDays"
                  value="sunday"
                />
                <span class="checkbox-text">일</span>
              </label>
            </div>
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
</template>

<script setup>
// 페이지 메타데이터
definePageMeta({
  title: '학생 등록',
  layout: false // AppLayout을 사용하지 않음
})

// 반응형 데이터
const form = ref({
  attendanceNumber: '',
  name: '',
  school: '',
  grade: '',
  gender: '',
  birthDate: '',
  phone: '',
  parentPhone: '',
  address: '',
  lockerNumber: '',
  registrationDate: new Date().toISOString().split('T')[0],
  attendanceDays: []
})

// 등원번호 자동 생성
const generateAttendanceNumber = () => {
  const year = new Date().getFullYear()
  const random = Math.floor(Math.random() * 1000).toString().padStart(3, '0')
  form.value.attendanceNumber = `${year}${random}`
}

// 폼 제출 처리
const handleSubmit = async () => {
  if (validateForm()) {
    try {
      // TODO: API 호출 로직 구현
      console.log('학생 등록 폼 제출:', form.value)
      alert('학생이 성공적으로 등록되었습니다!')
      resetForm()
    } catch (error) {
      console.error('학생 등록 실패:', error)
      alert('학생 등록에 실패했습니다. 다시 시도해주세요.')
    }
  }
}

// 폼 유효성 검사
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
  if (!form.value.birthDate) {
    alert('생년월일을 입력해주세요.')
    return false
  }
  if (!form.value.phone) {
    alert('전화번호를 입력해주세요.')
    return false
  }
  if (!form.value.parentPhone) {
    alert('보호자 전화번호를 입력해주세요.')
    return false
  }
  if (!form.value.registrationDate) {
    alert('등록일을 입력해주세요.')
    return false
  }
  return true
}

// 폼 초기화
const resetForm = () => {
  form.value = {
    attendanceNumber: '',
    name: '',
    school: '',
    grade: '',
    gender: '',
    birthDate: '',
    phone: '',
    parentPhone: '',
    address: '',
    lockerNumber: '',
    registrationDate: new Date().toISOString().split('T')[0],
    attendanceDays: []
  }
}

// 취소 처리
const handleCancel = () => {
  if (confirm('입력한 내용이 사라집니다. 정말 취소하시겠습니까?')) {
    resetForm()
    // 대시보드로 돌아가기
    navigateTo('/')
  }
}

// 페이지 로드 시 등원번호 자동 생성
onMounted(() => {
  generateAttendanceNumber()
})
</script>

<style scoped>
/* 페이지 스타일 */
.student-registration-page {
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
