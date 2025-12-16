<template>
    <div class="dashboard-container">
        <div class="dashboard-header" >
            <h1 class="dashboard-title">批处理命令管理页面</h1>
            <div class="user-info">
                <span class="username">admin</span>
                <button class="logout-btn btn btn-outline btn-sm" @click="handleLogout">
                    <svg class="logout-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path
                            d="M9 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H9"
                            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                        <path d="M16 17L21 12L16 7" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                            stroke-linejoin="round" />
                        <path d="M21 12H9" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                            stroke-linejoin="round" />
                    </svg>
                    退出登录
                </button>
            </div>
        </div>

        <div class="dashboard-main" >
            <div class="dashboard-content">
                <div class="batch-command-section card">
                    <div class="section-header">
                        <h2 class="section-title">批处理命令编辑器</h2>
                    </div>

                    <div class="batch-command-container">
                        <div class="command-editor">
                            <!-- <label class="label" for="batch-command">批处理命令内容</label> -->
                            <textarea 
                                id="batch-command" 
                                class="input command-textarea" 
                                v-model="currentCommand" 
                                @input="checkChanges"
                                placeholder="请输入批处理命令..."
                            ></textarea>
                            <div class="command-info">
                                <span>{{ commandLength }} 字符</span>
                                <span v-if="hasChanges" class="changes-indicator">有未保存的更改</span>
                            </div>
                        </div>

                        <div class="action-buttons">
                            <div class="file-suffix-selector">
                                <label class="suffix-label">
                                    自定义文件后缀
                                </label>
                                <input 
                                    type="text" 
                                    v-model="fileSuffix" 
                                    class="suffix-input" 
                                    placeholder="输入文件后缀 (例如: txt)"
                                />
                            </div>
                            <button 
                                class="btn btn-outline btn-lg back-btn" 
                                @click="handleBack"
                            >
                                查询
                            </button>
                            <button 
                                class="btn btn-lg save-btn" 
                                @click="handleSave"
                                :disabled="!hasChanges || isSaving"
                            >
                                <span v-if="!isSaving">保存更改</span>
                                <span v-if="isSaving" class="loading-spinner"></span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <el-card class="sidebar" style="padding: 1%;">
                <Markdown/>
            </el-card>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'
import { removeToken } from '../utils/auth'
import Markdown from '../components/markdown.vue'

// 路由实例
const router = useRouter()

// 响应式状态
const originalCommand = ref('')
const currentCommand = ref('')
const hasChanges = ref(false)
const isSaving = ref(false)
const fileSuffix = ref('')

// 计算属性
const commandLength = computed(() => currentCommand.value.length)

// 方法定义
const fetchBatchCommand = async () => {
    try {
        // 验证文件后缀
        const suffix = fileSuffix.value.trim().toUpperCase()
        const restrictedSuffixes = ['PDF', 'JPG', 'PNG', 'GIF']
        
        if (restrictedSuffixes.includes(suffix)) {
            alert('不允许自定义修改 PDF、JPG、PNG、GIF 格式的文件！')
            return
        }
        
        // 从API获取批处理命令
        originalCommand.value = ''

        const resp = await api.post('/print/read_context', {
            type: fileSuffix.value.trim()
        })
        
        originalCommand.value = resp.bat_command
        currentCommand.value = originalCommand.value
    } catch (error) {
        console.error('获取批处理命令失败:', error)
        // 提供默认值
        originalCommand.value = '暂时没有这个类型的批处理命令'
        currentCommand.value = originalCommand.value
    }
}

const checkChanges = () => {
    hasChanges.value = currentCommand.value !== originalCommand.value
}

const handleSave = async () => {
    if (!hasChanges.value) return
    
    // 验证文件后缀
    const suffix = fileSuffix.value.trim().toUpperCase()
    const restrictedSuffixes = ['PDF', 'JPG', 'PNG', 'GIF']
    
    if (restrictedSuffixes.includes(suffix)) {
        alert('不允许自定义修改 PDF、JPG、PNG、GIF 格式的文件！')
        return
    }
    
    isSaving.value = true
    try {
        // 保存批处理命令
        await api.post('/print/write_context', {
            bat_command: currentCommand.value,
            type: fileSuffix.value.trim()
        })
        originalCommand.value = currentCommand.value
        hasChanges.value = false
        alert('批处理命令已保存成功！')
    } catch (error) {
        console.error('保存批处理命令失败:', error)
        alert('保存失败，请稍后重试')
    } finally {
        isSaving.value = false
    }
}

