# 矿井巷道三维可视化模块

> 基于 **Three.js** 实现的矿井巷道网络三维交互式可视化，支持风速等级纹理渲染、动态风流动画与矿工人员实时漫游仿真。

---

## 目录

- [功能概览](#功能概览)
- [目录结构](#目录结构)
- [技术栈](#技术栈)
- [数据接口](#数据接口)
- [核心实现](#核心实现)
  - [场景初始化](#场景初始化)
  - [管道渲染](#管道渲染)
  - [风速纹理系统](#风速纹理系统)
  - [连接点球体](#连接点球体)
  - [矿工漫游动画](#矿工漫游动画)
  - [巷道标签](#巷道标签)
- [使用说明](#使用说明)
- [依赖说明](#依赖说明)

---

## 功能概览

| 功能 | 描述 |
|------|------|
| 🏗️ 巷道网络渲染 | 根据后端接口数据自动生成三维管道网络，每段巷道为一个 TubeGeometry |
| 🌬️ 风速纹理分级 | 按照 5 档风量阈值（≥2000 / ≥1000 / ≥500 / ≥100 / <100 m³/min）加载不同材质贴图 |
| 🔄 动态风流动画 | 纹理沿管道轴向持续滚动，直观展现通风气流方向与速度感 |
| 🔵 交叉节点处理 | 巷道交叉口处自动添加球形连接节点，并以该点连接的最高风速材质渲染 |
| 🧑‍🔧 矿工漫游仿真 | 8 名矿工 Sprite 随机分配至巷道，沿巷道来回弹跳移动，附带悬浮信息标签 |
| 🏷️ 巷道信息标签 | 每段巷道中点正上方展示管道名称与实时风量数值 |
| 🖱️ 三维交互控制 | 支持鼠标拖拽旋转、滚轮缩放、轨道阻尼，由 OrbitControls 提供 |

---

## 目录结构

```
threeD/
├── README.md                    # 本文档
├── threeDPage.vue               # 页面入口，包含布局框架与路由接入点
├── components/
│   └── threeDComponent.vue      # 核心三维可视化组件（Three.js 全部逻辑）
└── images/                      # 风速等级纹理贴图
    ├── 高标风速.jpg              # 高风速纹理（≥2000 m³/min）
    ├── 高标低风速.jpg            # 中高风速纹理（≥1000 m³/min）
    ├── 52.png                   # 中等风速纹理（≥500 m³/min）
    ├── 低标高风速.jpg            # 中低风速纹理（≥100 m³/min）
    └── 低标风速.png             # 低风速纹理（<100 m³/min）
```

> **注意**：矿工图片 `miner.png` 存放于 `public/models/` 目录下，由 Three.js 的 `TextureLoader` 通过静态资源路径加载。

---

## 技术栈

| 技术 | 版本要求 | 用途 |
|------|----------|------|
| [Vue 3](https://vuejs.org/) | ^3.x | 组件框架（`<script setup>` Composition API） |
| [Three.js](https://threejs.org/) | ^0.160+ | 3D 渲染引擎 |
| `three/examples/jsm/controls/OrbitControls` | 随 Three.js | 轨道相机控制器 |
| `three/src/extras/curves/CatmullRomCurve3` | 随 Three.js | 平滑曲线路径（用于生成 TubeGeometry） |
| [Element Plus](https://element-plus.org/) | ^2.x | UI 组件（按钮、消息提示） |

---

## 数据接口

组件通过 `proxy.$api.getThreeDTunnelsData()` 从后端获取巷道数据，接口应返回一个**巷道段对象数组**，每项字段如下：

```json
[
  {
    "id": 1,
    "tube_name": "主运巷道",
    "tube_wind_speed": 1500,
    "point_left_x": 4700,
    "point_left_y": 3800,
    "point_left_z": 0,
    "point_right_x": 4900,
    "point_right_y": 3800,
    "point_right_z": -200
  }
]
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | Number | 巷道唯一标识 |
| `tube_name` | String | 巷道名称（用于标签显示） |
| `tube_wind_speed` | Number | 风量（m³/min），决定纹理等级 |
| `point_left_x/y/z` | Number | 巷道左端点三维坐标 |
| `point_right_x/y/z` | Number | 巷道右端点三维坐标 |

> 坐标系说明：世界坐标单位为矿场工程坐标（通常为米），相机初始位置约在 `(4800, 3800, 1000)`，朝向中心点 `(4790, 3840, -790)`。

---

## 核心实现

### 场景初始化

在 `onMounted` → `nextTick` 钩子中调用 `init()` 完成一次性初始化：

```
场景 (Scene)
├── Group（所有巷道对象的容器，便于整体清除重建）
├── AmbientLight（环境光，强度 2.5）
└── PointLight（绿色点光源，位于场景中心上方）

相机：PerspectiveCamera(fov=75, near=1, far=30000)
渲染器：WebGLRenderer(antialias=true, alpha=true) — 透明背景，与页面渐变背景融合
控制器：OrbitControls，启用阻尼（dampingFactor=0.05）
```

---

### 管道渲染

每段巷道由 `createTube()` 函数生成：

```
两端点 → CatmullRomCurve3 路径 → TubeGeometry(segments=100, radius=3, radialSegments=64)
                                                            ↓
                                                    Mesh + 风速材质
                                                            ↓
                                              userData.windSpeed 存储风速值（供动画使用）
```

- 使用 `CatmullRomCurve3` 而非直线，为后续多点曲线扩展预留接口。
- `TubeGeometry` 分段数较高（100段），保证曲面圆滑。

---

### 风速纹理系统

风速纹理分 **5 个等级**，加载后设置 `RepeatWrapping`，贴图重复次数与巷道实际长度成正比：

```javascript
// 重复次数 = 巷道长度 / 20（横向） × 4（纵向）
material.map.repeat.set(tubeLength / 20, 4)
```

**动画循环**（`animate()` 中每帧执行）：

```javascript
// 纹理 offset.x 随帧递减，产生气流流动视觉效果
tube.material.map.offset.x -= windSpeed * 0.000001
```

风速越高，offset 变化越大，视觉上气流速度越快。

**风速分级阈值**：

| 等级 | 阈值（m³/min） | 贴图文件 |
|------|---------------|---------|
| 高风速 | ≥ 2000 | `高标风速.jpg` |
| 中高风速 | ≥ 1000 | `高标低风速.jpg` |
| 中等风速 | ≥ 500 | `52.png` |
| 中低风速 | ≥ 100 | `低标高风速.jpg` |
| 低风速 | < 100 | `低标风速.png` |

---

### 连接点球体

为消除巷道交叉口的接缝问题，组件对所有端点坐标去重，并以 `"x,y,z"` 字符串为 Key 存入 `Map`：

- 若同一节点被多段巷道共享，取**最高风速**所对应的材质渲染球体。
- 球体半径 **3.1**（略大于管道半径 3.0），避免深度冲突闪烁（Z-fighting）。

---

### 矿工漫游动画

**配置项**（`MINER_CONFIG`）：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `count` | 8 | 矿工总数 |
| `spriteScale` | 15 | Sprite 世界坐标大小 |
| `speed_min` | 0.0006 | 最小移动速度（进度/帧） |
| `speed_max` | 0.0008 | 最大移动速度 |
| `image_path` | `/models/miner.png` | 矿工图片路径 |

**每个矿工由一个 `Group` 组成**：

```
minerGroup
├── Sprite（矿工图片，renderOrder=10）
└── labelSprite（悬浮标签，renderOrder=11，位于矿工正上方）
    └── Canvas 绘制：深色半透明背景 + 青色边框 + 发光效果 + 向下连线
```

**运动逻辑**：每帧通过 `lerpVectors(p1, p2, progress)` 插值计算位置，到达端点后 `direction *= -1` 实现来回弹跳。

---

### 巷道标签

通过 Canvas 2D API 动态绘制文字标签，转为 `CanvasTexture` 后以 `Sprite` 形式显示在管道中点正上方 20 个世界坐标单位处：

- 白色文字，无背景，`depthTest: false`（始终可见，不被遮挡）
- 标签缩放按画布宽高比等比缩放，保持字符比例

---

## 使用说明

1. **启动项目**

   ```bash
   cd smves_vite
   npm install
   npm run dev
   ```

2. **访问页面**

   在路由中配置的 `/threeD` 路径访问，页面标题为「矿井巷道三维模型」。

3. **生成模型**

   点击页面上的「**生成巷道网络**」按钮，组件将：
   - 调用后端接口获取巷道数据
   - 渲染巷道管道网络与交叉节点
   - 初始化矿工漫游动画

   > ⚠️ 模型仅可生成一次，重复点击会弹出提示并跳过。

4. **交互操作**

   | 操作 | 效果 |
   |------|------|
   | 鼠标左键拖拽 | 旋转视角 |
   | 鼠标滚轮 | 推拉缩放 |
   | 鼠标右键拖拽 | 平移视角 |

---

## 依赖说明

确保以下静态资源已就位：

```
public/
├── images/
│   ├── bg.jpg           # 页面背景图
│   ├── 高标风速.jpg
│   ├── 高标低风速.jpg
│   ├── 52.png
│   ├── 低标高风速.jpg
│   └── 低标风速.png
└── models/
    └── miner.png        # 矿工人员图标（建议使用透明背景 PNG）
```

---

*文档生成时间：2026-05-13*
