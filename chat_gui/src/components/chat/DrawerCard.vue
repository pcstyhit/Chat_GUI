<template>
  <div
    class="container"
    :style="{ width: hideOrShowDrawerFlag ? '15%' : '30px' }"
  >
    <!-- 新建对话 -->
    <div class="new_chat">
      <el-button class="new_chat_icon" @click="newChat">
        <el-icon>
          <CirclePlusFilled />
        </el-icon>
      </el-button>
      <div v-if="hideOrShowDrawerFlag" class="new_chat_drawer">
        <el-button class="new_chat_button" @click="newChat">New Chat</el-button>
        <div style="border: 1px solid white; width: 100%"></div>
      </div>
    </div>

    <!-- 历史对话 -->
    <div class="chat_history">
      <el-button class="chat_history_icon" @click="hideOrShowDrawer">
        <el-icon v-if="hideOrShowDrawerFlag">
          <DArrowLeft />
        </el-icon>
        <el-icon v-if="!hideOrShowDrawerFlag">
          <DArrowRight />
        </el-icon>
      </el-button>

      <el-scrollbar v-if="hideOrShowDrawerFlag" class="chat_history_drawer">
        <div
          v-for="item in historyList"
          :key="item"
          class="chat_history_item"
          :style="{
            border:
              chatCid == item.chatCid
                ? '2px solid yellow'
                : '1px solid #8f8d8d',
          }"
        >
          <el-button
            class="drawer_history_button"
            @click="loadHistory(item.chatCid)"
          >
            <div class="history_text">
              <el-text truncated>{{ item.chatName }}</el-text>
            </div>
          </el-button>
          <el-button
            class="drawer_history_more"
            @click="downloadChatPrompt(item.chatCid)"
          >
            <el-icon>
              <Download />
            </el-icon>
          </el-button>
          <el-button
            class="drawer_history_more"
            @click="deleteChatByCid(item.chatCid)"
          >
            <el-icon>
              <DeleteFilled />
            </el-icon>
          </el-button>
          <el-button @click="editChatPrompt" class="drawer_history_more">
            <el-icon>
              <MoreFilled />
            </el-icon>
          </el-button>
        </div>
      </el-scrollbar>
    </div>
    <!-- 查看用户信息 -->
    <div class="chat_info">
      <el-button class="chat_info_icon" @click="logout">
        <el-icon>
          <Avatar />
        </el-icon>
      </el-button>

      <div v-if="hideOrShowDrawerFlag" class="chat_info_drawer">
        <div style="border: 1px solid white; width: 100%"></div>
        <!-- 用户信息 -->
        <div class="chat_info_item">
          <el-text class="chat_info_title_text" truncated>User:</el-text>
          <el-text class="chat_info_text" truncated> {{ user }}</el-text>
        </div>
        <!-- Tokens信息 -->
        <div class="chat_info_item">
          <el-text class="chat_info_title_text" truncated>Tokens:</el-text>
          <el-text class="chat_info_text" truncated>
            {{ tokens }}/{{ modelTokens }}</el-text
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from "vue";
import { useStore } from "vuex";
import { ElMessageBox, ElMessage } from "element-plus";
import { useRouter } from "vue-router";
import {
  getAllHistoryAPI,
  deleteChatAPI,
  loadChatHistoryAPI,
} from "../../apis/chatAPIs.js";
export default {
  emits: ["hideOrShowDrawer", "newChat", "updateHistory", "updateChatCard"],
  // vue3父子传值（setup函数和setup语法糖两版
  // https://juejin.cn/post/7246596605956194341
  props: {
    hideOrShowDrawerFlag: {
      type: Boolean,
      default: true,
    },
    modelTokens: {
      type: Number,
      default: 0,
    },
  },
  setup(props, context) {
    const historyList = ref(null);
    const router = useRouter();
    const store = useStore();
    const user = computed(() => store.state.user);
    const chatCid = computed(() => store.state.chatCid);
    const tokens = computed(() => store.state.tokens);
    const loginState = computed(() => store.state.loginState);

    /** ====================== 下面定义函数 ====================== */
    /** 向父组件发送显示或者隐藏侧边栏的信号, `返回是否开关侧边栏的布尔量`*/
    const hideOrShowDrawer = () => {
      var val = props.hideOrShowDrawerFlag ? false : true;
      context.emit("hideOrShowDrawer", val);
    };

    /** 获取服务器的历史对话记录 */
    const initHistoryList = async () => {
      var rea = await getAllHistoryAPI();
      historyList.value = rea.data;
    };

    /** 向父组件发送要新建对话的信号 */
    const newChat = () => {
      context.emit("newChat");
    };

    /** 向父组件发送加载对话的信号，并`返回对话的chatCid */
    const loadHistory = async (chatCid) => {
      var flag = false;
      await ElMessageBox.confirm("你想继续这个Chat进行对话吗?", "Warning", {
        confirmButtonText: "Yes",
        cancelButtonText: "Cancel",
        type: "warning",
      })
        .then(() => {
          flag = true;
        })
        .catch(() => {
          flag = false;
        });
      if (flag) {
        // 高亮显示当前对话
        context.emit("updateHistory", chatCid);
      }
    };

    const deleteChatByCid = async (chatCid) => {
      var flag = false;
      await ElMessageBox.confirm("删除这个对话?", "Warning", {
        confirmButtonText: "Yes",
        cancelButtonText: "Cancel",
        type: "warning",
      })
        .then(() => {
          flag = true;
        })
        .catch(() => {
          flag = false;
        });
      if (flag) {
        await deleteChatAPI(chatCid);
        await initHistoryList();
        flag = chatCid.value == chatCid;
        if (flag) {
          // 向父组件发出删除对话的信号，如果是当前对话需要更新界面
          context.emit("updateChatCard", { flag: flag });
        }
      }
    };

    const downloadChatPrompt = async (chatCid) => {
      var rea = await loadChatHistoryAPI(chatCid);
      if (rea.flag) {
        var dataObj = {
          prompt: rea.history,
          tokens: rea.tokens,
          modelTokens: rea.modelTokens,
        };

        // 将对象转换成JSON字符串
        const jsonData = JSON.stringify(dataObj);
        // 创建一个包含JSON字符串的Blob对象
        const jsonBlob = new Blob([jsonData], { type: "application/json" });

        // 使用URL.createObjectURL创建一个链接
        const url = URL.createObjectURL(jsonBlob);

        // 创建一个下载链接
        let downloadLink = document.createElement("a");
        downloadLink.href = url;
        downloadLink.download = "prompt.json"; // 指定下载文件名

        // 自动触发下载
        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
      }
    };

    const editChatPrompt = () => {
      ElMessage.info("参数修改, 敬请期待！");
    };

    const logout = async () => {
      var flag = false;
      await ElMessageBox.confirm("退出登录？", "Warning", {
        confirmButtonText: "Yes",
        cancelButtonText: "Cancel",
        type: "warning",
      })
        .then(() => {
          flag = true;
        })
        .catch(() => {
          flag = false;
        });
      if (flag) {
        router.push({
          path: "/",
        });
      }
    };

    onMounted(async () => {
      if (!loginState.value) {
        ElMessage.error("请先登录！");
        // 回到登录界面
        router.push({
          path: "/",
        });
      }
      // 获取服务器的历史对话记录
      await initHistoryList();
    });
    return {
      user,
      chatCid,
      tokens,
      historyList,
      hideOrShowDrawer,
      newChat,
      initHistoryList,
      loadHistory,
      deleteChatByCid,
      downloadChatPrompt,
      editChatPrompt,
      logout,
    };
  },
};
</script>

