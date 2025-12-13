<template>
    <div class="dashboard-container">
        <div class="dashboard-header">
            <h1 class="dashboard-title">EThink 社团专用打印页面</h1>
            <div class="user-info">
                <span class="username">{{ username }}</span>
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

        <div class="dashboard-content">
            <div class="main-layout" v-if="!isMobile">
                <!-- 左侧打印机状态 -->
                <div class="printers-sidebar card">
                    <div class="section-header">
                        <h2 class="section-title">打印机状态</h2>
                    </div>

                    <div class="printers-list">
                        <div class="printer-item" v-for="printer in printers" :key="printer.id"
                            :class="{ 'online': printer.status === 'online', 'offline': printer.status === 'offline' }">
                            <div class="printer-info">
                                <div class="printer-name">
                                    {{ printer.name }}
                                    <span class="printer-status-indicator"></span>
                                </div>
                                <div class="printer-details">
                                    <p>位置: {{ printer.location || '未设置' }}</p>
                                    <p>类型: {{ getPrinterTypeLabel(printer.type) }}</p>
                                    <p>任务队列: {{ printer.queue_count || 0 }} 个</p>
                                </div>
                            </div>
                            <div class="printer-status-text">
                                {{ printer.status === 'online' ? '在线' : '离线' }}
                            </div>
                        </div>
                    </div>
                </div>

                <div class="print-controls">
                    <!-- 上传区域 -->
                    <div class="upload-section card">
                        <div class="section-header">
                            <h2 class="section-title">上传打印文件</h2>
                        </div>

                        <div class="upload-area">
                            <FileDropzone @files-selected="handleFilesSelected" />

                            <div v-if="selectedFiles.length > 0" class="selected-files">
                                <h3 class="files-title">已选择文件 ({{ selectedFiles.length }})</h3>
                                <div class="files-list">
                                    <FileItem v-for="file in selectedFiles" :key="file.uid" :file="file"
                                        @remove="removeFile(file)" />
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- 打印选项 -->
                    <div class="print-options card">
                        <div class="section-header">
                            <h2 class="section-title">打印设置</h2>
                        </div>

                        <div class="options-vertical">
                            <div class="option-group">
                                <PrinterSelect :printers="printers" v-model="selectedPrinterId"
                                    @change="onPrinterChange" />
                            </div>

                            <!-- 打印份数 -->
                            <div class="option-group">
                                <label class="label" for="copies">打印份数</label>
                                <div class="option-wrapper">
                                    <input id="copies" class="input" type="number" v-model.number="copies" min="1"
                                        max="99" :disabled="!selectedPrinterId">
                                    <div v-if="!selectedPrinterId" class="placeholder-overlay">选择后展示</div>
                                </div>
                            </div>

                            <!-- 打印模式 -->
                            <div class="option-group">
                                <label class="label" for="print-mode">打印模式</label>
                                <div class="option-wrapper">
                                    <select id="print-mode" class="input" v-model="printMode"
                                        :disabled="!selectedPrinterId">
                                        <option value="1">单面打印</option>
                                        <option value="2">双面打印</option>
                                    </select>
                                    <div v-if="!selectedPrinterId" class="placeholder-overlay">选择后展示</div>
                                </div>
                            </div>

                            <!-- 颜色模式 -->
                            <div class="option-group">
                                <label class="label" for="color-mode">打印方向</label>
                                <div class="option-wrapper">
                                    <select id="color-mode" class="input" v-model="flatMode"
                                        :disabled="!selectedPrinterId">
                                        <option value="h">纵向打印</option>
                                        <option value="v">横向打印</option>
                                    </select>
                                    <div v-if="!selectedPrinterId" class="placeholder-overlay">选择后展示</div>
                                </div>
                            </div>

                            <!-- 操作按钮 -->
                            <div class="print-actions">
                                <button class="btn btn-lg print-btn" @click="submitPrintJob"
                                    :disabled="!canSubmit || isSubmitting || !selectedPrinterId">
                                    <span v-if="!isSubmitting">
                                        <svg class="print-icon" viewBox="0 0 24 24" fill="none"
                                            xmlns="http://www.w3.org/2000/svg">
                                            <path d="M6 9V2H18V9" stroke="currentColor" stroke-width="2"
                                                stroke-linecap="round" stroke-linejoin="round" />
                                            <path
                                                d="M6 18H4C3.46957 18 2.96086 17.7893 2.58579 17.4142C2.21071 17.0391 2 16.5304 2 16V15C2 14.4696 2.21071 13.9609 2.58579 13.5858C2.96086 13.2107 3.46957 13 4 13H20C20.5304 13 21.0391 13.2107 21.4142 13.5858C21.7893 13.9609 22 14.4696 22 15V16C22 16.5304 21.7893 17.0391 21.4142 17.4142C21.0391 17.7893 20.5304 18 20 18H18"
                                                stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                                stroke-linejoin="round" />
                                            <path d="M6 13V18H18V13" stroke="currentColor" stroke-width="2"
                                                stroke-linecap="round" stroke-linejoin="round" />
                                            <path d="M10 15H14" stroke="currentColor" stroke-width="2"
                                                stroke-linecap="round" stroke-linejoin="round" />
                                        </svg>
                                        提交打印任务
                                    </span>
                                    <span v-if="isSubmitting" class="loading-container">
                                        <span class="loading-spinner"></span>
                                        <span class="loading-text">提交中...</span>
                                    </span>
                                </button>

                                <button class="btn btn-outline btn-lg clear-btn" @click="clearFiles"
                                    :disabled="selectedFiles.length === 0 || isSubmitting">
                                    清空选择
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- 当前打印任务区域 -->
                    <div class="active-jobs card">
                        <div class="section-header">
                            <h2 class="section-title" style="flex-grow: 1;">
                                当前打印任务
                            </h2>
                            <button class="refresh-btn btn btn-outline btn-sm" style="margin-right: 10px;"
                                @click="ClearActiveJobs">
                                <span>清空</span>
                            </button>
                            <button class="refresh-btn btn btn-outline btn-sm" @click="fetchActiveJobs"
                                :disabled="isRefreshingJobs">
                                <span v-if="!isRefreshingJobs">刷新</span>
                                <span v-if="isRefreshingJobs" class="loading-spinner"></span>
                            </button>
                        </div>

                        <div class="jobs-list">
                            <div v-if="activeJobs.length > 0" class="jobs-table">
                                <div class="table-header">
                                    <div class="table-cell">任务ID</div>
                                    <div class="table-cell">文件名</div>
                                    <div class="table-cell">打印机</div>
                                    <div class="table-cell">份数</div>
                                    <div class="table-cell">状态</div>
                                    <div class="table-cell">进度</div>
                                    <div class="table-cell">操作</div>
                                </div>

                                <div class="table-row" v-for="job in activeJobs" :key="job.id"
                                    :class="{ 'job-completed': job.status === 'completed' }">
                                    <div class="table-cell">{{ job.id }}</div>
                                    <div class="table-cell">{{ job.filename }}</div>
                                    <div class="table-cell">{{ job.printer_name }}</div>
                                    <div class="table-cell">{{ job.copies }}</div>
                                    <div class="table-cell">
                                        <span class="status-badge" :class="getStatusBadgeClass(job.status)">
                                            {{ getStatusLabel(job.status) }}
                                        </span>
                                    </div>
                                    <div class="table-cell">
                                        <div v-if="job.status !== 'completed'" class="progress-container">
                                            <div class="progress-bar" :style="{ width: `${job.progress}%` }"
                                                :class="getProgressBarClass(job.status)"></div>
                                            <span class="progress-text">{{ job.progress }}%</span>
                                        </div>
                                        <div v-if="job.status === 'completed'" class="progress-text">完成</div>
                                    </div>
                                    <div class="table-cell">
                                        <button class="action-btn btn btn-outline btn-sm" @click="cancelJob(job.id)"
                                            :disabled="['completed', 'cancelled', 'failed'].includes(job.status)">
                                            取消
                                        </button>
                                    </div>
                                </div>
                            </div>

                            <div v-if="activeJobs.length === 0 && !isRefreshingJobs" class="empty-state">
                                <p>当前没有正在进行的打印任务</p>
                            </div>
                            <div v-if="isRefreshingJobs" class="loading-state">
                                <span class="loading-spinner"></span>
                                <p>正在加载任务...</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <!------------------------------------------------------------------------------------------->
            <!-- 移动端布局 -->
            <div class="mobile-layout" v-if="isMobile">
                <!-- 打印机状态 -->
                <div class="printers-status card">
                    <div class="section-header">
                        <h2 class="section-title">打印机状态</h2>
                    </div>

                    <div class="printers-list">
                        <div class="mobile-list-item printer-item" v-for="printer in printers" :key="printer.id"
                            :class="{ 'online': printer.status === 'online', 'offline': printer.status === 'offline' }">
                            <div class="mobile-list-item__main">
                                <div class="printer-name">
                                    {{ printer.name }}
                                    <span class="printer-status-indicator"></span>
                                </div>
                                <div class="printer-details">
                                    <p>位置: {{ printer.location || '未设置' }}</p>
                                    <p>类型: {{ getPrinterTypeLabel(printer.type) }}</p>
                                </div>
                            </div>
                            <div class="mobile-list-item__extra printer-job-count">
                                {{ printer.queue_count || 0 }} 个任务
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 上传区域 -->
                <div class="upload-section card">
                    <div class="section-header">
                        <h2 class="section-title">上传打印文件</h2>
                    </div>

                    <div class="upload-area">
                        <FileDropzone @files-selected="handleFilesSelected" />

                        <div v-if="selectedFiles.length > 0" class="selected-files">
                            <h3 class="files-title">已选择文件 ({{ selectedFiles.length }})</h3>
                            <div class="files-list">
                                <FileItem v-for="file in selectedFiles" :key="file.uid" :file="file"
                                    @remove="removeFile(file)" />
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 打印选项 -->
                <div class="print-options card">
                    <div class="section-header">
                        <h2 class="section-title">打印设置</h2>
                    </div>

                    <el-collapse accordion>
                        <el-collapse-item title="选择打印机">
                            <PrinterSelect :printers="printers" v-model="selectedPrinterId" @change="onPrinterChange" />
                        </el-collapse-item>

                        <el-collapse-item title="打印设置">
                            <div class="mobile-options">
                                <div class="option-group">
                                    <label class="label" for="copies-m">打印份数</label>
                                    <input id="copies-m" class="input" type="number" v-model.number="copies" min="1"
                                        max="99" :disabled="!selectedPrinterId">
                                    <span v-if="!selectedPrinterId" class="placeholder-text">选择后展示</span>
                                </div>

                                <div class="option-group">
                                    <label class="label" for="print-mode-m">打印模式</label>
                                    <select id="print-mode-m" class="input" v-model="printMode"
                                        :disabled="!selectedPrinterId">
                                        <option value="1">单面打印</option>
                                        <option value="2">双面打印</option>
                                    </select>
                                    <span v-if="!selectedPrinterId" class="placeholder-text">选择后展示</span>
                                </div>

                                <div class="option-group">
                                    <label class="label" for="color-mode-m">打印方向</label>
                                    <select id="color-mode-m" class="input" v-model="flatMode"
                                        :disabled="!selectedPrinterId">
                                        <option value="h">纵向打印</option>
                                        <option value="v">横向打印</option>
                                    </select>
                                    <span v-if="!selectedPrinterId" class="placeholder-text">选择后展示</span>
                                </div>
                            </div>
                        </el-collapse-item>
                    </el-collapse>

                    <div class="print-actions">
                        <button class="btn btn-lg print-btn" @click="submitPrintJob"
                            :disabled="!canSubmit || isSubmitting || !selectedPrinterId">
                            <span v-if="!isSubmitting">提交打印任务</span>
                            <span v-if="isSubmitting">提交中...</span>
                        </button>

                        <button class="btn btn-outline btn-lg clear-btn" @click="clearFiles"
                            :disabled="selectedFiles.length === 0 || isSubmitting">
                            清空选择
                        </button>
                    </div>
                </div>

                <!-- 当前打印任务 -->
                <div class="active-jobs card">
                    <div class="section-header">
                        <h2 class="section-title" style="flex-grow: 1;">当前打印任务</h2>
                        <button class="refresh-btn btn btn-outline btn-sm" style="margin-right: 10px;"
                            @click="ClearActiveJobs">
                            <span>清空</span>
                        </button>
                        <button class="refresh-btn btn btn-outline btn-sm" @click="fetchActiveJobs"
                            :disabled="isRefreshingJobs">
                            <span v-if="!isRefreshingJobs">刷新</span>
                            <span v-if="isRefreshingJobs" class="loading-spinner"></span>
                        </button>
                    </div>

                    <div class="jobs-list">
                        <div v-if="activeJobs.length > 0">
                            <div class="mobile-list-item" v-for="job in activeJobs" :key="job.id"
                                :class="{ 'job-completed': job.status === 'completed' }">
                                <div class="mobile-list-item__main">
                                    <div class="job-title">{{ job.filename }}</div>
                                    <div class="job-meta">
                                        <span>ID: {{ job.id }}</span>
                                        <span>打印机: {{ job.printer_name }}</span>
                                        <span>份数: {{ job.copies }}</span>
                                    </div>
                                    <div class="job-progress">
                                        <span class="status-badge" :class="getStatusBadgeClass(job.status)">
                                            {{ getStatusLabel(job.status) }}
                                        </span>
                                        <div v-if="job.status !== 'completed'" class="progress-container">
                                            <div class="progress-bar" :style="{ width: `${job.progress}%` }"
                                                :class="getProgressBarClass(job.status)"></div>
                                        </div>
                                    </div>
                                </div>
                                <div class="mobile-list-item__extra">
                                    <button class="action-btn btn btn-outline btn-sm" @click="cancelJob(job.id)"
                                        :disabled="['completed', 'cancelled', 'failed'].includes(job.status)">
                                        取消
                                    </button>
                                </div>
                            </div>
                        </div>

                        <div v-if="activeJobs.length === 0 && !isRefreshingJobs" class="empty-state">
                            <p>当前没有正在进行的打印任务</p>
                        </div>
                        <div v-if="isRefreshingJobs" class="loading-state">
                            <span class="loading-spinner"></span>
                            <p>正在加载任务...</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
