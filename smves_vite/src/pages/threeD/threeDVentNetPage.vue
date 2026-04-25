<template>
  <div class="threeDBody">
    <header class="threeDHeader">
      <!-- <button  onclick="send()" style="right: 0; display: inline-block; height: 20px; width: 100px;"> </button> -->
      <h1 style="text-align: center">矿井通风智能管控系统</h1>
      <div class="showTime"></div>
      <button class="small button" @click="getData()">形成巷道网络</button>
    </header>
    <!-- 页面主题部分 -->
    <div class="main_">
      <section class="mainbox">
        <!-- 第一列 -->
        <!-- <div class="column">
          <div class="panel line">
            <h2>主通风机智能监控</h2>
            <div class="chart"></div>
            <div class="panel-footer"></div>
          </div>
          <div class="panel bar">
            <h2>局部通风机智能管控</h2>
            <div class="chart"></div>
            <div class="panel-footer"></div>
          </div>
          <div class="panel pie">
            <h2>关键线路阻力检测</h2>
            <div class="chart"></div>
            <div class="panel-footer"></div>
          </div>
        </div> -->

        <!-- 第二列 -->
        <div class="column">
          <div class="column-main" style="height: 850px; width: 910px"></div>

          <!-- <div class="panel bottom-panel" style="position: absolute; bottom: -6%; margin-top: 20px">
            <h2>矿井风量精准检测</h2>
            <div class="chart bottom-chart"></div>
            <div class="panel-footer"></div>
          </div> -->
        </div>

        <!-- 第三列 -->
        <!-- <div class="column" style="width: 500px">
          <div class="panel pie2">
            <h2>采煤工作面通风智能管控</h2>
            <div class="chart"></div>

            <div class="panel-footer"></div>
          </div>
          <div class="panel">
            <h2>通风设备远程控制</h2>
            <div class="chart">
              <br />
              <br />
              <button class="btn" style="text-align: center">
                <span>远程自动平衡风门</span></button
              ><br />
              <button class="btn"><span>定量调节自动风窗</span></button><br />
              <button class="btn"><span>风量检测</span></button><br />
            </div>
            <div class="panel-footer"></div>
          </div>
          <div class="panel pie3">
            <h2>预警信息</h2>
            <div class="chart"></div>

            <div class="panel-footer"></div>
          </div>
        </div> -->
      </section>
    </div>
  </div>
</template>
<script>
export default {
  name: 'threeDVentNetPage',
}
</script>
<script setup>
/* eslint-disable */
import axios from 'axios'
import { onMounted, nextTick } from 'vue'
import $ from 'jquery'
import * as THREE from 'three'
import * as echarts from 'echarts'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'
// import type { nextTick } from 'process'
// window.echarts = echarts

const scene_property = {
  /* 点光源颜色 */
  //point_color : 0xffffff,
  point_color: 0x70db93,
  /* 点光源位置 */
  point_position_x: 400,
  point_position_y: 200,
  point_position_z: 300,
  /* 环境光 */
  ambient: 0x66ffff,
  /* 相机位置 */
  camera_position_x: 500,
  camera_position_y: 0,
  camera_position_z: 200,
  /* 渲染器_透明度*/
  renderer_setClearAlpha: 0.2,
  /* 渲染器的背景颜色 */
  renderer_setClearColor_bgcolor: 0x00008b,
  /* 渲染器不透明度 */
  renderer_setClearColor_degree: 0.001,
}

/** 管道对象 */
const tube_property = {
  side: THREE.DoubleSide,
  // 材质
  material_transparent: true,
  material_color: 0x99ffff,
  // 风速
  // wind_spreed:10;
}

const ball_property = {
  /* 属性 */
  ball_pro_x: 1,
  ball_pro_y: 32,
  ball_pro_z: 16,
  radius: 3,

  /* 颜色 */
  ball_color: 0x54e47b,
  ball_side: THREE.DoubleSide, //双面可见
}

