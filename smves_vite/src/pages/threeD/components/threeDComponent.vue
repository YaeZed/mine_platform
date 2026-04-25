<template>
  <div class="threeDComponent">
    <el-button class="threeD-button" type="primary" size="large" @click="renderModel">
      生成巷道网络
    </el-button>
    <div class="threeDTunnel-container" ref="threeDTunnelContainer"></div>
  </div>
</template>

<script setup>
import { ElMessage } from 'element-plus'
import { onMounted, ref, nextTick, getCurrentInstance } from 'vue'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'
// 导入平滑曲线模块
import { CatmullRomCurve3 } from 'three/src/extras/curves/CatmullRomCurve3.js'

const { proxy } = getCurrentInstance()

// 使用 ref 来获取 DOM 元素
const threeDTunnelContainer = ref(null)

// 定义场景、相机、渲染器等核心变量
let scene, camera, renderer, controls, group
// 用于存储需要纹理动画的管道
const animatedTubes = ref([])

// 定义是否已生成模型
let isModelGenerated = false

// 纹理加载器
const textureLoader = new THREE.TextureLoader()

// 获取巷道网络数据 (模拟)
const getData = async () => {
  console.log('正在获取数据...')
  try {
    const results = await proxy.$api.getThreeDTunnelsData()
    ElMessage({
      type: 'primary',
      message: '数据获取成功，模型渲染中...',
      showClose: true,
    })
    return results
  } catch (error) {
    ElMessage.error('数据获取失败')
    throw error
  }
}

// 获取管道的实际长度
const getTubeLength = (p1, p2) => {
  return new THREE.Vector3(p1.x, p1.y, p1.z).distanceTo(new THREE.Vector3(p2.x, p2.y, p2.z))
}

// --- 核心 Three.js 函数 ---

// 初始化函数: 负责所有一次性设置
const init = () => {
  const container = threeDTunnelContainer.value
  if (!container) return

  // 1. 场景
  scene = new THREE.Scene()
  group = new THREE.Group()
  scene.add(group)

  // 2. 相机
  camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 1, 30000)
  camera.position.set(4800, 3800, 1000)

  // 3. 渲染器
  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true })
  renderer.setSize(container.clientWidth, container.clientHeight)
  renderer.setPixelRatio(window.devicePixelRatio)
  // renderer.setClearColor(0x00008b, 0.2)
  renderer.sortObjects = false
  container.appendChild(renderer.domElement)

  // 4. 光源
  const ambientLight = new THREE.AmbientLight(0xffffff, 2.5)
  scene.add(ambientLight)
  const pointLight = new THREE.PointLight(0x70db93, 5000000, 0)
  pointLight.position.set(4700, 3800, 0)
  scene.add(pointLight)

  // 5. 控制器
  controls = new OrbitControls(camera, renderer.domElement)
  controls.enableDamping = true
  controls.dampingFactor = 0.05
  controls.rotateSpeed = 0.5
  controls.target.set(4790, 3840, -790)
  controls.update()

  // 6. 启动动画循环
  animate()
}

// 动画循环函数
const animate = () => {
  requestAnimationFrame(animate)

  animatedTubes.value.forEach((tube) => {
    if (tube.material.map && tube.userData.windSpeed) {
      const speedFactor = 0.000001
      tube.material.map.offset.x -= tube.userData.windSpeed * speedFactor
    }
  })

  controls.update()
  renderer.render(scene, camera)
}

