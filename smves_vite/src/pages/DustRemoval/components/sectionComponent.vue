<template>
  <div class="section-container">
    <div class="sectionComponent">
      <!-- 标题部分 -->
      <div class="section-title">{{ title }}</div>
      <!-- 内容部分 -->
      <div class="section-content">
        <slot></slot>
      </div>
      <div class="panel-footer"></div>
    </div>
  </div>
</template>

<script setup name="sectionComponent">
import { defineProps, ref, onMounted } from 'vue'

// 定义 props
defineProps({
  title: {
    type: String,
    required: true,
  },
})

// 定义内容高度
const contentHeight = ref(0)

// 监听窗口尺寸变化，动态调整内容高度
onMounted(() => {
  const handleResize = () => {
    contentHeight.value = window.innerHeight - 100 // 留出标题部分的空间
  }
  handleResize() // 初始化
  window.addEventListener('resize', handleResize)
  return () => window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.section-container {
  margin: 10px;
  flex-direction: column;
}
.sectionComponent {
  border-radius: 10px; /* 保持圆角 */
  color: #fff; /* 保持文字颜色为白色 */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 10px;
  height: 100%;
  position: relative; /* 为了让伪元素可以定位 */
  background: url(/images/line1.png) rgba(255, 255, 255, 0.03);
}

.sectionComponent::before {
  position: absolute;
  top: 0;
  left: 0;
  width: 10px;
  height: 10px;
  border-left: 2px solid #02a6b5;
  border-top: 2px solid #02a6b5;
  content: '';
  overflow: hidden;
}
.sectionComponent::after {
  position: absolute;
  top: 0;
  right: 0;
  width: 10px;
  height: 10px;
  border-right: 2px solid #02a6b5;
  border-top: 2px solid #02a6b5;
  content: '';
}

.panel-footer {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
}

.panel-footer::before {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 10px;
  height: 10px;
  border-left: 2px solid #02a6b5;
  border-bottom: 2px solid #02a6b5;
  content: '';
}

.panel-footer::after {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 10px;
  height: 10px;
  border-right: 2px solid #02a6b5;
  border-bottom: 2px solid #02a6b5;
  content: '';
}

.section-title {
  font-size: 25px;
  font-weight: bold;
}

.section-content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  width: 100%;
  height: 100%;
}
</style>