const tag_property = {
  /* 标签大小 */
  tag_scale: [20, 10, 1],
  /* 画布对象 */
}

// 原先tfwangluo
var textureLoader = new THREE.TextureLoader()
var texture = textureLoader.load('./images/箭头.png')
texture.wrapS = THREE.RepeatWrapping // THREE.RepeatWrapping，纹理将简单地重复到无穷大。
texture.wrapT = THREE.RepeatWrapping
texture.repeat.set(4, 2)

/* 球体：附属于管道 */
var ballGeometry = new THREE.SphereGeometry(
  ball_property.ball_pro_x,
  ball_property.ball_pro_y,
  ball_property.ball_pro_z,
)
var ballMaterial = new THREE.MeshBasicMaterial({
  color: ball_property.ball_color,
  side: ball_property.ball_side, //双面可见
})

/* canvas 画笔 */
function getTextToCanvas(text) {
  let width = 200
  let height = 100
  //let width = 512;
  //let height = 256;
  let canvas = document.createElement('canvas')
  canvas.width = width // 设置画布的宽度
  canvas.height = height // 设置画布的高度
  let contentStyle = canvas.getContext('2d') // 设置画布内2D相关属性
  // contentStyle.globalAlpha = 0.5
  // 精灵背景颜色
  // Tag 背景颜色
  /* 背景颜色透明 */
  contentStyle.fillStyle = 'rgba(255,255,255,0)'
  contentStyle.fillRect(0, 0, width, height)
  // 字体大小设置
  contentStyle.font = 33 + 'px ' + ' bold'
  //字体颜色设置
  contentStyle.fillStyle = '#ffffff'
  contentStyle.textAlign = 'center'
  contentStyle.textBaseline = 'middle'
  contentStyle.fillText(text, width / 2, height / 2)
  return canvas
}
var scene = new THREE.Scene()
var group = new THREE.Group()
var camera = new THREE.PerspectiveCamera(40, window.innerWidth / window.innerHeight, 1, 1000)

