<template>
  <div class="section-container">
    <div class="sectionComponent">
      <!-- 急停按钮 -->
      <div class="emergency-stop">
        <div class="red-circle">急停</div>
        <!-- 操作按钮 -->
        <div class="operation-buttons">
          <button class="green-btn" @click="startModelAnimation">启动</button>
          <button class="red-btn" @click="stopModelAnimation">停止</button>
        </div>
      </div>

      <!-- 参数控制部分 -->
      <div class="param-section">
        <div class="param-row">
          <!-- <div class="param-label">喷雾压力</div> -->
          <div class="param-label">风机转速</div>
          <div class="param-control">
            <span class="arrow-btn" @click="decrement('pressure')">❮</span>
            <span class="param-value">{{ pressure }}</span>
            <span class="arrow-btn" @click="increment('pressure')">❯</span>
          </div>
        </div>
        <div class="param-row">
          <!-- <div class="param-label">喷雾距离</div> -->
          <div class="param-label">风门开度</div>
          <div class="param-control">
            <span class="arrow-btn" @click="decrement('distance')">❮</span>
            <span class="param-value">{{ distance }}</span>
            <span class="arrow-btn" @click="increment('distance')">❯</span>
          </div>
        </div>
        <!-- 其他参数 -->
        <div class="param-row">
          <!-- <div class="param-label">喷雾流量</div> -->
          <div class="param-label">叶片角度</div>
          <div class="param-control">
            <span class="arrow-btn" @click="decrement('flow')">❮</span>
            <span class="param-value">{{ flow }}</span>
            <span class="arrow-btn" @click="increment('flow')">❯</span>
          </div>
        </div>
        <div class="param-row">
          <div class="param-label">循环时间</div>
          <div class="param-control">
            <span class="arrow-btn" @click="decrement('cycleTime')">❮</span>
            <span class="param-value">{{ cycleTime }}</span>
            <span class="arrow-btn" @click="increment('cycleTime')">❯</span>
          </div>
        </div>
        <div class="param-row">
          <!-- <div class="param-label">喷雾频率</div> -->
          <div class="param-label">电机功率</div>
          <div class="param-control">
            <span class="arrow-btn" @click="decrement('frequency')">❮</span>
            <span class="param-value">{{ frequency }}</span>
            <span class="arrow-btn" @click="increment('frequency')">❯</span>
          </div>
        </div>
        <div class="param-row">
          <!-- <div class="param-label">喷雾角度</div> -->
          <div class="param-label">变频参数</div>
          <div class="param-control">
            <span class="arrow-btn" @click="decrement('angle')">❮</span>
            <span class="param-value">{{ angle }}</span>
            <span class="arrow-btn" @click="increment('angle')">❯</span>
          </div>
        </div>
        <div class="param-row">
          <div class="param-label">工作模式</div>
          <div class="param-control">
            <selectComponent v-model="workMode" :options="workModeOptions" />
          </div>
        </div>
        <div class="param-row">
          <!-- <div class="param-label">喷嘴类型</div> -->
          <div class="param-label">风机类型</div>
          <div class="param-control">
            <selectComponent v-model="nozzleType" :options="nuzzleTypeOptions" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup name="deviceControlComponent">
import selectComponent from '../../../components/selectComponent.vue'
import { threeDModelDataStore } from '../../../store/store' ////导入三维模型的数据仓库
import { ref } from 'vue'

//声明数据仓库
const threeDModelData = threeDModelDataStore()

// 定义状态变量
const pressure = ref(10)
const distance = ref(10)
const flow = ref(10)
const cycleTime = ref(10)
const frequency = ref(10)
const angle = ref(10)
//喷嘴
const nozzleType = ref('请选择')
const nuzzleTypeOptions = ['请选择', '喷嘴1', '喷嘴2', '喷嘴3']
// const backgroundImage = ref('/public/images/下拉框.png')//自定义背景图片
//工作模式
const workMode = ref('请选择')
const workModeOptions = ['请选择', '模式1', '模式2']
// 定义参数增减逻辑
const increment = (param) => {
  switch (param) {
    case 'pressure':
      pressure.value = Math.min(pressure.value + 1, 50)
      //打印当前值
      console.log(pressure.value)
      break
    case 'distance':
      distance.value = Math.min(distance.value + 1, 50)
      break
    case 'flow':
      flow.value = Math.min(flow.value + 1, 50)
      break
    case 'cycleTime':
      cycleTime.value = Math.min(cycleTime.value + 1, 50)
      break
    case 'frequency':
      frequency.value = Math.min(frequency.value + 1, 50)
      break
    case 'angle':
      angle.value = Math.min(angle.value + 1, 90)
      break
    default:
      break
  }
}

