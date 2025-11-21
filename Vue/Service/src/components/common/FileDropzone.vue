<template>
  <div 
    class="dropzone"
    @dragover.prevent="handleDragOver"
    @dragleave.prevent="handleDragLeave"
    @drop.prevent="handleDrop"
    @click="triggerFileInput"
  >
    <input 
      type="file" 
      ref="fileInput" 
      class="file-input" 
      @change="handleFileSelect"
      accept=".pdf,.jpg,.jpeg,.png,.gif,.bmp,.tiff"
      multiple
    >
    
    <div class="dropzone-content">
      <div class="icon-container">
        <svg 
          class="upload-icon" 
          viewBox="0 0 24 24" 
          fill="none" 
          xmlns="http://www.w3.org/2000/svg"
        >
          <path 
            d="M12 16L8 12M12 16L16 12M12 16V8M20 12C20 16.4183 16.4183 20 12 20C7.58172 20 4 16.4183 4 12C4 7.58172 7.58172 4 12 4C16.4183 4 20 7.58172 20 12Z" 
            stroke="currentColor" 
            stroke-width="2" 
            stroke-linecap="round" 
            stroke-linejoin="round"
          />
        </svg>
      </div>
      
      <h3 class="dropzone-title">拖放文件到此处上传</h3>
      <p class="dropzone-subtitle">
        或点击选择文件 (支持 PDF, JPG, PNG, GIF 等格式)
      </p>
      
      <div v-if="isDragging" class="drag-overlay">
        <p>释放文件开始上传</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const fileInput = ref(null)
const isDragging = ref(false)

// 1. 定义组件要触发的事件
const emit = defineEmits(['files-selected'])

// 触发文件选择对话框
const triggerFileInput = () => {
  fileInput.value.click()
}

// 处理文件选择
const handleFileSelect = (event) => {
  const files = event.target.files
  if (files.length > 0) {
    emit('files-selected', Array.from(files))
    // 重置文件输入，以便能重复选择同一个文件
    event.target.value = null
  }
}

// 处理拖入事件
const handleDragOver = () => {
  isDragging.value = true
}

// 处理拖离事件
const handleDragLeave = () => {
  isDragging.value = false
}

// 处理放置事件
const handleDrop = (event) => {
  isDragging.value = false
  const files = event.dataTransfer.files
  if (files.length > 0) {
    emit('files-selected', Array.from(files))
  }
}
</script>

<style scoped>
.dropzone {
  border: 2px dashed var(--border-color);
  border-radius: 12px;
  padding: 40px 20px;
  text-align: center;
  cursor: pointer;
  transition: var(--transition-default);
  position: relative;
  overflow: hidden;
  background-color: var(--primary-light);
}

.dropzone:hover {
  border-color: var(--primary-color);
  background-color: rgba(66, 185, 131, 0.1);
}

.file-input {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  opacity: 0;
  cursor: pointer;
}

.dropzone-content {
  position: relative;
  z-index: 1;
}

.icon-container {
  width: 60px;
  height: 60px;
  margin: 0 auto 20px;
  background-color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.upload-icon {
  width: 30px;
  height: 30px;
  color: var(--primary-color);
}

.dropzone-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-color);
  margin-bottom: 10px;
}

.dropzone-subtitle {
  font-size: 14px;
  color: var(--text-light);
  max-width: 400px;
  margin: 0 auto;
}

.drag-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(66, 185, 131, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: var(--transition-default);
  z-index: 0;
}

.dropzone:has(.drag-overlay) {
  border-color: var(--primary-color);
}

.dropzone:has(.drag-overlay):hover .drag-overlay {
  opacity: 1;
}

.drag-overlay p {
  font-size: 16px;
  font-weight: 500;
  color: var(--primary-dark);
}
</style>