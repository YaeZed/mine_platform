<template>
  <div class="custom-select-container" ref="selectContainer" @click="toggleDropdown">
    <!-- 移除了背景图片绑定 -->
    <div class="custom-select">
      <span>{{ selectedOption }}</span>
      <!-- 下拉箭头，根据 isOpen 状态添加 'open' 类 -->
      <span class="select-arrow" :class="{ open: isOpen }"></span>
    </div>
    <transition name="dropdown">
      <ul v-if="isOpen" class="dropdown-list">
        <li
          v-for="(option, index) in options"
          :key="index"
          @click.stop="selectOption(option)"
          :class="{ selected: option === modelValue }"
        >
          {{ option }}
        </li>
      </ul>
    </transition>
  </div>
</template>

<script>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'

export default {
  name: 'SelectComponent',
  props: {
    modelValue: {
      type: String,
      default: '请选择', // 保持默认或改为 "选择..." 以获得更 iOS 的感觉
    },
    options: {
      type: Array,
      default: () => ['请选择', '类型1', '类型2'], // 保持默认或更改占位符
    },
    // backgroundImage 属性不再用于默认样式
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    const isOpen = ref(false) // 控制下拉列表是否打开
    const selectContainer = ref(null) // 引用容器 DOM 元素

    const selectedOption = computed(() => {
      // 确保如果 modelValue 为空，则显示第一个选项或默认占位符
      return props.modelValue || props.options[0] || '选择...'
    })

    const toggleDropdown = () => {
      // 切换下拉列表的显示状态
      isOpen.value = !isOpen.value
    }

    const selectOption = (option) => {
      // 当用户选择一个选项时触发
      // 可以根据需要添加逻辑，例如阻止重新选择占位符
      emit('update:modelValue', option) // 更新父组件绑定的值
      isOpen.value = false // 选择后关闭下拉列表
    }

    // 处理点击容器外部的事件，用于关闭下拉列表
    const handleClickOutside = (event) => {
      if (selectContainer.value && !selectContainer.value.contains(event.target)) {
        isOpen.value = false
      }
    }

    // 组件挂载后，添加全局点击事件监听器
    onMounted(() => {
      document.addEventListener('click', handleClickOutside)
    })

    // 组件卸载前，移除全局点击事件监听器
    onBeforeUnmount(() => {
      document.removeEventListener('click', handleClickOutside)
    })

    return {
      isOpen,
      selectedOption,
      toggleDropdown,
      selectOption,
      selectContainer,
    }
  },
}
</script>

<style>
/* 应用 box-sizing 或根据需要限定范围 */
*,
*::before,
*::after {
  box-sizing: border-box;
}

.custom-select-container {
  position: relative; /* 相对定位，用于下拉列表的绝对定位 */
  width: 180px; /* 稍宽一点以获得更好的间距 */
  font-family:
    -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Fira Sans',
    'Droid Sans', 'Helvetica Neue', sans-serif; /* 类似 iOS 的系统字体 */
}

.custom-select {
  display: flex; /* 使用 flexbox 进行对齐 */
  justify-content: space-between; /* 将文本和箭头推到两端 */
  align-items: center; /* 垂直居中内容 */
  background-color: #fff; /* 白色背景 */
  border: 1px solid #e0e0e0; /* 更柔和的边框颜色 */
  border-radius: 8px; /* 圆角，类似 iOS */
  padding: 10px 12px; /* 调整内边距 */
  cursor: pointer; /* 鼠标指针样式 */
  width: 100%; /* 宽度占满容器 */
  font-size: 16px; /* 常见的 iOS 字体大小 */
  color: #333; /* 标准文本颜色 */
  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease; /* 平滑过渡效果 */
}

.custom-select:hover {
  border-color: #c0c0c0; /* 悬停时边框颜色稍深 */
}

/* 下拉箭头样式 */
.select-arrow {
  width: 0;
  height: 0;
  border-left: 5px solid transparent; /* 透明左边框 */
  border-right: 5px solid transparent; /* 透明右边框 */
  border-top: 6px solid #8e8e93; /* iOS 灰色箭头颜色 */
  transition: transform 0.3s ease; /* 箭头旋转动画 */
  margin-left: 10px; /* 文本和箭头之间的间距 */
}

/* 下拉列表打开时旋转箭头 */
.select-arrow.open {
  transform: rotate(180deg);
}

/* 下拉列表样式 */
.dropdown-list {
  position: absolute; /* 绝对定位，相对于容器 */
  top: calc(100% + 4px); /* 定位在选择框下方，留有小间隙 */
  left: 0;
  width: 100%; /* 宽度与选择框一致 */
  background-color: #fff; /* 白色背景 */
  border: 1px solid #e0e0e0; /* 匹配边框 */
  border-radius: 8px; /* 圆角 */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); /* 轻微阴影增加深度感 */
  z-index: 1000; /* 确保在顶层显示 */
  list-style: none; /* 移除默认列表项目符号 */
  padding: 4px 0; /* 列表内部的垂直内边距 */
  margin: 0; /* 移除默认外边距 */
  max-height: 200px; /* 限制最大高度，超出则滚动 */
  overflow-y: auto; /* 允许垂直滚动 */
}

.dropdown-list li {
  font-size: 16px; /* 匹配选择框字体大小 */
  padding: 10px 12px; /* 列表项的内边距 */
  cursor: pointer; /* 鼠标指针样式 */
  color: #333; /* 文本颜色 */
  transition: background-color 0.2s ease; /* 平滑的悬停背景色过渡 */
  /* 可选：添加细微的分隔线 */
  /* border-bottom: 1px solid #f0f0f0; */
}

/* 可选：移除最后一个列表项的底部边框（如果使用了分隔线） */
/* .dropdown-list li:last-child {
  border-bottom: none;
} */

.dropdown-list li:hover {
  background-color: #f0f0f0; /* 浅灰色悬停背景 */
}

/* 下拉列表中选中项的样式 */
.dropdown-list li.selected {
  background-color: #eef5ff; /* 浅蓝色背景表示选中 */
  font-weight: 500; /* 字体稍粗 */
  color: #007aff; /* iOS 蓝色 */
}

/* 下拉列表过渡动画 */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease-out; /* 更快、更干净的过渡 */
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0; /* 从透明开始/结束 */
  transform: translateY(-5px); /* 轻微向上移动的效果 */
}
</style>