/**通风网络对象 */
function tfwangluo(div) {
  /*   var width = div.clientWidth; //窗口宽度
    var height = div.clientHeight; //窗口高度 */
  scene = new THREE.Scene()
  group = new THREE.Group()
  scene.add(group)
  /* 点光源 */
  var point = new THREE.PointLight(scene_property.point_color) //点光源颜色
  point.position.set(
    scene_property.point_position_x,
    scene_property.point_position_y,
    scene_property.point_position_z,
  )
  scene.add(point) //点光源添加到场景中
  /* 环境光 */
  var ambient = new THREE.AmbientLight(scene_property.ambient)
  scene.add(ambient)

  /* 相机 */
  //var k = width /height; //窗口宽高比
  //var s = 150; //三维场景显示范围控制系数，系数越大，显示的范围越大
  //let camera = new THREE.OrthographicCamera(-s * k, s * k, s, -s, 1, 1000);
  camera.position.set(
    scene_property.camera_position_x,
    scene_property.camera_position_y,
    scene_property.camera_position_z,
  )
  // camera.position.set(center.x, center.y, center.z - cameraDistance);
  // camera.near = 0.1;
  // camera.lookAt(scene.position);

  //将z轴朝上
  // camera.up.x = 0;
  // camera.up.y = 0;
  // camera.up.z = 1;

  /* 渲染器 */
  var renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true })
  renderer.setClearAlpha(scene_property.setClearAlpha)
  renderer.setSize(div.clientWidth, div.clientHeight)
  renderer.setClearColor(
    scene_property.renderer_setClearColor_bgcolor,
    scene_property.renderer_setClearColor_degree,
  ) // 背景颜色  和 不透明度
  div.appendChild(renderer.domElement)

  var this_scene = scene
  // 渲染函数
  function render() {
    texture.needsUpdate = true
    /* 巷道上箭头速度 */
    texture.offset.x -= 0.03
    //texture.offset.x += 0.3;
    renderer.render(this_scene, camera) //执行渲染操作
    requestAnimationFrame(render)
  }
  render()
  // 创建射线投射器
  const raycaster = new THREE.Raycaster()
  // 鼠标位置
  const mouse = new THREE.Vector2()

  const texture_clicked = textureLoader.load('./images/箭头4.png')
  texture_clicked.wrapS = THREE.RepeatWrapping // THREE.RepeatWrapping，纹理将简单地重复到无穷大。
  texture_clicked.wrapT = THREE.RepeatWrapping
  texture_clicked.repeat.set(4, 4)

  let selectedObject

  // 鼠标点击事件监听
  renderer.domElement.addEventListener('click', mouseClick, false)
  function mouseClick(event) {
    if (selectedObject) {
      selectedObject.material.map = texture
    }
    const canvas = renderer.domElement
    mouse.x = ((event.clientX - canvas.offsetLeft) / canvas.width) * 2 - 1
    mouse.y = -((event.clientY - canvas.offsetTop) / canvas.height) * 2 + 1
    // 设置射线起点为鼠标位置，射线的方向为相机视角方向
    raycaster.setFromCamera(mouse, camera)
    // 计算射线相交
    const intersects = raycaster.intersectObjects(scene.children, true)
    console.log(intersects)
    if (intersects.length > 0) {
      // 选中物体
      selectedObject = intersects[0].object
      if (selectedObject.material instanceof THREE.MeshLambertMaterial) {
        // 改变当前被点击物体的颜色
        selectedObject.material.map = texture_clicked
      }
    }
  }

  //创建控件对象  相机对象camera作为参数   控件可以监听鼠标的变化，改变相机对象的属性
  var controls = new OrbitControls(camera, renderer.domElement)
  //监听鼠标事件，触发渲染函数，更新canvas画布渲染效果
  controls.addEventListener('change', function () {
    // texture.needsUpdate = true;

    renderer.render(this_scene, camera) //执行渲染操作
  })

  // 控制旋转中心
  controls.target.set(1000, 0, 0)
  //启用阻尼效果
  // controls.enableDamping = true;
  // 阻尼系数
  // controls.dampingFactor = .05
  // 旋转速度
  controls.rotateSpeed = 0.5
  // 平移速度
  controls.panSpeed = 0.5
  // 自动旋转
  controls.autoRotate = true
  controls.autoRotateSpeed = 0.5

  /* 平面 */
  // var helper = new THREE.GridHelper(500, 20);
  // 	scene.add(helper);
  /* 坐标轴 */
  // var axisHelper = new THREE.AxisHelper(250);
  // scene.add(axisHelper);

  this.setTubes = function (tubes) {
    console.log(tubes)
    group = new THREE.Group()
    scene.add(group)
    for (var i = 0; i < tubes.length; i += 1) {
      group.add(tubes[i])
      // tubes[i].renderOrder = 999;
      // tubes[i].material.depthTest = false
      /* 如果管道存在，则有球在管道两端坐标     两端两个*/
      if (tubes[i].ballMesh1) {
        group.add(tubes[i].ballMesh1)
        // tubes[i].ballMesh1.renderOrder = 999;
        // tubes[i].ballMesh1.material.depthTest = false
      }
      if (tubes[i].ballMesh2) {
        group.add(tubes[i].ballMesh2)
        // tubes[i].ballMesh2.material.transparent=false
        // tubes[i].ballMesh2.renderOrder = 999;
      }
      /* 如果管道存在，则有标签在管道上 */
      if (tubes[i].tag) {
        // tubes[i].tag.renderOrder = -1;
        tubes[i].tag.material.depthTest = false
        group.add(tubes[i].tag)
      }
    }
  }

  this.updateTag = function (name, text) {
    var tagObject = scene.getObjectByName(name)
    if (tagObject.text != text) {
      var newMaterialMap = new THREE.TextureLoader().load(
        getTextToCanvas(text).toDataURL('image.png'),
      )
      tagObject.material.map = newMaterialMap
      tagObject.text = text
    }
  }
}

