<template>
  <div class="container">
    <!-- Settings overlay -->
    <SettingsCard />

    <!-- Sidebar -->
    <SidebarCard
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
import { ref, onMounted, computed } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import SettingsCard from "./SettingsCard.vue";
import SidebarCard from "./SidebarCard.vue";
import ChatCard from "./ChatCard.vue";
import { getAllHistoryAPI } from "../../apis/chat.js";

export default {
  name: "HomePage",
  components: { SidebarCard, ChatCard, SettingsCard },
  setup() {
    const isShowSidebar = ref(true);
    const store = useStore();
    const router = useRouter();
    const isLogged = computed(() => store.state.user.isLogged);

    /** ====================== 下面定义函数 ====================== */
    onMounted(async () => {
      if (!isLogged.value) {
        ElMessage.error("请先登录！");
        // 回到登录界面
        router.push({
          path: "/",
        });
      }
      // 获取服务器的历史对话记录
      var rea = await getAllHistoryAPI();
      store.commit("SET_CHATLIST_STATE", rea.data);
      store.commit("SET_CHATCID_STATE", "");
    });

    /** 根据子组件的信号来控制显示或者隐藏侧边栏 */
    const onShowSidebar = (val) => {
      isShowSidebar.value = val;
    };

    return {
      isShowSidebar,
      onShowSidebar,
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
