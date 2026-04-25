<template>
  <div class="container">
    <!-- 功能栏 -->
    <div class="func-bar">
      <div
        class="func-item"
        v-for="func in functionList"
        :key="func.name"
        @click="setActiveFunc(func.name)"
      >
        <el-icon><Folder /></el-icon>{{ func.label }}
      </div>
      <div class="user">
        <div class="avatar">
          <el-dropdown placement="bottom">
            <el-avatar src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" />
            <template #dropdown>
              <el-dropdown-menu>
                <!-- <el-dropdown-item>个人中心</el-dropdown-item> -->
                <el-dropdown-item @click="toHome">返回主页</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
        <span style="margin-left: 10px">{{ nickname }}</span>
      </div>
    </div>

    <!-- 菜单栏 -->
    <div class="menu-bar">
      <el-button type="primary" v-for="menuItem in currentMenuItems" :key="menuItem.name">
        {{ menuItem.label }}
      </el-button>
    </div>

    <!-- 标签栏 
    <div class="tag-bar">
      <el-tag
        class="tag-item"
        v-for="(tag, index) in tags"
        :key="index"
        size="large"
        :effect="route.name === tag ? 'dark' : 'plain'"
        closable
        @click="toPage(tag)"
        @close="closeTag(tag, index)"
        >{{ tag }}
      </el-tag>
    </div> -->

    <!-- 内容区 -->
    <div class="content-area">
      <router-view></router-view>
      <!-- 侧边栏 -->
      <div class="sidebar">
        <h3>侧边栏</h3>
        <ul>
          <li>Item 1</li>
          <li>Item 2</li>
          <li>Item 3</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useAllDataStore } from '@/store/store'
import { useRouter, useRoute } from 'vue-router'
import { ElMessageBox } from 'element-plus'

const router = useRouter()
const route = useRoute()
const store = useAllDataStore()
const currentMenuItems = computed(() => store.currentMenuItems)
const tags = computed(() => store.tags)
//没有tag时，跳转到空白页面
if (tags.value.length === 0) router.push({ name: 'functionNULL' })
const functionList = ref([
  { name: 'functionA', label: '功能 A' },
  { name: 'functionB', label: '功能 B' },
  { name: 'functionC', label: '功能 C' },
])
//从localStorage中获取用户信息
const userData = localStorage.getItem('userData')
const nickname = JSON.parse(userData).nickname
const toHome = () => {
  router.push('/HomePage')
}
// 点击功能栏时，激活对应的菜单
const setActiveFunc = (funcName) => {
  store.setActiveFunction(funcName)
  //路由跳转到对应的页面
  router.push({ name: funcName })
}
// //点击tag栏时，路由跳转到对应的页面，并激活对应的菜单
// const toPage = (tag) => {
//   router.push({ name: tag })
//   store.setActiveFunction(tag)
// }
//关闭tag
// const closeTag = (tag, index) => {
//   ElMessageBox.confirm('确认关闭？').then(() => {
//     store.closeTag(tag)

//     if (tags.value.length === 0) {
//       //当所有标签页都关闭时，跳转到空白页面，并清空菜单栏
//       router.push({ name: 'functionNULL' })
//       store.cleanMenu()
//       return
//     }

//     //如果关闭的tag不是当前页面，直接返回
//     if (tag !== route.name) return

//     if (tag === route.name) {
//       //如果是当前页面
//       if (index === tags.value.length && index > 0) {
//         //如果关闭的是最后一个tag，则跳转到index-1页面
//         router.push(tags.value[index - 1])
//         //激活菜单
//         store.setActiveFunction(tags.value[index - 1])
//       } else {
//         //如果不是最后一个tag，则跳转到下一个页面
//         //这里由于先调用更新函数，index已经减1了
//         router.push(tags.value[index])
//         //激活菜单
//         store.setActiveFunction(tags.value[index])
//       }
//     }
//   })
// }
</script>

<style scoped>
body {
  font-family:
    -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; /* iOS 常用字体 */
  margin: 0;
  padding: 0;
  background-color: #f2f2f7; /* 浅灰色背景 */
}

.container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

/* 功能栏 */
.func-bar {
  background-color: #fff; /* 白色背景 */
  padding: 10px;
  display: flex;
  border-bottom: 1px solid #d1d1d6; /* 细边框 */
  box-shadow: 0 1px 0 rgba(0, 0, 0, 0.05); /* 细微阴影 */
  position: relative;
}

.func-item {
  padding: 8px 12px;
  cursor: pointer;
  border-radius: 8px; /* 圆角 */
  transition: background-color 0.2s ease-in-out; /* 过渡效果 */
}

.func-item:hover {
  background-color: #e5e5ea; /* 浅灰色悬停背景 */
}
.user {
  display: flex;
  align-items: center;
  position: absolute;
  right: 50px;
}
.avatar {
  transition: transform 0.3s ease;
}
.avatar:hover {
  transform: scale(1.3);
}
/* 菜单栏 */
.menu-bar {
  background-color: #fff;
  padding: 10px;
  border-bottom: 1px solid #d1d1d6;
  box-shadow: 0 1px 0 rgba(0, 0, 0, 0.05);
}

/* 标签栏 */
.tag-bar {
  display: flex;
  background-color: #fff;
  border-bottom: 1px solid #d1d1d6;
  box-shadow: 0 1px 0 rgba(0, 0, 0, 0.05);
  overflow-x: auto; /* 允许水平滚动 */
  padding: 5px 0; /* 稍微调整 padding */
}
.tag-item {
  cursor: pointer;
  font-size: 14px;
  margin: 0 10px;
}

/* 内容区 */
.content-area {
  margin-left: 10px;
  display: flex;
  flex-grow: 1;
  background-color: #fff; /* 内容区白色背景 */
}

.main-content {
  padding: 20px;
  flex-grow: 1;
  font-size: 16px;
  line-height: 1.6;
}

.hidden {
  display: none;
}

/* 侧边栏 */
.sidebar {
  /* 侧边栏默认隐藏，新建页面时显示 */
  display: none;
  position: absolute;
  width: 250px; /* 加宽侧边栏 */
  background-color: #f9f9f9;
  padding: 20px;
  border-left: 1px solid #d1d1d6;
  right: 0;
}

.sidebar h3 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 10px;
}

.sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar li {
  padding: 8px 0;
  border-bottom: 1px solid #d1d1d6;
  font-size: 14px;
  cursor: pointer;
  transition: color 0.2s ease-in-out;
}

.sidebar li:hover {
  color: #007aff;
}

.sidebar li:last-child {
  border-bottom: none;
}
</style>