// console.log(tfwangluo(amount));
/* 管道 */
var tube = function (id, p1, p2, text) {
  var z1 = new THREE.Vector3(p1.x, p1.y, p1.z)
  var z2 = new THREE.Vector3(p2.x, p2.y, p2.z)
  let line = new THREE.LineCurve3(z1, z2)

  var CurvePath = new THREE.CurvePath() // 创建CurvePath对象
  CurvePath.curves.push(line) // 插入多段线条
  var geometry1 = new THREE.TubeGeometry(CurvePath, 100, 1, 25, false)

  // var tube_property1 = new tube_property();
  var material1 = new THREE.MeshLambertMaterial({
    transparent: tube_property.material_transparent,
    color: tube_property.material_color,
    side: tube_property.side, //双面可见
    map: texture,
    opacity: 0.6, //管道透明效果

    //transparent:false,
  }) //材质对象
  var mesh = new THREE.Mesh(geometry1, material1) //InstancedMesh
  // 计算模型尺寸   boundingBox.getSize()  该方法将返回一个包含模型尺寸的向量对象
  var boundingBox = new THREE.Box3().setFromObject(mesh)

  const size = new THREE.Vector3()
  boundingBox.getSize(size)
  // 计算相机位置
  // 将相机放在距离模型2倍尺寸的地方
  const cameraDistance = size.length() * 2
  const center = new THREE.Vector3()
  boundingBox.getCenter(center)

  camera.position.set(center.x, center.y, center.z - cameraDistance)
  camera.near = 0.1
  camera.far = cameraDistance * 10

  mesh.name = id
  var ballMesh1 = new THREE.Mesh(ballGeometry, ballMaterial)
  ballMesh1.position.set(p1.x, p1.y, p1.z)
  mesh.ballMesh1 = ballMesh1

  var ballMesh2 = new THREE.Mesh(ballGeometry, ballMaterial)
  ballMesh2.position.set(p2.x, p2.y, p2.z)
  mesh.ballMesh2 = ballMesh2
  // TODO 计算标签坐标
  if (text) {
    var tag1 = new tag(p1, p2, text)
    tag1.name = id + '_tag'
    mesh.tag = tag1
  }
  return mesh
}

var tag = function (p1, p2, text) {
  //let width = 200;
  //let height = 100;
  let width = 512
  let height = 256
  let canvas = document.createElement('canvas')
  canvas.width = width // 设置画布的宽度
  canvas.height = height // 设置画布的高度
  let contentStyle = canvas.getContext('2d') // 设置画布内2D相关属性
  // 精灵背景颜色
  //contentStyle.setColor = '#FFB6C1';

  //contentStyle.fillRect(40, 0, width, height);
  contentStyle.fillStyle = '#000000'
  contentStyle.fillRect(0, 0, width, height)
  // 字体大小设置
  contentStyle.font = 70 + 'px ' + ' bold'
  //字体颜色设置
  //contentStyle.fillStyle = '#FFB6C1';
  contentStyle.fillStyle = '#2891FF'
  contentStyle.textAlign = 'center'
  contentStyle.textBaseline = 'middle'
  contentStyle.fillText(text, width / 2, height / 2)
  /*    let contentStyle = canvas.getContext('2d'); // 设置画布内2D相关属性
     // 精灵背景颜色
     // contentStyle.setColor = '#FFFFFF';

     contentStyle.fillRect(40, 0, width, height);
     // 字体大小设置
     contentStyle.font = 60 + 'px '+' bold';
     //字体颜色设置
     contentStyle.fillStyle = '#fffafa';
     contentStyle.textAlign = 'center';
     contentStyle.textBaseline = 'middle';
     contentStyle.fillText(text, width/2, height/2); */

  var picUrl = getTextToCanvas(text).toDataURL('image.png')

  var texture = new THREE.TextureLoader().load(picUrl)
  // console.log(texture);

  var tagMaterial = new THREE.SpriteMaterial({
    //color: color,
    map: texture,
    transparent: false,
  })
  var tag = new THREE.Sprite(tagMaterial)
  // 设置位置
  var tag_x = parseInt((p1.x + p2.x) / 2)
  var tag_y = parseInt((p1.y + p2.y) / 2 + 5)
  var tag_z = parseInt((p1.z + p2.z) / 2)
  tag.position.set(tag_x, tag_y, tag_z)

  // 设置大小
  tag.scale.set(tag_property.tag_scale[0], tag_property.tag_scale[1], tag_property.tag_scale[2])
  tag.text = text
  return tag
}