const decrement = (param) => {
  switch (param) {
    case 'pressure':
      pressure.value = Math.max(pressure.value - 1, 0)
      console.log(pressure.value)
      break
    case 'distance':
      distance.value = Math.max(distance.value - 1, 0)
      break
    case 'flow':
      flow.value = Math.max(flow.value - 1, 0)
      break
    case 'cycleTime':
      cycleTime.value = Math.max(cycleTime.value - 1, 0)
      break
    case 'frequency':
      frequency.value = Math.max(frequency.value - 1, 0)
      break
    case 'angle':
      angle.value = Math.max(angle.value - 1, 0)
      break
    default:
      break
  }
}

// 定义启动模型动画函数
const startModelAnimation = () => {
  // 调用三维模型数据仓库的启动模型动画函数
  threeDModelData.startAnimation()
}

const stopModelAnimation = () => {
  threeDModelData.stopAnimation()
}
</script>

<style scoped>
/* 基础容器样式 */
.section-container {
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  height: 100%;
  width: 100%;
  padding: 20px; /* 在组件周围添加内边距 */
  box-sizing: border-box; /* 让内边距包含在元素的总宽高内 */
}

/* 主要组件卡片样式 */
.sectionComponent {
  border-radius: 16px; /* iOS 风格圆角 */
  padding: 24px; /* 卡片内部边距 */
  /* box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); 轻微的阴影效果 */
  width: 100%;
  max-width: 900px; /* 限制最大宽度，防止过度拉伸 */
  height: auto; /* 高度根据内容自适应 */
  max-height: 100%; /* 确保不超过父容器高度 */
  display: flex;
  flex-direction: row; /* 保持水平布局（左：急停，右：参数） */
  gap: 32px; /* 左侧（急停）和右侧（参数）区域之间的间距 */
  align-items: flex-start; /* 顶部对齐 */
  box-sizing: border-box;
}

/* 急停按钮区域 */
.emergency-stop {
  flex: 0 0 120px; /* 左侧区域固定宽度 */
  display: flex;
  flex-direction: column; /* 垂直排列（圆圈在上，按钮在下）*/
  align-items: center; /* 水平居中对齐 */
  gap: 24px; /* 红色圆圈和操作按钮之间的间距 */
  margin-top: 10px; /* 顶部微调，视觉上与参数行对齐 */
}

.red-circle {
  width: 100px;
  height: 100px;
  border-radius: 50%; /* 圆形 */
  background-color: #ff3b30; /* iOS 红色 */
  color: white;
  font-size: 20px;
  font-weight: 600; /* 字体加粗 */
  display: flex;
  justify-content: center;
  align-items: center;
  border: none; /* 移除之前的边框 */
  box-shadow: 0 4px 8px rgba(255, 59, 48, 0.3); /* 红色调阴影 */
  cursor: pointer; /* 鼠标悬停时显示为可点击状态 */
  transition:
    transform 0.1s ease-in-out,
    box-shadow 0.1s ease-in-out; /* 平滑过渡效果 */
}
.red-circle:hover {
  transform: scale(1.3); /* 鼠标悬停时放大 */
}
.red-circle:active {
  transform: scale(0.98); /* 鼠标按下时缩小 */
  box-shadow: none; /* 按下时移除阴影 */
}

.operation-buttons {
  /* flex: 2; 移除 flex 比例设置 */
  display: flex;
  flex-direction: column; /* 垂直堆叠按钮 */
  align-items: center; /* 居中对齐按钮 */
  gap: 12px; /* 按钮之间的间距 */
  /* margin-top: 20px; 移除固定边距，改用 gap 控制 */
}

