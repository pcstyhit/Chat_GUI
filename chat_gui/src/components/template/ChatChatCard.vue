<template>
  <div class="chat-container">
    <!-- header -->
    <div class="header">
      <!-- settings -->
      <el-tooltip content="Edit Current Chat" placement="bottom">
        <el-button class="settings">
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
        <div v-for="item in history" :key="item.id">
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
                  <el-button class="options-button">
                    <div
                      class="options-icon"
                      v-html="SVGS.eidtChatItemIcon"
                    ></div>
                  </el-button>
                </el-tooltip>
                <!-- delete request -->
                <el-tooltip content="Delete this request" placement="bottom">
                  <el-button class="options-button">
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
                  <el-button class="options-button">
                    <div
                      class="options-icon"
                      v-html="SVGS.eidtChatItemIcon"
                    ></div>
                  </el-button>
                </el-tooltip>
                <!-- delete response -->
                <el-tooltip content="Delete this response" placement="bottom">
                  <el-button class="options-button">
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
        :disabled="inputText == '' && !chatting"
        @click="sendContent"
      >
        <!-- send chat button -->
        <div
          v-if="!chatting"
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
</template>

<script>
import { ref, onMounted, nextTick } from "vue";
import * as SVGS from "../../assets/styles/chat/svgs.js";
// marked美化
import marked from "../../helper/markdownHelper.js";
export default {
  setup() {
    const history = ref([]);
    const inputText = ref("");
    const chatting = ref(false);
    const scrollbarRef = ref();
    const innerRef = ref();
    const isStreamResponse = ref(true);
    const isAutoToBottom = ref(true);
    onMounted(() => {});
    /** 模仿向服务器发送数据 */
    const sendContent = async () => {
      chatting.value = true;
      var msg = inputText.value.replace(/\n/g, "<br />");
      var ans = inputText.value.replace(/\\n/g, "\n");
      inputText.value = "";
      history.value.push({ id: "user", text: msg });
      // 从服务器获取回答
      await sleep(2000);
      var res = { data: { ans: ans, usage: 100 } };
      history.value.push({ id: "gpt", text: res.data.ans });
      chatting.value = false;
      await setScrollToBottom();
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
      await nextTick();
      const max = innerRef.value.clientHeight;
      console.log("max", max);
      scrollbarRef.value.setScrollTop(max);
    };

    return {
      SVGS,
      history,
      chatting,
      inputText,
      scrollbarRef,
      innerRef,
      isStreamResponse,
      isAutoToBottom,
      sendContent,
      marked,
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