<style scoped>
.container {
  display: flex;
  width: 15%;
  height: 100%;
  flex-direction: column;
}

.new_chat {
  background-color: black;
  border: none;
  border-radius: 0;
  width: 100%;
  height: 6%;
  display: flex;
  flex-direction: row;
  align-items: center;
}

.new_chat .new_chat_icon {
  height: 100%;
  width: 30px;
  border: none;
  background-color: transparent;
  margin: 0px 0px 0px 0%;
  padding: 0px 0px 0px 0px;
}

.new_chat .new_chat_drawer {
  height: 100%;
  width: 85%;
  border: none;
  background-color: rgb(46, 46, 46);
  margin: 0px 0px 0px 0%;
  padding: 0px 0px 0px 0px;
}

.new_chat .new_chat_button {
  background-color: transparent;
  color: white;
  border: 1px solid gray;
  width: 90%;
  height: 80%;
  margin: 2% 0% 2% 5%;
}
</style>

<style scoped>
.chat_history {
  background-color: black;
  border: none;
  border-radius: 0;
  width: 100%;
  height: 85%;
  display: flex;
  flex-direction: row;
  align-items: center;
}

.chat_history .chat_history_icon {
  height: 100%;
  width: 30px;
  border: none;
  background-color: transparent;
  margin: 0px 0px 0px 0%;
  padding: 0px 0px 0px 0px;
}

.chat_history .chat_history_drawer {
  height: 100%;
  width: 85%;
  border: none;
  background-color: rgb(46, 46, 46);
  margin: 0px 0px 0px 0%;
  padding: 0px 0px 0px 0px;
  max-height: 100%;
}

.chat_history .chat_history_drawer .chat_history_item {
  display: flex;
  align-items: center;
  width: 96%;
  margin: 5% 1% 0% 2%;
  border: 1px solid #8f8d8d;
  border-radius: 5px;
}

.chat_history .chat_history_drawer .drawer_history_button {
  height: 5%;
  width: 60%;
  border: none;
  margin: 0% 0% 0% 2%;
  background-color: transparent;
}

.chat_history .chat_history_drawer .drawer_history_button .history_text {
  width: 70%;
  height: 100%;
  margin: 0% 10% 0% 20%;
  color: #8f8d8d;
}

.chat_history .chat_history_drawer .drawer_history_more {
  height: 5%;
  width: 10%;
  border: none;
  background-color: transparent;
  margin: 0px 0px 0px 2%;
  padding: 0px 0px 0px 0px;
}
</style>

<style scoped>
.chat_info {
  background-color: black;
  border: none;
  border-radius: 0;
  width: 100%;
  height: 9%;
  display: flex;
  flex-direction: row;
  align-items: center;
}

.chat_info .chat_info_icon {
  height: 100%;
  width: 30px;
  border: none;
  background-color: transparent;
  margin: 0px 0px 0px 0%;
  padding: 0px 0px 0px 0px;
}

.chat_info .chat_info_drawer {
  height: 100%;
  width: 85%;
  border: none;
  background-color: rgb(46, 46, 46);
  margin: 0px 0px 0px 0%;
  padding: 0px 0px 0px 0px;
}

.chat_info .chat_info_item {
  margin: 2% 0% 0% 5%;
  height: 40%;
  width: 90%;
  display: flex;
  align-items: center;
  flex-direction: row;
}

.chat_info .chat_info_item .chat_info_title_text {
  height: 100%;
  width: 30%;
  font: bold;
  color: white;
}

.chat_info .chat_info_item .chat_info_text {
  height: 100%;
  width: 70%;
  color: white;
}
</style>