// 只导入真实存在的 Element Plus 组件
import {
    ElMessage,
    ElCollapse,
    ElCollapseItem
} from 'element-plus';
import { getUsername, removeToken } from '../utils/auth';
import api from '../services/api';
import { uploadPrintFile, getPrinters, getActiveJobs, cancelPrintJob } from '../services/printerService';
import { isValidFileType, createFilePreview, formatFileSize } from '../utils/helpers';
import FileDropzone from '../components/common/FileDropzone.vue';
import FileItem from '../components/common/FileItem.vue';
import PrinterSelect from '../components/common/PrinterSelect.vue';

const router = useRouter();
const username = ref(getUsername() || '用户');
const isMobile = ref(false);

// 文件和打印选项状态
const selectedFiles = ref([]);
const copies = ref(1);
const printMode = ref('1');
const flatMode = ref('h');
const isSubmitting = ref(false);

// 打印机状态
const printers = ref([]);
const selectedPrinterId = ref('');

// 任务状态
const activeJobs = ref([]);
const isRefreshingJobs = ref(false);

// 检查是否可以提交
const canSubmit = computed(() => {
    return selectedFiles.value.length > 0 && selectedPrinterId.value !== '';
});

// 页面加载时获取数据
onMounted(() => {
    isMobile.value = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || window.innerWidth < 768;
    fetchPrinters();
    fetchActiveJobs();
    // 每隔30秒自动刷新一次任务状态
    setInterval(fetchActiveJobs, 30000);
});

