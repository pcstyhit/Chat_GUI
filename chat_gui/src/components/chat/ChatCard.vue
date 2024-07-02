<template>
  <div class="chat-container">
    <!-- header -->
    <div class="header">
      <!-- settings -->
      <el-tooltip
        content="Edit Current Chat"
        placement="bottom"
        :show-after="500"
      >
        <el-button class="settings" @click="onShowSettings">
          <el-text class="settings-text" :tag="'b'">
            {{ chatParams.modelName }}
          </el-text>
          <div class="settings-icon" v-html="SVGS.settingsIcon"></div>
        </el-button>
      </el-tooltip>
      <div class="user-config">
        <!-- auto-to-bottom switch -->
        <div class="switch">
          <el-text class="c-label"> Auto To Bottom: </el-text>
          <el-switch
            class="c-switch"
            v-model="isAutoToBottom"
            :disabled="isChatting != 0"
          />
        </div>
        <!-- user info -->

        <el-tooltip
          content="User management"
          placement="bottom"
          :show-after="500"
        >
          <el-button class="user-man">
            <img
              src="../../../public/avatar.png"
              size="32"
              height="32"
              width="32"
            />
          </el-button>
        </el-tooltip>
      </div>
    </div>
    <!-- Message Output -->
    <div class="roles-card" v-if="chatCid == ''">
      <RolesCard />
    </div>
    <el-scrollbar v-else class="scroll-window" ref="scrollbarRef">
      <div ref="innerRef">
        <div v-for="item in chatHistory" :key="item.chatIid">
          <!-- user question -->
          <div v-if="item.role == 'user'" class="user">
            <div class="user-content">
              <!-- content detail -->
              <div class="text" v-html="item.text"></div>
              <!-- content options -->
              <div class="options" v-show="isChatting == 0">
                <!-- re-request -->
                <el-tooltip
                  content="Re-request; This will refresh the chats below"
                  placement="bottom"
                  :show-after="500"
                >
                  <el-button
                    class="options-button"
                    @click="onReGenerateContent(item)"
                  >
                    <div class="options-icon" v-html="SVGS.reRequestIcon"></div>
                  </el-button>
                </el-tooltip>
                <!-- edit request -->
                <el-tooltip
                  content="Edit this request"
                  placement="bottom"
                  :show-after="500"
                >
                  <el-button
                    class="options-button"
                    @click="onEditChatItem(item)"
                  >
                    <div
                      class="options-icon"
                      v-html="SVGS.eidtChatItemIcon"
                    ></div>
                  </el-button>
                </el-tooltip>
                <!-- delete request -->
                <el-tooltip
                  content="Delete this request"
                  placement="bottom"
                  :show-after="500"
                >
                  <el-button
                    class="options-button"
                    @click="onDeleteChatItem(item.chatIid)"
                  >
                    <div
                      class="options-icon"
                      v-html="SVGS.deleteChatItemIcon"
                    ></div>
                  </el-button>
                </el-tooltip>
              </div>
            </div>
          </div>
          <!-- gtp answer -->
          <div v-else class="assistant">
            <div class="assistant-icon" v-html="SVGS.gptIcon"></div>
            <div class="assistant-content">
              <!-- detail content -->
              <div class="text" v-html="item.text"></div>
              <div class="options" v-show="isChatting == 0">
                <!-- re-response -->
                <el-tooltip
                  content="Re-response"
                  placement="bottom"
                  :show-after="500"
                >
                  <el-button
                    class="options-button"
                    @click="onReGenerateContent(item)"
                  >
                    <div
                      class="options-icon"
                      v-html="SVGS.reResponseIcon"
                    ></div>
                  </el-button>
                </el-tooltip>
                <!-- edit response -->
                <el-tooltip
                  content="Edit this response"
                  placement="bottom"
                  :show-after="500"
                >
                  <el-button
                    class="options-button"
                    @click="onEditChatItem(item, index)"
                  >
                    <div
                      class="options-icon"
                      v-html="SVGS.eidtChatItemIcon"
                    ></div>
                  </el-button>
                </el-tooltip>
                <!-- delete response -->
                <el-tooltip
                  content="Delete this response"
                  placement="bottom"
                  :show-after="500"
                >
                  <el-button
                    class="options-button"
                    @click="onDeleteChatItem(item.chatIid, index)"
                  >
                    <div
                      class="options-icon"
                      v-html="SVGS.deleteChatItemIcon"
                    ></div>
                  </el-button>
                </el-tooltip>
                <!-- play audio response -->
                <el-tooltip
                  content="Read aloud"
                  placement="bottom"
                  :show-after="500"
                >
                  <el-button class="options-button" @click="onReadAloud(item)">
                    <div
                      v-if="!isReadAlouding"
                      class="options-icon"
                      v-html="SVGS.chatAudioStartIcon"
                    ></div>
                    <div
                      v-if="
                        isReadAlouding && isReadAloudChatIid == item.chatIid
                      "
                      class="options-icon"
                      v-html="SVGS.chatAudioStopIcon"
                    ></div>
                  </el-button>
                </el-tooltip>
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-scrollbar>
    <!-- Message Input -->
    <div class="input-card">
      <el-input
        class="custom-textarea"
        type="textarea"
        v-model="userQuestionText"
        placeholder="Please input your question ..."
        @keydown.enter="onEnterKeydown"
        :autosize="{ minRows: 1, maxRows: 8 }"
      ></el-input>
      <!-- send and pause button -->
      <el-button
        class="send-button"
        :disabled="userQuestionText == '' && isChatting != 0"
        @click="onSendContent"
      >
        <!-- send chat button -->
        <div
          v-if="isChatting == 0"
          :class="['svg-icon', { 'svg-icon-disable': userQuestionText == '' }]"
          v-html="SVGS.sendIcon"
        ></div>
        <!-- pause chat button -->
        <div v-else class="svg-icon" v-html="SVGS.pauseIcon"></div>
      </el-button>
    </div>
    <!-- footer -->
    <div class="footer">
      <el-text class="tips"> time: {{ requestTime }}ms </el-text>
      <el-text class="tips">
        {{ tokens }}/{{ chatParams.maxTokens }} tokens to be sent
      </el-text>
    </div>
  </div>
  <!-- item editor ovelay -->
  <ItemEditor
    v-model:isShowItemEditor="isShowItemEditor"
    v-model:editChatItemObj="editChatItemObj"
  />
  <audio id="audioElement"></audio>
