<template>
  <div class="container">
    <span>{{ flag }}</span>
    <el-button plain @click="open">Click to open the Message Box</el-button>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { showMessageBox, showMessage } from "../../helper/customMessage.js";

const flag = ref(null);
const confirmCallback = () => {
  showMessage("success", "OK了");
};

const cancelCallback = () => {
  showMessage("error", "不是很OK啊");
};
const open = async () => {
  flag.value = await showMessageBox(
    "测试自定义的ElMessageBox的样式",
    confirmCallback,
    cancelCallback
  );
};
</script>

<style lang="scss" scoped>
.container {
  width: 400px;
  height: 400px;
  background-color: rgb(176, 252, 227);
}
</style>
