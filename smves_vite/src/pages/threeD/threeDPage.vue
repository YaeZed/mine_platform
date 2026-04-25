<template>
  <div class="ThreeDPage">
    <!-- 头部 -->
    <header>
      <headerComponent propsTitle="矿井巷道三维模型"></headerComponent>
    </header>

    <!-- 主内容布局 -->
    <div class="layout">
      <!-- 左列 -->
      <div class="left-column"></div>
      <!-- 中间列 -->
      <div class="mid-column">
        <section-component>
          <threeDComponent></threeDComponent>
        </section-component>
      </div>
      <!-- 右列 -->
      <div class="right-column"></div>
    </div>
  </div>
</template>

<script setup>
import headerComponent from '@/components/headerComponent.vue'
import sectionComponent from '@/pages/DustRemoval/components/sectionComponent.vue'
import threeDComponent from './components/threeDComponent.vue'
</script>

<style scoped>
* {
  box-sizing: border-box;
}
.ThreeDPage {
  background: url('/images/bg.jpg') no-repeat center center;
  background-size: cover;
  background-attachment: fixed;
  height: 100vh;
  margin: 0;
}
header {
  top: 0;
  left: 0;
  width: 100%;
  height: 50px;
}

.layout {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  padding: 20px;
  height: 90vh;
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
</style>