// 获取打印机列表
const fetchPrinters = async () => {
    try {
        const data = await getPrinters();
        printers.value = (data.printers || []).map(p => {
            return {
                ...p,
                id: String(p.id),
                type: p.type || '未知类型',
            };
        });
        if (printers.value.length > 0 && !selectedPrinterId.value) {
            const defaultPrinter = printers.value.find(p => p.status === 'online') || printers.value[0];
            selectedPrinterId.value = defaultPrinter.id;
            onPrinterChange(defaultPrinter.id);
        }
    } catch (error) {
        ElMessage.error(error.error || '获取打印机列表失败');
    }
};

// 获取当前打印任务
const fetchActiveJobs = async () => {
    isRefreshingJobs.value = true;
    try {
        const data = await getActiveJobs();
        activeJobs.value = data.jobs || [];
    } catch (error) {
        ElMessage.error(error.error || '获取打印任务失败');
    } finally {
        isRefreshingJobs.value = false;
    }
};

const ClearActiveJobs = () => {
    api.get('/print/jobs/clear_completed')
        .then(response => {
            ElMessage.success('已清除所有活动打印任务');
            fetchActiveJobs();
        })
        .catch(error => {
            ElMessage.error('清除活动打印任务失败');
        });
};

// 处理文件选择
const handleFilesSelected = async (files) => {
    for (const file of files) {
        if (!isValidFileType(file)) {
            ElMessage.warning(`文件 "${file.name}" 格式不支持，已跳过。`);
            continue;
        }

        if (selectedFiles.value.some(f => f.name === file.name && f.size === file.size)) {
            ElMessage.info(`文件 "${file.name}" 已在列表中。`);
            continue;
        }

        try {
            file.previewUrl = await createFilePreview(file);
            file.uid = Date.now() + Math.random().toString(36).substr(2, 9); // 生成唯一ID
            selectedFiles.value.push(file);
        } catch (error) {
            ElMessage.error(`处理文件 "${file.name}" 时出错。`);
        }
    }
};

