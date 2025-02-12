<template>
  <div>
    <input type="text" v-model="inputValue" @focus="onInputFocus" @blur="onInputBlur">
    <button @click="speak">发送</button>
  </div>


</template>

<script setup lang="ts">
import * as THREE from 'three';
import { FBXLoader } from 'three/examples/jsm/loaders/FBXLoader';
import { reactive, ref } from 'vue';
import { ElMessage } from 'element-plus'
const inputValue = ref('');
let inputFlag = false;
import axios from '@/utils/axios';
let sound;
const speak = () => {
  const dataToSend = {
    inputValue: inputValue.value
  };
  axios({
    method: 'post',
    url: '/audio/speak',
    data: dataToSend,
    responseType: 'blob' // 设置响应类型为 blob
  })
    .then(response => {
      // 创建一个 Blob 对象并通过 URL.createObjectURL() 方法创建一个临时 URL
      const audioUrl = window.URL.createObjectURL(new Blob([response.data]));

      // 创建一个音频对象和音频加载器
      const listener = new THREE.AudioListener();
      camera.add(listener);
      sound = new THREE.PositionalAudio(listener);
      const audioLoader = new THREE.AudioLoader();

      // 加载音频文件
      audioLoader.load(audioUrl, function (buffer) {
        sound.setBuffer(buffer);
        sound.setVolume(1);
        sound.setRefDistance(1); // 设置音频的参考距离
        sound.play();

        // 获取PannerNode并设置位置
        const panner = sound.panner;
        panner.setPosition(model.position.x, model.position.y, model.position.z); // 设置初始位置
      });
      inputValue.value = '';
      ElMessage.success('发送成功')
    })
    .catch(error => {
      ElMessage.error('Error downloading audio:', error);
    });
}


//场景
const scene = new THREE.Scene();

//相机
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 3, 5);

//渲染器
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.shadowMap.enabled = true;
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setClearColor(0xffffff);
document.body.appendChild(renderer.domElement);

let keyCodeW = false;
let keyCodeS = false;
let keyCodeA = false;
let keyCodeD = false;
let keyCodeK = false;
let model;
let mixers = []; // 将 mixer 变量改为数组形式
let idelAction;
let moveAction;
const duration = 0.5; // 过渡时间（秒）

const loader = new FBXLoader();

// 加载停留动作模型
loader.load('/models/stand.fbx', function (standObject) {
  // 设置停留动作模型
  model = standObject;
  model.scale.set(0.02, 0.02, 0.02);
  model.castShadow = true;
  scene.add(model);

  // 创建停留动作的 AnimationMixer
  mixers[0] = new THREE.AnimationMixer(model);
  idelAction = mixers[0].clipAction(model.animations[0]);
  idelAction.timeScale = 1;
  idelAction.loop = THREE.LoopRepeat;

  // 加载走路动作模型
  loader.load('/models/walking.fbx', function (walkingObject) {
    // 设置走路动作模型
    const walkingModel = walkingObject;
    walkingModel.scale.set(0.02, 0.02, 0.02);
    // 获取停留动作模型的动画数组
    const animations = model.animations;

    // 添加走路动作的动画剪辑到停留动作模型的动画数组中
    animations.push(...walkingModel.animations);

    // 将复制的走路动作添加到停留动作模型
    mixers[1] = new THREE.AnimationMixer(model);
    moveAction = mixers[1].clipAction(model.animations[2]);
    moveAction.timeScale = 1;
    moveAction.loop = THREE.LoopRepeat;

    // 开始播放停留动作
    idelAction.play();

  });
});




const ambientLight = new THREE.AmbientLight(0x404040, 1);
scene.add(ambientLight);

let dLight = null;
{
  const light = new THREE.PointLight(0xffffff, 1);
  light.position.set(50, 50, 50);
  scene.add(light);
  dLight = light
}


// 更新声音源的位置
function updateSoundPosition(position) {
  if (sound) {
    const panner = sound.panner;
    panner.setPosition(position.x, position.y, position.z);
  }

}


//地面
const planeGeometry = new THREE.PlaneGeometry(100, 100);
const planeMaterial = new THREE.MeshStandardMaterial({ color: 0xaaaaaa });
const plane = new THREE.Mesh(planeGeometry, planeMaterial);
plane.rotation.x = - Math.PI / 2;
plane.name = "plane";

plane.receiveShadow = true;
scene.add(plane);

const gridHelper = new THREE.GridHelper(100, 100);
scene.add(gridHelper);

var clock = new THREE.Clock();

function animate() {
  requestAnimationFrame(animate);
  const delta = clock.getDelta();
  mixers.forEach(mixer => mixer.update(delta)); // 更新所有的 AnimationMixer
  if (model) {
    updateSoundPosition(model.position);
    onCodeMove(model);

  }
  renderer.render(scene, camera);
}
// const idleToMove = () => {
//   // 结束第一个动画并淡出
//   action1.fadeOut(duration);

