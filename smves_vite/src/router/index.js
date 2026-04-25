import { createRouter, createWebHistory } from 'vue-router' // 更新导入
import LoginPage from '../pages/User/LoginPage.vue'
import RegisterPage from '../pages/User/RegisterPage.vue'
import HomePage from '../pages/User/HomePage.vue'
import threeDPage from '@/pages/threeD/threeDPage.vue'
import threeDVentNetPage from '../pages/threeD/threeDVentNetPage.vue'
import DustRemovalPage from '@/pages/DustRemoval/DustRemovalPage.vue'
// 创建路由实例
const routes = [
  {
    path: '/',
    redirect: '/Login',
  },
  {
    path: '/Login',
    name: 'LoginPage',
    component: LoginPage,
  },
  {
    path: '/Register',
    name: 'RegisterPage',
    component: RegisterPage,
  },
  {
    path: '/Home',
    name: 'HomePage',
    component: HomePage,
  },
  {
    path: '/threeDVentNet',
    name: 'threeDVentNetComponentPage',
    component: threeDVentNetPage,
  },
  {
    path: '/threeD',
    name: 'threeDPage',
    component: threeDPage,
  },
  {
    path: '/DustRemoval',
    name: 'DustRemovalPage',
    component: DustRemovalPage,
  },
  {
    path: '/Mine',
    name: 'MinePage',
    component: () => import('@/pages/mine/MinePage.vue'),
    children: [
      {
        path: 'functionNULL',
        name: 'functionNULL',
        component: () => import('@/pages/mine/components/functionNULL.vue'),
      },
      {
        path: 'functionA',
        name: 'functionA',
        component: () => import('@/pages/mine/components/functionA.vue'),
      },
      {
        path: 'functionB',
        name: 'functionB',
        component: () => import('@/pages/mine/components/functionB.vue'),
      },
      {
        path: 'functionC',
        name: 'functionC',
        component: () => import('@/pages/mine/components/functionC.vue'),
      },
    ],
  },
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router // 导出路由实例