// 移除文件
const removeFile = (fileToRemove) => {
    if (fileToRemove.previewUrl && fileToRemove.previewUrl.startsWith('blob:')) {
        URL.revokeObjectURL(fileToRemove.previewUrl);
    }
    selectedFiles.value = selectedFiles.value.filter(file => file.uid !== fileToRemove.uid);
};

// 清空所有文件
const clearFiles = () => {
    selectedFiles.value.forEach(file => {
        if (file.previewUrl && file.previewUrl.startsWith('blob:')) {
            URL.revokeObjectURL(file.previewUrl);
        }
    });
    selectedFiles.value = [];
};

// 打印机变化时的处理
const onPrinterChange = (printerId) => {
    flatMode.value = 'h'; // 默认纵向打印
};

// 提交打印任务
const submitPrintJob = async () => {
    if (!canSubmit.value) return;

    const formData = new FormData();
    selectedFiles.value.forEach(file => formData.append('files', file));
    formData.append('copies', copies.value);
    formData.append('printer_id', selectedPrinterId.value);
    formData.append('print_mode', printMode.value);
    formData.append('flat_mode', flatMode.value);

    isSubmitting.value = true;
    try {
        const response = await uploadPrintFile(formData);
        ElMessage.success(response.message || '打印任务已成功提交');
        clearFiles();
        // 提交成功后立即刷新任务列表
        setTimeout(fetchActiveJobs, 1000);
    } catch (error) {
        ElMessage.error(error.error || '提交打印任务失败，请重试');
    } finally {
        isSubmitting.value = false;
    }
};

