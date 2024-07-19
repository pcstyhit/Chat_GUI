<template>
  <!-- overlay-dialog -->
  <el-drawer
    class="chat-settings-drawer"
    v-model="isOpenSettingDialog"
    :before-close="onCancleSettings"
  >
    <!-- header -->
    <template #header>
      <div class="header">
        <el-text class="label">Edit Current Chat Settings</el-text>
      </div>
    </template>

    <!-- settings tab -->
    <div class="content">
      <el-divider class="divider" />

      <el-scrollbar class="scroll-bar">
        <!-- chat name and model type -->
        <div class="title">
          <el-text class="label">Edit chat name and model type.</el-text>
        </div>
        <div class="item">
          <el-text class="item-text">Chat name: </el-text>
          <el-input class="input" v-model="chatParams.chatName" />
        </div>
        <div class="item">
          <el-text class="item-text">Select model: </el-text>
          <el-select v-model="chatParams.modelName" class="item-select">
            <el-option
              v-for="item in chatModelList"
              :key="item.modelName"
              :label="item.modelName"
              :value="item.modelName"
              @change="onSelectModel(item)"
            />
          </el-select>
        </div>
        <el-divider class="divider" />
        <!-- chat prompts -->
        <div class="title">
          <el-text class="label">Edit chat prompts</el-text>
        </div>
        <div class="item">
          <el-text class="item-text">Use default settings: </el-text>
          <el-switch class="c-switch" v-model="isUseDefaultPrompt" />
        </div>
        <div class="item-textarea">
          <el-text class="item-text">System: </el-text>
          <el-input
            class="input"
            type="textarea"
            v-model="chatSysPrompt"
            @input="updateChatPrompts"
          />
        </div>
        <div class="item-textarea">
          <el-text class="item-text">User: </el-text>
          <el-input
            class="input"
            type="textarea"
            v-model="chatUserPrompt"
            @input="updateChatPrompts"
          />
        </div>
        <div class="item-textarea">
          <el-text class="item-text">Assist: </el-text>
          <el-input
            class="input"
            type="textarea"
            v-model="chatAssPrompt"
            @input="updateChatPrompts"
          />
        </div>
        <el-divider class="divider" />
        <!-- chat parameters -->
        <div class="title">
          <el-text class="label">Edit chat parameters.</el-text>
        </div>
        <div class="item">
          <el-text class="item-text">Use default settings: </el-text>
          <el-switch class="c-switch" v-model="isUseDefaultParams" />
        </div>
        <div class="item">
          <el-text class="item-text">Passed Message(1~20): </el-text>
          <el-slider
            class="slider"
            v-model="chatParams.passedMsgLen"
            :min="1"
            :max="20"
          />
          <el-input
            v-model.number="chatParams.passedMsgLen"
            class="input-slider"
            @input="validateRange('passedMsgLen', 1, 20)"
          />
        </div>
        <div class="item">
          <el-text class="item-text">Max Response(1~8192): </el-text>
          <el-slider
            class="slider"
            v-model="chatParams.maxResponseTokens"
            :min="1"
            :max="8192"
          />
          <el-input
            v-model.number="chatParams.maxResponseTokens"
            class="input-slider"
            @input="validateRange('maxResponseTokens', 1, 8192)"
          />
        </div>
        <div class="item">
          <el-text class="item-text">Temperature(0.1~1): </el-text>
          <el-slider
            class="slider"
            v-model="chatParams.temperature"
            :min="0.01"
            :max="1"
            :step="0.01"
          />
          <el-input
            v-model.number="chatParams.temperature"
            class="input-slider"
            @input="validateRange('temperature', 0.1, 1)"
          />
        </div>
        <div class="item">
          <el-text class="item-text">Top P(0.1~1): </el-text>
          <el-slider
            class="slider"
            v-model="chatParams.topP"
            :min="0.01"
            :max="1"
            :step="0.01"
          />
          <el-input
            v-model.number="chatParams.topP"
            class="input-slider"
            @input="validateRange('topP', 0.1, 1)"
          />
        </div>
        <div class="item">
          <el-text class="item-text">Frequecy penalty(0~2): </el-text>
          <el-slider
            class="slider"
            v-model="chatParams.frequecyPenaty"
            :min="0"
            :max="2"
            :step="0.01"
          />
          <el-input
            v-model.number="chatParams.frequecyPenaty"
            class="input-slider"
            @input="validateRange('frequecyPenaty', 0, 2)"
          />
        </div>
        <div class="item">
          <el-text class="item-text">Presence penalty(0~2): </el-text>
          <el-slider
            class="slider"
            v-model="chatParams.presentPenaty"
            :min="0"
            :max="2"
            :step="0.01"
          />
          <el-input
            v-model.number="chatParams.presentPenaty"
            class="input-slider"
            @input="validateRange('presentPenaty', 0, 2)"
          />
        </div>
        <div class="item-textarea">
          <el-text class="item-text">Stop sequences: </el-text>
          <el-input
            class="input"
            type="textarea"
            v-model="chatStopSequence"
            @input="validStopSequence"
          />
        </div>
      </el-scrollbar>
      <el-divider class="divider" />
    </div>
    <template #footer>
      <div class="dialog-footer">
        <el-button class="cancel" @click="onCancleSettings">Cancel</el-button>
        <el-button v-if="isNewChat" class="confirm" @click="onStartChat">
          Confirm
        </el-button>
        <el-button v-else class="confirm" @click="onStartChat">
          Save
        </el-button>
      </div>
    </template>
  </el-drawer>
