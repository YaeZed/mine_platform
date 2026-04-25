<template>
  <div class="alarm-stats-container">
    <div class="alarm-icons">
      <!-- 预警图标区域 (保持不变) -->
      <div class="alarm-icon red">
        <img src="/images/yujingRed.png" alt="红色预警" />
        <p>红色预警</p>
      </div>
      <div class="alarm-icon orange">
        <img src="/images/yujingOrange.png" alt="橙色预警" />
        <p>橙色预警</p>
      </div>
      <div class="alarm-icon yellow">
        <img src="/images/yujingYellow.png" alt="黄色预警" />
        <p>黄色预警</p>
      </div>
      <div class="alarm-icon blue">
        <img src="/images/yujingBlue.png" alt="蓝色预警" />
        <p>蓝色预警</p>
      </div>
    </div>
    <div class="chart-title">
      <h3>近七日报警统计</h3>
      <!-- 稍微简化标题 -->
    </div>
    <div ref="chartRef" class="chart"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import { ref, onMounted, onBeforeUnmount } from 'vue'

export default {
  name: 'alarmCountComponent',
  setup() {
    const chartRef = ref(null)
    let chartInstance = null

    // --- Mock Data (保持不变) ---
    const chartData = [
      { date: '10/01', count: 5 },
      { date: '10/02', count: 8 }, // 修改一些数据让曲线更明显
      { date: '10/03', count: 6 },
      { date: '10/04', count: 10 },
      { date: '10/05', count: 7 },
      { date: '10/06', count: 12 },
      { date: '10/07', count: 9 },
    ]

    const initChart = () => {
      chartInstance = echarts.init(chartRef.value)

      const option = {
        tooltip: {
          trigger: 'axis', // 坐标轴触发
          axisPointer: {
            type: 'cross', // 十字准星指示器
            lineStyle: {
              // 竖线样式
              color: '#5685F7',
              width: 1,
              type: 'solid',
            },
            crossStyle: {
              color: '#999',
            },
            label: {
              // 坐标轴指示器的文本标签样式
              backgroundColor: '#6a7985',
            },
          },
          backgroundColor: 'rgba(10, 25, 50, 0.85)', // Tooltip 背景色
          borderColor: '#17E9E0', // Tooltip 边框色
          borderWidth: 1,
          textStyle: {
            color: '#FFF', // Tooltip 文字颜色
            fontSize: 12,
          },
          formatter: function (params) {
            // 自定义 Tooltip 内容
            let result = params[0].name + '<br/>' // 日期
            params.forEach(function (item) {
              result += `<span style="display:inline-block;margin-right:5px;border-radius:10px;width:10px;height:10px;background-color:${item.color};"></span>` // 系列颜色圆点
              result += item.seriesName + ': ' + item.value + '<br/>' // 系列名和值
            })
            return result
          },
        },
        grid: {
          left: '3%', // 调整边距
          right: '4%',
          top: '15%', // 给 tooltip 留出更多空间
          bottom: '5%', // 减少底部边距
          containLabel: true, // 关键，防止标签溢出
        },
        xAxis: {
          type: 'category',
          boundaryGap: false, // **重要**：让面积图紧贴 Y 轴开始
          data: chartData.map((item) => item.date),
          axisLine: {
            // 轴线
            show: false, // 不显示轴线
          },
          axisTick: {
            // 刻度
            show: false, // 不显示刻度
          },
          axisLabel: {
            // 标签
            color: '#A0A0A0', // 标签颜色 (浅灰)
            fontSize: 10, // 字体大小
            margin: 10, // 标签与轴线距离
          },
        },
        yAxis: {
          type: 'value',
          axisLine: {
            // 轴线
            show: false, // 不显示轴线
          },
          axisLabel: {
            // 标签
            color: '#A0A0A0', // 标签颜色
            fontSize: 10,
            margin: 10,
          },
          splitLine: {
            // 网格线
            show: true,
            lineStyle: {
              color: 'rgba(255, 255, 255, 0.1)', // 非常淡的网格线
              type: 'dashed', // 虚线
            },
          },
        },
        series: [
          {
            name: '报警次数', // 系列名称，会显示在 tooltip 中
            type: 'line',
            smooth: true, // **关键**：平滑曲线
            symbol: 'circle', // 数据点形状
            showSymbol: true, // 是否显示数据点，可以设为 false，hover 时再显示
            symbolSize: 6, // 数据点大小
            itemStyle: {
              // 数据点样式
              color: '#17E9E0', // 数据点颜色 (亮青色)
              borderColor: 'rgba(23, 233, 224, 0.5)', // 数据点边框，半透明
              borderWidth: 4, // 数据点边框宽度 (制造光晕效果)
            },
            lineStyle: {
              // 线条样式
              width: 2, // 线条宽度
              color: '#17E9E0', // 线条颜色
              shadowColor: 'rgba(23, 233, 224, 0.5)', // 线条阴影
              shadowBlur: 8,
            },
            areaStyle: {
              // **关键**：区域填充样式
              // 使用渐变色
              color: new echarts.graphic.LinearGradient(
                0,
                0,
                0,
                1, // (x1, y1, x2, y2) - 从上到下
                [
                  {
                    offset: 0,
                    color: 'rgba(23, 233, 224, 0.3)', // 起始颜色 (带透明度)
                  },
                  {
                    offset: 1,
                    color: 'rgba(10, 25, 50, 0)', // 结束颜色 (完全透明或接近背景)
                  },
                ],
              ),
            },
            data: chartData.map((item) => item.count), // 数据
            emphasis: {
              // 鼠标悬停时的高亮样式
              focus: 'series', // 聚焦当前系列
              itemStyle: {
                symbolSize: 8, // 增大标记点
                borderColor: 'rgba(23, 233, 224, 1)', // 边框更明显
                borderWidth: 5,
              },
              lineStyle: {
                width: 3, // 线条加粗
              },
            },
          },
        ],
      }

      chartInstance.setOption(option)
    }

    const resizeChart = () => {
      if (chartInstance) {
        chartInstance.resize()
      }
    }

    onMounted(() => {
      initChart()
      window.addEventListener('resize', resizeChart)
    })

    onBeforeUnmount(() => {
      window.removeEventListener('resize', resizeChart)
      if (chartInstance) {
        chartInstance.dispose()
        chartInstance = null
      }
    })

    return {
      chartRef,
    }
  },
}
</script>