//   // 开始第二个动画并淡入
//   action2.fadeIn(duration);

//   // 在第一个动画结束时停止
//   action1.play().reset().fadeOut(duration);

//   // 在第二个动画开始时播放
//   action2.play().reset().fadeIn(duration);

// }
animate();
document.addEventListener(
  'keydown',
  (e) => {
    if (!inputFlag) {
      var ev = e || window.event;
      switch (ev.keyCode) {
        case 87: // W
          keyCodeW = true;
          if (idelAction) {
            idelAction.stop();
          }
          if (moveAction) {
            moveAction.play();
          }
          break;
        case 83: // S
          keyCodeS = true;
          if (idelAction) {
            idelAction.stop();
          }
          if (moveAction) {
            moveAction.play();
          }
          break;
        case 65: // A
          keyCodeA = true;
          if (idelAction) {
            idelAction.stop();
          }
          if (moveAction) {
            moveAction.play();
          }
          break;
        case 68: // D
          keyCodeD = true;
          if (idelAction) {
            idelAction.stop();
          }
          if (moveAction) {
            moveAction.play();
          }
          break;
        case 75: // K
          keyCodeK = true;
          if (idelAction) {
            idelAction.stop();
          }
          if (moveAction) {
            moveAction.play();
          }
          break;
        default:
          break;
      }
      onCodeMove(model);
    }

  },
  false
);

document.addEventListener(
  'keyup',
  (e) => {
    if (!inputFlag) {
      var ev = e || window.event;
      switch (ev.keyCode) {
        case 87: // W
          keyCodeW = false;
          break;
        case 83: // S
          keyCodeS = false;
          break;
        case 65: // A
          keyCodeA = false;
          break;
        case 68: // D
          keyCodeD = false;
          break;
        default:
          break;
      }
      // 如果没有任何按键按下，则播放停留动作，否则继续播放移动动作
      if (!keyCodeW && !keyCodeS && !keyCodeA && !keyCodeD) {
        if (idelAction) {
          idelAction.play();
        }
        if (moveAction) {
          moveAction.stop();
        }
      } else {
        if (idelAction) {
          idelAction.stop();
        }
        if (moveAction) {
          moveAction.play();
        }
      }
      onCodeMove(model);
    }

  },
  false
);

let mesgSpeed = 0.1;
let cameraSpeed = 0.05;
function onCodeMove(mesh) {
  if (keyCodeW) {
    mesh.position.z -= mesgSpeed;
    camera.position.z -= cameraSpeed;
    dLight.position.z = 0.2;
    mesh.rotation.y = Math.PI;
  }
  if (keyCodeA) {
    mesh.position.x -= mesgSpeed;
    camera.position.x -= cameraSpeed;
    dLight.position.x -= 0.2;
    mesh.rotation.y = Math.PI * 1.5;
  }
  if (keyCodeS) {
    mesh.position.z += mesgSpeed;
    camera.position.z += cameraSpeed;
    dLight.position.z += 0.2;
    mesh.rotation.y = 0;
  }
  if (keyCodeD) {
    mesh.position.x += mesgSpeed;
    camera.position.x += cameraSpeed;
    dLight.position.x += 0.2;
    mesh.rotation.y = Math.PI / 2;
  }

  if (keyCodeW && keyCodeD) {
    mesh.rotation.y = Math.PI * 0.75;
  }
  if (keyCodeW && keyCodeA) {
    mesh.rotation.y = Math.PI * 1.25;
  }
  if (keyCodeA && keyCodeS) {
    mesh.rotation.y = Math.PI * 1.75;
  }
  if (keyCodeS && keyCodeD) {
    mesh.rotation.y = Math.PI * 0.25;
  }


}

const onInputFocus = () => {
  // 如果存在模型，则暂停模型移动
  inputFlag = true;
};

// 监听输入框失去焦点事件
const onInputBlur = () => {
  // 如果存在模型，则恢复模型移动
  inputFlag = false;
};

</script>



<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

input {


  background-color: rgba(255, 255, 255, 0.5);
  /* 使用 rgba 设置背景色，并指定透明度为 0.5 */
  padding: 10px;
  border-radius: 5px;
  width: 300px;
  /* 输入框宽度 */
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  outline: none;
}

div {
  position: fixed;
  left: 50%;
  bottom: 8%;
  /* 距离屏幕底部的距离 */
  transform: translateX(-50%);
}

button {
  padding: 9px 26px;
  border-radius: 5px;
  border: none;
  background-color: rgba(0, 128, 255, 0.5);
  /* 淡蓝色半透明 */
  color: white;
  /* 文字颜色 */
  font-size: 16px;
  /* 字体大小 */
  cursor: pointer;
  /* 鼠标指针样式 */
  transition: background-color 0.3s ease;
  margin-left: 5px;
  vertical-align: middle;
  /* 过渡效果 */
}

button:hover {
  background-color: rgba(0, 128, 255, 0.8);
  /* 淡蓝色半透明，悬停时更加明亮 */
}
</style>