// 取消打印任务
const cancelJob = async (jobId) => {
    try {
        const response = await cancelPrintJob(jobId);
        ElMessage.success(response.message || '打印任务已取消');
        fetchActiveJobs(); // 取消后刷新任务列表
    } catch (error) {
        ElMessage.error(error.error || '取消打印任务失败');
    }
};

// 退出登录
const handleLogout = () => {
    removeToken();
    router.push('/login');
    ElMessage.success('已成功退出登录');
};

// 辅助函数 - 获取打印机类型标签
const getPrinterTypeLabel = (type) => {
    return type;
};

// 辅助函数 - 获取任务状态标签
const getStatusLabel = (status) => {
    const statusLabels = {
        'pending': '等待中',
        'processing': '打印中',
        'completed': '已完成',
        'cancelled': '已取消',
        'failed': '失败'
    };
    return statusLabels[status] || '未知状态';
};

// 辅助函数 - 获取任务状态徽章样式
const getStatusBadgeClass = (status) => {
    const classes = {
        'pending': 'badge-pending',
        'processing': 'badge-processing',
        'completed': 'badge-completed',
        'cancelled': 'badge-cancelled',
        'failed': 'badge-failed'
    };
    return classes[status] || '';
};

// 辅助函数 - 获取进度条样式
const getProgressBarClass = (status) => {
    const classes = {
        'pending': 'progress-pending',
        'processing': 'progress-processing',
        'failed': 'progress-failed'
    };
    return classes[status] || '';
};
</script>

