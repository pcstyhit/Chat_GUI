<template>
  <!-- overlay-dialog -->
  <el-dialog
    class="home-user-settings-overlay"
    v-model="centerDialogVisible"
    align-center
    append-to-body
    :close-on-click-modal="false"
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
            <div class="item">
              <div class="item-label">
                <el-text class="text">Used API tokens: </el-text>
              </div>
              <el-input class="input-middle" />
            </div>
            <div class="item">
              <el-button> Logout </el-button>
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
              <el-select v-model="model" class="item-select">
                <el-option
                  v-for="item in modelList"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                  @change="onSelectModel(item)"
                />
              </el-select>
            </div>
            <div class="item-textarea">
              <div class="item-label">
                <div class="tips" v-html="SVGS.tipsIcon" />
                <el-text class="text">System prompt: </el-text>
              </div>
              <el-input class="input" type="textarea" />
            </div>
            <div class="item-textarea">
              <div class="item-label">
                <div class="tips" v-html="SVGS.tipsIcon" />
                <el-text class="text">Assist prompt: </el-text>
              </div>
              <el-input class="input" type="textarea" />
            </div>
            <div class="item-textarea">
              <div class="item-label">
                <div class="tips" v-html="SVGS.tipsIcon" />
                <el-text class="text">User prompt: </el-text>
              </div>
              <el-input class="input" type="textarea" />
            </div>
            <div class="item">
              <div class="item-label">
                <div class="tips" v-html="SVGS.tipsIcon" />
                <el-text class="text">Passed Message: </el-text>
              </div>
              <el-input class="input-middle" />
              <el-text class="c-input-tips">value range: 1~20</el-text>
            </div>
            <div class="item">
              <div class="item-label">
                <div class="tips" v-html="SVGS.tipsIcon" />
                <el-text class="text">Max Response: </el-text>
              </div>
              <el-input class="input-middle" />
              <el-text class="c-input-tips">value range: 1~8192</el-text>
            </div>
            <div class="item">
              <div class="item-label">
                <div class="tips" v-html="SVGS.tipsIcon" />
                <el-text class="text">Temperature: </el-text>
              </div>
              <el-input class="input-middle" />
              <el-text class="c-input-tips">value range: 0.1~1</el-text>
            </div>
            <div class="item">
              <div class="item-label">
                <div class="tips" v-html="SVGS.tipsIcon" />
                <el-text class="text">Top P: </el-text>
              </div>
              <el-input class="input-middle" />
              <el-text class="c-input-tips">value range: 0.1~1</el-text>
            </div>
            <div class="item">
              <div class="item-label">
                <div class="tips" v-html="SVGS.tipsIcon" />
                <el-text class="text">Frequecy penalty: </el-text>
              </div>
              <el-input class="input-middle" />
              <el-text class="c-input-tips">value range: 0~2</el-text>
            </div>
            <div class="item">
              <div class="item-label">
                <div class="tips" v-html="SVGS.tipsIcon" />
                <el-text class="text">Presence penalty: </el-text>
              </div>
              <el-input class="input-middle" />
              <el-text class="c-input-tips">value range: 0~2</el-text>
            </div>
            <div class="item">
              <div class="item-label">
                <div class="tips" v-html="SVGS.tipsIcon" />
                <el-text class="text">Stop sequences: </el-text>
              </div>
              <el-input class="input-fit" />
            </div>
          </el-scrollbar>
        </el-tab-pane>
        <!-- parameter setting -->
        <el-tab-pane>
          <template #label>
            <span class="tabs-label">
              <div class="icon" v-html="SVGS.userSpeechIcon"></div>
              <el-text class="text">Speech</el-text>
            </span>
          </template>
          <div class="scroll-bar"></div>
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
              <el-slider class="slider" v-model="value3" :min="1" :max="400" />
              <el-input class="input-slider" />
            </div>
            <div class="item">
              <div class="item-label">
                <div class="tips" v-html="SVGS.tipsIcon" />
                <el-text class="text">Use proxy: </el-text>
              </div>
              <el-switch class="c-switch" />
            </div>
            <div class="item">
              <div class="item-label">
                <div class="tips" v-html="SVGS.tipsIcon" />
                <el-text class="text">Proxy URL: </el-text>
              </div>
              <el-input class="input-fit" />
            </div>
            <div class="item">
              <div class="item-label">
                <el-text class="text">Delete All Chat: </el-text>
              </div>
              <el-button> Delete all </el-button>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
    <template #footer>
      <div class="dialog-footer">
        <el-button class="cancel" @click="centerDialogVisible = false"
          >Cancel</el-button
        >
        <el-button class="confirm" @click="centerDialogVisible = false">
          Confirm
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref } from "vue";
import * as SVGS from "../../assets/styles/home/svgs.js";
const centerDialogVisible = ref(true);

const modelList = ref([
  { label: "GPT-4o", value: 128 },
  { label: "GPT-4", value: 32 },
]);
const model = modelList.value[0];
</script>

<style lang="scss">
.content {
  .el-tabs__active-bar {
    background-color: #7d7d7d !important;
  }
}
</style>
