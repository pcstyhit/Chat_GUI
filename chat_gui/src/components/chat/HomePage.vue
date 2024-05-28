<template>
  <div class="container">
    <!-- Settings overlay -->
    <SettingsCard @startChat="startChat" />

    <!-- Sidebar -->
    <SidebarCard
      ref="SidebarCardRef"
      :isShowSidebar="isShowSidebar"
      :tokens="tokens"
      :modelTokens="modelTokens"
      @onShowSidebar="onShowSidebar"
      @newChat="newChat"
      @updateHistory="updateHistory"
      @updateChatCard="updateChatCard"
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
import SettingsCard from "./SettingsCard.vue";
import SidebarCard from "./SidebarCard.vue";
import ChatCard from "./ChatCard.vue";
import { loadChatHistoryAPI } from "../../apis/chatAPIs.js";
import { ElMessage } from "element-plus";

export default {
  name: "HomePage",
  components: { SidebarCard, ChatCard, SettingsCard },
  setup() {
    const store = useStore();
    const model = ref("");
    const inputText = ref("");
    const historyList = ref([]);
    const tokens = computed(() => store.state.chat.tokens);
    const modelTokens = ref(0);
    const isShowSidebar = ref(true);
    const SidebarCardRef = ref();

    /** ====================== 下面定义函数 ====================== */
    onMounted(() => {});

    /** 根据子组件的信号来控制显示或者隐藏侧边栏 */
    const onShowSidebar = (val) => {
      isShowSidebar.value = val;
    };

    /** 从子组件获得新建对话的信号，去除对话的高亮显示 */
    const newChat = () => {
      store.commit("SET_EDIT_CHAT_SETTINGS_STATE", true);
      // 去除对话高亮显示
      store.commit("SET_CHATCID_STATE", "");
      store.commit("SET_CHATHISTORY_STATE", []);
    };

    /** 开始新的对话，并且父组件调用子组件来初始化整个对话列表 */
    const startChat = async (val) => {
      // vue3.0父组件调用子组件里的方法
      // https://blog.csdn.net/qq_16151185/article/details/109464095
      await SidebarCardRef.value.initHistoryList();
      await updateHistory(val.chatCid);
    };

    /** 通过子组件返回来的对话名称来获取对话，并更新到界面上 */
    const updateHistory = async (chatCid) => {
      // 高亮显示对话
      store.commit("SET_CHATCID_STATE", chatCid);
      // 更新对话
      var rea = await loadChatHistoryAPI(chatCid);

      if (rea.flag == false) {
        ElMessage.error(rea.log);
        return;
      }

      store.commit("SET_CHATHISTORY_STATE", []);
      rea.history.forEach((element) => {
        if (element.role == "user") {
          store.commit("PUSH_CHATHISTORY_STATE", {
            chatIid: element.chatIid,
            id: "user",
            text: element.content,
          });
        }
        if (element.role == "assistant") {
          store.commit("PUSH_CHATHISTORY_STATE", {
            chatIid: element.chatIid,
            id: "gpt",
            text: element.content,
          });
        }
      });
      store.commit("SET_TOKENS_STATE", rea.tokens);
      modelTokens.value = rea.modelTokens;
    };

    /** 子组件删除对话后需要判断是否需要更新当前的对话的卡片 */
    const updateChatCard = async (val) => {
      if (val.flag) {
        tokens.value = 0;
        modelTokens.value = 0;
        // 显示新建chat卡片
        store.commit("SET_EDIT_CHAT_SETTINGS_STATE", true);
        // 清空背景记录
        store.commit("SET_CHATHISTORY_STATE", []);
      }
    };

    return {
      isShowSidebar,
      model,
      historyList,
      tokens,
      modelTokens,
      inputText,
      SidebarCardRef,
      onShowSidebar,
      newChat,
      startChat,
      updateChatCard,
      updateHistory,
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
