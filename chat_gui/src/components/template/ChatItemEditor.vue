<template>
  <!-- overlay-dialog -->
  <el-dialog
    class="chat-item-editor-overlay"
    v-model="centerDialogVisible"
    align-center
    append-to-body
    :close-on-click-modal="false"
  >
    <!-- header -->
    <template #header>
      <div class="header">
        <el-text :tag="'b'" class="label">Edit chat item</el-text>
      </div>
      <el-divider class="divider" />
    </template>
    <!-- settings tab -->
    <div class="content">
      <el-input
        class="editor"
        v-model="value"
        type="textarea"
        :autosize="{ minRows: 1, maxRows: 8 }"
      >
      </el-input>
    </div>
    <template #footer>
      <div class="dialog-footer">
        <el-button class="cancel" @click="centerDialogVisible = false"
          >Cancel</el-button
        >
        <el-button class="save" @click="centerDialogVisible = false">
          Save
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
    const value = ref("");
    return {
      SVGS,
      centerDialogVisible,
      value,
    };
  },
};
</script>

<style lang="scss" scoped>
.editor :deep(.el-textarea__inner) {
  height: 100% !important;
  border: none !important; /* Remove border */
  outline: none; /* Remove focus outline */
  box-shadow: none; /* Remove any box shadow */
  background-color: #f4f4f4;
  resize: none !important;
}
</style>
