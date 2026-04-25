<template>
  <div class="login-container">
    <div class="layer">
      <div class="some-space">
        <div class="form">
          <h2>矿井通风优态运行调控系统</h2>
          <div class="item">
            <i class="iconfont icon-user"></i>
            <input
              autocomplete="off"
              type="text"
              class="input"
              v-model="username"
              placeholder="请输入用户名"
            />
          </div>

          <div class="item">
            <i class="iconfont icon-user"></i>
            <input
              autocomplete="off"
              type="password"
              class="input"
              v-model="password"
              @keyup.enter="login"
              placeholder="请输入密码"
            />
          </div>

          <button class="loginBtn" :disabled="isLoginAble" @click.stop="login">立即登录</button>
          <button class="loginBtn" @click.stop="ToRegister">注册账号</button>
          <div class="tip">默认用户名：YaeZed, 默认密码：160722</div>
        </div>
      </div>
    </div>
    <!--粒子功能实现，未实现-->
    <vue-particles
      id="tsparticles"
      color="#6495ED"
      :particleOpacity="0.7"
      :particlesNumber="80"
      shapeType="circle"
      :particleSize="4"
      linesColor="#6495ED"
      :linesWidth="1"
      :lineLinked="true"
      :lineOpacity="0.6"
      :linesDistance="150"
      :moveSpeed="3"
      :hoverEffect="true"
      hoverMode="grab"
      :clickEffect="true"
      clickMode="push"
    >
    </vue-particles>
    <bgAnimation></bgAnimation>
    <!--<modal title="提示"
					:content="modalContent"
					:visible.sync="visible"
					@confirm="confirm">
		</modal>-->
  </div>
</template>

<script>
import bgAnimation from '../../components/bgAnimationComponent.vue'
import { ElNotification } from 'element-plus'
import api from '../../api/api' // 导入 api.js
import { useUserDataStore } from '../../store/store' // 导入 userData store
export default {
  name: 'LoginPage',
  components: {
    bgAnimation,
  },
  data() {
    return {
      username: 'YaeZed',
      password: '160722',
    }
  },
  computed: {
    isLoginAble() {
      return !(this.username && this.password)
    },
  },
  methods: {
    async login() {
      try {
        const response = await api.login({
          // 调用 api.js 的 login 方法
          username: this.username,
          password: this.password,
        })
        console.log(response)
        if (response) {
          setTimeout(() => {
            ElNotification({
              title: this.getTitle(),
              message: '登录成功',
              type: 'success',
              duration: 2000,
            })
          }, 500)

          // 获取用户信息
          const { id, username, nickname, token, mobile, email } = response

          // 获取 store 实例
          const userDataStore = useUserDataStore()

          // 将用户信息存储到 store
          userDataStore.userData.id = id
          userDataStore.userData.nickname = nickname
          userDataStore.userData.username = username
          userDataStore.userData.token = token
          userDataStore.userData.mobile = mobile
          userDataStore.userData.email = email

          // 存储token, 存储username
          sessionStorage.setItem('username', username)
          localStorage.setItem('token', token)

          // 跳转到主页
          this.$router.push({
            path: '/HomePage',
          })
        }
      } catch (error) {
        console.error('登录失败:', error)
        ElNotification({
          title: '登录失败',
          message: '请检查用户名和密码',
          type: 'error',
          duration: 1000,
        })
      }
    },
    getTitle() {
      const userDataStore = useUserDataStore()
      const nickname = userDataStore.userData.nickname
      let date = new Date()
      let hour = date.getHours()
      if (hour <= 6) {
        return `深夜了! ${nickname}, 记得早点休息哦`
      } else if (hour <= 11) {
        return `早上好! ${nickname}, 活力满满`
      } else if (hour <= 13) {
        return `中午好! ${nickname}, 适当休息一会儿~`
      } else if (hour <= 17) {
        return `下午好! ${nickname}, 精神饱满`
      } else if (hour <= 21) {
        return `晚上好! ${nickname}, 祝您工作顺利`
      }
    },
    ToRegister() {
      this.$router.push({
        path: '/Register',
      })
    },
  },
  mounted() {
    document.title = '登录'
  },
}
</script>

<style lang="scss" scoped>
.login-container {
  .layer {
    position: absolute;
    height: 100%;
    width: 100%;
  }

  .some-space {
    color: white;
    font-weight: 100;
    letter-spacing: 2px;
    position: absolute;
    top: 50%;
    left: 50%;
    z-index: 1001;
    -webkit-transform: translate3d(-50%, -50%, 0);
    transform: translate3d(-50%, -50%, 0);

    -ms-animation: cloud 2s 3s ease-in infinite alternate;
    -moz-animation: cloud 2s 3s ease-in infinite alternate;
    -webkit-animation: cloud 2s 3s ease-in infinite alternate;
    -o-animation: cloud 2s 3s ease-in infinite alternate;
    -webkit-animation: cloud 2s 3s ease-in infinite alternate;
    animation: cloud 2s 3s ease-in infinite alternate;
  }

  .form {
    width: 460px;
    height: auto;
    background: rgba(36, 36, 85, 0.5);
    margin: 0 auto;
    padding: 35px 30px 25px;
    box-shadow: 0 0 25px rgba(255, 255, 255, 0.5);
    border-radius: 10px;

    .item {
      display: flex;
      align-items: center;
      margin-bottom: 25px;
      border-bottom: 1px solid #d3d7f7;

      i {
        color: #d3d7f7;
        margin-right: 10px;
      }
    }

    h2 {
      text-align: center;
      font-weight: normal;
      font-size: 26px;
      color: #d3d7f7;
      padding-bottom: 35px;
    }

    .input {
      font-size: 16px;
      line-height: 30px;
      width: 100%;
      color: #d3d7f7;
      outline: none;
      border: none;
      background-color: rgba(0, 0, 0, 0);
      padding: 10px 0;
    }

    .loginBtn {
      width: 100%;
      padding: 12px 0;
      border: 1px solid #d3d7f7;
      font-size: 16px;
      color: #d3d7f7;
      cursor: pointer;
      background: transparent;
      border-radius: 4px;
      margin-top: 10px;

      &:hover {
        color: #fff;
        background: #0090ff;
        border-color: #0090ff;
      }
    }

    .loginBtn:disabled {
      background-color: grey;
      /* 禁用状态的背景颜色 */
      color: #d3d3d3;
      /* 禁用状态的字体颜色 */
      cursor: not-allowed;
      /* 鼠标悬停时不显示手形光标 */
    }

    .tip {
      font-size: 12px;
      padding-top: 20px;
    }
  }

  input::-webkit-input-placeholder {
    color: #d3d7f7;
  }

  input::-moz-placeholder {
    /* Mozilla Firefox 19+ */
    color: #d3d7f7;
  }

  input:-moz-placeholder {
    /* Mozilla Firefox 4 to 18 */
    color: #d3d7f7;
  }

  input:-ms-input-placeholder {
    /* Internet Explorer 10-11 */
    color: #d3d7f7;
  }
}
</style>
