<template>
  <div class="chat-roles-card">
    <div class="container">
      <div class="role-group">
        <div
          class="role-card"
          @click="
            () => {
              console.log(`Hello world 1`);
            }
          "
        >
          <el-tooltip
            content="Upload chat history"
            placement="bottom"
            :show-after="500"
          >
            <div class="tips" v-html="SVGS.roleTipsSettings"></div>
          </el-tooltip>

          <div class="icon" v-html="SVGS.roleUploadIcon"></div>
          <el-text class="label">Upload History</el-text>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as SVGS from "../../assets/styles/chat/svgs.js";
export default {
  setup() {
    return {
      SVGS,
    };
  },
};
</script>