<style scoped>
/* 基础布局 */
.dashboard-container {
    padding: 20px;
    max-width: 1600px;
    margin: 0 auto;
}

.dashboard-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
}

.dashboard-title {
    font-size: 24px;
    font-weight: 600;
    color: var(--text-color);
}

.user-info {
    display: flex;
    align-items: center;
    gap: 12px;
}

.username {
    font-weight: 500;
}

.logout-icon {
    width: 16px;
    height: 16px;
    margin-right: 4px;
}

.dashboard-content {
    display: flex;
    flex-direction: column;
    gap: 24px;
}

.card {
    background-color: var(--card-bg);
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    padding: 24px;
    transition: var(--transition-default);
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}

.section-title {
    font-size: 18px;
    font-weight: 600;
    color: var(--text-color);
}

/* 上传区域 */
.upload-area {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.selected-files {
    margin-top: 16px;
}

.files-title {
    font-size: 16px;
    font-weight: 500;
    margin-bottom: 12px;
}

.files-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
    max-height: 300px;
    overflow-y: auto;
    padding-right: 8px;
}

/* 打印选项 */
.print-options {
    margin-top: 24px;
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.option-group {
    margin-bottom: 16px;
}

/* 桌面端布局 */
.desktop-layout {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}

.options-grid.desktop-layout {
    flex-direction: row;
    align-items: flex-end;
}

.options-grid.desktop-layout .option-group {
    flex: 1;
    min-width: 200px;
    margin-bottom: 0;
}

.status-cards.desktop-layout {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 24px;
}

/* 移动端布局 */
.mobile-layout {
    display: none;
}

/* 响应式断点 */
@media (max-width: 1024px) {
    .status-cards.desktop-layout {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 768px) {
    .desktop-layout {
        display: none;
    }

    .mobile-layout {
        display: block;
    }

    .dashboard-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 12px;
    }

    .upload-section,
    .active-jobs,
    .printers-status {
        padding: 16px;
    }

    .mobile-options {
        display: flex;
        flex-direction: column;
        gap: 16px;
    }
}

/* 打印操作按钮 */
.print-actions {
    display: flex;
    gap: 12px;
    margin-top: 16px;
}

.print-btn {
    flex: 1;
    background-color: var(--primary-color);
}

.clear-btn {
    flex-shrink: 0;
}

.print-icon {
    width: 18px;
    height: 18px;
    margin-right: 8px;
}

/* 任务列表 */
.jobs-table {
    width: 100%;
    border-collapse: collapse;
}

.table-header {
    display: grid;
    grid-template-columns: 80px 1fr 120px 60px 100px 1fr 100px;
    padding: 12px 16px;
    background-color: var(--primary-light);
    border-radius: 8px 8px 0 0;
    font-weight: 500;
    color: var(--text-color);
}

.table-row {
    display: grid;
    grid-template-columns: 80px 1fr 120px 60px 100px 1fr 100px;
    padding: 12px 16px;
    border-bottom: 1px solid var(--border-color);
    align-items: center;
}

.table-row:last-child {
    border-bottom: none;
    border-radius: 0 0 8px 8px;
}

.table-cell {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

/* 打印机列表 */
.printers-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.printer-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px;
    border-radius: 8px;
    background-color: white;
    border: 1px solid var(--border-color);
    transition: var(--transition-default);
}

.printer-item.online {
    border-color: var(--success-color);
}

.printer-item.offline {
    border-color: var(--border-color);
    opacity: 0.7;
}

.printer-info {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.printer-name {
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 8px;
}

.printer-status-indicator {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
}

.printer-item.online .printer-status-indicator {
    background-color: var(--success-color);
}

.printer-item.offline .printer-status-indicator {
    background-color: var(--text-light);
}

.printer-details {
    font-size: 14px;
    color: var(--text-light);
}

.printer-status-text {
    font-weight: 500;
    padding: 4px 8px;
    border-radius: 4px;
}

.printer-item.online .printer-status-text {
    background-color: rgba(82, 196, 26, 0.1);
    color: var(--success-color);
}

.printer-item.offline .printer-status-text {
    background-color: rgba(102, 112, 123, 0.1);
    color: var(--text-light);
}

/* 进度条 */
.progress-container {
    width: 100%;
    height: 8px;
    background-color: var(--border-color);
    border-radius: 4px;
    overflow: hidden;
    position: relative;
}

.progress-bar {
    height: 100%;
    border-radius: 4px;
    transition: width 0.3s ease;
}

.progress-processing {
    background-color: var(--primary-color);
}

.progress-pending {
    background-color: var(--warning-color);
}

.progress-failed {
    background-color: var(--error-color);
}

.progress-text {
    font-size: 14px;
    margin-top: 4px;
    color: var(--text-light);
}

/* 状态徽章 */
.status-badge {
    display: inline-block;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 14px;
    font-weight: 500;
}

.badge-pending {
    background-color: rgba(250, 173, 20, 0.1);
    color: var(--warning-color);
}

.badge-processing {
    background-color: rgba(66, 185, 131, 0.1);
    color: var(--primary-color);
}

.badge-completed {
    background-color: rgba(82, 196, 26, 0.1);
    color: var(--success-color);
}

.badge-cancelled {
    background-color: rgba(102, 112, 123, 0.1);
    color: var(--text-light);
}

.badge-failed {
    background-color: rgba(255, 77, 79, 0.1);
    color: var(--error-color);
}

/* 空状态和加载状态 */
.empty-state,
.loading-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px 20px;
    color: var(--text-light);
    text-align: center;
}

.loading-state {
    gap: 12px;
}

/* 移动端任务列表样式 */
.job-title {
    font-weight: 500;
}

.job-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 8px 16px;
    font-size: 14px;
    color: var(--text-light);
    margin-top: 4px;
}

