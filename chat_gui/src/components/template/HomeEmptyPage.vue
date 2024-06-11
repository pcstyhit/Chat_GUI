<template>
  <div class="container">
    <span>{{ helloWorld }}</span>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
export default {
  setup() {
    const helloWorld = ref("");
    onMounted(() => {
      helloWorld.value = "hello empty page";
    });
    return {
      helloWorld,
    };
  },
};
</script>

<style scoped>
.container {
  width: 200px;
  height: 200px;
  background-color: aquamarine;
}
</style>