/* 通用按钮样式 */
.green-btn,
.red-btn {
  width: 100px;
  height: 44px; /* iOS 标准触摸目标高度 */
  border: none; /* 无边框 */
  border-radius: 12px; /* 圆角 */
  font-size: 16px;
  font-weight: 500; /* 中等字重 */
  color: white;
  cursor: pointer;
  background-size: contain; /* 如果使用背景图，确保图片适应 */
  background-repeat: no-repeat;
  background-position: center;
  transition:
    transform 0.1s ease-in-out,
    box-shadow 0.1s ease-in-out; /* 平滑过渡效果 */
  padding: 0; /* 如果完全使用背景图，移除默认内边距 */
  text-align: center; /* 如果不用图片，文字居中 */
  line-height: 44px; /* 垂直居中文本 */
}

/* 特定按钮颜色 */
.green-btn {
  /* background: url('/public/images/按钮.png'); */ /* 如果图片是必须的，保留此行 */
  background-color: #34c759; /* iOS 绿色 */
  box-shadow: 0 3px 6px rgba(52, 199, 89, 0.2); /* 绿色调阴影 */
}

.red-btn {
  /* background: url('/public/images/按钮.png'); */ /* 如果图片是必须的，保留此行 */
  background-color: #ff3b30; /* iOS 红色 */
  box-shadow: 0 3px 6px rgba(255, 59, 48, 0.2); /* 红色调阴影 */
}

/* 按钮悬停/激活状态 */
.green-btn:hover,
.red-btn:hover {
  transform: scale(1.1); /* 悬停时轻微放大 */
}
.green-btn:active,
.red-btn:active {
  transform: scale(0.98); /* 按下时轻微缩小 */
  box-shadow: none; /* 按下时移除阴影 */
}

/* 参数控制区域 */
.param-section {
  flex: 1; /* 占据剩余空间 */
  display: grid; /* 使用 Grid 布局 */
  /* 改动：固定为两列，每列占据可用空间的一半 */
  grid-template-columns: repeat(2, 1fr);
  /* 可以稍微减小间距，让布局更紧凑 */
  gap: 12px 18px; /* 行间距12px，列间距18px (根据需要调整) */
  width: auto; /* 宽度由 flexbox 控制 */
  min-width: 0; /* 防止 grid 子项撑破容器 */
}

.param-row {
  padding: 10px;
  display: flex;
  align-items: center; /* 垂直居中对齐 */
  justify-content: space-between; /* 两端对齐 */
  font-size: 18px; /* iOS 标准文字大小 */
  color: hsl(240, 7%, 97%);
  /* margin-top: -20px; 移除负边距 */
  width: 100%;
}

.param-label {
  flex: 0 1 auto; /* 允许标签收缩，但不允许增长 */
  text-align: left; /* 标签左对齐 */
  margin-right: 10px; /* 右边距 */
  color: hsl(210, 8%, 91%);
  opacity: 0.8; /* 轻微降低不透明度 */
  white-space: nowrap; /* 防止标签换行 */
}

.param-control {
  display: flex;
  align-items: center; /* 垂直居中对齐 */
  gap: 8px; /* 箭头按钮和数值之间的间距 */
  flex: 1 0 auto; /* 允许控制部分占据空间 */
  justify-content: center; /* 控制部分中心对齐 */
}

.param-value {
  width: auto; /* 宽度自适应 */
  min-width: 30px; /* 最小宽度 */
  text-align: center; /* 文字居中 */
  font-weight: 500; /* 中等字重 */
  color: #f2f4f6;
}

/* 箭头按钮（步进器样式） */
.arrow-btn {
  width: 30px;
  height: 30px;
  border: none; /* 移除边框 */
  border-radius: 8px; /* 圆角 */
  background-color: #e5e5ea; /* iOS 浅灰色控件背景 */
  color: #007aff; /* iOS 蓝色强调色 */
  font-size: 18px;
  font-weight: 600; /* 箭头加粗 */
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: background-color 0.2s ease; /* 背景色过渡效果 */
  margin: 0; /* 移除之前的边距 */
}

.arrow-btn:hover {
  background-color: #d1d1d6; /* 悬停时颜色变深 */
}

.arrow-btn:active {
  background-color: #c7c7cc; /* 按下时颜色更深 */
}
</style>
