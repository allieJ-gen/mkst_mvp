<template>
  <div class="student-registration-form">
    <!-- 폼 헤더 -->
    <div class="form-header">
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
          </div>
        </div>
      </div>

      <!-- 연락처 정보 섹션 -->
      <div class="form-section">
        <h2 class="text-title-3 section-title">연락처 정보</h2>
        
        <div class="form-grid">
          <!-- 학생 휴대폰 -->
          <div class="form-group">
            <label class="input-label" for="studentPhone">
              학생 휴대폰
            </label>
            <input
              id="studentPhone"
              v-model="form.studentPhone"
              type="tel"
              class="input-field"
              placeholder="010-0000-0000"
              pattern="[0-9]{3}-[0-9]{4}-[0-9]{4}"
            />
          </div>

          <!-- 보호자 휴대폰 -->
          <div class="form-group">
            <label class="input-label" for="parentPhone">
              보호자 휴대폰 <span class="required">*</span>
            </label>
            <input
              id="parentPhone"
              v-model="form.parentPhone"
              type="tel"
              class="input-field"
              placeholder="010-0000-0000"
              pattern="[0-9]{3}-[0-9]{4}-[0-9]{4}"
              required
            />
          </div>
        </div>
      </div>

      <!-- 사물함 섹션 -->
      <div class="form-section">
        <h2 class="text-title-3 section-title">사물함 배정</h2>
        
        <div class="form-group">
          <label class="checkbox-label">
            <input
              type="checkbox"
              v-model="form.autoAssignLocker"
            />
            <span class="checkbox-text">자동으로 빈 사물함 배정</span>
          </label>
        </div>

        <div v-if="!form.autoAssignLocker" class="form-group">
          <label class="input-label" for="lockerNumber">
            사물함 번호 선택
          </label>
          <select
            id="lockerNumber"
            v-model="form.lockerNumber"
            class="input-field"
          >
            <option value="">사물함을 선택하세요</option>
            <option v-for="locker in availableLockers" :key="locker" :value="locker">
              {{ locker }}번
            </option>
          </select>
        </div>
      </div>

      <!-- 폼 액션 -->
      <div class="form-actions">
        <button type="button" class="btn btn-secondary" @click="handleCancel">
          취소
        </button>
        <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
          {{ isSubmitting ? '등록 중...' : '학생 등록' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'

// 폼 데이터
const form = reactive({
  attendanceNumber: '',
  name: '',
  school: '',
  grade: '',
  gender: '',
  firstAttendanceDate: '',
  studentPhone: '',
  parentPhone: '',
  autoAssignLocker: true,
  lockerNumber: ''
})

// 상태 관리
const isSubmitting = ref(false)

// 사용 가능한 사물함 (임시 데이터)
const availableLockers = computed(() => {
  // 실제로는 API에서 가져올 데이터
  return Array.from({ length: 50 }, (_, i) => i + 1)
})

// 등원번호 생성
const generateAttendanceNumber = async () => {
  try {
    // API 호출하여 등원번호 생성
    const response = await fetch('/api/students/generate-attendance-number/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        parent_phone: form.parentPhone
      })
    })
    
    if (response.ok) {
      const data = await response.json()
      form.attendanceNumber = data.attendance_number
    }
  } catch (error) {
    console.error('등원번호 생성 실패:', error)
    // 임시로 랜덤 번호 생성
    form.attendanceNumber = Math.floor(Math.random() * 90000) + 10000
  }
}

// 폼 제출
const handleSubmit = async () => {
  if (!validateForm()) return
  
  isSubmitting.value = true
  
  try {
    // API 호출하여 학생 등록
    const response = await fetch('/api/students/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(form)
    })
    
    if (response.ok) {
      // 성공 처리
      alert('학생이 성공적으로 등록되었습니다!')
      resetForm()
    } else {
      throw new Error('등록 실패')
    }
  } catch (error) {
    console.error('학생 등록 실패:', error)
    alert('학생 등록에 실패했습니다. 다시 시도해주세요.')
  } finally {
    isSubmitting.value = false
  }
}

// 폼 검증
const validateForm = () => {
  if (!form.name || !form.school || !form.grade || !form.gender || !form.firstAttendanceDate || !form.parentPhone) {
    alert('필수 항목을 모두 입력해주세요.')
    return false
  }
  
  if (form.parentPhone && !/^[0-9]{3}-[0-9]{4}-[0-9]{4}$/.test(form.parentPhone)) {
    alert('보호자 휴대폰 번호 형식이 올바르지 않습니다.')
    return false
  }
  
  return true
}

// 폼 초기화
const resetForm = () => {
  Object.assign(form, {
    attendanceNumber: '',
    name: '',
    school: '',
    grade: '',
    gender: '',
    firstAttendanceDate: '',
    studentPhone: '',
    parentPhone: '',
    autoAssignLocker: true,
    lockerNumber: ''
  })
}

// 취소 처리
const handleCancel = () => {
  if (confirm('입력한 내용이 모두 사라집니다. 정말 취소하시겠습니까?')) {
    resetForm()
  }
}
</script>

<style scoped>
.student-registration-form {
  max-width: 800px;
  margin: 0 auto;
}

.form-header {
  text-align: center;
  margin-bottom: var(--spacing-2xl);
}

.form-header h1 {
  margin-bottom: var(--spacing-sm);
  color: var(--color-text-primary);
}

.form-header p {
  color: var(--color-text-secondary);
}

.form-container {
  background-color: var(--color-surface);
  border-radius: var(--border-radius-xl);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
}

.form-section {
  padding: var(--spacing-xl);
  border-bottom: 1px solid var(--color-border-light);
}

.form-section:last-child {
  border-bottom: none;
}

.section-title {
  margin-bottom: var(--spacing-lg);
  color: var(--color-text-primary);
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-lg);
}

.form-group {
  display: flex;
  flex-direction: column;
}

.required {
  color: var(--color-red);
  margin-left: var(--spacing-xs);
}

.input-with-button {
  display: flex;
  gap: var(--spacing-sm);
}

.input-with-button .input-field {
  flex: 1;
}

.generate-btn {
  white-space: nowrap;
  min-width: 80px;
}

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

.radio-label input[type="radio"] {
  width: 18px;
  height: 18px;
  accent-color: var(--color-blue);
}

.radio-text {
  font-size: var(--font-size-body);
  color: var(--color-text-primary);
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  accent-color: var(--color-blue);
}

.checkbox-text {
  font-size: var(--font-size-body);
  color: var(--color-text-primary);
}

.form-actions {
  padding: var(--spacing-xl);
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-md);
  background-color: var(--color-secondary-surface);
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .form-actions .btn {
    width: 100%;
  }
}
</style>
