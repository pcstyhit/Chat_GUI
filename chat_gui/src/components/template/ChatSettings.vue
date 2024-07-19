<template>
  <!-- overlay-dialog -->
  <el-drawer class="chat-settings-drawer" v-model="centerDialogVisible">
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
          <el-input class="input" />
        </div>
        <div class="item">
          <el-text class="item-text">Select model: </el-text>
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
        <el-divider class="divider" />
        <!-- chat prompts -->
        <div class="title">
          <div class="icon" v-html="chatSetttingsTipsIcon"></div>
          <el-text class="label">Edit chat prompts</el-text>
        </div>
        <div class="item">
          <el-text class="item-text">Use default settings: </el-text>
          <el-switch class="c-switch" v-model="isAutoToBottom" />
        </div>
        <div class="item-textarea">
          <el-text class="item-text">System: </el-text>
          <el-input class="input" type="textarea" v-model="a" />
        </div>
        <div class="item-textarea">
          <el-text class="item-text">Assist: </el-text>
          <el-input class="input" type="textarea" v-model="b" />
        </div>
        <div class="item-textarea">
          <el-text class="item-text">User: </el-text>
          <el-input class="input" type="textarea" v-model="c" />
        </div>
        <el-divider class="divider" />
        <!-- chat parameters -->
        <div class="title">
          <el-text class="label">Edit chat parameters.</el-text>
        </div>
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
      </el-scrollbar>
      <el-divider class="divider" />
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
  </el-drawer>
</template>

<script setup>
import { ref } from "vue";
import { chatSetttingsTipsIcon } from "../../assets/styles/chat/svgs.js";
const centerDialogVisible = ref(true);

const modelList = ref([
  { label: "GPT-4o", value: 128 },
  { label: "GPT-4", value: 32 },
]);
const model = modelList.value[0];

const onSelectModel = (val) => {
  model.value = val;
};

const a = ref("");
const b = ref("");
const c = ref("");
</script>
