// src/services/printerService.js

import api from './api'

// 获取打印机列表
export const getPrinters = async () => {
  return await api.get('/printers')
}

// 上传打印文件
export const uploadPrintFile = async (formData) => {
  return await api.post('/print/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 获取打印任务状态
export const getActiveJobs = async () => { // 注意：函数名从 getPrintJobStatus 改为 getActiveJobs，更符合其功能
  return await api.get('/print/jobs')
}

// 新增：取消打印任务
export const cancelPrintJob = async (jobId) => {
  // 假设后端取消任务的接口是 /print/jobs/{jobId}/cancel
  // 请根据你的实际后端 API 进行修改
  return await api.post(`/print/jobs/${jobId}/cancel`) 
}

// 注意：如果你的后端使用 DELETE 请求来取消任务，请使用以下代码：
// export const cancelPrintJob = async (jobId) => {
//   return await api.delete(`/print/jobs/${jobId}`)
// }