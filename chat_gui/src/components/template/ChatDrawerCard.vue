<template>
  <div
    class="container"
    :style="{ width: hideOrShowDrawerFlag ? '15%' : '30px' }"
  >
    <!-- 新建对话 -->
    <div class="new_chat">
      <el-button class="new_chat_icon">
        <el-icon><CirclePlusFilled /></el-icon>
      </el-button>
      <div v-if="hideOrShowDrawerFlag" class="new_chat_drawer">
        <el-button class="new_chat_button">New Chat</el-button>
        <div style="border: 1px solid white; width: 100%"></div>
      </div>
    </div>

    <!-- 历史对话 -->
    <div class="chat_history">
      <el-button class="chat_history_icon" @click="hideOrShowDrawer">
        <el-icon v-if="hideOrShowDrawerFlag"><DArrowLeft /></el-icon>
        <el-icon v-if="!hideOrShowDrawerFlag"><DArrowRight /></el-icon>
      </el-button>

      <el-scrollbar v-if="hideOrShowDrawerFlag" class="chat_history_drawer">
        <div
          v-for="item in historyList"
          :key="item"
          class="chat_history_item"
          :style="{
            border: chatName == item ? '2px solid yellow' : '1px solid #8f8d8d',
          }"
        >
          <el-button class="drawer_history_button"
            ><div class="history_text">
              <el-text truncated>{{ item }}</el-text>
            </div></el-button
          >
          <el-button class="drawer_history_more">
            <el-icon><Download /></el-icon>
          </el-button>
          <el-button class="drawer_history_more">
            <el-icon><DeleteFilled /></el-icon>
          </el-button>
          <el-button class="drawer_history_more">
            <el-icon><MoreFilled /></el-icon>
          </el-button>
        </div>
      </el-scrollbar>
    </div>
    <!-- 查看用户信息 -->
    <div class="chat_info">
      <el-button class="chat_info_icon">
        <el-icon><Avatar /></el-icon>
      </el-button>

      <div v-if="hideOrShowDrawerFlag" class="chat_info_drawer">
        <div style="border: 1px solid white; width: 100%"></div>
        <!-- 用户信息 -->
        <div class="chat_info_item">
          <el-text class="chat_info_title_text" truncated>User:</el-text>
          <el-text class="chat_info_text" truncated> {{ "PLDZ" }}</el-text>
        </div>
        <!-- Tokens信息 -->
        <div class="chat_info_item">
          <el-text class="chat_info_title_text" truncated>Tokens:</el-text>
          <el-text class="chat_info_text" truncated>
            {{ 32768 }}/{{ 32768 }}</el-text
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
export default {
  setup() {
    const hideOrShowDrawerFlag = ref(true);
    const chatName = ref("1234");
    const historyList = ref([
      "RN_WIGHGDGJ",
      "HHDYUUEIO",
      "1234",
      "HJDHGYIUGEUI",
      "YJYJGDYUIGE",
      "IUHG3EUIYHUI",
      "KUWEUIHUDE",
      "YIDGUIEYHIHR",
      "IWETIUY3EIU3Y298I7",
      "7836E789YHDIUH378TGIY",
      "UDYT8736TGJYHDGYU",
      "UIYD897I3YHUIH32",
      ":UYDGEYUIUEYUGB",
      "U3T7831TYIUH",
      "389EY8903UY08OHOE",
      "UERGIUGHDUKIHE",
      "IUH3GEUIYH8392",
      "I73EYUIGB3I21TY7",
      "KRD3JY98IU7HDKUJ",
      ":UIYU390EUOIU3H2RIU",
    ]);

    const hideOrShowDrawer = () => {
      hideOrShowDrawerFlag.value = !hideOrShowDrawerFlag.value;
    };

    const newChat = () => {};
    return {
      hideOrShowDrawerFlag,
      chatName,
      historyList,
      hideOrShowDrawer,
      newChat,
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