var tfwangluo1

function getData() {
  send()
  updateData()
}
function send() {
  axios
    .get('http://127.0.0.1:8000/api/mines/ThreeDMineTunnel/')
    .then(function (response) {
      // console.log("数据类型：", typeof response.data);
      // console.log("数据内容：", response.data);
      var results = response.data
      /* 管道，循环遍历results数组，创建管道对象 */
      var tubes = []
      for (var i = 0; i < results.data.length; i++) {
        var id = results.data[i].id
        // console.log("进入循环");
        var p1 = {
          x: parseFloat(results.data[i].point_left_x),
          y: parseFloat(results.data[i].point_left_y),
          z: parseFloat(results.data[i].point_left_z),
        }
        var p2 = {
          x: parseFloat(results.data[i].point_right_x),
          y: parseFloat(results.data[i].point_right_y),
          z: parseFloat(results.data[i].point_right_z),
        }
        let text = '风速：' + results.data[i].tube_wind_speed + 'm/s'
        console.log(id, p1, p2, text)
        tubes.push(new tube(id, p1, p2, text))
      }
      console.log('tubes:' + tubes)
      tfwangluo1.setTubes(tubes)
    })
    .catch(function (error) {
      console.error('发生错误：', error)
    })
}

function updateData() {
  axios
    .get('http://127.0.0.1:8000/api/mines/ThreeDMineTunnel/')
    .then(function (response) {
      console.log(response.data)
      var results = response.data
      for (var i = 0; i < results.data.length; i++) {
        tfwangluo1.updateTag(
          results.data[i].id + '_tag',
          '风速：' + results.data[i].tube_wind_speed + 'm/s',
        )
        // console.log(response.data[i].tube_wind_speed);
      }
    })
    .catch(function (error) {
      console.error('发生错误：', error)
    })
    .then(() => {
      setTimeout(updateData, 1000) // 每1000毫秒调用一次updateData
    })
}

