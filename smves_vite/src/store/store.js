import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'
import api from '@/api/api'
//第一个参数要求是一个独一无二的名字
//第二个参数可接受两类值：Setup 函数或 Option 对象。
export const useAllDataStore = defineStore('allData', () => {
  //在 Setup Store 中：
  //ref() 就是 state 属性
  //computed() 就是 getters
  //function() 就是 actions
  const activeFunction = ref('')
  //标签页
  const tags = ref([])
  const menuItems = ref({
    functionA: [
      { id: 1, name: 'menuA1', label: '菜单A1' },
      { id: 2, name: 'menuA2', label: '菜单A2' },
    ],
    functionB: [
      { id: 3, name: 'menuB1', label: '菜单B1' },
      { id: 4, name: 'menuB2', label: '菜单B2' },
    ],
    functionC: [
      { id: 5, name: 'menuC1', label: '菜单C1' },
      { id: 6, name: 'menuC2', label: '菜单C2' },
    ],
  })

  const setActiveFunction = (functionName) => {
    activeFunction.value = functionName
    //如果tags中没有当前功能的页面，则添加
    if (!tags.value.includes(functionName)) {
      tags.value.push(functionName)
    }
  }
  //关闭页面，删除tag
  const closeTag = (tag) => {
    const index = tags.value.indexOf(tag)
    if (index !== -1) {
      tags.value.splice(index, 1)
    }
  }
  //激活当前功能下的菜单
  const currentMenuItems = computed(() => menuItems.value[activeFunction.value] || [])

  //清空菜单栏
  const cleanMenu = () => (activeFunction.value = '')
  return {
    activeFunction,
    menuItems,
    currentMenuItems,
    setActiveFunction,
    tags,
    closeTag,
    cleanMenu,
  }
})

export const useUserDataStore = defineStore(
  'userData',
  () => {
    const userData = ref({
      id: null, // 修改 id 的初始值为 null
      avatar: '',
      nickname: '',
      mobile: '',
      email: '',
      token: '',
    })
    // 使用 watch 监听 userData 的变化，并将其存储到 localStorage
    watch(
      userData,
      (newValue) => {
        localStorage.setItem('userData', JSON.stringify(newValue))
      },
      { deep: true }, // 深度监听，确保对象内部属性的变化也能被监听到
    )
    const updateUserData = (newUserData) => {
      console.log('发送的数据', newUserData)
      api
        .editUser(newUserData)
        .then((res) => {
          // console.log('收到的响应', res) // 检查响应
          if (res) {
            // 检查 res 是否为真值
            // userData.value = res; // 确保 res 是用户对象
            // 或者，更安全的方式是：
            userData.value = { ...userData.value, ...res } //只更新接收到的属性值，保持其他值不变
          } else {
            console.error('更新用户信息失败:', res)
          }
        })
        .catch((error) => {
          console.error('请求错误:', error)
        })
    }

    return {
      userData,
      updateUserData,
    }
  },
  //持久化存储
  {
    persist: {
      enabled: true,
      storage: localStorage, // 明确指定 localStorage
      key: 'userData', // 自定义 key，方便查看
    },
  },
)

export const threeDModelDataStore = defineStore('threeDModelData', () => {
  const isActive = ref(false)

  const startAnimation = () => {
    isActive.value = true
  }

  const stopAnimation = () => {
    isActive.value = false
  }

  return {
    isActive,
    startAnimation,
    stopAnimation,
  }
})
