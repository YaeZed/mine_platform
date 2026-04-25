<template>
  <div class="DustRemovalPage">
    <!-- 头部组件 -->
    <header>
      <headerComponent propsTitle="智能掘进除尘系统" />
    </header>

    <!-- 选择按钮 -->
    <div class="card-select-btn" @click="toggleCardOptions">组件选择</div>
    <!-- 选项卡 -->
    <div class="card-options">
      <div class="card">
        <label> <input type="checkbox" value="device-status" checked /> 设备运行状态 </label>
      </div>
      <div class="card">
        <label> <input type="checkbox" value="alarm-count" checked /> 报警统计 </label>
      </div>
      <div class="card">
        <label> <input type="checkbox" value="warning-info" checked /> 报警信息 </label>
      </div>
      <!-- <div class="card">
        <label> <input type="checkbox" value="blank" checked /> 留白 </label>
      </div> -->
      <div class="card">
        <label> <input type="checkbox" value="device-control" checked /> 通风设备控制台 </label>
      </div>
      <div class="card">
        <label> <input type="checkbox" value="water-ball" checked /> 工作参数 </label>
      </div>
      <div class="card">
        <label> <input type="checkbox" value="ring-chart" checked /> 环境参数 </label>
      </div>
      <div class="card">
        <label> <input type="checkbox" value="dust-monitoring" checked /> 监控画面 </label>
      </div>
    </div>

    <!-- 内容布局 -->
    <div class="layout">
      <!-- 左列 -->
      <div class="left-column">
        <sectionComponent id="device-status" class="showComponent" title="设备运行状态">
          <div class="component-container">
            <statusSliderComponent />
            <runningTimeComponent />
          </div>
        </sectionComponent>
        <sectionComponent id="alarm-count" class="showComponent" title="报警统计">
          <alarmCountComponent />
        </sectionComponent>
        <sectionComponent id="warning-info" class="showComponent" title="报警信息（读取参数）">
          <warningInfoComponent />
        </sectionComponent>
      </div>
      <!-- 中间列 -->
      <div class="mid-column">
        <sectionComponent id="blank" class="showComponent" title="三维模型">
          <threeDModelComponent
            src="/public/models/花洒水汽.blend1.glb"
            :playback-rate="0.6"
            background-img="/public/images/bg.jpg"
          />
        </sectionComponent>
        <sectionComponent id="device-control" class="showComponent" title="通风设备控制台">
          <deviceControlComponent />
        </sectionComponent>
      </div>
      <!-- 右列 -->
      <div class="right-column">
        <sectionComponent id="water-ball" class="showComponent" title="工作参数（读取参数）">
          <waterBallComponent />
        </sectionComponent>
        <sectionComponent id="ring-chart" class="showComponent" title="环境参数（读取参数）">
          <div class="ring-section">
            <ringChartComponent />
          </div>
        </sectionComponent>
        <sectionComponent id="dust-monitoring" class="showComponent" title="监控画面（连接摄像头）">
          <img src="/images/风门.jpg" alt="Dust Monitoring" class="monitoring-image" />
        </sectionComponent>
      </div>
    </div>
  </div>
</template>

<script setup name="DustRemovalPage">
import waterBallComponent from './components/waterBallComponent.vue'
import sectionComponent from '@/pages/DustRemoval/components/sectionComponent.vue'
import headerComponent from '@/components/headerComponent.vue'
import ringChartComponent from '@/pages/DustRemoval/components/ringChartComponent.vue'
import warningInfoComponent from '@/pages/DustRemoval/components/warningInfoComponent.vue'
import alarmCountComponent from '@/pages/DustRemoval/components/alarmCountComponent.vue'
import runningTimeComponent from '@/pages/DustRemoval/components/runningTimeComponent.vue'
import statusSliderComponent from '@/pages/DustRemoval/components/statusSliderComponent.vue'
import deviceControlComponent from '@/pages/DustRemoval/components/deviceControlComponent.vue'
import threeDModelComponent from '@/pages/DustRemoval/components/threeDModelComponent.vue'

