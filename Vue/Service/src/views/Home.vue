<script setup>
import mds from '../components/Preload.vue'
</script>

<template>
  <!-- 新增唯一根容器，包裹所有内容 -->
  <div class="page-root"> 
    <div class="w-container">
      <a href="https://vite.dev" target="_blank">
        <img src="/vite.svg" class="logo" alt="Vite logo" />
      </a>
      <a href="https://vuejs.org/" target="_blank">
        <img src="/vue.svg" class="logo vue" alt="Vue logo" />
      </a>
      <a href="https://flask.palletsprojects.com/en/stable/" target="_blank">
        <img src="/flask.svg" class="logo flask" alt="Flask logo" />
      </a>
    </div>

    <mds/>
  </div>
</template>

<style scoped>
/* 根容器样式（可选，保证布局不变） */
.page-root {
  width: 100%;
  height: 100%;
  box-sizing: border-box;
}

.w-container {
  display: flex;
  text-align: center;
  margin: auto;
  justify-content: center;
  padding: 2%;
}

.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
.logo.flask:hover {
  filter: drop-shadow(0 0 2em #50bbf4aa);
}
</style>