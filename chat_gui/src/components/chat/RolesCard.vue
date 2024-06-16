<template>
  <div class="chat-roles-card">
    <div class="container">
      <div class="role-group">
        <div class="role-card" @click="handleFileUpload">
          <el-tooltip
            content="Upload chat history with default model parameters"
            placement="bottom"
            :show-after="500"
          >
            <div class="tips" v-html="SVGS.roleTipsSettings"></div>
          </el-tooltip>

          <div class="icon" v-html="SVGS.roleUploadIcon"></div>
          <el-text class="label">Upload History</el-text>
        </div>
        <div class="role-card" @click="onNewGhostChat(ghostTemplate.translate)">
          <el-tooltip
            content="中英互译助手"
            placement="bottom"
            :show-after="500"
          >
            <div class="tips" v-html="SVGS.roleTipsGhost"></div>
          </el-tooltip>

          <div class="icon" v-html="SVGS.roleTranslateIcon"></div>
          <el-text class="label">Translate helper</el-text>
        </div>
        <div
          class="role-card"
          @click="onNewGhostChat(ghostTemplate.gitCommitHelper)"
        >
          <el-tooltip
            content="git commit和git emoji的助手"
            placement="bottom"
            :show-after="500"
          >
            <div class="tips" v-html="SVGS.roleTipsGhost"></div>
          </el-tooltip>

          <div class="icon" v-html="SVGS.roleGitCommitIcon"></div>
          <el-text class="label">Git Commit Helper</el-text>
        </div>
      </div>
      <!-- 隐藏的文件输入元素 -->
      <input
        type="file"
        ref="fileInput"
        accept="application/json"
        style="display: none"
        @change="readFile"
      />
    </div>
  </div>
</template>

<script>
import * as SVGS from "../../assets/styles/chat/svgs.js";
import { computed } from "vue";
import { useStore } from "vuex";
import { ElMessage } from "element-plus";
import { uploadChatHistory, newGhostChatAPI } from "../../apis/chatAPIs.js";
export default {
  setup() {
    const store = useStore();
    const ghostTemplate = {
      translate: {
        type: `translate`,
        msg: `好的, 我是一个中英互译助手, 请开始输入中文或者英文，我会为你进行翻译并列出翻译中的关键 😎`,
        name: `👻 中英互译助手`,
      },
      gitCommitHelper: {
        type: `gitCommitHelper`,
        msg: `好的, 我是一个git commit定制化的助手, 请开始输入你的commit 👻`,
        name: `👏 git commit 助手`,
      },
    };

    const chatParams = computed(() => store.state.chat.chatParams);
    // 处理点击事件并触发文件输入点击
    const handleFileUpload = () => {
      const fileInput = document.createElement("input");
      fileInput.type = "file";
      fileInput.accept = "application/json";
      fileInput.style.display = "none";
      fileInput.addEventListener("change", readFile);
      document.body.appendChild(fileInput);
      fileInput.click();
    };

    // 读取选中的文件并将其内容打印到控制台
    const readFile = (event) => {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = async (e) => {
          try {
            const jsonContent = JSON.parse(e.target.result);
            // 读取到文本的内容
            var rea = await uploadChatHistory(jsonContent);
            if (!rea.flag) {
              ElMessage.error("SERVER 解析 JSON 出错:");
              return;
            }
            // 解析成功新建对话
            store.commit("SET_NEWCHATCID_STATE", rea.chatCid);
            store.commit("SET_CHATHISTORY_STATE", rea.history);
            // 更新下次要发送的消息的tokens数量
            store.commit("SET_TOKENS_STATE", rea.tokens);
            // 更新对话名称
            store.commit("PUSH_CHATLIST_STATE", {
              chatCid: rea.chatCid,
              chatName: chatParams.value.chatName,
            });
          } catch (error) {
            ElMessage.error("WEB 解析 JSON 出错:", error);
          }
        };
        // 将文件读取为文本
        reader.readAsText(file);
      }
    };

    const onNewGhostChat = async (item) => {
      var rea = await newGhostChatAPI(item.type);
      if (!rea.flag) {
        ElMessage.error("New Ghost chat error 😫");
        return;
      }

      // 解析成功新建对话
      store.commit("SET_NEWCHATCID_STATE", rea.chatCid);
      // 设置对话的参数
      store.commit("SET_CHATPARAMS_STATE", rea.chatParams);
      // 给个默认显示的对话内容
      store.commit("PUSH_CHATHISTORY_STATE", {
        chatIid: "xxx-xxx-xxx",
        role: "assistant",
        content: item.msg,
        text: item.msg,
      });
      // 更新下次要发送的消息的tokens数量
      store.commit("SET_TOKENS_STATE", rea.tokens);
      // 更新对话名称
      store.commit("PUSH_CHATLIST_STATE", {
        chatCid: rea.chatCid,
        chatName: item.name,
      });
    };

    return {
      handleFileUpload,
      onNewGhostChat,
      readFile,
      ghostTemplate,
      SVGS,
    };
  },
};
</script>