.job-progress {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 8px;
}

.printer-job-count {
    font-size: 14px;
    color: var(--text-light);
}

/* 主布局样式 */
.main-layout {
    display: flex;
    gap: 20px;
    width: 100%;
}

/* 左侧打印机状态 */
.printers-sidebar {
    width: 300px;
    flex-shrink: 0;
}

/* 右侧打印控制区域 */
.print-controls {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    gap: 20px;
}

/* 纵向排列的选项 */
.options-vertical {
    display: flex;
    flex-direction: column;
    gap: 20px;
    padding: 20px;
}

.option-group {
    width: 100%;
}

.option-value {
    position: relative;
}

/* 未选择打印机时的占位文本 */
.placeholder-text {
    position: absolute;
    left: 12px;
    top: 50%;
    transform: translateY(-50%);
    color: #999;
    pointer-events: none;
}

/* 响应式调整 */
@media (max-width: 768px) {
    .main-layout {
        flex-direction: column;
    }

    .printers-sidebar {
        width: 100%;
    }
}

/* 选项容器 */
.option-wrapper {
    position: relative;
    width: 100%;
}

/* 输入框基础样式 */
.option-group .input {
    width: 100%;
    padding: 8px 12px;
    box-sizing: border-box;
    border: 1px solid #ddd;
    border-radius: 4px;
    background-color: #fff;
}

/* 禁用状态的输入框样式 */
.option-group .input:disabled {
    background-color: #f5f5f5;
    /* 关键：去掉禁用状态的灰色遮罩效果 */
    opacity: 1;
    color: transparent;
    /* 隐藏默认的禁用文本 */
}

/* 提示文本覆盖层 */
.placeholder-overlay {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    padding: 0 12px;
    box-sizing: border-box;
    color: #999;
    pointer-events: none;
    /* 允许点击穿透到下方的输入框 */
    border: 1px solid #ddd;
    border-radius: 4px;
    background-color: #f5f5f5;
}
</style>