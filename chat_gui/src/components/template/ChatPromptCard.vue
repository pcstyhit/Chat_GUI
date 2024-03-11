<template>
  <div class="container">
    <div class="prompt-settings">
      <!-- 基本的信息 -->
      <div class="prompt-item">
        <div class="prompt-title">
          <el-text>Model Type:</el-text>
        </div>
        <div class="prompt-element">
          <el-select v-model="model">
            <el-option
              v-for="item in modelTypes"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </div>
      </div>
      <div class="prompt-item">
        <div class="prompt-title">
          <el-text>Chat Name:</el-text>
        </div>
        <div class="prompt-element">
          <el-input v-model="chatName" />
        </div>
      </div>
      <!-- Prompt内容 -->
      <div style="width: 100%; border: 1px solid rgb(128, 128, 128)"></div>
      <div class="prompt-item">
        <div class="prompt-title">
          <el-text>System Content:</el-text>
        </div>
        <div class="prompt-element">
          <el-input type="textarea" v-model="systemContent" />
        </div>
      </div>
      <div style="width: 100%; margin-top: 20px"></div>
      <div class="prompt-item">
        <div class="prompt-title">
          <el-text>User Content:</el-text>
        </div>
        <div class="prompt-element">
          <el-input type="textarea" v-model="userContent" />
        </div>
      </div>
      <div style="width: 100%; margin-top: 20px"></div>
      <div class="prompt-item">
        <div class="prompt-title">
          <el-text>Assistant Content:</el-text>
        </div>
        <div class="prompt-element">
          <el-input type="textarea" v-model="assistantContent" />
        </div>
      </div>
      <div style="width: 100%; margin-top: 20px"></div>
      <div class="prompt-item">
        <div class="prompt-title" :style="{ width: '60%' }">
          <el-button @click="loadPromptFile" :style="{ width: '80%' }">
            <el-icon><FolderOpened /></el-icon>Load file</el-button
          >
        </div>
        <div
          class="prompt-element"
          :style="{
            width: '40%',
            display: 'flex',
            'justify-content': 'flex-end',
          }"
        >
          <el-checkbox
            v-model="useDefaultPromptData"
            @change="changePromptByFile"
            >Use Prompt Data</el-checkbox
          >
        </div>
      </div>
      <div style="width: 100%; border: 1px solid rgb(167, 167, 167)"></div>
      <!-- 模型的参数 -->
      <div class="prompt-item">
        <div class="prompt-title-2">
          <el-text>Passed Message(0~20):</el-text>
        </div>
        <div class="prompt-element-2">
          <el-input v-model="passedMsg" />
        </div>
      </div>
      <div class="prompt-item">
        <div class="prompt-title-2">
          <el-text>Max Response(0~8192):</el-text>
        </div>
        <div class="prompt-element-2">
          <el-input v-model="maxResponse" />
        </div>
      </div>

      <div class="prompt-item">
        <div class="prompt-title-2">
          <el-text>Temperature(0~1):</el-text>
        </div>
        <div class="prompt-element-2">
          <el-input v-model="temperature" />
        </div>
      </div>
      <div class="prompt-item">
        <div class="prompt-title-2">
          <el-text>Top P(0~1):</el-text>
        </div>
        <div class="prompt-element-2">
          <el-input v-model="topP" />
        </div>
      </div>
      <div class="prompt-item">
        <div class="prompt-title-2">
          <el-text>Frequecy penalty(0~2):</el-text>
        </div>
        <div class="prompt-element-2">
          <el-input v-model="frequecyPenaty" />
        </div>
      </div>
      <div class="prompt-item">
        <div class="prompt-title-2">
          <el-text>Presence penalty(0~2):</el-text>
        </div>
        <div class="prompt-element-2">
          <el-input v-model="presentPenaty" />
        </div>
      </div>
      <div class="prompt-item">
        <div class="prompt-title">
          <el-text>Stop sequences:</el-text>
        </div>
        <div class="prompt-element">
          <el-input type="textarea" v-model="stopSequence" />
        </div>
      </div>
      <div style="width: 100%; margin-top: 20px"></div>
      <div style="width: 100%; border: 1px solid rgb(167, 167, 167)"></div>
      <div
        class="prompt-element"
        :style="{
          width: '100%',
          display: 'flex',
          'justify-content': 'flex-end',
        }"
      >
        <el-checkbox v-model="useDefault" @change="customPrompt"
          >Use Default Prompt</el-checkbox
        >
      </div>
      <div class="prompt-item">
        <el-button
          @click="startChat"
          :style="{ width: '90%', 'margin-left': '5%' }"
          ><el-icon><Promotion /></el-icon>Start Chat</el-button
        >
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { ElMessage } from "element-plus";
export default {
  setup() {
    const model = ref("gpt4-32k");
    const modelTypes = ref([
      { value: 32 * 1024, label: "gpt4-32k" },
      { value: 16 * 1024, label: "gpt4" },
      { value: 32 * 1024, label: "gpt3.5-32k-turbo" },
    ]);
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
    onMounted(() => {
      // 使用默认的prompt
      if (useDefault.value) {
        useDefaultPrompt();
      }
    });

    const padZero = (value) => {
      return String(value).padStart(2, "0");
    };

    const useDefaultPrompt = () => {
      const now = new Date();
      useDefaultPromptData.value = true;
      changePromptByFile();
      chatName.value = `${now.getFullYear()}-${padZero(
        now.getMonth() + 1
      )}-${padZero(now.getDate())}-${padZero(now.getHours())}-${padZero(
        now.getMinutes()
      )}-${padZero(now.getSeconds())}`;
      maxResponse.value = 800;
      temperature.value = 0.7;
      topP.value = 0.95;
      frequecyPenaty.value = 0;
      presentPenaty.value = 0;
      stopSequence.value = "";
      passedMsg.value = 10;
    };

    const changePromptByFile = () => {
      if (useDefaultPromptData.value) {
        systemContent.value =
          "You are Chat GPT-4 a large language model of OpenAI.";
      } else {
        systemContent.value = "";
        userContent.value = "";
        assistantContent.value = "";
      }
    };

    const customPrompt = () => {
      // 使用默认的prompt
      if (useDefault.value) {
        useDefaultPrompt();
      } else {
        chatName.value = "";
      }
    };

    const startChat = async () => {
      const regex = /^[a-zA-Z0-9+-_]+$/;
      if (!regex.test(chatName.value)) {
        ElMessage.error("必须给对话起合适的名称(字母/数字/下划线/+-符号组成)");
      }
    };

    const loadPromptFile = () => {
      ElMessage.info("敬请期待！");
    };

    return {
      model,
      modelTypes,
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
      changePromptByFile,
      customPrompt,
      startChat,
      loadPromptFile,
    };
  },
};
</script>

<style scoped>
.container {
  display: flex;
  width: 100%;
  height: 100%;
}

.prompt-settings {
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
