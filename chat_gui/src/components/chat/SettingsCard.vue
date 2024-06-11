<template>
  <!-- overlay-dialog -->
  <el-dialog
    class="chat-settings-overlay"
    v-model="isOpenSettingDialog"
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
              <el-input v-model="chatParams.chatName" class="input" />
            </div>

            <div class="item">
              <el-text class="item-text">Select model: </el-text>
              <el-select v-model="chatParams.modelName">
                <el-option
                  v-for="item in chatParams.modelList"
                  :key="item"
                  :label="item.label"
                  :value="item.value"
                  @click="onSelectModel(item)"
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
              <el-text class="item-text">Prompts: </el-text>
              <el-input
                :value="JSON.stringify(chatParams.promptTemplate)"
                class="input"
              />
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
              <!-- use default assistant parameters -->
              <el-text class="item-text">Use default parameters: </el-text>
              <el-switch class="c-switch" v-model="isUseDefaultParams" />
            </div>
            <!-- passed recode message -->
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
                @input="
                  () => {
                    chatParams.passedMsgLen =
                      chatParams.passedMsgLen >= 20
                        ? 20
                        : chatParams.passedMsgLen;
                    chatParams.passedMsgLen =
                      chatParams.passedMsgLen <= 1
                        ? 1
                        : chatParams.passedMsgLen;
                  }
                "
              />
            </div>
            <!-- max response tokens -->
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
                @input="
                  () => {
                    chatParams.maxResponseTokens =
                      chatParams.maxResponseTokens >= 8192
                        ? 8192
                        : chatParams.maxResponseTokens;
                    chatParams.maxResponseTokens =
                      chatParams.maxResponseTokens <= 1
                        ? 1
                        : chatParams.maxResponseTokens;
                  }
                "
              />
            </div>
            <!-- temperature -->
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
                @input="
                  () => {
                    chatParams.temperature =
                      chatParams.temperature >= 1 ? 1 : chatParams.temperature;
                    chatParams.temperature =
                      chatParams.temperature <= 0.01
                        ? 0.01
                        : chatParams.temperature;
                  }
                "
              />
            </div>
            <!-- topP -->
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
                @input="
                  () => {
                    chatParams.topP =
                      chatParams.topP >= 1 ? 1 : chatParams.topP;
                    chatParams.topP =
                      chatParams.topP <= 0.01 ? 0.01 : chatParams.topP;
                  }
                "
              />
            </div>
            <!-- Frequecy penalty -->
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
                @input="
                  () => {
                    chatParams.frequecyPenaty =
                      chatParams.frequecyPenaty >= 2
                        ? 2
                        : chatParams.frequecyPenaty;
                    chatParams.frequecyPenaty =
                      chatParams.frequecyPenaty <= 0
                        ? 0
                        : chatParams.frequecyPenaty;
                  }
                "
              />
            </div>
            <!-- Presence penalty -->
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
                @input="
                  () => {
                    chatParams.presentPenaty =
                      chatParams.presentPenaty >= 2
                        ? 2
                        : chatParams.presentPenaty;
                    chatParams.presentPenaty =
                      chatParams.presentPenaty <= 0
                        ? 0
                        : chatParams.presentPenaty;
                  }
                "
              />
            </div>
            <!-- stop sequences -->
            <div class="item">
              <el-text class="item-text">Stop sequences: </el-text>
              <el-input v-model="chatParams.stopSequence" class="input" />
            </div>
          </div>
        </el-tab-pane>
        <!-- settings setting -->
        <el-tab-pane>
          <template #label>
            <span class="tabs-label">
              <div class="icon" v-html="SVGS.userSettingsIcon"></div>
              <el-text class="text">Settings</el-text>
            </span>
          </template>
          <div class="scroll-bar">
            <!-- render charcters -->
            <div class="item">
              <el-text class="item-text">Max render characters: </el-text>
              <el-slider
                class="slider"
                v-model="chatParams.webRenderStrLen"
                :min="1"
                :max="800"
                :step="1"
              />
              <el-input
                v-model.number="chatParams.webRenderStrLen"
                class="input-slider"
                @input="
                  () => {
                    chatParams.webRenderStrLen =
                      chatParams.webRenderStrLen >= 800
                        ? 800
                        : chatParams.webRenderStrLen;
                    chatParams.webRenderStrLen =
                      chatParams.webRenderStrLen <= 1
                        ? 1
                        : chatParams.webRenderStrLen;
                  }
                "
              />
            </div>
            <!-- default prompt switch -->
            <div class="item">
              <el-text class="item-text">Use proxy: </el-text>
              <el-switch class="c-switch" v-model="chatParams.isUseProxy" />
            </div>
            <div class="item">
              <el-text class="item-text">Proxy URL: </el-text>
              <el-input
                :disabled="!chatParams.isUseProxy"
                :value="JSON.stringify(chatParams.proxyURL)"
                class="input"
              />
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
    <template #footer>
      <div class="dialog-footer">
        <el-button v-if="!isNewChat" class="cancel" @click="onCancleSettings"
          >Cancel</el-button
        >
        <el-button v-if="isNewChat" class="confirm" @click="onStartChat">
          Confirm
        </el-button>
        <el-button v-else class="confirm" @click="onStartChat">
          Save
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script>
import { ref, computed, watch, onMounted } from "vue";
import { useStore } from "vuex";
import { ElMessage } from "element-plus";
import * as SVGS from "../../assets/styles/chat/svgs.js";
import {
  addNewChatAPI,
  getChatParamsAPI,
  setChatParamsAPI,
} from "../../apis/chatAPIs.js";

