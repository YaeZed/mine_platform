<template>
  <header class="header">
    <h1>{{ props.propsTitle }}</h1>
    <!-- 时间组件 -->
    <div class="time-container">
      当前时间：
      {{ currentTime }}
    </div>

    <button class="home-btn" @click="() => $router.push('/HomePage')">返回主页</button>
  </header>
</template>

<script setup name="headerComponent">
import { ref, onMounted } from 'vue'

// 定义父传子标题
const props = defineProps(['propsTitle'])

// 实现时间更新
const currentTime = ref('')

function updateClock() {
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0') // 补齐两位
  const date = String(now.getDate()).padStart(2, '0')
  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')
  const seconds = String(now.getSeconds()).padStart(2, '0')
  currentTime.value = `${year}-${month}-${date} ${hours}:${minutes}:${seconds}`
}
onMounted(() => {
  updateClock()
  setInterval(updateClock, 1000) // 每秒更新
})
</script>

<style scoped>
.header {
  position: relative; /* 确保内部元素可使用绝对定位 */
  text-align: center; /* 标题居中 */
  color: #fff;
  background: url('/public/images/head_bg.png') no-repeat center center/cover;
}

h1 {
  font-size: 50px;
  line-height: normal;
  margin: 0;
  letter-spacing: 20px; /* 字间距 */
}

.time-container {
  position: absolute; /* 绝对定位 */
  bottom: 10px; /* 距离标题底部10px */
  left: 10px; /* 距离标题左侧10px */
  font-size: 25px; /* 时间字体大小 */
  color: #fff; /* 时间字体颜色 */
  font-weight: bold; /* 时间字体加粗 */
}
.home-btn {
  position: absolute; /* 绝对定位 */
  bottom: 10px; /* 距离标题底部10px */
  right: 10px; /* 距离标题左侧10px */
  font-size: 18px; /* 时间字体大小 */
  color: #fff; /* 时间字体颜色 */
  font-weight: bold; /* 时间字体加粗 */
}
.home-btn {
  /* 基本样式 */
  background-color: #007aff; /* 苹果蓝色 */
  color: white;
  font-size: 16px; /* 根据你的需求调整 */
  font-weight: 500; /* 稍微粗一点，更现代 */
  padding: 10px 20px; /* 上下10px，左右20px 内边距 */
  border: none;
  border-radius: 8px; /* 圆角 */
  cursor: pointer;
  /* iOS 按钮文字默认并不是加粗的，所以这里不加粗 */
  /* 阴影效果 - 增加立体感 */
  box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.15); /* 轻微的阴影 */
  /* 过渡效果 - 让点击更流畅 */
  transition: all 0.2s ease-in-out;
  /* 字体 */
  font-family:
    -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; /* 苹果系统字体 */
}
.home-btn:hover {
  /* hover 状态 - 稍微调整阴影 */
  box-shadow: 0px 5px 8px rgba(0, 0, 0, 0.2);
  transform: translateY(-3px); /* 稍微向上移动一点 */
}
.home-btn:active {
  /* 点击状态 - 更明显的反馈 */
  background-color: #0062cc; /* 稍微深一点的蓝色 */
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);
  transform: translateY(3px); /* 稍微向下移动一点 */
}
</style>
