<template>
  <div ref="containerRef" class="glb-viewer-container"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, defineProps, watch } from 'vue'
import * as THREE from 'three'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'
import { TextureLoader } from 'three'
import { threeDModelDataStore } from '../../../store/store' // 导入三维模型的数据仓库

// --- Refs ---
const containerRef = ref(null)

// 声明数据仓库
const threeDModelData = threeDModelDataStore()

// --- Three.js 相关的变量 ---
let scene, camera, renderer, controls, mixer, clock
let animationFrameId = null // 用于管理动画循环
let model
let animationAction // 用于存储需要进行时间判断的动画动作

// 父组件传递参数
const props = defineProps({
  src: {
    type: String,
    required: true,
  },
  playbackRate: {
    type: Number,
    default: 1,
  },
  backgroundImg: {
    type: String,
    default: null,
  },
})

// --- 动画播放函数 ---
// 从头开始播放所有动画
const playAnimations = () => {
  if (mixer && model && model.animations.length) {
    // .reset() 确保每次调用都是从第一帧开始播放
    model.animations.forEach((clip) => {
      mixer.clipAction(clip).reset().play()
    })
  }
}

// --- 动画暂停函数 ---
// 停止所有动画并将其重置到第一帧
const stopAnimations = () => {
  if (mixer) {
    // stopAllAction() 会停止所有正在播放的动作，并恢复到初始状态
    mixer.stopAllAction()
  }
}

// --- 动画渲染循环 ---
// 这个循环会持续运行，用于渲染场景和更新控制器
// --- 动画渲染循环 ---
const animate = () => {
  animationFrameId = requestAnimationFrame(animate)
  const delta = clock.getDelta()

  // 只有当 Pinia 状态为 active 时，才更新 mixer (播放动画)
  if (mixer && threeDModelData.isActive) {
    mixer.update(delta)

    // --- 在这里获取动画播放时间 ---
    // if (animationAction) {
    //   const currentTime = animationAction.time // 获取当前播放时间（秒）
    //   const totalDuration = animationAction.getClip().duration // 获取动画总时长（秒）

    //   // 打印到控制台，.toFixed(2) 保留两位小数，方便查看
    //   console.log(`当前播放时间: ${currentTime.toFixed(2)}s / ${totalDuration.toFixed(2)}s`)
    // }

    // 您原有的手动循环逻辑
    if (animationAction && animationAction.time >= animationAction.getClip().duration) {
      playAnimations()
    }
  }

  controls.update()
  renderer.render(scene, camera)
}

// --- 监听数据仓库的变化 ---
watch(
  () => threeDModelData.isActive,
  (newVal) => {
    // 防止在模型和 mixer 初始化完成前触发
    if (!mixer) return

    if (newVal) {
      console.log('Pinia: 开始播放动画')
      playAnimations()
    } else {
      console.log('Pinia: 停止播放动画')
      stopAnimations()
    }
  },
)

// --- 初始化 Three.js 场景 ---
const init = () => {
  if (!containerRef.value) return

  const container = containerRef.value
  if (props.backgroundImg) {
    const textureLoader = new TextureLoader()
    textureLoader.load(props.backgroundImg, (texture) => {
      scene.background = texture
    })
  }

  scene = new THREE.Scene()
  const width = container.clientWidth
  const height = container.clientHeight
  camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 1000)
  camera.position.set(0.0208, 6.8237, 9.4574)
  renderer = new THREE.WebGLRenderer({ antialias: true })
  renderer.setSize(width, height)
  renderer.setPixelRatio(window.devicePixelRatio)
  renderer.outputEncoding = THREE.sRGBEncoding
  container.appendChild(renderer.domElement)

  const ambientLight = new THREE.AmbientLight(0xffffff, 0.5)
  scene.add(ambientLight)
  const directionalLight = new THREE.DirectionalLight(0xffffff, 1)
  directionalLight.position.set(5, 10, 7.5)
  scene.add(directionalLight)
  controls = new OrbitControls(camera, renderer.domElement)
  controls.target.set(-0.4537, 6.106, -0.3517)
  controls.update()

  const loader = new GLTFLoader()
  loader.load(
    props.src,
    (gltf) => {
      model = gltf.scene
      scene.add(model)

      // 在这里设置好 animation mixer，但先不播放动画
      // 动画的播放将完全由 Pinia 状态来控制
      if (gltf.animations && gltf.animations.length) {
        mixer = new THREE.AnimationMixer(model)
        mixer.timeScale = props.playbackRate
        model.animations = gltf.animations

        // 【已修改】获取第一个动画的引用，用于后续的时间判断循环
        animationAction = mixer.clipAction(gltf.animations[0])
      }
    },
    undefined,
    (error) => {
      console.error('加载 GLB 文件时发生错误:', error)
    },
  )
  clock = new THREE.Clock()
}

// --- 其他函数与生命周期钩子 ---
const onResize = () => {
  if (!camera || !renderer || !containerRef.value) return
  const container = containerRef.value
  const width = container.clientWidth
  const height = container.clientHeight
  camera.aspect = width / height
  camera.updateProjectionMatrix()
  renderer.setSize(width, height)
}

let resizeObserver
onMounted(() => {
  init()
  // 初始化后立刻启动渲染循环
  // 场景会持续渲染，从而允许相机交互
  animate()

  if (containerRef.value) {
    resizeObserver = new ResizeObserver(onResize)
    resizeObserver.observe(containerRef.value)
  }
})

onUnmounted(() => {
  // 组件卸载时停止渲染循环
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId)
  }

  if (resizeObserver && containerRef.value) {
    resizeObserver.unobserve(containerRef.value)
  }
  if (renderer) {
    renderer.dispose()
    if (renderer.domElement.parentElement) {
      renderer.domElement.parentElement.removeChild(renderer.domElement)
    }
  }
})
</script>

<style>
.glb-viewer-container {
  width: 100%;
  height: 100%;
  min-height: 400px;
  overflow: hidden;
}
</style>
