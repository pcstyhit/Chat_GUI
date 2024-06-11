<template>
  <div class="container">
    <!-- Settings overlay -->
    <SettingsCard @onUpdateChatNameList="onUpdateChatNameList" />

    <!-- Sidebar -->
    <SidebarCard
      ref="SidebarCardRef"
      :isShowSidebar="isShowSidebar"
      @onShowSidebar="onShowSidebar"
    />

    <!-- Chat main worksapce -->
    <div class="right-card">
      <ChatCard />
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import SettingsCard from "./SettingsCard.vue";
import SidebarCard from "./SidebarCard.vue";
import ChatCard from "./ChatCard.vue";

export default {
  name: "HomePage",
  components: { SidebarCard, ChatCard, SettingsCard },
  setup() {
    const isShowSidebar = ref(true);
    const SidebarCardRef = ref();

    /** ====================== 下面定义函数 ====================== */
    onMounted(() => {});

    /** 根据子组件的信号来控制显示或者隐藏侧边栏 */
    const onShowSidebar = (val) => {
      isShowSidebar.value = val;
    };

    /** 开始新的对话，并且父组件调用子组件来初始化整个对话列表 */
    const onUpdateChatNameList = async () => {
      // vue3.0父组件调用子组件里的方法
      // https://blog.csdn.net/qq_16151185/article/details/109464095
      await SidebarCardRef.value.handleInitHistoryList();
    };

    return {
      isShowSidebar,
      SidebarCardRef,
      onShowSidebar,
      onUpdateChatNameList,
    };
  },
};
</script>

<style scoped>
.container {
  display: flex;
  height: 100vh;
  width: 100vw;
}

.right-card {
  width: calc(100% - 232px);
  height: 100%;
}
</style>
