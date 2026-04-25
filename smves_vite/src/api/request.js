import axios from 'axios'
import { ElMessage } from 'element-plus'

const request = axios.create({
  baseURL: 'http://localhost:8000/api', // api的base_url
  timeout: 5000, // 请求超时时间
})
const NETWORK_ERROR_MSG = '网络错误，请检查网络连接'
// 添加请求拦截器
request.interceptors.request.use(
  function (config) {
    // 在发送请求之前做些什么
    return config
  },
  function (error) {
    // 对请求错误做些什么
    return Promise.reject(error)
  },
)

// 添加响应拦截器
request.interceptors.response.use((res) => {
  console.log(res.data)
  // 对响应数据做点什么
  const { status, data, message } = res.data
  if (status === 200) {
    return data
  } else {
    ElMessage.error(message || NETWORK_ERROR_MSG)
    return Promise.reject(message || NETWORK_ERROR_MSG)
  }
})

export default request
