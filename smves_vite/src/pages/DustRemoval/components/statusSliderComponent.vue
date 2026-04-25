<template>
  <!-- 主包裹容器 -->
  <div class="status-slider-wrapper">
    <!-- 状态标签 -->
    <span class="status-label">风机状态</span>

    <!-- 包含滑块和下方状态文本的容器 -->
    <div class="slider-section">
      <div class="slider-container">
        <input
          ref="sliderInputRef"
          type="range"
          min="0"
          max="100"
          step="25"
          v-model.number="sliderValue"
          @input="handleSliderInput"
          class="custom-slider"
        />
      </div>
      <!-- 状态标签容器 -->
      <div class="status-labels-container">
        <span
          v-for="(status, index) in statuses"
          :key="status"
          :class="{ active: currentStatusIndex === index }"
          @click="setStatus(status)"
          class="status-label-item"
        >
          {{ status }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup name="statusSliderComponent">
import { ref, computed, onMounted, watch } from 'vue' // Import onMounted and watch

const sliderValue = ref(50)
const statuses = ['关机', '启动中', '运行中', '暂停', '停止']
const sliderInputRef = ref(null) // Ref for the input element

const currentStatusIndex = computed(() => {
  return Math.round(sliderValue.value / 25)
})

// Function to update the slider's background style
const updateSliderProgressStyle = (value) => {
  if (sliderInputRef.value) {
    const element = sliderInputRef.value
    const min = Number(element.min) || 0
    const max = Number(element.max) || 100
    const percentage = ((value - min) / (max - min)) * 100
    // Set the CSS variable --slider-progress on the input element
    element.style.setProperty('--slider-progress', `${percentage}%`)
  }
}

// Handler for the slider's input event
const handleSliderInput = (event) => {
  // v-model already updated sliderValue
  const currentValue = event.target.valueAsNumber // Use valueAsNumber for precision
  updateSliderProgressStyle(currentValue) // Update style based on the new value
  console.log(`滑动到值: ${currentValue}, 状态: ${statuses[currentStatusIndex.value]}`)
}

// Handler for clicking status labels
const setStatus = (status) => {
  const index = statuses.indexOf(status)
  if (index !== -1) {
    const newValue = index * 25
    sliderValue.value = newValue // Update the model value
    // Style will be updated via the watch below
    console.log(`点击设置状态: ${status}, 值: ${newValue}`)
  }
}

// Watch for changes in sliderValue (e.g., from setStatus) and update style
watch(sliderValue, (newValue) => {
  updateSliderProgressStyle(newValue)
})

// Set initial style when the component mounts
onMounted(() => {
  updateSliderProgressStyle(sliderValue.value)
})
</script>

<style scoped>
.status-slider-wrapper {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 1px; /* Reduced padding */
  font-family:
    -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Fira Sans',
    'Droid Sans', 'Helvetica Neue', sans-serif;
  width: 100%;
  max-width: 450px;
  margin: 0 auto;
}

.status-label {
  font-size: 20px;
  color: hsl(0, 16%, 93%);
  font-weight: 500;
  margin-bottom: 15px;
}

.slider-section {
  width: 100%;
  display: flex;
  flex-direction: column;
}

.slider-container {
  position: relative;
  width: 100%;
}

/* --- Custom Slider Styles --- */
.custom-slider {
  -webkit-appearance: none;
  appearance: none;
  width: 100%;
  height: 8px;
  /* Default background is now the "empty" part */
  background: #e0e0e0;
  border-radius: 5px;
  outline: none;
  cursor: pointer;
  display: block;
  /* Define the CSS variable for progress */
  --slider-progress: 50%; /* Default value (can be anything) */
}

/* Apply the gradient background using the CSS variable */
.custom-slider {
  /* Blue color (#007aff) up to the variable percentage, then gray (#e0e0e0) */
  background: linear-gradient(
    to right,
    #007aff var(--slider-progress),
    #e0e0e0 var(--slider-progress)
  );
}

/* --- Thumb Styles (Keep as before) --- */
.custom-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 22px;
  height: 22px;
  background: #007aff; /* Thumb color */
  border-radius: 50%;
  border: 2px solid #fff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  margin-top: -7px; /* Adjust vertical alignment */
  position: relative; /* Needed for z-index if thumb overlaps complex tracks */
  z-index: 2; /* Ensure thumb is above the track gradient */
}

.custom-slider::-moz-range-thumb {
  width: 18px; /* Adjusted for Firefox consistency */
  height: 18px;
  background: #007aff;
  border-radius: 50%;
  border: 2px solid #fff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  border: none;
  position: relative; /* Needed for z-index */
  z-index: 2; /* Ensure thumb is above the track gradient */
}

/* Firefox specific progress (optional but good practice) */
/* We hide the default Firefox progress bar because we use the gradient method */
.custom-slider::-moz-range-progress {
  background-color: transparent; /* Hide default progress */
}
/* We already style the main track with gradient, so ::-moz-range-track can be minimal */
.custom-slider::-moz-range-track {
  height: 8px;
  background: transparent; /* Track itself is handled by the input's gradient */
  border-radius: 5px;
}

/* --- Status Labels Container (Keep as before) --- */
.status-labels-container {
  display: flex;
  justify-content: space-between;
  width: 100%;
  padding: 0 5px;
  box-sizing: border-box;
  margin-top: 8px;
}

.status-label-item {
  font-size: 17px;
  color: #888;
  text-align: center;
  cursor: pointer;
  transition:
    color 0.3s ease,
    font-weight 0.3s ease;
  position: relative;
}

.status-labels-container .status-label-item:first-child {
  text-align: left;
}
.status-labels-container .status-label-item:last-child {
  text-align: right;
}

.status-labels-container .status-label-item.active {
  color: #007aff; /* Active label color */
  font-weight: 600;
}
</style>
