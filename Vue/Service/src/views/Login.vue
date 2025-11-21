<template>
  <div class="login-container">
    <div class="login-bg"></div>
    
    <div class="login-card slide-enter-active">
      <div class="login-header">
        <div class="logo">
          <svg 
            class="logo-icon" 
            viewBox="0 0 24 24" 
            fill="none" 
            xmlns="http://www.w3.org/2000/svg"
          >
            <path 
              d="M6 9V2H18V9" 
              stroke="currentColor" 
              stroke-width="2" 
              stroke-linecap="round" 
              stroke-linejoin="round"
            />
            <path 
              d="M6 18H4C3.46957 18 2.96086 17.7893 2.58579 17.4142C2.21071 17.0391 2 16.5304 2 16V15C2 14.4696 2.21071 13.9609 2.58579 13.5858C2.96086 13.2107 3.46957 13 4 13H20C20.5304 13 21.0391 13.2107 21.4142 13.5858C21.7893 13.9609 22 14.4696 22 15V16C22 16.5304 21.7893 17.0391 21.4142 17.4142C21.0391 17.7893 20.5304 18 20 18H18" 
              stroke="currentColor" 
              stroke-width="2" 
              stroke-linecap="round" 
              stroke-linejoin="round"
            />
            <path 
              d="M6 13V18H18V13" 
              stroke="currentColor" 
              stroke-width="2" 
              stroke-linecap="round" 
              stroke-linejoin="round"
            />
            <path 
              d="M10 15H14" 
              stroke="currentColor" 
              stroke-width="2" 
              stroke-linecap="round" 
              stroke-linejoin="round"
            />
          </svg>
          <span class="logo-text">{{ appTitle }}</span>
        </div>
        <h2 class="login-title">用户登录</h2>
      </div>
      
      <form class="login-form" @submit.prevent="handleLogin">
        <div class="form-group">
          <label class="label" for="username">用户名</label>
          <div class="input-group">
            <div class="input-icon">
              <svg 
                viewBox="0 0 24 24" 
                fill="none" 
                xmlns="http://www.w3.org/2000/svg"
              >
                <path 
                  d="M20 21V19C20 18.4696 19.7893 17.9609 19.4142 17.5858C19.0391 17.2107 18.5304 17 18 17H6C5.46957 17 4.96086 17.2107 4.58579 17.5858C4.21071 17.9609 4 18.4696 4 19V21" 
                  stroke="currentColor" 
                  stroke-width="2" 
                  stroke-linecap="round" 
                  stroke-linejoin="round"
                />
                <path 
                  d="M12 11C13.6569 11 15 9.65685 15 8C15 6.34315 13.6569 5 12 5C10.3431 5 9 6.34315 9 8C9 9.65685 10.3431 11 12 11Z" 
                  stroke="currentColor" 
                  stroke-width="2" 
                  stroke-linecap="round" 
                  stroke-linejoin="round"
                />
                <path 
                  d="M4 11V7C4 6.46957 4.21071 5.96086 4.58579 5.58579C4.96086 5.21071 5.46957 5 6 5H18C18.5304 5 19.0391 5.21071 19.4142 5.58579C19.7893 5.96086 20 6.46957 20 7V11" 
                  stroke="currentColor" 
                  stroke-width="2" 
                  stroke-linecap="round" 
                  stroke-linejoin="round"
                />
              </svg>
            </div>
            <input 
              id="username" 
              class="input" 
              v-model="username" 
              placeholder="请输入用户名" 
              required
              autocomplete="username"
            >
          </div>
        </div>
        
        <div class="form-group">
          <label class="label" for="password">密码</label>
          <div class="input-group">
            <div class="input-icon">
              <svg 
                viewBox="0 0 24 24" 
                fill="none" 
                xmlns="http://www.w3.org/2000/svg"
              >
                <path 
                  d="M12 15C13.6569 15 15 13.6569 15 12C15 10.3431 13.6569 9 12 9C10.3431 9 9 10.3431 9 12C9 13.6569 10.3431 15 12 15Z" 
                  stroke="currentColor" 
                  stroke-width="2" 
                  stroke-linecap="round" 
                  stroke-linejoin="round"
                />
                <path 
                  d="M19.4 15C19.2669 15.3016 19.256 15.6362 19.366 15.9523C19.476 16.2684 19.7025 16.5408 19.9993 16.7393C20.2961 16.9379 20.6427 17.0445 21 17.0445C21.3573 17.0445 21.7039 16.9379 22.0007 16.7393C22.2975 16.5408 22.524 16.2684 22.634 15.9523C22.744 15.6362 22.7331 15.3016 22.6 15C22.4669 14.6984 22.456 14.3638 22.566 14.0477C22.676 13.7316 22.9025 13.4592 23.1993 13.2607C23.4961 13.0621 23.8427 12.9555 24.2 12.9555C24.5573 12.9555 24.9039 13.0621 25.2007 13.2607C25.4975 13.4592 25.724 13.7316 25.834 14.0477C25.944 14.3638 25.9331 14.6984 25.8 15" 
                  stroke="currentColor" 
                  stroke-width="2" 
                  stroke-linecap="round" 
                  stroke-linejoin="round"
                />
                <path 
                  d="M1 15C1.13313 15.3016 1.14401 15.6362 1.03401 15.9523C0.924014 16.2684 0.697527 16.5408 0.400735 16.7393C0.103943 16.9379 -0.24262 17.0445 -0.6 17.0445C-0.957284 17.0445 -1.30394 16.9379 -1.60073 16.7393C-1.89752 16.5408 -2.12401 16.2684 -2.23401 15.9523C-2.34401 15.6362 -2.33313 15.3016 -2.2 15C-2.33313 14.6984 -2.34401 14.3638 -2.23401 14.0477C-2.12401 13.7316 -1.89752 13.4592 -1.60073 13.2607C-1.30394 13.0621 -0.957284 12.9555 -0.6 12.9555C-0.24262 12.9555 0.103943 13.0621 0.400735 13.2607C0.697527 13.4592 0.924014 13.7316 1.03401 14.0477C1.14401 14.3638 1.13313 14.6984 1 15Z" 
                  stroke="currentColor" 
                  stroke-width="2" 
                  stroke-linecap="round" 
                  stroke-linejoin="round"
                />
                <path 
                  d="M8.59 11C8.23555 10.4258 8.27618 9.72406 8.70342 9.17365C9.13066 8.62324 9.89664 8.33333 10.6667 8.33333H13.3333C14.1033 8.33333 14.8693 8.62324 15.2966 9.17365C15.7238 9.72406 15.7644 10.4258 15.41 11L13.21 14.3333C12.9579 14.6874 12.6005 14.9427 12.1849 15.0663C11.7694 15.1899 11.3256 15.1801 10.9221 15.0444C10.5185 14.9087 10.1724 14.6521 10 14.3333L8.59 11Z" 
                  stroke="currentColor" 
                  stroke-width="2" 
                  stroke-linecap="round" 
                  stroke-linejoin="round"
                />
              </svg>
            </div>
            <input 
              id="password" 
              class="input" 
              v-model="password" 
              placeholder="请输入密码" 
              required
              :type="showPassword ? 'text' : 'password'"
              autocomplete="current-password"
            >
            <button 
              type="button" 
              class="toggle-password" 
              @click="showPassword = !showPassword"
              aria-label="显示/隐藏密码"
            >
              <svg 
                v-if="!showPassword" 
                viewBox="0 0 24 24" 
                fill="none" 
                xmlns="http://www.w3.org/2000/svg"
              >
                <path 
                  d="M12 4.5C7 4.5 2.73 7.61 1 12C2.73 16.39 7 19.5 12 19.5C17 19.5 21.27 16.39 23 12C21.27 7.61 17 4.5 12 4.5Z" 
                  stroke="currentColor" 
                  stroke-width="2" 
                  stroke-linecap="round" 
                  stroke-linejoin="round"
                />
                <path 
                  d="M12 12V12.01" 
                  stroke="currentColor" 
                  stroke-width="2" 
                  stroke-linecap="round" 
                  stroke-linejoin="round"
                />
              </svg>
              <svg 
                v-if="showPassword" 
                viewBox="0 0 24 24" 
                fill="none" 
                xmlns="http://www.w3.org/2000/svg"
              >
                <path 
                  d="M2 12C2 17.5228 6.47715 22 12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12Z" 
                  stroke="currentColor" 
                  stroke-width="2" 
                  stroke-linecap="round" 
                  stroke-linejoin="round"
                />
                <path 
                  d="M15.5 8C16.8807 8 18 9.11929 18 10.5C18 11.8807 16.8807 13 15.5 13C14.1193 13 13 11.8807 13 10.5C13 9.11929 14.1193 8 15.5 8Z" 
                  stroke="currentColor" 
                  stroke-width="2" 
                  stroke-linecap="round" 
                  stroke-linejoin="round"
                />
                <path 
                  d="M8.5 8C9.88071 8 11 9.11929 11 10.5C11 11.8807 9.88071 13 8.5 13C7.11929 13 6 11.8807 6 10.5C6 9.11929 7.11929 8 8.5 8Z" 
                  stroke="currentColor" 
                  stroke-width="2" 
                  stroke-linecap="round" 
                  stroke-linejoin="round"
                />
                <path 
                  d="M2 12H22" 
                  stroke="currentColor" 
                  stroke-width="2" 
                  stroke-linecap="round" 
                  stroke-linejoin="round"
                />
              </svg>
            </button>
          </div>
        </div>
        
        <div class="form-actions">
          <button 
            type="submit" 
            class="btn btn-lg login-btn"
            :disabled="isLoading"
          >
            <span v-if="!isLoading">登录</span>
            <span v-if="isLoading" class="loading-container">
              <span class="loading-spinner"></span>
              <span class="loading-text">登录中...</span>
            </span>
          </button>
        </div>
        
        <div class="error-message" v-if="error" :class="{'slide-enter-active': showError}">
          <svg 
            class="error-icon" 
            viewBox="0 0 24 24" 
            fill="none" 
            xmlns="http://www.w3.org/2000/svg"
          >
            <path 
              d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" 
              stroke="currentColor" 
              stroke-width="2" 
              stroke-linecap="round" 
              stroke-linejoin="round"
            />
            <path 
              d="M12 6V12L16 14" 
              stroke="currentColor" 
              stroke-width="2" 
              stroke-linecap="round" 
              stroke-linejoin="round"
            />
          </svg>
          {{ error }}
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { setLoginCookie } from '../utils/auth'

