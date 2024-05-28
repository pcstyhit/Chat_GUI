<template>
  <div class="chat-container">
    <!-- header -->
    <div class="header">
      <!-- settings -->
      <el-tooltip content="Edit Current Chat" placement="bottom">
        <el-button class="settings" @click="onShowSettings">
          <el-text class="settings-text" :tag="'b'"> GPT4o </el-text>
          <div class="settings-icon" v-html="SVGS.settingsIcon"></div>
        </el-button>
      </el-tooltip>
      <div class="user-config">
        <!-- stream switch -->
        <div class="switch">
          <el-text class="c-label"> Stream Response: </el-text>
          <el-switch class="c-switch" v-model="isStreamResponse" />
        </div>
        <!-- auto-to-bottom switch -->
        <div class="switch">
          <el-text class="c-label"> Auto To Bottom: </el-text>
          <el-switch class="c-switch" v-model="isAutoToBottom" />
        </div>
        <!-- user info -->

        <el-tooltip content="User management" placement="bottom">
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
    <el-scrollbar class="scroll-window" ref="scrollbarRef">
      <div ref="innerRef">
        <div v-for="item in chatHistory" :key="item.id">
          <!-- user question -->
          <div v-if="item.id == 'user'" class="user">
            <div class="user-content">
              <!-- content detail -->
              <div class="text" v-html="item.text"></div>
              <!-- content options -->
              <div class="options">
                <!-- re-request -->
                <el-tooltip
                  content="Re-request; This will refresh the chats below"
                  placement="bottom"
                >
                  <el-button class="options-button">
                    <div class="options-icon" v-html="SVGS.reRequestIcon"></div>
                  </el-button>
                </el-tooltip>
                <!-- edit request -->
                <el-tooltip content="Edit this request" placement="bottom">
                  <el-button
                    class="options-button"
                    @click="editChatItem(item, index)"
                  >
                    <div
                      class="options-icon"
                      v-html="SVGS.eidtChatItemIcon"
                    ></div>
                  </el-button>
                </el-tooltip>
                <!-- delete request -->
                <el-tooltip content="Delete this request" placement="bottom">
                  <el-button
                    class="options-button"
                    @click="deleteChatItem(item.chatIid, index)"
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
          <div v-else class="gpt">
            <div class="gpt-icon" v-html="SVGS.gptIcon"></div>
            <div class="gpt-content">
              <!-- detail content -->
              <div class="text" v-html="marked.render(item.text)"></div>
              <div class="options">
                <!-- re-response -->
                <el-tooltip content="Re-response" placement="bottom">
                  <el-button class="options-button">
                    <div
                      class="options-icon"
                      v-html="SVGS.reResponseIcon"
                    ></div>
                  </el-button>
                </el-tooltip>
                <!-- edit response -->
                <el-tooltip content="Edit this response" placement="bottom">
                  <el-button
                    class="options-button"
                    @click="editChatItem(item, index)"
                  >
                    <div
                      class="options-icon"
                      v-html="SVGS.eidtChatItemIcon"
                    ></div>
                  </el-button>
                </el-tooltip>
                <!-- delete response -->
                <el-tooltip content="Delete this response" placement="bottom">
                  <el-button
                    class="options-button"
                    @click="deleteChatItem(item.chatIid, index)"
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
        </div>
      </div>
    </el-scrollbar>
    <!-- Message Input -->
    <div class="input-card">
      <el-input
        class="custom-textarea"
        type="textarea"
        v-model="inputText"
        placeholder="Please input your question ..."
        @keyup.enter="sendContent"
        :autosize="{ minRows: 1, maxRows: 8 }"
      ></el-input>
      <!-- send and pause button -->
      <el-button
        class="send-button"
        :disabled="inputText == '' && !isChatting"
        @click="sendContent"
      >
        <!-- send chat button -->
        <div
          v-if="!isChatting"
          :class="['svg-icon', { 'svg-icon-disable': inputText == '' }]"
          v-html="SVGS.sendIcon"
        ></div>
        <!-- pause chat button -->
        <div v-else class="svg-icon" v-html="SVGS.pauseIcon"></div>
      </el-button>
    </div>
    <!-- footer -->
    <div class="footer">
      <el-text class="tips"> time: 110ms </el-text>
      <el-text class="tips"> 11/128000 tokens to be sent </el-text>
    </div>
  </div>
  <!-- item editor ovelay -->
  <ItemEditor
    v-model:isShowItemEditor="isShowItemEditor"
    v-model:editChatValue="editChatValue"
  />
</template>

