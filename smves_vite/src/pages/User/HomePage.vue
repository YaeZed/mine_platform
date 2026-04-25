<template>
  <div class="body">
    <!-- 侧边栏 -->
    <aside class="sidebar">
      <div class="logo">个人中心</div>
      <ul class="menu">
        <li @click="() => $router.push('/HomePage')">
          <i class="iconfont icon-home"></i>
          <span>首页</span>
        </li>
        <li @click="() => $router.push('/DustRemoval')">
          <i class="iconfont icon-a-zu19743"></i>
          <span>除尘系统</span>
        </li>
        <li>
          <i class="iconfont icon-sensor"></i>
          <span>留白</span>
        </li>
        <li>
          <i class="iconfont icon-key"></i>
          <span>留白</span>
        </li>
        <li>
          <i class="iconfont icon-lianxiwomen"></i>
          <span>联系我们</span>
        </li>
        <li>
          <i class="iconfont icon-xitongwendang"></i>
          <span>系统文档</span>
        </li>
      </ul>
    </aside>

    <!-- 主内容 -->
    <div class="main">
      <header class="homeHeader">
        <div class="title"></div>
        <div class="profile">
          <div class="avatar">
            <el-dropdown placement="bottom">
              <el-avatar
                src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"
              />
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="openProfileDialog">个人信息</el-dropdown-item>
                  <el-dropdown-item @click="logout">退出</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
          <span style="margin-left: 10px">{{ nickname }}</span>
        </div>
      </header>

      <main class="content">
        <div class="grid-container">
          <div v-for="mine in minesList" :key="mine.mine_id" class="card">
            <div class="card-image"></div>
            <div class="card-content">
              <h2 class="card-title">
                {{ mine.mine_name }}
              </h2>
              <p class="card-description">
                {{ mine.mine_desc }}
              </p>
              <a href="#" @click="openMine" class="card-button">查看矿井通风运行调控系统</a>
              <div class="card-actions">
                <a href="#" class="action-button edit-button" @click="openEditForm(mine.mine_id)"
                  >编辑</a
                >
                <!-- 编辑矿井表单 -->
                <div
                  class="form-popup"
                  :id="'EditForm_' + mine.mine_id"
                  style="padding: 10px; width: 200px; font-size: 12px"
                >
                  <form class="form-container" method="post">
                    <h1>矿井信息</h1>
                    <label for="mine_name">
                      <b>矿井名称</b>
                    </label>
                    <input
                      type="text"
                      v-model="editingMine.mine_name"
                      name="mine_name"
                      required
                      style="width: calc(100% - 10px); padding: 8px; margin: 5px 0; font-size: 12px"
                    />
                    <label for="mine_desc">
                      <b>矿井描述</b>
                    </label>
                    <input
                      type="text"
                      v-model="editingMine.mine_desc"
                      name="mine_desc"
                      required
                      style="width: calc(100% - 10px); padding: 8px; margin: 5px 0; font-size: 12px"
                    />
                    <button
                      type="button"
                      class="btn"
                      style="padding: 8px 12px; font-size: 12px"
                      @click="updateMineProject(mine.mine_id)"
                    >
                      提交
                    </button>
                    <button
                      type="button"
                      class="btn cancel"
                      @click="closeEditForm('EditForm_' + mine.mine_id)"
                      style="padding: 8px 12px; font-size: 12px"
                    >
                      关闭
                    </button>
                  </form>
                </div>
                <a class="action-button delete-button" @click="deleteMineProject(mine.mine_id)"
                  >删除</a
                >
              </div>
            </div>
          </div>
          <div class="card">
            <div class="card-image"></div>
            <div class="card-content">
              <h2 class="card-title">新增矿井</h2>
              <p class="card-description">点击按钮以新增矿井。</p>
              <a href="#" class="card-button" @click="openForm">新增矿井</a>
            </div>
          </div>
          <!-- 新增矿井表单 -->
          <div class="form-popup" id="myForm">
            <form action="#" class="form-container" method="post">
              <h1>矿井信息</h1>
              <label for="mine_name">
                <b>矿井名称</b>
              </label>
              <input type="text" placeholder="输入矿井名称" v-model="newMine.mine_name" required />
              <br />
              <label for="mine_desc">
                <b>矿井描述</b>
              </label>
              <input type="text" placeholder="输入矿井描述" v-model="newMine.mine_desc" required />
              <button type="button" class="btn" @click="addMineProject">提交</button>
              <button type="button" class="btn cancel" @click="closeForm">关闭</button>
            </form>
          </div>
        </div>
      </main>
      <footer class="footer">
        <!-- 底部固定区域 -->
        <!-- 底部内容 -->
      </footer>
    </div>

    <!-- 用户信息编辑对话框 -->
    <el-dialog v-model="profileDialogVisible" width="30%" class="profile-dialog">
      <h3 style="text-align: center; font-size: 1.5rem">个人信息</h3>
      <el-form :model="profileForm" label-width="100px" class="profile-form">
        <!-- <el-form-item label="头像" class="profile-form-item">
          <div class="avatar-wrapper">
            <el-avatar :src="profileForm.avatar" :size="50" class="profile-avatar" />
            <el-upload
              class="avatar-uploader"
              action="#"
              :show-file-list="false"
              :auto-upload="false"
            >
              <el-button size="small" class="upload-button">更换头像</el-button>
            </el-upload>
          </div>
        </el-form-item> -->
        <el-form-item label="用户名" class="profile-form-item">
          <el-input v-model="profileForm.nickname" class="profile-input" />
        </el-form-item>
        <el-form-item label="邮箱" class="profile-form-item">
          <el-input v-model="profileForm.email" class="profile-input" />
        </el-form-item>
        <el-form-item label="电话" class="profile-form-item">
          <el-input v-model="profileForm.mobile" class="profile-input" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="closeProfileDialog" class="cancel-button">取消</el-button>
          <el-button type="primary" @click="saveProfile" class="save-button">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ElMessageBox, ElMessage } from 'element-plus'
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserDataStore } from '../../store/store' // 导入 userData store
const userDataStore = useUserDataStore() // 声明 userData store
let nickname = userDataStore.userData.nickname
// 路由
const router = useRouter()

