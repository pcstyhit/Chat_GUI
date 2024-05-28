<template>
  <!-- overlay-dialog -->
  <el-dialog
    class="chat-settings-overlay"
    v-model="isEditChatSettings"
    align-center
    append-to-body
    :show-close="false"
    :close-on-click-modal="false"
  >
    <!-- header -->
    <template #header>
      <div class="header">
        <el-text :tag="'b'" class="label">Settings</el-text>
      </div>
      <el-divider class="divider" />
    </template>
    <!-- settings tab -->
    <div class="content">
      <el-tabs tab-position="left" class="tabs">
        <!-- prompt setting -->
        <el-tab-pane>
          <template #label>
            <span class="tabs-label">
              <div class="icon" v-html="SVGS.promptIcon"></div>
              <el-text class="text">Prompt</el-text>
            </span>
          </template>
          <div class="scroll-bar">
            <!-- chat name -->
            <div class="item">
              <el-text class="item-text">Chat name: </el-text>
              <el-input v-model="chatName" class="input" />
            </div>

            <div class="item">
              <el-text class="item-text">Select model: </el-text>
              <el-select v-model="model">
                <el-option
                  v-for="item in modelList"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                  @change="onSelectModel(item)"
                />
              </el-select>
            </div>
            <!-- divider -->
            <el-divider class="divider" />
            <!-- default prompt switch -->
            <div class="item">
              <el-text class="item-text">Use default prompt: </el-text>
              <el-switch class="c-switch" v-model="isUseDefaultPrompt" />
            </div>
            <!-- system prompt -->
            <div class="item">
              <el-text class="item-text">System: </el-text>
              <el-input v-model="systemContent" class="input" />
            </div>
            <!-- assistant prompt -->
            <div class="item">
              <el-text class="item-text">Assist: </el-text>
              <el-input v-model="assistantContent" class="input" />
            </div>
            <!-- user prompt -->
            <div class="item">
              <el-text class="item-text">User: </el-text>
              <el-input v-model="userContent" class="input" />
            </div>
          </div>
        </el-tab-pane>
        <!-- parameter setting -->
        <el-tab-pane>
          <template #label>
            <span class="tabs-label">
              <div class="icon" v-html="SVGS.paramIcon"></div>
              <el-text class="text">Parameters</el-text>
            </span>
          </template>
          <div class="scroll-bar">
            <div class="item">
              <!-- use default gpt parameters -->
              <el-text class="item-text">Use default parameters: </el-text>
              <el-switch class="c-switch" v-model="isUseDefaultParams" />
            </div>
            <!-- passed recode message -->
            <div class="item">
              <el-text class="item-text">Passed Message(1~20): </el-text>
              <el-slider
                class="slider"
                v-model="passedMsg"
                :min="1"
                :max="20"
              />
              <el-input v-model="passedMsg" class="input-slider" />
            </div>
            <!-- max response tokens -->
            <div class="item">
              <el-text class="item-text">Max Response(1~8192): </el-text>
              <el-slider
                class="slider"
                v-model="maxResponse"
                :min="1"
                :max="8192"
              />
              <el-input v-model="maxResponse" class="input-slider" />
            </div>
            <!-- temperature -->
            <div class="item">
              <el-text class="item-text">Temperature(0.1~1): </el-text>
              <el-slider
                class="slider"
                v-model="temperature"
                :min="0.01"
                :max="1"
                :step="0.01"
              />
              <el-input v-model="temperature" class="input-slider" />
            </div>
            <!-- topP -->
            <div class="item">
              <el-text class="item-text">Top P(0.1~1): </el-text>
              <el-slider
                class="slider"
                v-model="topP"
                :min="0.01"
                :max="1"
                :step="0.01"
              />
              <el-input v-model="topP" class="input-slider" />
            </div>
            <!-- Frequecy penalty -->
            <div class="item">
              <el-text class="item-text">Frequecy penalty(0~2): </el-text>
              <el-slider
                class="slider"
                v-model="frequecyPenaty"
                :min="0"
                :max="2"
                :step="0.01"
              />
              <el-input v-model="frequecyPenaty" class="input-slider" />
            </div>
            <!-- Presence penalty -->
            <div class="item">
              <el-text class="item-text">Presence penalty(0~2): </el-text>
              <el-slider
                class="slider"
                v-model="presentPenaty"
                :min="0"
                :max="2"
                :step="0.01"
              />
              <el-input v-model="presentPenaty" class="input-slider" />
            </div>
            <!-- stop sequences -->
            <div class="item">
              <el-text class="item-text">Stop sequences: </el-text>
              <el-input v-model="stopSequence" class="input" />
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
    <template #footer>
      <div class="dialog-footer">
        <el-button v-if="!isNewChat" class="cancel" @click="cancleSettings"
          >Cancel</el-button
        >
        <el-button v-if="isNewChat" class="confirm" @click="startChat">
          Confirm
        </el-button>
        <el-button v-else class="confirm" @click="startChat"> Save </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script>