<script>
import { ref, onMounted, nextTick, computed } from "vue";
import { ElMessage } from "element-plus";
import { useStore } from "vuex";
import { chatStreamAPI } from "../../apis/chatStream.js";
import * as SVGS from "../../assets/styles/chat/svgs.js";
import {
  setUserMsgAPI,
  editChatItemAPI,
  deletChatItemAPI,
} from "../../apis/chatAPIs";
import marked from "../../helper/markdownHelper.js";
import { ElMessageBox } from "element-plus";
import ItemEditor from "./ItemEditor.vue";

export default {
  components: { ItemEditor },
  setup() {
    const store = useStore();
    const inputText = ref("");
    const scrollbarRef = ref();
    const innerRef = ref(); // 控制自动刷新到最底部
    const chatHistory = computed(() => store.state.chat.chatHistory);
    const isChatting = computed(() => store.state.chat.isChatting);
    const isStreamResponse = ref(true);
    const isAutoToBottom = ref(true);
    const isShowItemEditor = ref(false);
    const editChatValue = ref("");
    const editChatIndex = ref(-1);
    const chatIid = ref(-1);
    onMounted(() => {
      console.log("ehl");
    });

    /** 输入框的按键组合键 */
    const handleKeydown = async (event) => {
      // Enter 和 Shift 键表示换行的操作
      if (event.key === "Enter" && !event.shiftKey) {
        // 阻止默认行为（换行）并发送内容
        event.preventDefault();
        await sendContent();
      }
    };

    /** 向服务器发送数据 */
    const sendContent = async () => {
      if (isChatting.value) {
        ElMessage.warning("请等待服务器回答完成！");
        return;
      }

      // 将html元素text转成字符串
      var msg = inputText.value.replace(/\n/g, "<br />");
      // 置空输入框
      inputText.value = "";
      // 控制再也不能发送对话
      store.commit("SET_ISCHATTING_STATE", true);
      var rea = await setUserMsgAPI(msg);
      if (rea.flag) {
        // 更新对话
        store.commit("PUSH_CHATHISTORY_STATE", {
          chatIid: rea.chatIid,
          id: "user",
          text: msg,
        });
      }

      // 刷新对话框到最底部
      await setScrollToBottom();
      // 从服务端获得输出
      await chatStreamAPI("active");
    };

    /** 无关紧要的延迟函数 */
    const sleep = async (ms) => {
      return new Promise((resolve) => setTimeout(resolve, ms));
    };

    /**
     * 默认显示最新的内容，拖拉条滚动到最底部
     * Element-plus】如何让滚动条永远在最底部（支持在线演示）
     * https://blog.csdn.net/qq_42203909/article/details/133816286
     */
    const setScrollToBottom = async () => {
      if (!isAutoToBottom.value) return;
      await nextTick();
      const max = innerRef.value.clientHeight;
      scrollbarRef.value.setScrollTop(max);
    };

    /** 编辑某个聊天对话，修改prompt */
    const editChatItem = (item, index) => {
      if (isChatting.value) {
        ElMessage.warning("请等待服务器回答完成！");
        return;
      }

      isShowItemEditor.value = true;
      editChatValue.value = item.text;
      chatIid.value = item.chatIid;
      editChatIndex.value = index;
    };

    /** 删除某个chat */
    const deleteChatItem = async (chatIid, index) => {
      if (isChatting.value) {
        ElMessage.warning("请等待服务器回答完成！");
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
        var rea = await deletChatItemAPI(chatIid);
        if (rea.flag == true) {
          ElMessage.success("删除成功");
          store.commit("DELETE_CHATHISTORY_ITEM", index);
        } else {
          ElMessage.error("删除失败");
        }
      }
    };

    /** 保存对某个对话的修改 */
    const saveChatItem = async () => {
      var flag = false;
      await ElMessageBox.confirm(
        "保存对这个对话的内容的修改吗(无法撤销)?",
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
        var rea = await editChatItemAPI(chatIid.value, editChatValue.value);
        if (rea.flag == true) {
          ElMessage.success("修改成功");
          store.commit("EDIT_CHATHISTORY_ITEM", {
            index: editChatIndex.value,
            data: editChatValue.value,
          });
        } else {
          ElMessage.error("修改失败");
        }

        isShowItemEditor.value = false;
      }
    };

    /** 显示对话的编辑弹窗 chat-settings-overlay */
    const onShowSettings = () => {
      store.commit("SET_EDIT_CHAT_SETTINGS_STATE", true);
    };

    return {
      SVGS,
      isChatting,
      inputText,
      scrollbarRef,
      innerRef,
      chatHistory,
      marked,
      isShowItemEditor,
      editChatValue,
      isStreamResponse,
      isAutoToBottom,
      sendContent,
      handleKeydown,
      sleep,
      editChatItem,
      deleteChatItem,
      saveChatItem,
      onShowSettings,
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