// 矿井列表
const minesList = ref([])

// 新增矿井数据
const newMine = reactive({
  mine_name: '',
  mine_desc: '',
})

// 编辑矿井数据
const editingMine = reactive({
  mine_name: '',
  mine_desc: '',
})
// 是否显示个人信息编辑对话框
const profileDialogVisible = ref(false)
// 个人信息表单数据 (使用 reactive 创建独立的响应式对象)
const profileForm = reactive({
  id: null,
  avatar: '',
  nickname: '',
  mobile: '',
  email: '',
  token: '',
})
// 原始个人信息数据，用于判断是否修改
const originalProfileForm = ref(null) // 使用 ref 存储原始数据
onMounted(() => {
  // 组件挂载后，从 store 初始化 profileForm
  Object.assign(profileForm, userDataStore.userData)
  // 深拷贝 userDataStore.userData 到 originalProfileForm
  // 这里采用间接赋值，防止数据被修改时，原始数据也被修改
  originalProfileForm.value = JSON.parse(JSON.stringify(userDataStore.userData))
})
// 打开个人信息编辑框
const openProfileDialog = () => {
  profileDialogVisible.value = true
}
// 保存个人信息
const saveProfile = async () => {
  // 调用 store 里的更新方法
  userDataStore.updateUserData(profileForm) // 传递 profileForm 对象
  ElMessage.success('个人信息保存成功!')
  //将nickname赋值为新的值
  nickname = profileForm.nickname
  //更新originalProfileForm
  originalProfileForm.value = JSON.parse(JSON.stringify(profileForm))
  profileDialogVisible.value = false
}
// 深比较两个对象是否相等
const deepCompare = (obj1, obj2) => {
  return JSON.stringify(obj1) === JSON.stringify(obj2)
}
// 关闭个人信息编辑框
const closeProfileDialog = () => {
  if (!deepCompare(profileForm, originalProfileForm.value)) {
    //如果发生了修改
    ElMessageBox.confirm('您已修改个人信息，是否保存？', '提示', {
      confirmButtonText: '保存',
      cancelButtonText: '放弃',
      type: 'warning',
    })
      .then(() => {
        // 如果用户点击保存
        saveProfile()
      })
      .catch(() => {
        // 如果用户点击放弃，则恢复到原始数据
        Object.assign(profileForm, JSON.parse(JSON.stringify(originalProfileForm.value)))
        profileDialogVisible.value = false
        ElMessage({
          type: 'info',
          message: '已放弃保存',
        })
      })
  } else {
    profileDialogVisible.value = false
  }
}
// 打开编辑矿井表单
const openEditForm = (mine_id) => {
  const mine = minesList.value.find((item) => item.mine_id === mine_id)
  if (mine) {
    editingMine.mine_name = mine.mine_name
    editingMine.mine_desc = mine.mine_desc
    document.getElementById('EditForm_' + mine_id).style.display = 'block'
  }
}

