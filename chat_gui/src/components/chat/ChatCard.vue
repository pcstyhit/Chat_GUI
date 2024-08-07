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
        <!-- user info -->
        <el-tooltip
          content="User management"
          placement="bottom"
          :show-after="500"
        >
          <el-button class="user-man" @click="onShowUserSettingOverlay">
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
    <div class="roles-card" v-if="isShowRoleCard">
      <RolesCard />
    </div>
    <!-- Message Output -->
    <el-scrollbar class="scroll-window" ref="scrollbarRef">
      <div id="chat-messages-container" ref="innerRef"></div>
    </el-scrollbar>
    <!-- Message Input -->
    <div class="input-card" id="chat-input-card">
      <el-button class="attach-button" @click="uploadImageFile">
        <!-- pause chat button -->
        <div class="icon" v-html="SVGS.chatAttachIcon"></div>
      </el-button>
      <div class="input-area">
        <div class="imgs" id="chat-input-imgs"></div>
        <el-input
          class="custom-textarea"
          type="textarea"
          v-model="userQuestionText"
          placeholder="Please input your question ..."
          @keydown.enter="onEnterKeydown"
          :autosize="{ minRows: 1, maxRows: 4 }"
        ></el-input>
      </div>
      <!-- send and pause button -->
      <el-button class="send-button" @click="onSendContent">
        <!-- send chat button -->
        <div
          v-if="!isChatting"
          :class="['svg-icon', { 'svg-icon-disable': userQuestionText == '' }]"
          v-html="SVGS.sendIcon"
        ></div>
        <!-- pause chat button -->
        <div v-else class="svg-icon" v-html="SVGS.pauseIcon"></div>
      </el-button>
    </div>
    <!-- footer -->
    <div class="footer">
      <el-text class="tips"> time: {{ requestTimeObj.time }}ms </el-text>
      <el-text class="tips">
        {{ tokens }}/{{ chatParams.maxTokens }} tokens to be sent
      </el-text>
    </div>
  </div>
  <!-- item editor ovelay -->
  <TextEditor />
  <UserSettings />
</template>

<script setup>
import * as SVGS from "../../assets/styles/chat/svgs.js";
import TextEditor from "../common/TextEditor.vue";
import RolesCard from "./RolesCard.vue";
import UserSettings from "../home/UserSettings.vue";
import chatCardHandler from "../../helper/chat/card.js";

import { useStore } from "vuex";
import { ref, computed, watch, onMounted, nextTick } from "vue";
import { showMessage, showMessageBox } from "../../helper/customMessage.js";
import { pasteImage, uploadImageFile } from "../../helper/user/files.js";

const store = useStore();
const chatParams = computed(() => store.state.chat.chatParams);
const tokens = computed(() => store.state.chat.tokens);

const userQuestionText = ref("");
const isChatting = ref(false);
const isShowRoleCard = ref(true);
const requestTimeObj = ref({
  startTime: 0,
  time: 0,
});

const scrollbarRef = ref();
const innerRef = ref();

onMounted(() => {
  pasteImage();
});

watch(
  () => store.state.chat.chatCid,
  async (value) => {
    if (value !== "") {
      isShowRoleCard.value = false;
    } else {
      isShowRoleCard.value = true;
      requestTimeObj.value.time = 0;
    }
  }
);

/** 输入框的按键组合键 */
const onEnterKeydown = async (event) => {
  // Enter 和 Shift 键表示换行的操作
  if (event.key === "Enter" && !event.shiftKey) {
    // 阻止默认行为（换行）并发送内容
    event.preventDefault();
    if (isShowRoleCard.value) isShowRoleCard.value = false;
    await onSendContent();
  }
};

/** 向服务器发送数据 */
const onSendContent = async () => {
  if (isChatting.value) {
    const flag = await showMessageBox("取消继续生成对话吗?");
    if (flag) {
      chatCardHandler.stopChat();
      isChatting.value = false;
    }
    return;
  }

  // 及时清空对话框
  var msg = userQuestionText.value;
  if (msg == "") {
    showMessage("warning", "输入正确的问题");
    return;
  }
  userQuestionText.value = "";

  // 请求API
  isChatting.value = true;
  startRequestTime();

  await chatCardHandler.sendChat(msg, setScrollToBottom);
  isChatting.value = false;
  chatCardHandler.addListener();
  stopRequestTime();
};

const startRequestTime = () => {
  requestTimeObj.value.time = 0;
  requestTimeObj.value.startTime = new Date().getTime();
};

const stopRequestTime = () => {
  requestTimeObj.value.time =
    new Date().getTime() - requestTimeObj.value.startTime;
};

/**
 * 默认显示最新的内容，拖拉条滚动到最底部
 * Element-plus】如何让滚动条永远在最底部（支持在线演示）
 * https://blog.csdn.net/qq_42203909/article/details/133816286
 */
const setScrollToBottom = async () => {
  await nextTick();
  const max = innerRef.value.clientHeight;
  scrollbarRef.value.setScrollTop(max);
};

/** 显示对话的编辑弹窗 chat-settings-overlay */
const onShowSettings = () => {
  store.commit("SET_CHAT_SHOWSETTINGUI", true);
};

const onShowUserSettingOverlay = () => {
  store.commit("SET_USER_SHOWSETTINGUI", true);
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