</template>

<script setup>
import { ref, computed, watch } from "vue";
import { useStore } from "vuex";
import { showMessage } from "../../helper/customMessage.js";
import { addNewChatAPI, setChatParamsAPI } from "../../apis/chat.js";

// 从store中得到关于chat的状态
const store = useStore();

// 控制对话框的属性
const isOpenSettingDialog = ref(false);

// 根据store存的chat的chatCid是不是''判断是不是新建对话
const isNewChat = computed(() => store.state.chat.chatCid == "");
const chatCid = computed(() => store.state.chat.chatCid);
const chatModelList = computed(() => store.state.chat.modelList);

// 要被修改的对话的全部参数
const chatParams = ref({});
const chatSysPrompt = ref("");
const chatUserPrompt = ref("");
const chatAssPrompt = ref("");
const chatStopSequence = ref("");

const isUseDefaultPrompt = ref(true);
const isUseDefaultParams = ref(true);

// 绕过v-model提示的computed是readonly的行为
watch(
  () => store.state.chat.isEditChatSettings,
  async (value) => {
    isOpenSettingDialog.value = value == 1;
    if (isOpenSettingDialog.value) {
      Object.keys(store.state.chat.chatParams).forEach((key) => {
        chatParams.value[key] = store.state.chat.chatParams[key];
      });
      // 更新对应的 chat prompt的值
      chatSysPrompt.value = getPromptContentByRole("system");
      chatUserPrompt.value = getPromptContentByRole("user");
      chatAssPrompt.value = getPromptContentByRole("assistant");
      chatStopSequence.value = JSON.stringify(chatParams.value.stopSequence);
    }
  }
);

/**
 * *************************
 * 处理Save/Confirm(也就是新建对话)的逻辑函数
 * *************************
 * */
const handleSetChatParams = async () => {
  // 要编辑/新建的chatCid的值
  var currentChatCid = chatCid.value;
  // 是否新建对话的标志
  if (isNewChat.value) {
    // 发送请求来获取有效的ChatCid
    var rea = await addNewChatAPI();
    if (!rea.flag) return false;
    // 🎉 有效的ChatCid, 新建对话成功！ 存入store
    store.commit("SET_NEWCHATCID", rea.chatCid);
    currentChatCid = rea.chatCid;

    // 新建的对话存入store里
    store.commit("PUSH_CHATNAMELIST", {
      chatCid: rea.chatCid,
      chatName: chatParams.value.chatName,
    });
  }

  // 开始设置对话的参数到数据库
  rea = await setChatParamsAPI(currentChatCid, chatParams.value);
  if (!rea.flag) return false;

  store.commit("SET_CHATPARAMS", chatParams.value);
  // 参数修改完成之后更新label
  store.commit("SET_CHAT_SHOWSETTINGUI", -1);
  store.commit("EDIT_CHATNAMELIST", {
    chatCid: currentChatCid,
    chatName: chatParams.value.chatName,
  });
  return true;
};

const validateRange = (param, min, max) => {
  chatParams.value[param] = Math.max(
    min,
    Math.min(max, chatParams.value[param])
  );
};

const validStopSequence = () => {
  const resultArray = chatStopSequence.value.replace(/\n/g, "").split(";");
  // 检查结果是否是数组
  if (Array.isArray(resultArray)) {
    chatParams.value.stopSequence = resultArray;
  } else {
    showMessage("error", "Chat stop sequence必须是数组类型的字符串");
  }
};

const updateChatPrompts = () => {
  const key = "content";
  const tmpPrompts = [
    { role: "system", content: (chatSysPrompt.value || "").replace(/\n/g, "") },
    { role: "user", content: (chatUserPrompt.value || "").replace(/\n/g, "") },
    {
      role: "assistant",
      content: (chatAssPrompt.value || "").replace(/\n/g, ""),
    },
  ];
  chatParams.value.prompts = tmpPrompts.filter(
    (item) => item[key] !== "" && item[key] !== undefined
  );
};

/**
 * *************************
 * 选择合适的模型
 * *************************
 * */
const onSelectModel = (item) => {
  chatParams.value.modelName = item.modelName;
  chatParams.value.maxTokens = item.maxTokens;
  chatParams.value.modelType = item.modelType;
};

/**  定义一个函数来获取指定角色的提示内容 */
const getPromptContentByRole = (role) => {
  if (chatParams.value.prompts) {
    return (chatParams.value.prompts.find((item) => item.role === role) || {})
      .content;
  }
  return "";
};

/**
 * *************************
 * 关闭当前的setting窗口
 * *************************
 * */
const onCancleSettings = async () => {
  isOpenSettingDialog.value = false;
  store.commit("SET_CHAT_SHOWSETTINGUI", 0);
};

/**
 * *************************
 * 向server发送请求创建对应的对话的channel
 * *************************
 * */
const onStartChat = async () => {
  if (chatParams.value.chatName == "") {
    showMessage("error", "😡 Chat 的名称不能为空!");
    return;
  }

  // 提前关闭窗口, 再进行API请求, 使得新建chat的逻辑不会和编辑chat的时候的chatCid不为空的保存逻辑冲突
  isOpenSettingDialog.value = false;

  // 判断是新建还是保存
  var flag = await handleSetChatParams();
  if (!flag) {
    showMessage("error", "Start Chat error!");
    return;
  }
};
</script>
