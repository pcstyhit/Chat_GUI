<template>
  <div class="app">
    <UI />
  </div>
</template>

<script>
import UI from "./components/chat/HomePage.vue";

export default {
  name: "App",
  components: {
    UI,
  },
};
</script>

<style>
.app {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  width: 100%;
}
</style>