const handleBack = () => {
    fetchBatchCommand()
}

const handleLogout = () => {
    removeToken()
    router.push('/login')
}

</script>

<style scoped>
.dashboard-container {
    max-width: 100%;
    margin: 0 auto;
    padding: 20px;
}

.dashboard-main {
    display: flex;
    gap: 20px;
}

.sidebar {
    width: 30%;
    background-color: #ffffff;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    overflow: hidden;
}

.sidebar-menu {
    padding: 10px 0;
}

.menu-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 15px 20px;
    cursor: pointer;
    transition: all 0.3s ease;
    color: #34495e;
    font-weight: 500;
    text-decoration: none;
}

.menu-item:hover {
    background-color: #f5f5f5;
    color: #3498db;
}

.menu-item.active {
    background-color: #3498db;
    color: #ffffff;
}

.menu-icon {
    width: 20px;
    height: 20px;
    stroke-width: 2;
}

.dashboard-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
    padding-bottom: 15px;
    border-bottom: 1px solid #e0e0e0;
}

.dashboard-title {
    margin: 0;
    font-size: 24px;
    font-weight: 600;
    color: #2c3e50;
}

.user-info {
    display: flex;
    align-items: center;
    gap: 15px;
}

.username {
    font-weight: 500;
    color: #34495e;
}

.logout-btn {
    display: flex;
    align-items: center;
    gap: 5px;
    color: #2cad37;
}

.logout-icon {
    width: 16px;
    height: 16px;
}

.dashboard-content {
    display: flex;
    justify-content: center;
    width: 70%;
}

.batch-command-section {
    width: 100%;
    background-color: #ffffff;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 25px;
}

.section-header {
    margin-bottom: 20px;
}

.section-title {
    margin: 0;
    font-size: 20px;
    font-weight: 600;
    color: #2c3e50;
}

.batch-command-container {
    display: flex;
    flex-direction: column;
    gap: 25px;
}

.command-editor {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.label {
    font-weight: 500;
    color: #34495e;
    margin-bottom: 5px;
}

.command-textarea {
    width: 100%;
    min-height: 350px;
    padding: 15px;
    font-family: 'Courier New', Courier, monospace;
    font-size: 14px;
    line-height: 1.6;
    border: 1px solid #ddd;
    border-radius: 4px;
    resize: vertical;
    background-color: #fafafa;
    box-sizing: border-box;
}

.command-textarea:focus {
    outline: none;
    border-color: #29f596;
    box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.command-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 12px;
    color: #7f8c8d;
}

.changes-indicator {
    color: #e74c3c;
    font-weight: 500;
}

.action-buttons {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    gap: 15px;
    margin-top: 10px;
}

.file-suffix-selector {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-right: auto;
}

.suffix-label {
    display: flex;
    align-items: center;
    gap: 5px;
    padding-right: 10px;
    font-weight: 500;
    color: #34495e;
}

.suffix-input {
    width: 200px;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 14px;
}

.suffix-input:focus {
    outline: none;
    border-color: #3498db;
    box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.back-btn {
    color: #7f8c8d;
}

.save-btn {
    background-color: #07ca41;
    color: white;
}

.save-btn:hover:not(:disabled) {
    background-color: #17a114;
}

.save-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.loading-spinner {
    display: inline-block;
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    border-top-color: #fff;
    animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* 响应式设计 */
@media (max-width: 768px) {
    .dashboard-container {
        padding: 15px;
    }
    
    .dashboard-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 15px;
    }
    
    .user-info {
        align-self: flex-end;
    }
    
    .batch-command-section {
        padding: 20px;
    }
    
    .command-textarea {
        min-height: 200px;
    }
    
    .action-buttons {
        flex-direction: column;
        align-items: flex-start;
    }
    
    .file-suffix-selector {
        margin-right: 0;
        margin-bottom: 10px;
        width: 100%;
    }
    
    .suffix-input {
        width: 100%;
    }
}
</style>