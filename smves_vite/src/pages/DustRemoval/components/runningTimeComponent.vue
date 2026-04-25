<template>
  <div class="running-time">
    <!-- 左侧部分 -->
    <div class="left-part">
      <span class="label">运行时长：</span>
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="arc-circle"
        width="60"
        height="60"
        viewBox="0 0 60 60"
      >
        <!-- 背景圆圈（可选，用于参考） -->
        <!-- <circle cx="30" cy="30" r="25" fill="transparent" stroke="#444" stroke-width="3" /> -->

        <!-- 进度圆圈 -->
        <circle
          class="progress-circle"
          cx="30"
          cy="30"
          r="25"
          fill="transparent"
          stroke="#00bfff"
          stroke-width="3"
          :stroke-dasharray="circumference"
          :stroke-dashoffset="runtimeOffset"
          transform="rotate(-90 30 30)"
        />

        <!-- 圆圈内的文字 -->
        <text x="50%" y="50%" text-anchor="middle" dominant-baseline="middle" class="value-text">
          {{ runTimeValue }}h
        </text>
      </svg>
    </div>

    <!-- 右侧部分 -->
    <div class="right-part">
      <span class="label">累计运行时长：</span>
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="arc-circle"
        width="60"
        height="60"
        viewBox="0 0 60 60"
      >
        <!-- 进度圆圈 -->
        <circle
          class="progress-circle"
          cx="30"
          cy="30"
          r="25"
          fill="transparent"
          stroke="#00bfff"
          stroke-width="3"
          :stroke-dasharray="circumference"
          :stroke-dashoffset="totalRuntimeOffset"
          transform="rotate(-90 30 30)"
        />

        <!-- 圆圈内的文字 -->
        <text x="50%" y="50%" text-anchor="middle" dominant-baseline="middle" class="value-text">
          {{ totalRunTimeValue }}h
        </text>
      </svg>
    </div>
  </div>
</template>

<script setup name="runningTimeComponent">
import { ref, computed } from 'vue'

// 示例数据（根据需要可以改为 props 或状态管理）
const runTimeValue = ref(25) // 当前运行时长（小时）
const totalRunTimeValue = ref(150) // 累计运行时长（小时）
const maxTimeForCircle = ref(100) // 圆圈表示的最大时长（例如 100 小时）

const radius = 25
const circumference = computed(() => 2 * Math.PI * radius) // 圆的周长，大约为 157

// 根据当前值和最大值计算描边偏移量
// 偏移量 = 周长 * (1 - 百分比)
const runtimeOffset = computed(() => {
  const percentage = Math.min(runTimeValue.value / maxTimeForCircle.value, 1) // 最大为 100%
  return circumference.value * (1 - percentage)
})

const totalRuntimeOffset = computed(() => {
  // 假设累计时长也使用相同的最大值进行计算
  const percentage = Math.min(totalRunTimeValue.value / maxTimeForCircle.value, 1)
  return circumference.value * (1 - percentage)
  // 如果累计时长总是显示满圆，可以使用：
  // return 0;
})
</script>

<style scoped>
/* 容器样式 */
.running-time {
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center;
  gap: 40px; /* 左右部分之间的间距 */
  color: white;
  font-family: 'Arial', sans-serif;
  padding: 10px; /* 添加内边距 */
}

/* 左右部分样式 */
.left-part,
.right-part {
  display: flex;
  align-items: center;
  gap: 10px; /* 标签和 SVG 之间的间距 */
}

/* 标签文字样式 */
.label {
  font-size: 20px;
  flex-shrink: 0; /* 防止标签被压缩 */
}

/* SVG 容器样式 */
.arc-circle {
  display: inline-block;
  position: relative;
}

/* 进度圆圈样式 */
.progress-circle {
  fill: transparent;
  stroke: #00bfff; /* 深天蓝色 */
  stroke-width: 3;
  stroke-linecap: round; /* 圆角线帽 */
  transition: stroke-dashoffset 0.5s ease-out; /* 动画过渡效果 */
}

/* 圆圈中的文字样式 */
.value-text {
  font-size: 14px;
  font-weight: bold;
  fill: white; /* 文本颜色 */
}
</style>
