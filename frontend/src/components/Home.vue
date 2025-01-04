<template>
  <div class="container">
    <h1 id="head">welcome to jarvis study helper</h1>
    <p id="description">-- A math\English problem solver</p>
    <button @click="ClickStart" id="start">开始</button>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";

const router=useRouter();
const ClickStart = () => {
  router.push("/chat");
};
</script>

<style scoped>
.container {
  width: 100%;
  height: 100vh;
  background-image: url("@/assets/xxbg.jpg");
  background-size: 45% 100%;
  background-position: right;
  background-repeat: no-repeat;
  position: fixed;
  top: 0;
  left: 0;
}

#head {
  background: linear-gradient(to right, purple, gray);
  -webkit-background-clip: text;
  color: transparent;
  position: absolute;
  top: 35%;
  left: 25%;
  transform: translateX(-50%);
}
#description {
  color: rgb(190, 190, 243);
  font-size: 1.5em;
  position: absolute;
  top: 45%;
  left: 25%;
}
#start {
  position: absolute;
  top: 55%;
  left: 10%;
  transform: translateX(-50%);
  width: 200px;
  height: 40px;
  background: white;
  border-style: solid;
  border-width: 2px;
  border-color: black;
}
</style> 