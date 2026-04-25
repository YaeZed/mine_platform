import request from './request'

export default {
  //用户登录
  login(data) {
    return request({
      url: '/users/login/',
      method: 'post',
      data: data,
    })
  },
  //用户编辑
  editUser(data) {
    return request({
      url: `/users/edit/${data.id}/`,
      method: 'post',
      data: data,
    })
  },
  //获取三维巷道模型数据
  getThreeDTunnelsData() {
    return request({
      url: '/mines/ThreeDMineTunnel/',
      method: 'get',
    })
  },
}
