<template>
  <div class="alarm-container">
    <table class="alarm-table">
      <thead>
        <tr>
          <!-- 为 # 列添加了特定类名以方便样式控制 -->
          <th class="header-index">#</th>
          <th>报警内容</th>
          <th>报警时间和状态</th>
        </tr>
      </thead>
      <tbody>
        <!-- 如果 item.id 是真正唯一的，用它作 key 更好，否则对于静态列表 index 也可以 -->
        <tr v-for="(item, index) in alarmData" :key="item.id">
          <!-- 为 # 列添加了特定类名 -->
          <td class="cell-index">{{ index + 1 }}</td>
          <td>{{ item.content }}</td>
          <td>{{ item.date }} {{ item.status }}</td>
          <!-- 为清晰起见，日期和状态间加了空格 -->
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup name="warningInfoComponent">
// 获取参数 (数据保持不变)
var alarmData = [
  { id: 1, content: '喷雾压力异常', date: '2024-10-01', status: '未处理' },
  { id: 2, content: '电器系统故障', date: '2024-10-01', status: '已处理' },
  { id: 3, content: '维护提示', date: '2024-10-01', status: '未处理' },
  { id: 4, content: '喷雾流量异常', date: '2024-10-01', status: '未处理' },
  { id: 5, content: '维护提示', date: '2024-10-01', status: '已处理' },
  { id: 6, content: '电池电量低', date: '2024-10-01', status: '未处理' },
  { id: 7, content: '设备温度过高', date: '2024-10-01', status: '已处理' },
  { id: 8, content: '维护提示', date: '2024-10-01', status: '未处理' },
  { id: 9, content: '喷雾压力异常', date: '2024-10-01', status: '未处理' },
]
</script>

<style scoped>
/* 定义标准的类 iOS 颜色变量 */
:root {
  --ios-background-color: #ffffff; /* 白色背景 */
  --ios-secondary-background-color: #f2f2f7; /* 浅灰色，用于细微区分 */
  --ios-text-color: #000000; /* 黑色文本 */
  --ios-separator-color: #c6c6c8; /* 标准分隔线颜色 */
  --ios-header-text-color: #6d6d72; /* 稍微柔和的表头文本颜色 */
}

.alarm-container {
  background: var(--ios-background-color);
  color: var(--ios-text-color);
  border-radius: 10px; /* 类似 iOS 的稍圆边角 */
  width: 100%;
  height: 100%;
  max-height: 220px;
  overflow: auto; /* 保留滚动条 */
  box-sizing: border-box;
  /* 可选：如果不想表格紧贴容器边缘，可以添加内边距 */
  /* padding: 0 15px; */
  border: 1px solid var(--ios-separator-color); /* 可选：为容器添加细微边框 */
}

.alarm-table {
  width: 100%;
  border-collapse: collapse; /* 改为 collapse 使线条更干净 */
  border-spacing: 0;
  /* 使用常见的系统字体栈 */
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  font-size: 15px; /* 典型的 iOS 表格字体大小 */
}

.alarm-table th,
.alarm-table td {
  padding: 12px 15px; /* 增加内边距 */
  text-align: center; /* iOS 表格通常左对齐 */
  border: none; /* 移除所有默认边框 */
  /* 添加底部边框来模仿 iOS 的行分隔符 */
  border-bottom: 1px solid var(--ios-separator-color);
  white-space: nowrap; /* 初始不换行 */
  overflow: hidden; /* 隐藏溢出内容 */
  text-overflow: ellipsis; /* 内容溢出时显示省略号 */
}

/* 选中除最后一行外的所有行的单元格，添加分隔线 */
.alarm-table tbody tr:last-child td {
  border-bottom: none; /* 最后一项后不需要分隔线 */
}

.alarm-table th {
  background: var(--ios-secondary-background-color); /* 可选的低调表头背景*/
  /* background: #fff; 或者保持白色 */
  font-weight: 800; /* 稍粗的表头字体 */
  color: var(--ios-header-text-color); /* 柔和的表头文本颜色 */
  font-size: 23px; /* 表头字体通常稍小 */
  text-transform: uppercase; /* 可选：表头大写 */
  /* 确保表头边框一致或稍强 */
  border-bottom: 1px solid var(--ios-separator-color);
}

/* 为 '#' 索引列设置特定样式 */
.header-index,
.cell-index {
  text-align: center; /* 居中索引数字 */
  width: 40px; /* 给它一个固定的、较小的宽度 */
  padding-left: 15px; /* 调整内边距以适应居中 */
  padding-right: 5px;
}

/* 移除隔行变色 - iOS 通常使用统一背景 */
.alarm-table tr {
  background: var(--ios-background-color); /* 确保所有行都是白色 */
}

/* 美化滚动条 (Webkit 浏览器特定，并非所有浏览器有效) */
.alarm-container::-webkit-scrollbar {
  width: 5px;
}

.alarm-container::-webkit-scrollbar-track {
  background: var(--ios-secondary-background-color);
  border-radius: 10px;
}

.alarm-container::-webkit-scrollbar-thumb {
  background-color: var(--ios-separator-color);
  border-radius: 10px;
}

/* 添加悬停效果 (可选，原生 iOS 中不常见，但在 Web 中较好) */
.alarm-table tbody tr:hover {
  background-color: var(--ios-secondary-background-color);
}
</style>