// 主渲染函数，由按钮点击触发
const renderModel = async () => {
  if (isModelGenerated) {
    ElMessage.info('模型已经生成，请勿重复点击。')
    return
  }

  try {
    const tubesData = await getData()
    if (!tubesData || tubesData.length === 0) {
      ElMessage.warning('未获取到有效的巷道数据。')
      return
    }

    group.clear()
    animatedTubes.value = []

    const textures = {
      high_speed: textureLoader.load('/images/高标风速.jpg'),
      high_lower_speed: textureLoader.load('/images/高标低风速.jpg'),
      mid_speed: textureLoader.load('/images/52.png'),
      low_higher_speed: textureLoader.load('/images/低标高风速.jpg'),
      low_speed: textureLoader.load('/images/低标风速.png'),
    }

    const materials = {
      highSpeed: new THREE.MeshBasicMaterial({ map: textures.high_speed, side: THREE.DoubleSide }),
      highLowerSpeed: new THREE.MeshBasicMaterial({
        map: textures.high_lower_speed,
        side: THREE.DoubleSide,
      }),
      midSpeed: new THREE.MeshBasicMaterial({ map: textures.mid_speed, side: THREE.DoubleSide }),
      lowHigherSpeed: new THREE.MeshBasicMaterial({
        map: textures.low_higher_speed,
        side: THREE.DoubleSide,
      }),
      lowSpeed: new THREE.MeshBasicMaterial({ map: textures.low_speed, side: THREE.DoubleSide }),
    }

    // --- 升级版修改：开始 ---
    // 1. Map现在存储一个对象，包含点、最大风速和对应的材质
    const uniquePoints = new Map()
    // --- 升级版修改：结束 ---

    tubesData.forEach((data) => {
      const p1 = {
        x: Number(data['point_left_x']),
        y: Number(data['point_left_y']),
        z: Number(data['point_left_z']),
      }
      const p2 = {
        x: Number(data['point_right_x']),
        y: Number(data['point_right_y']),
        z: Number(data['point_right_z']),
      }

      if (isNaN(p1.x) || isNaN(p1.y) || isNaN(p1.z) || isNaN(p2.x) || isNaN(p2.y) || isNaN(p2.z)) {
        console.error('Invalid coordinates:', data)
        return
      }

      const text = `${data['tube_name']} 风量: ${data['tube_wind_speed']} m³/min`
      let material
      const speed = data['tube_wind_speed']

      if (speed >= 2000) material = materials.highSpeed
      else if (speed >= 1000) material = materials.highLowerSpeed
      else if (speed >= 500) material = materials.midSpeed
      else if (speed >= 100) material = materials.lowHigherSpeed
      else material = materials.lowSpeed

      // --- 升级版修改：开始 ---
      // 2. 定义一个更新函数，用于检查并更新连接点的材质
      const updateJunctionPoint = (point, key) => {
        if (!uniquePoints.has(key)) {
          // 如果点不存在，则直接存入
          uniquePoints.set(key, {
            point: new THREE.Vector3(point.x, point.y, point.z),
            maxSpeed: speed,
            material: material,
          })
        } else {
          // 如果点已存在，比较风速
          const existingPoint = uniquePoints.get(key)
          if (speed > existingPoint.maxSpeed) {
            // 如果当前管道风速更高，则更新该点的材质和最大风速
            existingPoint.maxSpeed = speed
            existingPoint.material = material
          }
        }
      }

      const key1 = `${p1.x},${p1.y},${p1.z}`
      const key2 = `${p2.x},${p2.y},${p2.z}`
      updateJunctionPoint(p1, key1)
      updateJunctionPoint(p2, key2)
      // --- 升级版修改：结束 ---

      material.map.wrapS = THREE.RepeatWrapping
      material.map.wrapT = THREE.RepeatWrapping
      const tubeLength = getTubeLength(p1, p2)
      material.map.repeat.set(tubeLength / 20, 4)

      const newTube = createTube(data.id, p1, p2, text, material, speed)
      if (newTube) {
        group.add(newTube)
        animatedTubes.value.push(newTube)
      }
    })

    // --- 升级版修改：开始 ---
    // 3. 创建连接点球体时，使用记录下的、风速最高的材质
    const junctionGeometry = new THREE.SphereGeometry(3.1, 32, 16) // 半径略微增大一点点(如3.1)，可以避免与管道表面重叠可能产生的闪烁问题

    for (const junction of uniquePoints.values()) {
      // 直接使用存储在 junction 对象中的材质
      const junctionSphere = new THREE.Mesh(junctionGeometry, junction.material)
      junctionSphere.position.copy(junction.point)
      group.add(junctionSphere)

      // 如果连接点材质也是需要动画的，也把它加入列表
      // 注意：这要求所有材质的纹理都已经设置了 RepeatWrapping
      if (junction.material.map && junction.material.map.wrapS === THREE.RepeatWrapping) {
        const animatedSphere = junctionSphere
        animatedSphere.userData.windSpeed = junction.maxSpeed // 将风速也存起来
        animatedTubes.value.push(animatedSphere)
      }
    }
    // --- 升级版修改：结束 ---

    isModelGenerated = true
  } catch (error) {
    console.error('模型生成失败:', error)
    ElMessage.error(`模型生成失败: ${error.message}`)
    isModelGenerated = false
  }
}