import { ref, onMounted, computed } from "vue";
import { useStore } from "vuex";
import { ElMessage } from "element-plus";
import * as SVGS from "../../assets/styles/chat/svgs.js";
import { newChatAPI, setChatParamsAPI } from "../../apis/chatAPIs.js";

export default {
  name: "PromptCard",
  emits: ["startChat"],
  setup(props, context) {
    // 从store中得到关于chat的状态
    const store = useStore();
    const isEditChatSettings = computed(
      () => store.state.chat.isEditChatSettings
    );
    // 根据store存的chat的history判断是不是新建对话
    const isNewChat = computed(() => store.state.chat.chatHistory.length == 0);

    // chat的名称
    const chatName = ref("");

    // 默认的模型参数, TODO 后续可选的模型参数信息从server中获得
    const modelList = ref([
      { label: "GPT-4o", value: 128 },
      { label: "GPT-4", value: 32 },
    ]);
    const model = modelList.value[0];

    // prompt 的 响应式变量
    const isUseDefaultPrompt = ref(true);
    const systemContent = ref("");
    const userContent = ref("");
    const assistantContent = ref("");

    // 和gpt交互的参数
    const isUseDefaultParams = ref(true);
    const passedMsg = ref(20);
    const maxResponse = ref(2048);
    const temperature = ref(0.7);
    const topP = ref(0.95);
    const frequecyPenaty = ref(0);
    const presentPenaty = ref(0);
    const stopSequence = ref("");

    onMounted(() => {
      // 使用默认的prompt
      isUseDefaultPrompt.value = true;
      isUseDefaultParams.value = true;
      useDefaultPrompt();
    });

    /** 将响应式变量全部重置到初始化的值 */
    const useDefaultPrompt = () => {
      // 时间辅助函数
      const padZero = (value) => {
        return String(value).padStart(2, "0");
      };

      const now = new Date();
      // 随机提供对话名称
      chatName.value = `${padZero(now.getMonth() + 1)}${padZero(
        now.getDate()
      )}_${padZero(now.getHours())}${padZero(now.getMinutes())}${padZero(
        now.getSeconds()
      )}`;

      // 重置prompt回到最初状态
      systemContent.value =
        "You are Chat GPT-4 a large language model of OpenAI.";
      assistantContent.value = "";
      userContent.value = "";
      // 重置parameters回到最初状态
      passedMsg.value = 20;
      maxResponse.value = 2048;
      temperature.value = 0.7;
      topP.value = 0.95;
      frequecyPenaty.value = 0;
      presentPenaty.value = 0;
      stopSequence.value = "";
    };

    /** 关闭当前的setting窗口 */
    const cancleSettings = () => {
      store.commit("SET_EDIT_CHAT_SETTINGS_STATE", false);
    };

    /** 向server发送请求创建对应的对话的channel */
    const startChat = async () => {
      if (chatName.value == "") {
        ElMessage.error("😡 Chat 的名称不能为空!");
        return;
      }
      // 发送请求
      var rea = await newChatAPI(chatName.value);
      if (!rea.flag) {
        ElMessage.error("创建对话失败!");
        return;
      }
      // set chat config
      await setChatParamsAPI("GPT4o", systemContent.value, passedMsg.value);
      // emit signal to show chat card.
      context.emit("startChat", {
        chatCid: rea.chatCid,
        rea: true,
      });
      ElMessage.info("参数的修改,暂时支持默认, 敬请期待(2024-03-13) 👻!");
      cancleSettings();
    };

    return {
      isEditChatSettings,
      SVGS,
      model,
      modelList,
      isUseDefaultPrompt,
      chatName,
      systemContent,
      userContent,
      assistantContent,
      isUseDefaultParams,
      passedMsg,
      maxResponse,
      temperature,
      topP,
      frequecyPenaty,
      presentPenaty,
      stopSequence,
      isNewChat,
      startChat,
      cancleSettings,
    };
  },
};
</script>

<style scoped>
.prompt-settings {
  position: relative;
  left: 35%;
  border: 1px solid rgb(84, 126, 66);
  width: 30%;
  height: 60%;
  display: flex;
  flex-direction: column;
}

.prompt-item {
  width: 100%;
  height: 6%;
  margin-top: 5px;
  margin-bottom: 10px;
  display: flex;
  flex-direction: row;
  align-items: center;
}

.prompt-title {
  width: 40%;
  height: 100%;
  margin-right: 10px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.prompt-title-2 {
  width: 60%;
  height: 100%;
  margin-right: 10px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.prompt-element {
  width: 60%;
  height: 100%;
}

.prompt-element-2 {
  width: 40%;
  height: 100%;
}
</style>

<style scoped>
.prompt-element:deep(.el-textarea__inner) {
  resize: none !important;
}
</style>