// 关闭编辑矿井表单
const closeEditForm = (formId) => {
  document.getElementById(formId).style.display = 'none'
}

// 打开新增矿井表单
const openForm = () => {
  newMine.mine_name = ''
  newMine.mine_desc = ''
  document.getElementById('myForm').style.display = 'block'
}

// 关闭新增矿井表单
const closeForm = () => {
  document.getElementById('myForm').style.display = 'none'
}

// 获取矿井数据
const fetchMinesData = async () => {
  const url = '/mines/MinesList/'
  const token = localStorage.getItem('token')
  const currentUsername = sessionStorage.getItem('username') || '用户名'

  const headers = {
    'Content-Type': 'application/json',
    Authorization: 'JWT ' + token,
    'X-username': currentUsername,
  }

  try {
    const response = await axios.get(url, { headers })
    minesList.value = response.data.data
  } catch (error) {
    console.error('获取矿井数据失败:', error)
    ElMessage.error('获取矿井数据失败，请稍后再试。')
  }
}

// 新增矿井
const addMineProject = async () => {
  const url = '/mines/MinesList/'
  try {
    const response = await axios.post(url, {
      mine_name: newMine.mine_name,
      mine_desc: newMine.mine_desc,
      mine_username: sessionStorage.getItem('username') || '用户名',
    })

    if (response.status === 201) {
      await fetchMinesData()
      closeForm()
      ElMessage.success('新增矿井成功。')
      newMine.mine_name = ''
      newMine.mine_desc = ''
    } else {
      ElMessage.error('新增矿井失败，请稍后再试。')
    }
  } catch (error) {
    console.error('新增矿井失败:', error)
    ElMessage.error('新增矿井失败，请稍后再试。')
  }
}

// 打开矿井通风3d视图
const openMine = () => {
  router.push('/Mine')
}

// 更新矿井信息
const updateMineProject = async (mine_id) => {
  const url = `/mines/MinesDetail/${mine_id}/`
  try {
    const response = await axios.post(url, {
      mine_name: editingMine.mine_name,
      mine_desc: editingMine.mine_desc,
    })

    if (response.status === 200) {
      await fetchMinesData()
      closeEditForm('EditForm_' + mine_id)
      ElMessage.success('更新矿井信息成功。')
    } else {
      ElMessage.error('更新矿井信息失败，请稍后再试。')
    }
  } catch (error) {
    console.error('更新矿井信息失败:', error)
    ElMessage.error('更新矿井信息失败，请稍后再试。')
  }
}

// 删除矿井
const deleteMineProject = async (mine_id) => {
  const url = `/mines/MinesDetail/${mine_id}/`
  try {
    const response = await axios.delete(url)

    if (response.status === 204) {
      await fetchMinesData()
      ElMessage.success('删除矿井成功。')
    } else {
      ElMessage.error('删除矿井失败，请稍后再试。')
    }
  } catch (error) {
    console.error('删除矿井失败:', error)
    ElMessage.error('删除矿井失败，请稍后再试。')
  }
}