</template>

<script>
import { ref, nextTick, computed, watch } from "vue";
import { ElMessage } from "element-plus";
import { useStore } from "vuex";
import * as SVGS from "../../assets/styles/chat/svgs.js";
import {
  setUserMsgAPI,
  deleteChatItemAPI,
  createEventSourceAPI,
  reGenerateContentAPI,
  addNewChatAPI,
  setChatParamsAPI,
  chatAudioAPI,
} from "../../apis/chat.js";
import { URL } from "../../apis/common.js";
import { textToHtml } from "../../helper/formatHelper.js";
import { ElMessageBox } from "element-plus";
import ItemEditor from "./ItemEditor.vue";
import RolesCard from "./RolesCard.vue";

export default {
  components: { ItemEditor, RolesCard },
  setup() {
    const store = useStore();
    const userQuestionText = ref("");
    const scrollbarRef = ref();
    const innerRef = ref(); // 控制自动刷新到最底部

    const chatHistory = computed(() => store.state.chat.chatHistory);
    const chatCid = computed(() => store.state.chat.chatCid);
    const chatParams = computed(() => store.state.chat.chatParams);
    const isChatting = computed(() => store.state.chat.isChatting);
    const tokens = computed(() => store.state.chat.tokens);
    const requestTime = computed(() => store.state.chat.requestTime);

    const isAutoToBottom = ref(false);
    const isShowItemEditor = ref(false);
    const editChatItemObj = ref({});

    const isReadAlouding = ref(false);
    const isReadAloudChatIid = ref("");

    watch(
      () => isChatting.value,
      async () => {
        if (isAutoToBottom.value) {
          await setScrollToBottom();
        }
      }
    );

    /** 输入框的按键组合键 */
    const onEnterKeydown = async (event) => {
      // Enter 和 Shift 键表示换行的操作
      if (event.key === "Enter" && !event.shiftKey) {
        // 阻止默认行为（换行）并发送内容
        event.preventDefault();
        await onSendContent();
      }
    };

    /** 向服务器发送数据 */
    const onSendContent = async () => {
      // 及时清空对话框
      var msg = userQuestionText.value;
      userQuestionText.value = "";

      var sendChatCid = chatCid.value !== "" ? chatCid.value : "";
      if (isChatting.value != 0) {
        ElMessage.warning("请等待服务器回答完成！");
        return;
      }

      if (chatCid.value == "") {
        // 没有新建对话需要新建对话
        ElMessage.info("默认参数开始对话, 初始化数据库 ... ...");
        var rea = await addNewChatAPI(chatParams.value.chatName);
        if (!rea.flag) return false;
        // 得到ChatCid
        sendChatCid = rea.chatCid;
        rea = await setChatParamsAPI(sendChatCid, chatParams.value);
        if (!rea.flag) return false;
        // 🎉 有效的ChatCid, 新建对话成功！ 存入store
        store.commit("SET_NEWCHATCID_STATE", sendChatCid);
        store.commit("PUSH_CHATLIST_STATE", {
          chatCid: sendChatCid,
          chatName: chatParams.value.chatName,
        });
      }

      // 发送消息
      rea = await setUserMsgAPI(msg);
      if (rea.flag) {
        // 更新对话
        store.commit("PUSH_CHATHISTORY_STATE", {
          chatIid: rea.chatIid,
          role: "user",
          content: msg,
          text: textToHtml(msg),
        });

        // 更新tokens
        store.commit("SET_TOKENS_STATE", rea.tokens);

        // 控制再也不能发送对话, 晚于store.chathistory更新 这样可以保证autoToBottom
        store.commit("SET_ISCHATTING_STATE", 1);
        store.commit("SET_IS_UPDATE_REQUEST_TIME", false);
        // 从服务端获得输出
        await createEventSourceAPI(sendChatCid);
      } else {
        ElMessage.error("GPT API tokens error");
      }
    };

    /**
     * 默认显示最新的内容，拖拉条滚动到最底部
     * Element-plus 如何让滚动条永远在最底部（支持在线演示）
     * https://blog.csdn.net/qq_42203909/article/details/133816286
     */
    const setScrollToBottom = async () => {
      await nextTick();
      const max = innerRef.value.clientHeight;
      scrollbarRef.value.setScrollTop(max);
    };

    /** 重新发送对话请求 */
    const onReGenerateContent = async (item) => {
      if (chatParams.value.isGhostChat) {
        ElMessage.warning("幽灵对话不支持修改内容 🤔");
        return;
      }
      var rea = await reGenerateContentAPI(item.role, item.chatIid);
      if (rea.flag) {
        // 重新更新tokens
        store.commit("SET_TOKENS_STATE", rea.tokens);
        // 对store的内容进行修改
        store.commit("SET_REGENERATE_CHATHISTORY", item);
        // 重置时间戳的信息
        store.commit("SET_IS_UPDATE_REQUEST_TIME", false);
        // 从服务端获得输出
        await createEventSourceAPI(chatCid.value);
      } else {
        ElMessage.error("🤔 无效操作！");
      }
    };

    /** 编辑某个聊天对话，修改prompt */
    const onEditChatItem = (item) => {
      if (chatParams.value.isGhostChat) {
        ElMessage.warning("幽灵对话不支持修改内容 🤔");
        return;
      }
      isShowItemEditor.value = true;
      // 对el-input输入框内容/gpt返回给到的内容 这里先不做处理了，留给子组件做
      // ⭐ 必须采用深拷贝方法
      editChatItemObj.value = {
        role: item.role,
        content: item.content,
        text: item.text,
        chatIid: item.chatIid,
      };
    };

    /** 删除某个chat */
    const onDeleteChatItem = async (chatIid) => {
      if (chatParams.value.isGhostChat) {
        ElMessage.warning("幽灵对话不支持修改内容 🤔");
        return;
      }
      var flag = false;
      await ElMessageBox.confirm(
        "删除这个对话的内容吗(删除无法恢复)?",
        "Warning",
        {
          confirmButtonText: "Yes",
          cancelButtonText: "Cancel",
          type: "warning",
        }
      )
        .then(() => {
          flag = true;
        })
        .catch(() => {
          flag = false;
        });
      if (flag) {
        var rea = await deleteChatItemAPI(chatIid);
        if (rea.flag == true) {
          ElMessage.success("删除成功");
          store.commit("DELETE_CHATHISTORY_ITEM", chatIid);
        } else {
          ElMessage.error("删除失败");
        }
      }
    };

    /** 显示对话的编辑弹窗 chat-settings-overlay */
    const onShowSettings = () => {
      store.commit("SET_EDIT_CHAT_SETTINGS_STATE", 1);
    };

    /** 点击按钮 开始播放音频 */
    const onReadAloud = async (item) => {
      const audioElement = document.getElementById("audioElement");

      if (isReadAlouding.value) {
        // 结束播放
        audioElement.pause();
        audioElement.src = "";
        isReadAloudChatIid.value = "";
        isReadAlouding.value = false;
        return;
      }

      ElMessage.info("开始生成音频文件... ...");
      isReadAloudChatIid.value = item.chatIid;
      var rea = await chatAudioAPI(item.content);
      if (!rea.flag) {
        ElMessage.error("尝试获取音频失败！ 😥");
        return;
      }
      isReadAlouding.value = true;

      ElMessage.info("开始播放音频... ...");
      audioElement.src = `${URL}/chat/audio/${rea.data}`;

      // 播放结束主动关闭
      audioElement.addEventListener("ended", () => {
        isReadAlouding.value = false;
        audioElement.src = "";
        isReadAloudChatIid.value = "";
      });

      audioElement.play();
    };

    return {
      SVGS,
      chatCid,
      isChatting,
      userQuestionText,
      scrollbarRef,
      innerRef,
      chatHistory,
      chatParams,
      tokens,
      requestTime,
      isShowItemEditor,
      editChatItemObj,
      isAutoToBottom,
      onSendContent,
      onEnterKeydown,
      onEditChatItem,
      onDeleteChatItem,
      onShowSettings,
      onReGenerateContent,
      isReadAlouding,
      isReadAloudChatIid,
      onReadAloud,
    };
  },
};
</script>

<style lang="scss" scoped>
.custom-textarea :deep(.el-textarea__inner) {
  border: none !important; /* Remove border */
  outline: none; /* Remove focus outline */
  box-shadow: none; /* Remove any box shadow */
  background-color: #f4f4f4;
  resize: none !important;
}

.scroll-window :deep(.el-button) {
  margin-left: 0px !important;
  padding: 0px !important;
}
</style>
