<template>
  <!-- overlay-dialog -->
  <el-dialog
    class="chat-item-editor-overlay"
    v-model="isShowDialog"
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
        v-model="inputText"
        type="textarea"
        :autosize="{ minRows: 1, maxRows: 8 }"
      >
      </el-input>
    </div>
    <template #footer>
      <div class="dialog-footer">
        <el-button class="cancel" @click="isShowDialog = false"
          >Cancel</el-button
        >
        <el-button class="save" @click="isShowDialog = false"> Save </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script>
import { ref, watch } from "vue";
import * as SVGS from "../../assets/styles/chat/svgs.js";
export default {
  props: {
    isShowItemEditor: {
      type: Boolean,
      default: false,
    },
    editChatValue: {
      type: String,
      default: "",
    },
  },
  emits: ["update:isShowItemEditor", "update:editChatValue"],
  setup(props, { emit }) {
    const isShowDialog = ref(props.isShowItemEditor);
    const inputText = ref(props.editChatValue);

    // 双向绑定数据
    watch(
      () => props.isShowItemEditor,
      (newValue) => {
        console.log(props.isShowItemEditor);
        isShowDialog.value = newValue;
      }
    );

    watch(isShowDialog, (newValue) => {
      console.log(props.isShowItemEditor);
      emit("update:isShowItemEditor", newValue);
    });

    watch(
      () => props.editChatValue,
      (newValue) => {
        console.log(props.editChatValue);
        inputText.value = newValue;
      }
    );

    watch(inputText, (newValue) => {
      emit("update:editChatValue", newValue);
    });
    return {
      SVGS,
      isShowDialog,
      inputText,
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
