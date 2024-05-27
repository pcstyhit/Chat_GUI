<template>
  <div class="chat-sidebar-container" id="chat-sidebar-container">
    <!-- header -->
    <div class="header">
      <!-- sidebar -->
      <el-tooltip content="Close sidebar" placement="bottom">
        <el-button class="button" @click="onShowSidebar">
          <div class="svg-icon" v-html="SVGS.sildbarIcon"></div>
        </el-button>
      </el-tooltip>
      <!-- new chat -->
      <el-tooltip content="New Chat" placement="bottom">
        <el-button class="button">
          <div class="svg-icon" v-html="SVGS.newChatIcon"></div>
        </el-button>
      </el-tooltip>
    </div>
    <!-- content -->
    <div v-show="isShowSidebar" class="content">
      <div class="chats">
        <!-- chat history list -->
        <div v-for="item in historyList" :key="item">
          <!-- chat item -->
          <el-button
            @click="onSelectChat(item)"
            :class="['chat-item', { 'selected-chat-item': chatName === item }]"
          >
            <!-- chat item label -->
            <el-text
              class="truncated-text"
              :tag="chatName === item ? 'b' : 'span'"
              >{{ item }}</el-text
            >
            <!-- chat item options -->
            <el-dropdown trigger="click" class="options">
              <div
                class="svg-icon"
                v-html="SVGS.optionsIcon"
                @click.stop="onShowChatOpts"
              ></div>

              <template #dropdown>
                <el-dropdown-menu>
                  <!-- download or share -->
                  <el-dropdown-item @click.stop="onDownloadChat">
                    <div class="svg-icon" v-html="SVGS.downloadIcon"></div>
                    <el-text style="margin-left: 8px">Download</el-text>
                  </el-dropdown-item>
                  <!-- rename -->
                  <el-dropdown-item @click.stop="onEditChat">
                    <div class="svg-icon" v-html="SVGS.editIcon"></div>
                    <el-text style="margin-left: 8px">Edit</el-text>
                  </el-dropdown-item>
                  <!-- delete -->
                  <el-dropdown-item
                    @click.stop="onDeleteChat"
                    style="color: red"
                  >
                    <div class="svg-icon" v-html="SVGS.deleteIcon"></div>
                    <el-text style="color: red; margin-left: 8px"
                      >Delete</el-text
                    >
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, unref } from "vue";
import * as SVGS from "../../assets/styles/chat/svgs.js";
import * as DOMSIZE from "../../assets/styles/consts.js";
export default {
  setup() {
    const isShowSidebar = ref(true);
    const chatName = ref("1234");
    const chatOptsPopRef = ref(null);
    const historyList = ref([
      "RN_WIGHGDGJ",
      "HHDYUUEIO",
      "1234",
      "HJDHGYIUGEUI",
      "YJYJGDYUIGE7836E789YHDIUH378TGIY",
    ]);

    /** 尝试动态的调整侧边栏大小，显示隐藏对话记录 */
    const onShowSidebar = () => {
      var sidebarDOM = document.getElementById("chat-sidebar-container");
      isShowSidebar.value = !isShowSidebar.value;
      if (!isShowSidebar.value) {
        sidebarDOM.style.width = `${DOMSIZE.SIDEBAR_MIN_WIDTH}px`;
        sidebarDOM.style.backgroundColor = "transparent";
      } else {
        sidebarDOM.style.width = "";
        sidebarDOM.style.backgroundColor = DOMSIZE.SIDEBAR_BACKGROUND_COLOR;
      }
    };

    /** 选择对应的chat名称/id */
    const onSelectChat = (val) => {
      chatName.value = val;
    };

    /** 显示多选的菜单还要记录是哪个对话要显示这些内容 */
    const onShowChatOpts = (event) => {
      event.stopPropagation();
    };

    const onClickOutside = () => {
      unref(chatOptsPopRef).chatOptsPopRef?.delayHide?.();
    };

    const newChat = () => {};

    const onDownloadChat = () => {
      console.log("1");
    };

    const onEditChat = () => {
      console.log("2");
    };
    const onDeleteChat = () => {
      console.log("3");
    };
    return {
      SVGS,
      isShowSidebar,
      chatName,
      historyList,
      chatOptsPopRef,
      onShowSidebar,
      newChat,
      onSelectChat,
      onShowChatOpts,
      onClickOutside,
      onDownloadChat,
      onEditChat,
      onDeleteChat,
    };
  },
};
</script>