<style scoped>
.alarm-stats-container {
  color: #fff;
  padding: 10px; /* 整体内边距 */
  font-family: 'Microsoft YaHei', sans-serif; /* 换个更现代的字体 */
  width: 100%;
  height: 100%;
  display: flex; /* 使用 Flexbox 布局 */
  flex-direction: column; /* 垂直排列 */
  box-sizing: border-box; /* padding 不会撑大盒子 */
  /* background-color: #0a101c; 如果需要背景色 */
}

/* 预警图标区域 */
.alarm-icons {
  display: flex;
  justify-content: space-around; /* 图标均匀分布，两边留空 */
  align-items: center;
  padding: 5px 0 15px 0; /* 调整上下内边距 */
  flex-shrink: 0; /* 防止图标区域被压缩 */
}

/* 单个图标 */
.alarm-icon {
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* 图标图片 */
.alarm-icon img {
  width: 45px; /* 稍微调整大小 */
  height: 45px;
  object-fit: contain; /* 保持图片比例 */
}

/* 图标标题 */
.alarm-icon p {
  margin-top: 8px;
  font-size: 13px; /* 调整字体大小 */
  font-weight: normal; /* 可以不用加粗 */
  color: #c0c0c0; /* 标题颜色可以淡一点 */
}

.chart-title {
  margin-left: 5px; /* 左边稍微缩进 */
  margin-top: 0;
  margin-bottom: 5px; /* 标题和图表间距 */
  font-size: 16px; /* 调整标题字体大小 */
  color: #e0e0e0;
  font-weight: 500; /* 适中字重 */
  flex-shrink: 0; /* 防止标题被压缩 */
}
.chart-title h3 {
  margin: 0; /* 移除 h3 的默认 margin */
  padding: 0;
}

.chart {
  width: 100%;
  flex-grow: 1; /* **关键**：让图表区域占据剩余的所有垂直空间 */
  min-height: 150px; /* 保证最小高度 */
  /* height: 150px; */ /* 移除固定高度 */
}
</style>