// 创建管道（使用 CatmullRomCurve3 创建平滑连接）
const createTube = (id, p1, p2, text, material, speed) => {
  // 1. 创建管道几何体
  const startPoint = new THREE.Vector3(p1.x, p1.y, p1.z)
  const endPoint = new THREE.Vector3(p2.x, p2.y, p2.z)

  // 创建一个包含两个点的平滑曲线
  // 由于你的数据是独立的管道段，我们直接使用这两个点来定义曲线
  const path = new CatmullRomCurve3([startPoint, endPoint])

  // 使用平滑曲线生成管道
  // tubeSegments: 增加分段数使管道更平滑
  // radius: 管道半径
  // radialSegments: 增加径向分段数使管道更圆滑
  const tubeGeometry = new THREE.TubeGeometry(path, 100, 3, 64, false)

  const tubeMesh = new THREE.Mesh(tubeGeometry, material)
  tubeMesh.name = `tube-${id}`
  tubeMesh.userData.windSpeed = speed || 0

  // 2. 移除之前创建的连接点球体，因为平滑曲线不再需要它们

  // 3. 创建文本标签
  if (text) {
    const tag = createTag(p1, p2, text)
    if (tag) {
      tubeMesh.add(tag)
    }
  }

  return tubeMesh
}

// 标签生成函数
const createTag = (p1, p2, text) => {
  const canvas = getTextToCanvas(text)
  const texture = new THREE.CanvasTexture(canvas)
  texture.needsUpdate = true
  texture.minFilter = THREE.LinearFilter
  texture.magFilter = THREE.LinearFilter

  const tagMaterial = new THREE.SpriteMaterial({
    map: texture,
    depthTest: false,
    transparent: true,
    opacity: 1,
  })

  const tag = new THREE.Sprite(tagMaterial)

  const tag_x = (p1.x + p2.x) / 2
  const tag_y = (p1.y + p2.y) / 2 + 20
  const tag_z = (p1.z + p2.z) / 2
  tag.position.set(tag_x, tag_y, tag_z)

  // 动态设置标签大小
  const scaleFactor = 10
  tag.scale.set((canvas.width / canvas.height) * scaleFactor, scaleFactor, 1)

  tag.text = text
  return tag
}

// 文本转 Canvas 的函数，负责生成高分辨率、自适应的标签
const getTextToCanvas = (text) => {
  const canvas = document.createElement('canvas')
  const ctx = canvas.getContext('2d')

  // 1. 设置字体和基础尺寸
  const fontSize = 28 // 增加字体大小
  const padding = 20
  const font = `bold ${fontSize}px sans-serif`
  ctx.font = font

  // 2. 测量文本宽度
  const metrics = ctx.measureText(text)
  const textWidth = metrics.width
  const textHeight = fontSize

  // 3. 动态设置画布尺寸以适应文本
  canvas.width = textWidth + padding * 2
  canvas.height = textHeight + padding * 2

  // 4. 重新设置字体和样式（因为改变画布尺寸会重置上下文）
  ctx.font = font
  ctx.fillStyle = '#FFFFFF'
  ctx.textAlign = 'center'
  ctx.textBaseline = 'middle'

  // 5. 绘制文本
  ctx.fillText(text, canvas.width / 2, canvas.height / 2)

  return canvas
}

// onMounted 钩子
onMounted(() => {
  nextTick(() => {
    init()
  })
})
</script>

<style scoped>
.threeDComponent {
  background-image: linear-gradient(to top, #09203f 0%, #537895 100%);
}

.threeDTunnel-container {
  width: 1700px;
  height: 850px;
}

.threeD-button:hover {
  box-shadow: 0px 5px 8px rgba(0, 0, 0, 0.2);
  transform: translateY(-3px);
}

.threeD-button:active {
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);
  transform: translateY(3px);
}
</style>
