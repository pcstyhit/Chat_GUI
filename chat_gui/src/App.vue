<template>
  <div class="app">
    <router-view />
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style>
.app {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  font-family: "Microsoft YaHei";
  /* 允许在webview中拷贝文字 */
  user-select: text;
}
</style>
