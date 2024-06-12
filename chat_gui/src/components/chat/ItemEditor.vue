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
        v-model="beEditedChatItem.content"
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
        <el-button class="save" @click="handleSaveEditItem"> Save </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script>
import { ref, watch } from "vue";
import { useStore } from "vuex";
import * as SVGS from "../../assets/styles/chat/svgs.js";
import { ElMessageBox, ElMessage } from "element-plus";
import { editChatItemAPI } from "../../apis/chatAPIs";
export default {
  props: {
    isShowItemEditor: {
      type: Boolean,
      default: false,
    },
    editChatItemObj: {
      type: Object,
      default: () => ({}),
    },
  },
  emits: ["update:isShowItemEditor", "update:editChatItemObj"],
  setup(props, { emit }) {
    const store = useStore();

    const isShowDialog = ref(props.isShowItemEditor);
    const beEditedChatItem = ref(props.editChatItemObj);

    // 双向绑定数据
    watch(
      () => props.isShowItemEditor,
      (newValue) => {
        isShowDialog.value = newValue;
      }
    );

    watch(isShowDialog, (newValue) => {
      emit("update:isShowItemEditor", newValue);
    });

    watch(
      () => props.editChatItemObj,
      (newValue) => {
        beEditedChatItem.value = newValue;
      }
    );

    /** TODO 😡 需要看看为什么子组件和父组件没有在watch这个变量时候 没有同步 */
    watch(beEditedChatItem, (newValue) => {
      emit("update:editChatItemObj", newValue);
    });

    /** 因为beEditedChatItem和父组件存在双向绑定，只要通知父组件执行值的更新就可以了 */
    const handleSaveEditItem = async () => {
      var flag = false;
      await ElMessageBox.confirm(
        "保存对这个对话的内容的修改吗(无法撤销)?",
        "Warning",
        {
          confirmButtonText: "Yes",
          cancelButtonText: "Cancel",
          type: "warning",
        }
      )
        .then(() => {
          flag = true;
        })
        .catch(() => {
          flag = false;
        });
      if (flag) {
        var rea = await editChatItemAPI(
          beEditedChatItem.value.chatIid,
          beEditedChatItem.value.content
        );
        if (rea.flag == true) {
          ElMessage.success("修改成功");
          store.commit("CHANGE_SPEC_CHATITEM_HISTORY", beEditedChatItem.value);
        } else {
          ElMessage.error("修改失败");
        }
      }
      isShowDialog.value = false;
    };
    return {
      SVGS,
      isShowDialog,
      beEditedChatItem,
      handleSaveEditItem,
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
