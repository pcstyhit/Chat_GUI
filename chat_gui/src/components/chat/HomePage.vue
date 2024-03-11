<template>
  <div class="container">
    <!-- 侧边栏 -->
    <DrawerCard
      ref="DrawerCardRef"
      :hideOrShowDrawerFlag="hideOrShowDrawerFlag"
      :tokens="tokens"
      :modelTokens="modelTokens"
      @hideOrShowDrawer="hideOrShowDrawer"
      @newChat="newChat"
      @updateHistory="updateHistory"
      @updateChatCard="updateChatCard"
    />

    <!-- Chat 聊天主界面 -->
    <div v-if="!promptFlag" class="right-card">
      <PromptCard @startChat="startChat" />
    </div>
    <div v-else class="right-card">
      <ChatCard />
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from "vue";
import { useStore } from "vuex";
import PromptCard from "./PromptCard.vue";
import DrawerCard from "./DrawerCard.vue";
import ChatCard from "./ChatCard.vue";
import { loadChatHistoryAPI } from "../../apis/chatAPIs.js";
import { ElMessage } from "element-plus";

export default {
  name: "HomePage",
  components: { DrawerCard, ChatCard, PromptCard },
  setup() {
    const store = useStore();
    const model = ref("");
    const inputText = ref("");
    const historyList = ref([]);
    const promptFlag = ref(false);
    const tokens = computed(() => store.state.tokens);
    const modelTokens = ref(0);
    const hideOrShowDrawerFlag = ref(true);
    const DrawerCardRef = ref();

    /** ====================== 下面定义函数 ====================== */
    onMounted(() => {});

    /** 根据子组件的信号来控制显示或者隐藏侧边栏 */
    const hideOrShowDrawer = (val) => {
      hideOrShowDrawerFlag.value = val;
    };

    /** 从子组件获得新建对话的信号，去除对话的高亮显示 */
    const newChat = () => {
      // 去除对话高亮显示
      store.commit("SET_CHATCID_STATE", "");
      promptFlag.value = false;
    };

    /** 开始新的对话，并且父组件调用子组件来初始化整个对话列表 */
    const startChat = async (val) => {
      promptFlag.value = val.rea;

      if (promptFlag.value) {
        // vue3.0父组件调用子组件里的方法
        // https://blog.csdn.net/qq_16151185/article/details/109464095
        await DrawerCardRef.value.initHistoryList();
        await updateHistory(val.chatCid);
      }
    };

    /** 通过子组件返回来的对话名称来获取对话，并更新到界面上 */
    const updateHistory = async (chatCid) => {
      // 关闭prompt卡片
      promptFlag.value = true;
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
        promptFlag.value = false;
      }
    };

    return {
      hideOrShowDrawerFlag,
      model,
      promptFlag,
      historyList,
      tokens,
      modelTokens,
      inputText,
      DrawerCardRef,
      hideOrShowDrawer,
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
  width: 100%;
  height: 100%;
}

.right-card .right-card-input {
  flex: 1;
  width: 100%;
  height: 12vh;
  padding: 10px;
}
</style>

<style scoped>
.right-card-input:deep(.el-textarea__inner) {
  resize: none !important;
}
</style>
