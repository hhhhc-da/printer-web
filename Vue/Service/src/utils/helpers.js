// 文件大小格式化
export const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 验证文件类型
export const isValidFileType = (file) => {
  const allowedTypes = [
    'application/pdf',
    'image/jpeg',
    'image/png',
    'image/gif',
    'image/bmp',
    'image/tiff'
  ]
  
  // 同时检查文件扩展名
  const allowedExtensions = ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
  const fileExtension = file.name.toLowerCase().slice(file.name.lastIndexOf('.'))
  
  return allowedTypes.includes(file.type) || allowedExtensions.includes(fileExtension)
}

// 生成文件预览URL
export const createFilePreview = (file) => {
  return new Promise((resolve) => {
    if (file.type.startsWith('image/')) {
      const reader = new FileReader()
      reader.onload = (e) => resolve(e.target.result)
      reader.readAsDataURL(file)
    } else if (file.type === 'application/pdf') {
      resolve('https://via.placeholder.com/150x200?text=PDF+文件')
    } else {
      resolve('https://via.placeholder.com/150x200?text=文档文件')
    }
  })
}