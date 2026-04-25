<template>
  <div class="param-container">
    <div class="circle-group">
      <div class="circle-item" v-for="(param, index) in params" :key="index">
        <div ref="chartRefs" class="chart"></div>
        <div class="param-label">
          <p>{{ param.label }}</p>
          <p>{{ param.value }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup name="waterBallComponent">
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import 'echarts-liquidfill'

// 获取参数
const params = [
  // { label: '喷雾流量', value: '5升/分钟', percentage: 0.5 },
  // { label: '喷雾压力', value: '10MPa', percentage: 0.5 },
  // { label: '当前功率', value: '50kW', percentage: 0.5 },
  // { label: '累计能耗', value: '100kWh', percentage: 0.5 },
  { label: '风机转速', value: '6.643m/s', percentage: 0.5 },
  { label: '风门角度', value: '30度', percentage: 0.5 },
  { label: '当前功率', value: '50kW', percentage: 0.5 },
  { label: '累计能耗', value: '100kWh', percentage: 0.5 },
]

const chartRefs = ref([])

// 初始化图表
const initCharts = () => {
  chartRefs.value.forEach((chartElement, index) => {
    const chart = echarts.init(chartElement)
    const option = {
      series: [
        {
          type: 'liquidFill',
          data: [params[index].percentage],
          radius: '90%', // 调整球体大小
          backgroundStyle: {
            borderColor: '#156ACF', //动态边框颜色
            borderWidth: 1,
            color: '#0F225A', // 动态背景颜色
          },
          label: {
            formatter: `${params[index].percentage * 100}%`,
            color: '#ffffff', // 动态文字颜色
            insideColor: '#ffffff',
            fontSize: 20,
          },
          outline: {
            show: true,
            borderDistance: 8,
            itemStyle: {
              borderWidth: 2,
              borderColor: '#156ACF', // 边框颜色
            },
          },
        },
      ],
    }

    chart.setOption(option)
  })
}
onMounted(() => {
  initCharts()
})
</script>

<style scoped>
.param-container {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px 0;
  box-sizing: border-box;
}

.circle-group {
  display: flex;
  justify-content: center; /* 子元素居中 */
  gap: 40px; /* 设置子项之间的固定间隔 */
  width: 100%;
  max-width: 1200px;
}

.circle-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.chart {
  width: 120px;
  height: 120px;
}

.param-label {
  text-align: center;
  margin-top: 10px;
  color: whitesmoke;
}

.param-label p:first-child {
  font-weight: bold;
}

.param-label p:last-child {
  font-size: 14px;
}
</style>
