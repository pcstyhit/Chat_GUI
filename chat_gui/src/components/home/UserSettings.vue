<template>
  <!-- overlay-dialog -->
  <el-dialog
    class="home-user-settings-overlay"
    v-model="isShowUserSettings"
    align-center
    append-to-body
    @close="onCloseUserSettingOverlay"
  >
    <!-- header -->
    <template #header>
      <div class="header">
        <el-text :tag="'b'" class="label">User Settings</el-text>
      </div>
      <el-divider class="divider" />
    </template>
    <!-- profile settings -->
    <div class="content">
      <el-tabs tab-position="left" class="tabs">
        <el-tab-pane>
          <template #label>
            <span class="tabs-label">
              <div class="icon" v-html="SVGS.userProfileIcon"></div>
              <el-text class="text">Profile</el-text>
            </span>
          </template>
          <div class="scroll-bar">
            <div class="profile">
              <div class="avatar">
                <img :src="avatarImg" />
                <button class="upload-button" @click="onUploadAvatar">
                  Upload avatar
                </button>
              </div>
              <div class="avatar-info">
                <el-text class="text">User name: {{ userName }}</el-text>
                <el-text class="text">Uid: {{ userId }}</el-text>
                <el-button class="logout" @click="onLogout"> Logout </el-button>
              </div>
            </div>
          </div>
        </el-tab-pane>
        <!-- chat setting -->
        <el-tab-pane>
          <template #label>
            <span class="tabs-label">
              <div class="icon" v-html="SVGS.userChatParamsIcon"></div>
              <el-text class="text">Chat</el-text>
            </span>
          </template>
          <el-scrollbar class="scroll-bar">
            <div class="item">
              <div class="item-label">
                <div class="tips" v-html="SVGS.tipsIcon" />
                <el-text class="text">Model: </el-text>
              </div>
              <el-select v-model="chatParams.modelName" class="item-select">
                <el-option
                  v-for="item in chatModelList"
                  :key="item.modelName"
                  :label="item.modelName"
                  :value="item.modelName"
                  @click="onSelectModel(chatParams, item)"
                />
              </el-select>
            </div>
            <div class="item-textarea">
              <div class="item-label">
                <div class="tips" v-html="SVGS.tipsIcon" />
                <el-text class="text">System prompt: </el-text>
              </div>
              <el-input
                class="input"
                type="textarea"
                v-model="chatSysPrompt"
                @input="updateChatPrompts"
              />
            </div>
            <div class="item-textarea">
              <div class="item-label">
                <div class="tips" v-html="SVGS.tipsIcon" />
                <el-text class="text">User prompt: </el-text>
              </div>
              <el-input
                class="input"
                type="textarea"
                v-model="chatUserPrompt"
                @input="updateChatPrompts"
              />
            </div>
            <div class="item-textarea">
              <div class="item-label">
                <div class="tips" v-html="SVGS.tipsIcon" />
                <el-text class="text">Assist prompt: </el-text>
              </div>
              <el-input
                class="input"
                type="textarea"
                v-model="chatAssPrompt"
                @input="updateChatPrompts"
              />
            </div>
            <div class="item">
              <div class="item-label">
                <div class="tips" v-html="SVGS.tipsIcon" />
                <el-text class="text">Passed Message: </el-text>
              </div>
              <el-input
                class="input-middle"
                v-model.number="chatParams.passedMsgLen"
                @input="validateRange('passedMsgLen', 1, 20)"
              />
              <el-text class="c-input-tips">value range: 1~20</el-text>
            </div>
            <div class="item">
              <div class="item-label">
                <div class="tips" v-html="SVGS.tipsIcon" />
                <el-text class="text">Max Response: </el-text>
              </div>
              <el-input
                class="input-middle"
                v-model="chatParams.maxResponseTokens"
                @input="validateRange('maxResponseTokens', 1, 8192)"
              />
              <el-text class="c-input-tips">value range: 1~8192</el-text>
            </div>
            <div class="item">
              <div class="item-label">
                <div class="tips" v-html="SVGS.tipsIcon" />
                <el-text class="text">Temperature: </el-text>
              </div>
              <el-input
                class="input-middle"
                v-model="chatParams.temperature"
                @input="validateRange('temperature', 0.1, 1)"
              />
              <el-text class="c-input-tips">value range: 0.1~1</el-text>
            </div>
            <div class="item">
              <div class="item-label">
                <div class="tips" v-html="SVGS.tipsIcon" />
                <el-text class="text">Top P: </el-text>
              </div>
              <el-input
                class="input-middle"
                v-model="chatParams.topP"
                @input="validateRange('topP', 0.1, 1)"
              />
              <el-text class="c-input-tips">value range: 0.1~1</el-text>
            </div>
            <div class="item">
              <div class="item-label">
                <div class="tips" v-html="SVGS.tipsIcon" />
                <el-text class="text">Frequecy penalty: </el-text>
              </div>
              <el-input
                class="input-middle"
                v-model="chatParams.frequecyPenaty"
                @input="validateRange('frequecyPenaty', 0, 2)"
              />
              <el-text class="c-input-tips">value range: 0~2</el-text>
            </div>
            <div class="item">
              <div class="item-label">
                <div class="tips" v-html="SVGS.tipsIcon" />
                <el-text class="text">Presence penalty: </el-text>
              </div>
              <el-input
                class="input-middle"
                v-model="chatParams.presentPenaty"
                @input="validateRange('presentPenaty', 0, 2)"
              />
              <el-text class="c-input-tips">value range: 0~2</el-text>
            </div>
            <div class="item">
              <div class="item-label">
                <div class="tips" v-html="SVGS.tipsIcon" />
                <el-text class="text">Stop sequences: </el-text>
              </div>
              <el-input
                class="input-fit"
                v-model="chatStopSequence"
                @input="validStopSequence(chatParams, chatStopSequence)"
              />
            </div>
          </el-scrollbar>
        </el-tab-pane>
        <!-- current user setting -->
        <el-tab-pane>
          <template #label>
            <span class="tabs-label">
              <div class="icon" v-html="SVGS.userSettingsIcon"></div>
              <el-text class="text">Settings</el-text>
            </span>
          </template>
          <div class="scroll-bar">
            <div class="item">
              <div class="item-label">
                <div class="tips" v-html="SVGS.tipsIcon" />
                <el-text class="text">Markdown render: </el-text>
              </div>
              <el-slider
                v-model="userSettings.wenMarkDownRenderChars"
                class="slider"
                :min="1"
                :max="20"
              />
              <el-input
                class="input-slider"
                v-model="userSettings.wenMarkDownRenderChars"
              />
            </div>
            <div class="item">
              <div class="item-label">
                <div class="tips" v-html="SVGS.tipsIcon" />
                <el-text class="text">Use proxy: </el-text>
              </div>
              <el-switch
                class="c-switch"
                v-model="userSettings.isUseProxy"
                @change="onChangeProxy"
              />
            </div>
            <div class="item">
              <div class="item-label">
                <div class="tips" v-html="SVGS.tipsIcon" />
                <el-text class="text">Proxy URL: </el-text>
              </div>
              <el-input class="input-fit" v-model="userSettings.proxyURL" />
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
    <template #footer>
      <div class="dialog-footer">
        <el-button class="cancel" @click="onCloseUserSettingOverlay"
          >Cancel</el-button
        >
        <el-button class="confirm" @click="onConfirmSetting">
          Confirm
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { computed, watch, ref } from "vue";
import { useStore } from "vuex";
import * as SVGS from "../../assets/styles/home/svgs.js";
import { showMessage } from "../../helper/customMessage.js";
import { confirmUserSettings } from "../../helper/user/common.js";
import {
  onSelectModel,
  getPromptByRole,
  handleChatPrompts,
  validStopSequence,
} from "../../helper/chat/settings.js";