onMounted(() => {
  nextTick(() => {
    // runCharts()
    // 确保 DOM 完全渲染
    var div = document.querySelector('.column-main') // 选择 .column-main 元素
    if (div) {
      // 检查元素是否存在
      console.log(div.offsetHeight) // 打印高度
      // initScene(div); // 可以根据需要启用这一行
      tfwangluo1 = new tfwangluo(div) // 创建 tfwangluo 实例
    } else {
      console.error('.column-main not found') // 错误处理
    }
  })
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  user-select: none;
}
.threeDBody {
  background: url(../images/bg.jpg) no-repeat top center;
  line-height: 1.15;
  background-size: 100% 100%;
  background-attachment: fixed;
}
.threeDHeader {
  height: 4rem; /* 增大高度 */
  background: url(../images/head_bg.png) no-repeat;
  background-size: cover;
}
.threeDHeader h1 {
  color: white;
  font-size: 2rem; /* 增大字体大小 */
  line-height: 2rem; /* 调整行高来与新的高度匹配 */
  text-align: center;
}
.threeDHeader .showTime {
  position: absolute;
  right: 0.375rem;
  line-height: 0.9375rem;
  color: rgba(255, 255, 255, 0.7);
  top: 0;
}
.small.button {
  display: inline-block;
  padding: 0.5rem 1rem;
  font-size: 0.82rem; /* 调整字体大小 */
  color: #fff; /* 字体颜色为白色 */
  background-color: #007bff; /* 按钮背景色 */
  border: none; /* 去掉边框 */
  border-radius: 0.25rem; /* 圆角 */
  text-align: center; /* 文字居中 */
  cursor: pointer; /* 鼠标悬停时显示为手型 */
  transition: background-color 0.3s; /* 背景颜色过渡效果 */
}

.small.button:hover {
  background-color: #0056b3; /* 鼠标悬停时背景色变化 */
}
.mainbox {
  display: flex;
  width: 100%;
  min-width: 1024px;
  margin: 0 auto;
  padding: 0.125rem 0.125rem 0;
}
.mainbox .column {
  flex: 2;
}
.mainbox .column:nth-child(2) {
  flex: 5;
  margin: 0 0.125rem 0.1875rem;
  overflow: hidden;
}
.mainbox .panel {
  position: relative;
  height: 14rem;
  padding: 0 0.1875rem 0.5rem;
  border: 1px solid rgba(25, 186, 139, 0.17);
  margin-bottom: 0.1875rem;
  background: url(../images/line1.png) rgba(255, 255, 255, 0.03);
}
.mainbox .panel::before {
  position: absolute;
  top: 0;
  left: 0;
  width: 10px;
  height: 10px;
  border-left: 2px solid #02a6b5;
  border-top: 2px solid #02a6b5;
  content: '';
  overflow: hidden;
}
.mainbox .panel::after {
  position: absolute;
  top: 0;
  right: 0;
  width: 10px;
  height: 10px;
  border-right: 2px solid #02a6b5;
  border-top: 2px solid #02a6b5;
  content: '';
}
.mainbox .panel .panel-footer {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
}
.mainbox .panel .panel-footer::before {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 10px;
  height: 10px;
  border-left: 2px solid #02a6b5;
  border-bottom: 2px solid #02a6b5;
  content: '';
}
.mainbox .panel .panel-footer::after {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 10px;
  height: 10px;
  border-right: 2px solid #02a6b5;
  border-bottom: 2px solid #02a6b5;
  content: '';
}
.mainbox .panel h2 {
  height: auto; /* 自动调整高度 */
  color: #fff;
  line-height: 1.2; /* 调整行高 */
  text-align: center;
  font-size: 1rem; /* 调整字体大小 */
  font-weight: 400;
  white-space: normal; /* 允许换行 */
  overflow-wrap: break-word; /* 允许长单词换行 */
}

.mainbox .panel .chart {
  height: 13rem;
}
.mainbox .panel .chart2 {
  display: inline-block;
  height: 1.5rem;
  width: 2.87rem;
  background-color: #02a6b5;
  margin: 2px;
  border-radius: 2rem;
}
.mainbox .panel .column-main {
  height: 850px;
}
.mainbox .bottom-panel {
  width: 835px;
  margin: 0.125rem;
}
.mainbox .btn {
  display: inline-block;
  padding-left: 10px;
  border-radius: 4px;
  background-color: #5fa0fa;
  border-left: 20px;
  color: #ffffff;
  text-align: center;
  font-size: 15px;
  padding: 2px;
  width: 266px;
  height: 37px;
  transition: all 0.7s;
  cursor: pointer;
  margin-bottom: 15px;
  margin-left: 50px;
  vertical-align: middle;
}
.mainbox .btn span {
  cursor: pointer;
  display: inline-block;
  position: relative;
  transition: 0.5s;
}
.mainbox .btn span:after {
  content: '»';
  position: absolute;
  opacity: 0;
  top: 0;
  right: -20px;
  transition: 0.5s;
}
.mainbox .btn:hover span {
  padding-right: 25px;
}
.mainbox .btn:hover span:after {
  opacity: 1;
  right: 0;
}
</style>