// 退出系统
const logout = () => {
  //移除session
  localStorage.removeItem('token')
  localStorage.removeItem('userData')
  sessionStorage.removeItem('username')
  router.push('/login')
}

// 组件挂载后执行
onMounted(async () => {
  await fetchMinesData()
  document.title = '个人中心'
})
</script>

<style scoped>
@font-face {
  font-family: 'iconfont'; /* Project id 4906105 */
  src:
    url('//at.alicdn.com/t/c/font_4906105_806xb3k3ntq.woff2?t=1745585666473') format('woff2'),
    url('//at.alicdn.com/t/c/font_4906105_806xb3k3ntq.woff?t=1745585666473') format('woff'),
    url('//at.alicdn.com/t/c/font_4906105_806xb3k3ntq.ttf?t=1745585666473') format('truetype');
}

.iconfont {
  font-family: 'iconfont' !important;
  font-size: 16px;
  font-style: normal;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.icon-xitongwendang:before {
  content: '\e701';
  color: #007bff;
}

.icon-lianxiwomen:before {
  content: '\e699';
  color: #007bff;
}

.icon-user:before {
  content: '\e600';
  color: #007bff;
}

.icon-home:before {
  content: '\e608';
  color: #007bff;
}

.icon-a-zu19743:before {
  content: '\e601';
  color: #007bff;
}

/* 布局样式 */
.body {
  display: flex;
  height: 100vh;
}

/* 侧边栏样式 */
.sidebar {
  width: 200px;
  background-color: #ffffff;
  font-family: 'Arial', sans-serif;
  border-right: 1px solid #eee;
}

.logo {
  font-size: 20px;
  font-weight: bold;
  padding: 20px;
  text-align: center;
}

.menu {
  list-style: none;
  padding: 10px 0;
  margin: 0;
}

.menu li {
  display: flex;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #e0e0e0;
  font-size: 16px; /* 调整字体大小 */
  cursor: pointer;
  transition:
    background-color 0.3s ease,
    transform 0.2s ease;
  color: #333;
}

.menu li:hover {
  background-color: #f7f7f7;
  transform: scale(1.02);
}

.menu li i {
  margin-right: 8px;
  font-size: 18px; /* 调整图标大小 */
  color: #555;
}

/* 主内容区 */
.main {
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* Header 样式 */
.homeHeader {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 3px solid #f0f0f0;
  background-color: #ffffff;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
  margin-bottom: 10px;
}

.profile {
  display: flex;
  align-items: center;
  position: relative; /* 添加 position: relative; */
  cursor: pointer;
}

.username {
  margin-right: 10px;
  font-size: 16px;
  color: #666666;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: #eee;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666;
  font-size: 20px;
  cursor: pointer;
  margin-right: 10px;
  box-shadow: inset 0 0 0 1px #fff;
  transition: transform 0.3s ease;
}
.avatar:hover {
  transform: scale(1.6);
}

/* 用户菜单样式 */
.user-menu {
  position: absolute;
  top: 100%; /* 放在头像下方 */
  right: 0;
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 5px 0;
  list-style: none;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  z-index: 10;
  min-width: 120px;
}

.user-menu li {
  padding: 8px 15px;
  font-size: 14px;
  color: #333;
  cursor: pointer;
  transition: background-color 0.2s ease;
  white-space: nowrap;
}

.user-menu li:hover {
  background-color: #f0f0f0;
}

/* 卡片布局 */
.content {
  flex: 1;
  padding: 20px;
  box-sizing: border-box;
  overflow-y: auto;
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  justify-items: center;
}

.card {
  width: 100%;
  background: white;
  border-radius: 15px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  transition:
    transform 0.3s ease-in-out,
    box-shadow 0.3s;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
}

.card-actions {
  position: absolute;
  bottom: 10px;
  right: 10px;
  opacity: 0;
  transition: opacity 0.3s ease-in-out;
}

.card:hover .card-actions {
  opacity: 1;
}

.action-button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 8px 12px;
  margin-left: 5px;
  cursor: pointer;
  border-radius: 5px;
  font-size: 14px;
  transition: background-color 0.3s ease-in-out;
}

.action-button:hover {
  background-color: #0056b3;
}

.card-image {
  width: 100%;
  height: 200px;
  background-size: cover;
  background-position: center;
}

.card-content {
  padding: 20px;
  text-align: center;
}

.card-title {
  font-size: 22px;
  color: #333;
  margin-bottom: 10px;
}

.card-description {
  font-size: 14px;
  color: #666;
  margin-bottom: 20px;
}

.card-button {
  display: inline-block;
  padding: 10px 20px;
  background: linear-gradient(135deg, #6e45e2, #88d3ce);
  color: white;
  text-decoration: none;
  border-radius: 5px;
  transition: background 0.3s;
}

.card-button:hover {
  background: linear-gradient(135deg, #5a37c2, #72b2a7);
}

.form-popup {
  display: none;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: white;
  border-radius: 15px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.25);
  padding: 20px;
  width: 300px;
  /* 调整宽度 */
  z-index: 1000;
  transition: opacity 0.3s ease-in-out;
}

.form-popup.show {
  display: block;
  opacity: 1;
}

.form-container {
  text-align: center;
  max-width: 300px;
  /* 调整最大宽度 */
  padding: 15px;
  background-color: white;
}

.form-container h1 {
  color: #333;
  margin-bottom: 15px;
  font-size: 22px;
  /* 调整标题字体大小 */
}

.form-container input[type='text'],
.form-container input[type='password'] {
  width: calc(100% - 20px);
  padding: 10px;
  margin: 8px 0;
  border: 2px solid #ddd;
  background: #f9f9f9;
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.3s;
}

.form-container input[type='text']:focus,
.form-container input[type='password']:focus {
  border-color: #6e45e2;
  outline: none;
}

.form-container .btn {
  background: linear-gradient(135deg, #6e45e2, #88d3ce);
  color: white;
  padding: 12px 16px;
  border: none;
  cursor: pointer;
  width: 100%;
  margin-top: 15px;
  border-radius: 8px;
  font-size: 14px;
  transition: background 0.3s;
}

.form-container .cancel {
  background: linear-gradient(135deg, #ff6a00, #ee0979);
}

.form-container .btn:hover {
  background: linear-gradient(135deg, #5a37c2, #72b2a7);
}

/* 底部样式 */
.footer {
  text-align: center;
  padding: 10px;
  background-color: #f5f5f5;
  border-top: 1px solid #ddd;
}

/* -------------------- 个人信息编辑对话框样式 -------------------- */
.profile-dialog {
  /* 对话框整体样式 */
}
.profile-form {
  padding: 20px; /* 表单内边距 */
}
.profile-form-item {
  margin-bottom: 20px; /* 表单项间距 */
}
.avatar-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 15px;
}
.profile-avatar {
  margin-bottom: 10px;
  border-radius: 50%; /* 圆形头像 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 阴影 */
}
.upload-button {
  /* 更换头像按钮样式 */
  background-color: #409eff;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.upload-button:hover {
  background-color: #66b1ff;
}
.profile-input {
  /* 输入框样式 */
  border-radius: 5px;
  /* padding: 8px; */
  width: 100%;
  box-sizing: border-box; /* 确保内边距不影响宽度 */
}
.dialog-footer {
  /* 对话框底部按钮样式 */
  text-align: right;
}
.cancel-button {
  /* 取消按钮样式 */
  margin-right: 10px;
  background-color: #ddd;
  color: #333;
  border: none;
  padding: 8px 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.cancel-button:hover {
  background-color: #eee;
}
.save-button {
  /* 保存按钮样式 */
  background-color: #67c23a;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.save-button:hover {
  background-color: #85ce61;
}
</style>