export default {
  emits: ["onUpdateChatNameList"],
  setup(props, context) {
    // 从store中得到关于chat的状态
    const store = useStore();

    // 控制对话框的属性
    const isOpenSettingDialog = ref(true);

    // 根据store存的chat的chatCid是不是''判断是不是新建对话
    const isNewChat = computed(() => store.state.chat.chatCid == "");
    const chatCid = computed(() => store.state.chat.chatCid);

    // 要被修改的对话的全部参数
    const chatParams = ref({});

    const isUseDefaultPrompt = ref(true);
    const isUseDefaultParams = ref(true);

    // 绕过v-model提示的computed是readonly的行为
    watch(
      () => store.state.chat.isEditChatSettings,
      async (value) => {
        isOpenSettingDialog.value = value;
        if (value) {
          // 新建对话从SERVER获得参数
          if (isNewChat.value) {
            await handleGetDefaultChatParams();
          } else {
            // 切换chatCid时候已经更新了store的chatParams,因为没有watch到就在这里用赋值的方式更新
            Object.keys(store.state.chat.chatParams).forEach((key) => {
              chatParams.value[key] = store.state.chat.chatParams[key];
            });
          }
        }
      }
    );

    // TODO: 优化这部分的逻辑
    watch(
      () => store.state.chat.chatParams,
      () => {
        console.log(
          "😡 直接监听object是无效的. 所以更新chatParams的行为放到了isEditChatSettings内"
        );
      }
    );

    /**
     * *************************
     * 初始化时候要获得一次默认的参数
     * *************************
     * */
    onMounted(async () => {
      await handleGetDefaultChatParams();
    });

    /**
     * *************************
     * 从SERVER获得默认的chatParams来更新当前的对话参数.
     * *************************
     * */
    const handleGetDefaultChatParams = async () => {
      var rea = await getChatParamsAPI("");
      if (rea.flag) {
        Object.keys(rea.data).forEach((key) => {
          chatParams.value[key] = rea.data[key];
        });
      }
    };

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
        var rea = await addNewChatAPI(chatParams.value.chatName);
        if (!rea.flag) return false;
        // 🎉 有效的ChatCid, 新建对话成功！ 存入store
        store.commit("SET_NEWCHATCID_STATE", rea.chatCid);
        currentChatCid = rea.chatCid;
        // 新建的对话要高亮
        context.emit("onUpdateChatNameList");
      }

      // 开始设置对话的参数到数据库
      rea = await setChatParamsAPI(currentChatCid, chatParams.value);
      if (!rea.flag) return false;

      store.commit("SET_CHATPARAMS_STATE", chatParams.value);
      return true;
    };

    /**
     * *************************
     * 选择合适的模型
     * *************************
     * */
    const onSelectModel = (item) => {
      chatParams.value.modelName = item.label;
      chatParams.value.maxTokens = item.value;
      chatParams.value.modelType = item.mtype;
    };

    /**
     * *************************
     * 关闭当前的setting窗口
     * *************************
     * */
    const onCancleSettings = async () => {
      //重置全部的isEdit属性
      isOpenSettingDialog.value = false;
      store.commit("SET_EDIT_CHAT_SETTINGS_STATE", false);
    };

    /**
     * *************************
     * 向server发送请求创建对应的对话的channel
     * *************************
     * */
    const onStartChat = async () => {
      if (chatParams.value.chatName == "") {
        ElMessage.error("😡 Chat 的名称不能为空!");
        return;
      }

      await onCancleSettings();

      // 判断是新建还是保存
      var flag = await handleSetChatParams();
      if (!flag) {
        ElMessage.error("Start Chat error!");
        return;
      }
    };

    return {
      isOpenSettingDialog,
      isNewChat,
      SVGS,
      chatParams,
      isUseDefaultPrompt,
      isUseDefaultParams,
      onSelectModel,
      onStartChat,
      onCancleSettings,
    };
  },
};
</script>
