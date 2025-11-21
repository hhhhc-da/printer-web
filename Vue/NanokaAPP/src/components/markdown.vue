<template>
  <div class="container">
    <!-- 左侧静态表格区域 -->
    <div class="table-container">
      <h3>技术目录</h3>
      <table>
        <thead>
          <tr>
            <th>组件</th>
            <th>技术</th>
          </tr>
        </thead>
        <tbody>
          <!-- 后端部分：合并 3 行 -->
          <tr>
            <td rowspan="3">后端</td>
            <td>waitress WSGI 服务器</td>
          </tr>
          <tr>
            <td>Flask 高性能 HTTP 服务器</td>
          </tr>
          <tr>
            <td>Python 3.12 环境</td>
          </tr>

          <!-- 前端部分：合并 2 行 -->
          <tr>
            <td rowspan="2">前端</td>
            <td>Vue 极简前端框架</td>
          </tr>
          <tr>
            <td>Vite 模板</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 右侧 Markdown 展示区域 -->
    <div class="markdown-container">
      <div class="preview-container">
        <h4>简介</h4>
        <!-- 修复：将 :content 改为 :source -->
        <MarkdownIt :source="markdownContent" class="markdown-preview" />
      </div>

      <div>
        即刻前往打印页面: <a href="http://192.168.1.72/print" target="_blank">http://192.168.1.72/print</a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import MarkdownIt from 'vue3-markdown-it'

// 初始 Markdown 内容（示例）
const markdownContent = ref(`### Nanoka 的后端 Root 文件目录
---

所有用到的技术都在左侧，请根据需要进行修改

所有的 __前端__ 文件都在 __Vue__ 文件夹下，所有的 __后端__ 文件都在 __Python/WSGI__ 目录下

本服务器已配置 __Redis、PostgreSQL、Nginx、Node.js（Nvm）、VScode__
`)
</script>

<style scoped>
.container {
  display: flex;
  gap: 20px;
  padding: 20px;
  min-height: 60vh;
  box-sizing: border-box;
  background-color: #f5f5f5;
}

/* 左侧表格样式 */
.table-container {
  flex: 0 0 300px;
  /* 固定宽度 */
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

th,
td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}

th {
  background-color: #f0f0f0;
  font-weight: bold;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

/* 右侧 Markdown 区域样式 */
.markdown-container {
  flex: 1;
  /* 占剩余空间 */
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.editor-container {
  margin-bottom: 20px;
}

.markdown-editor {
  width: 100%;
  min-height: 200px;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-family: monospace;
  resize: vertical;
  box-sizing: border-box;
  outline: none;
  /* 去除默认聚焦边框 */
  transition: border-color 0.3s;
}

/* 编辑器聚焦样式优化 */
.markdown-editor:focus {
  border-color: #42b983;
  box-shadow: 0 0 0 2px rgba(66, 185, 131, 0.2);
}

.preview-container {
  border-top: 1px solid #eee;
  padding-top: 20px;
}

.markdown-preview {
  line-height: 1.8;
  /* 优化行高，提升可读性 */
  color: #333;
}

/* Markdown 预览样式增强 */
.markdown-preview h1,
.markdown-preview h2,
.markdown-preview h3 {
  margin: 20px 0 12px;
  border-bottom: 1px solid #eee;
  padding-bottom: 8px;
  color: #2c3e50;
}

.markdown-preview h1 {
  font-size: 24px;
}

.markdown-preview h2 {
  font-size: 20px;
}

.markdown-preview h3 {
  font-size: 18px;
}

.markdown-preview p {
  margin: 12px 0;
}

.markdown-preview ul,
.markdown-preview ol {
  margin: 12px 0 12px 28px;
  padding-left: 8px;
}

.markdown-preview li {
  margin: 4px 0;
}

.markdown-preview blockquote {
  border-left: 4px solid #42b983;
  /* 调整引用边框颜色，更醒目 */
  padding-left: 16px;
  margin: 12px 0;
  color: #666;
  background-color: #f8f9fa;
  /* 增加引用背景色 */
}

/* 代码块样式优化（继承组件自带的高亮） */
.markdown-preview pre {
  background: #f5f5f5;
  padding: 16px;
  border-radius: 6px;
  overflow-x: auto;
  margin: 12px 0;
  font-size: 14px;
}

.markdown-preview code {
  background: #f0f0f0;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 14px;
}

.markdown-preview img {
  max-width: 100%;
  border-radius: 6px;
  margin: 12px 0;
  border: 1px solid #eee;
  /* 给图片加轻微边框 */
}

.markdown-preview a {
  color: #42b983;
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: all 0.3s;
}

.markdown-preview a:hover {
  text-decoration: none;
  border-color: #42b983;
  color: #359469;
}
</style>