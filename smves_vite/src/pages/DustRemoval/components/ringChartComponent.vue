<template>
  <div class="ring-chart-container">
    <!-- 遍历数据以创建多个图表组件 -->
    <div class="ring-chart-component" v-for="(item, index) in data" :key="index">
      <!-- 图表容器 div, 通过 chartRefs 引用 -->
      <div ref="chartRefs" class="chart"></div>
      <!-- 图表下方的标签 -->
      <div class="label">{{ item.title }}</div>
    </div>
  </div>
</template>

<script setup name="ringChartComponent">
import * as echarts from 'echarts'
import { onMounted, ref, nextTick } from 'vue' // 如果需要处理复杂的 DOM 操作，可以导入 nextTick，但这里可能不需要

// 图表的示例数据
const data = ref([
  // { percentage: 0.6, title: '工作面湿度' },
  // { percentage: 0.5, title: '粉尘浓度' },
  // { percentage: 0.3, title: '环境湿度' },
  { percentage: 0.6, title: '瓦斯浓度' },
  { percentage: 0.5, title: '粉尘浓度' },
  { percentage: 0.3, title: '环境湿度' },
])

// 用于持有图表 DOM 元素的 ref 数组
const chartRefs = ref([])

// 初始化单个 ECharts 实例的函数
const initChart = (chartElement, percentage, title) => {
  // 如果存在现有图表实例，先销毁，防止重新渲染时内存泄漏
  const existingInstance = echarts.getInstanceByDom(chartElement)
  if (existingInstance) {
    echarts.dispose(existingInstance)
  }

  const chart = echarts.init(chartElement)
  const option = {
    // 提示框配置 (可选，但推荐)
    tooltip: {
      formatter: `${title}: ${(percentage * 100).toFixed(0)}%`, // 简单的提示框，显示标题和百分比
    },
    series: [
      {
        name: 'Progress', // 系列名称
        type: 'gauge', // 使用仪表盘类型实现圆环效果
        startAngle: 90, // 起始角度设为顶部 (12 点钟方向)
        endAngle: -270, // 结束角度设为 -270 度，逆时针画完一圈
        radius: '90%', // *** 调整半径以防边缘接触容器，特别是线条加粗后 ***
        pointer: { show: false }, // 隐藏仪表盘指针
        progress: {
          show: true, // 显示进度弧
          overlap: false, // *** 设置 overlap: false, 让 axisLine 作为背景完整显示 ***
          width: 12, // *** 增加进度弧的厚度 ***
          itemStyle: {
            color: '#13B5E6', // 进度弧的颜色 (与原代码和图片一致)
            // 可选：如果需要圆角效果，可以添加 borderRadius (可能需要微调起始/结束角度)
            // borderRadius: 5,
          },
          roundCap: true, // *** 使进度条两端变为圆角 ***
        },
        axisLine: {
          show: true, // 确保轴线 (背景轨道) 可见
          lineStyle: {
            width: 12, // *** 增加背景轨道的厚度 (与 progress 宽度匹配) ***
            color: [
              // 定义轴线的颜色
              [1, '#2A3A5B'], // *** 对整个轨道使用新的背景色 ***
            ],
            // 这里不再需要根据百分比分段颜色，因为 'progress' 系列会负责绘制彩色部分
          },
          animation: false, // 禁用轴线动画，避免更新时背景重绘问题
        },
        splitLine: { show: false }, // 隐藏分割线
        axisTick: { show: false }, // 隐藏刻度线
        axisLabel: { show: false }, // 隐藏刻度标签
        detail: {
          // 中心百分比文字的配置
          valueAnimation: true, // 启用数值动画
          fontSize: 18, // *** 调整百分比文字的字体大小 ***
          fontWeight: 'bold', // 保持粗体
          offsetCenter: [0, '0%'], // *** 将文字垂直居中 ***
          color: '#fff', // 文字颜色 (白色)
          formatter: (value) => {
            // 使用函数进行格式化控制
            return `${value.toFixed(0)}%` // 显示为不带小数的百分比
          },
        },
        data: [percentage * 100], // 系列数据
        // 设置仪表盘的最小值和最大值
        min: 0,
        max: 100,
        // 确保进度条动画平滑 (如果需要)
        // progress: { /* ... */ animation: true, animationDuration: 1000 },
      },
    ],
  }
  chart.setOption(option)

  // 可选：添加窗口大小调整监听器
  // 如果容器大小会动态变化，考虑使用 ResizeObserver 以获得更好的性能
  const resizeChart = () => {
    chart.resize()
  }
  window.addEventListener('resize', resizeChart)

  // 组件卸载时清理 resize 监听器 (重要!)
  // 这最好在 onUnmounted 钩子中处理，但需要稍微修改 setup 结构
  // 这里为了简单起见，仅指出需要清理。
}

// 组件挂载后初始化图表
onMounted(() => {
  // 使用 nextTick 确保 DOM 元素已准备就绪，尤其是在使用 v-if/v-show 时
  nextTick(() => {
    if (chartRefs.value && chartRefs.value.length > 0) {
      chartRefs.value.forEach((chartElement, index) => {
        // 确保元素实际存在并且有对应数据再初始化
        if (chartElement && data.value[index]) {
          initChart(chartElement, data.value[index].percentage, data.value[index].title)
        } else {
          console.warn(`索引 ${index} 处的图表元素未找到或缺少数据。`)
        }
      })
    } else {
      console.warn('chartRefs 未能正确填充。')
    }
  })
})

// 可选: 如果添加了 resize 监听器，添加 onUnmounted 钩子进行清理
// import { onUnmounted } from 'vue';
// onUnmounted(() => {
//   // 移除 resize 监听器
//   // 如有必要，销毁 ECharts 实例
//   chartRefs.value.forEach(chartElement => {
//      if (chartElement) {
//         const instance = echarts.getInstanceByDom(chartElement);
//         if (instance) {
//            // 如果手动添加了与实例相关的监听器，移除它们
//            echarts.dispose(instance);
//         }
//      }
//   });
//   // 如果全局添加了 window resize 监听器，移除它
//   // window.removeEventListener('resize', resizeChart); // 需要存储 resizeChart 函数的引用
// });
</script>

<style scoped>
.ring-chart-container {
  display: flex;
  justify-content: center; /* 水平居中图表 */
  align-items: center;
  gap: 30px; /* *** 增加图表之间的间距 *** */
  padding: 1px; /* 在容器周围添加一些内边距 */
  width: fit-content; /* 让容器宽度适应内容 */
  margin: auto; /* 如果需要，让容器在页面上居中 */
}

.ring-chart-component {
  display: flex;
  flex-direction: column; /* 垂直堆叠图表和标签 */
  justify-content: center;
  align-items: center;
  width: 150px; /* *** 调整每个组件的宽度 *** */
  height: 160px; /* *** 调整高度以舒适地容纳标签 *** */
}

.chart {
  width: 120px; /* *** 为图表 div 设置明确的大小 *** */
  height: 120px; /* *** 保持正方形 *** */
}

.label {
  margin-top: 15px; /* *** 调整图表下方标签的上外边距 *** */
  text-align: center;
  color: #fff; /* 标签文字颜色 */
  font-size: 17px; /* 标签字体大小 */
}
</style>