const toggleCardOptions = () => {
  const cardOptions = document.querySelector('.card-options')
  // 切换选项卡显示
  cardOptions.classList.toggle('show')

  // 切换选项卡
  // 获取所有选项卡
  const checkboxs = document.querySelectorAll('.card input[type="checkbox"]')
  // 遍历选项卡，添加change事件，如果选中则显示对应组件，否则隐藏
  checkboxs.forEach((checkbox) => {
    checkbox.addEventListener('change', () => {
      // 获取当前选项卡的 value
      const id = checkbox.value
      // 根据 value 获取对应id的组件
      const component = document.querySelector(`#${id}`)
      if (checkbox.checked) {
        component.style.display = 'block'
      } else {
        component.style.display = 'none'
      }
    })
  })
}
</script>

<style scoped>
* {
  box-sizing: border-box;
}
.DustRemovalPage {
  background: url(/images/bg.jpg) no-repeat center center;
  background-size: cover; /* 使用cover使背景图片覆盖整个元素 */
  background-attachment: fixed; /* 背景固定不随内容滚动 */
  height: 100vh; /* 确保div的高度是视口高度的100% */
  margin: 0;
}
header {
  top: 0;
  left: 0;
  width: 100%;
  height: 50px;
}
.card-select-btn {
  position: absolute; /* 绝对定位 */
  top: auto;
  left: 30px;
}
.card-select-btn {
  /* 基本样式 */
  background-color: #007aff; /* 苹果蓝色 */
  color: white;
  font-size: 15px; /* 根据你的需求调整 */
  font-weight: 500; /* 稍微粗一点，更现代 */
  padding: 5px 20px; /* 上下10px，左右20px 内边距 */
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
.card-select-btn:hover {
  /* hover 状态 - 稍微调整阴影 */
  box-shadow: 0px 5px 8px rgba(0, 0, 0, 0.2);
  transform: translateY(-3px); /* 稍微向上移动一点 */
}
.card-select-btn:active {
  /* 点击状态 - 更明显的反馈 */
  background-color: #0062cc; /* 稍微深一点的蓝色 */
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);
  transform: translateY(3px); /* 稍微向下移动一点 */
}
.card-options {
  position: absolute;
  left: 30px;
  top: 78px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 10px;
  z-index: 10;
  grid-template-columns: repeat(1, 1fr);
  gap: 10px;

  /* 初始状态：完全透明且不可见 */
  opacity: 0;
  visibility: hidden; /* 确保在 opacity 为 0 时不占据空间 */

  /* 添加过渡效果 */
  transition:
    opacity 0.3s ease,
    visibility 0.3s ease;
}

.card {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.card label {
  display: block;
  cursor: pointer;
}

.card input[type='checkbox'] {
  margin-bottom: 5px;
}

/* 显示卡片选项 */
.card-options.show {
  display: grid; /* 需要保留，以便在显示时正确布局 */
  opacity: 1; /* 完全可见 */
  visibility: visible; /* 确保元素可见 */
}

/* 显示组件 */
.showComponent {
  display: block;
}
.layout {
  display: flex;
  flex-direction: row; /* 横向排列子项 */
  justify-content: space-between; /* 子项之间均匀分布 */
  padding: 20px; /* 四周留白，根据需要调整 */
  height: 90vh;
}
.component-container {
  display: flex;
  flex-direction: column; /* 垂直排列 */
  gap: 20px; /* 组件之间的间隔 */
}
.left-column {
  flex: 2; /* 左列宽度设置为1份 */
  display: flex;
  flex-direction: column;
}

.mid-column {
  flex: 2.5; /* 中列宽度设置为2份（两倍于左右列） */
  display: flex;
  flex-direction: column;
}

.right-column {
  flex: 2; /* 右列宽度设置为1份 */
  display: flex;
  flex-direction: column;
}
.ring-section {
  display: flex;
  gap: 40px;
  justify-content: space-around; /* 水平排列均分 */
}
.monitoring-image {
  width: 600px; /* 或指定具体宽度 */
  height: 315px; /* 保持图片比例 */
}
</style>
