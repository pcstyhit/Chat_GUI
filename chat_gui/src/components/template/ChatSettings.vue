<template>
  <!-- overlay-dialog -->
  <el-dialog
    class="chat-settings-overlay"
    v-model="centerDialogVisible"
    align-center
    append-to-body
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
            <div class="item">
              <el-text class="item-text">Chat name: </el-text>
              <el-input class="input" />
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
            <el-divider class="divider" />
            <div class="item">
              <el-text class="item-text">Use default settings: </el-text>
              <el-switch class="c-switch" v-model="isAutoToBottom" />
            </div>
            <div class="item">
              <el-text class="item-text">System: </el-text>
              <el-input class="input" />
            </div>
            <div class="item">
              <el-text class="item-text">Assist: </el-text>
              <el-input class="input" />
            </div>
            <div class="item">
              <el-text class="item-text">User: </el-text>
              <el-input class="input" />
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
              <el-text class="item-text">Use default settings: </el-text>
              <el-switch class="c-switch" v-model="isAutoToBottom" />
            </div>
            <div class="item">
              <el-text class="item-text">Passed Message(1~20): </el-text>
              <el-slider class="slider" v-model="value3" :min="1" :max="20" />
              <el-input class="input-slider" />
            </div>
            <div class="item">
              <el-text class="item-text">Max Response(1~8192): </el-text>
              <el-slider class="slider" v-model="value3" :min="1" :max="8192" />
              <el-input class="input-slider" />
            </div>
            <div class="item">
              <el-text class="item-text">Temperature(0.1~1): </el-text>
              <el-slider
                class="slider"
                v-model="value3"
                :min="0.01"
                :max="1"
                :step="0.01"
              />
              <el-input class="input-slider" />
            </div>
            <div class="item">
              <el-text class="item-text">Top P(0.1~1): </el-text>
              <el-slider
                class="slider"
                v-model="value3"
                :min="0.01"
                :max="1"
                :step="0.01"
              />
              <el-input class="input-slider" />
            </div>
            <div class="item">
              <el-text class="item-text">Frequecy penalty(0~2): </el-text>
              <el-slider
                class="slider"
                v-model="value3"
                :min="0"
                :max="2"
                :step="0.01"
              />
              <el-input class="input-slider" />
            </div>
            <div class="item">
              <el-text class="item-text">Presence penalty(0~2): </el-text>
              <el-slider
                class="slider"
                v-model="value3"
                :min="0"
                :max="2"
                :step="0.01"
              />
              <el-input class="input-slider" />
            </div>
            <div class="item">
              <el-text class="item-text">Stop sequences: </el-text>
              <el-input class="input" />
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
    <template #footer>
      <div class="dialog-footer">
        <el-button class="cancle" @click="centerDialogVisible = false"
          >Cancel</el-button
        >
        <el-button class="confirm" @click="centerDialogVisible = false">
          Confirm
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script>
import { ref } from "vue";
import * as SVGS from "../../assets/styles/chat/svgs.js";
export default {
  setup() {
    const centerDialogVisible = ref(true);

    const modelList = ref([
      { label: "GPT-4o", value: 128 },
      { label: "GPT-4", value: 32 },
    ]);
    const model = modelList.value[0];

    const chatName = ref("");
    const systemContent = ref("");
    const userContent = ref("");
    const assistantContent = ref("");
    const useDefaultPromptData = ref(true);
    const useDefault = ref(true);
    const passedMsg = ref(10);
    const maxResponse = ref(800);
    const temperature = ref(0.7);
    const topP = ref(0.95);
    const frequecyPenaty = ref(0);
    const presentPenaty = ref(0);
    const stopSequence = ref("");

    const onSelectModel = (val) => {
      model.value = val;
    };

    return {
      SVGS,
      centerDialogVisible,
      modelList,
      model,
      chatName,
      systemContent,
      userContent,
      assistantContent,
      useDefault,
      useDefaultPromptData,
      maxResponse,
      temperature,
      topP,
      frequecyPenaty,
      presentPenaty,
      stopSequence,
      passedMsg,
      onSelectModel,
    };
  },
};
</script>

<style lang="scss">
.content {
  .el-tabs__active-bar {
    background-color: #7d7d7d !important;
  }
}
</style>