const router = useRouter()

const appTitle = import.meta.env.VITE_APP_TITLE || 'GreenPrint打印系统'
const username = ref('')
const password = ref('')
const showPassword = ref(false)
const error = ref('')
const showError = ref(false)
const isLoading = ref(false)

// 处理登录
const handleLogin = async () => {
  // 重置错误状态
  error.value = ''
  showError.value = false
  
  // 基本验证
  if (!username.value.trim()) {
    error.value = '请输入用户名'
    showError.value = true
    return
  }
  
  if (!password.value.trim()) {
    error.value = '请输入密码'
    showError.value = true
    return
  }
  
  // 开始登录流程
  isLoading.value = true
  
  try {
    const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/login`, {
      username: username.value,
      password: password.value
    })
    
    const { username: resName, token } = response.data
    
    if (response.status === 200 && token) {
      setLoginCookie(resName, token)
      router.push('/print')
    } else {
      error.value = response.data.error || '用户名或密码错误'
      showError.value = true
    }
  } catch (err) {
    console.error('登录请求失败:', err)
    if (err.response?.data?.error) {
      error.value = err.response.data.error
    } else {
      error.value = '网络错误，请稍后再试'
    }
    showError.value = true
  } finally {
    isLoading.value = false
  }
}

// 挂载时聚焦用户名输入框
onMounted(() => {
  const usernameInput = document.getElementById('username')
  if (usernameInput) {
    usernameInput.focus()
  }
  
  // 检查URL中是否有错误参数
  const urlParams = new URLSearchParams(window.location.search)
  const errorParam = urlParams.get('error')
  if (errorParam) {
    error.value = decodeURIComponent(errorParam)
    showError.value = true
  }
})
</script>

<style scoped>
.login-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  position: relative;
  padding: 20px;
}

.login-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: var(--primary-light);
  z-index: 0;
  background-image: 
    radial-gradient(circle at 25% 15%, rgba(66, 185, 131, 0.05) 0%, transparent 50%),
    radial-gradient(circle at 75% 85%, rgba(66, 185, 131, 0.05) 0%, transparent 50%);
}

.login-card {
  width: 100%;
  max-width: 420px;
  background-color: white;
  border-radius: 20px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.05);
  padding: 40px 30px;
  position: relative;
  z-index: 1;
}

.login-header {
  margin-bottom: 30px;
  text-align: center;
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
}

.logo-icon {
  width: 36px;
  height: 36px;
  color: var(--primary-color);
  margin-right: 10px;
}

.logo-text {
  font-size: 24px;
  font-weight: 700;
  color: var(--primary-color);
}

.login-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--text-color);
}

.login-form {
  margin-top: 20px;
}

.form-group {
  margin-bottom: 24px;
}

.input-group {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 12px;
  pointer-events: none;
}

.input-icon svg {
  width: 18px;
  height: 18px;
  color: var(--text-light);
}

.input {
  padding-left: 40px;
}

.toggle-password {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.toggle-password svg {
  width: 18px;
  height: 18px;
  color: var(--text-light);
  transition: var(--transition-default);
}

.toggle-password:hover svg {
  color: var(--primary-color);
}

.form-actions {
  margin-top: 40px;
}

.login-btn {
  width: 100%;
  background-color: var(--primary-color);
  font-size: 16px;
}

.login-btn:hover {
  background-color: var(--primary-dark);
}

.loading-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.loading-text {
  font-weight: 500;
}

.error-message {
  background-color: rgba(255, 77, 79, 0.1);
  color: var(--error-color);
  padding: 12px 16px;
  border-radius: 8px;
  margin-top: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  opacity: 0;
  transform: translateY(10px);
}

.error-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

/* 动画效果 */
.slide-enter-active {
  animation: slideIn 0.3s ease forwards;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>