const store = useStore();
const isShowUserSettings = ref(false);
const userName = computed(() => store.state.user.name);
const userId = computed(() => store.state.user.uid);
const avatarImg = computed(() => store.state.user.avatar);

const chatModelList = computed(() => store.state.chat.modelList);
const chatParams = ref({});
const chatSysPrompt = ref("");
const chatUserPrompt = ref("");
const chatAssPrompt = ref("");
const chatStopSequence = ref("");

const userSettings = ref({});

watch(
  () => store.state.user.isShowUserSettings,
  async (value) => {
    isShowUserSettings.value = value;
    if (value) {
      Object.keys(store.state.user.userDefaultChatParams).forEach((key) => {
        chatParams.value[key] = store.state.user.userDefaultChatParams[key];
      });
      Object.keys(store.state.user.userDefaultSettings).forEach((key) => {
        userSettings.value[key] = store.state.user.userDefaultSettings[key];
      });
      chatSysPrompt.value = getPromptByRole(chatParams.value, "system");
      chatUserPrompt.value = getPromptByRole(chatParams.value, "user");
      chatAssPrompt.value = getPromptByRole(chatParams.value, "assistant");
      chatStopSequence.value = chatParams.value.stopSequence.join(";");
    }
  }
);

/** validateRange 限制参数的范围 这个内容可以不用抽出去 */
const validateRange = (param, min, max) => {
  chatParams.value[param] = Math.max(
    min,
    Math.min(max, chatParams.value[param])
  );
};

/** updateChatPrompts 动态更新提示词的内容 */
const updateChatPrompts = () => {
  handleChatPrompts(
    chatParams.value,
    chatSysPrompt.value,
    chatUserPrompt.value,
    chatAssPrompt.value
  );
};

/** onUploadAvatar 更新头像 */
const onUploadAvatar = () => {
  showMessage("info", "没做这个功能 🚀");
};

/** onChangeProxy 开关代理时候会更新代理的互斥条件 */
const onChangeProxy = () => {
  if (userSettings.value.isUseProxy == false) userSettings.value.proxyURL = "";
};

/** onLogout 点击logout触发的函数 */
const onLogout = () => {
  showMessage("info", "就不让你logout 🤣");
};

/** onConfirmSetting 点击保存用户的设置 */
const onConfirmSetting = async () => {
  var flag = await confirmUserSettings(chatParams.value, userSettings.value);
  if (flag) showMessage("success", "设置用户的参数成功! 😀");
  onCloseUserSettingOverlay();
};

/** onCloseUserSettingOverlay 关掉用户设置的overlay */
const onCloseUserSettingOverlay = () => {
  store.commit("SET_USER_SHOWSETTINGUI", false);
};
</script>

<style lang="scss">
.content {
  .el-tabs__active-bar {
    background-color: #7d7d7d !important;
  }
}
</style>
