import { createStore } from "vuex";
import { ChatState } from "./chat";
import { UserState } from "./user";

import { getSpecChatHistoryAPI, getChatParamsAPI } from "../apis/chat.js";

const state = {
  user: { ...UserState },
  chat: { ...ChatState },
};

const mutations = {
  /** @param {state} state */
  SET_USER_NAME(state, data) {
    state.user.setUserName(data);
  },

  /** @param {state} state */
  SET_BASIC_AUTH(state, data) {
    state.user.setBasicAuth(data);
  },

  /** @param {state} state */
  SET_LOGIN_STATE(state, data) {
    state.user.setLoginState(data);
  },

  /** @param {state} state */
  SET_CHATLIST_STATE(state, data) {
    state.user.sethChat(data);
  },

  /** @param {state} state */
  PUSH_CHATLIST_STATE(state, data) {
    state.user.pushChat(data);
  },

  /** @param {state} state */
  DELETE_CHATLIST_STATE(state, data) {
    state.user.deleteChatByChatCid(data);
  },

  /** @param {state} state */
  SET_CHATHISTORY_STATE(state, data) {
    state.chat.resetChatHistory(data);
  },

  /** @param {state} state */
  PUSH_CHATHISTORY_STATE(state, data) {
    state.chat.pushChatHistory(data);
  },

  /** @param {state} state */
  CHANGE_SPEC_CHATITEM_HISTORY(state, chatItemObj) {
    state.chat.changeSpecChatItemHistory(chatItemObj);
  },

  /** @param {state} state */
  SET_ISCHATTING_STATE(state, data) {
    state.chat.setIsChattingState(data);
  },

  /** @param {state} state */
  SET_TOKENS_STATE(state, data) {
    state.chat.setTokens(data);
  },

  /** @param {state} state */
  SET_NEWCHATCID_STATE(state, data) {
    state.chat.setChatCid(data);
    state.chat.chatHistory = [];
  },

  /** @param {state} state */
  async SET_CHATCID_STATE(state, data) {
    state.chat.setChatCid(data);
    state.chat.chatHistory = [];

    // 不为空的chatCid代表切换对话就需要更新对话的参数和历史记录
    var rea = await getChatParamsAPI(data);
    if (rea.flag) state.chat.resetChatParams(rea.data);

    // 如果data是空""就代表进入了新建对话情况,不需要从SERVER加载对话了
    if (data == "") {
      state.chat.tokens = 0;
      state.chat.requestTime = 0;
      return;
    }
    // 更新这个对话的历史记录
    rea = await getSpecChatHistoryAPI(data);
    if (rea.flag) {
      state.chat.resetChatHistory(rea.history);
      // 更新下次要发送的消息的tokens数量
      state.chat.tokens = rea.tokens;
    }
  },

  /** @param {state} state */
  SET_CHATPARAMS_STATE(state, data) {
    state.chat.resetChatParams(data);
  },

  /** @param {state} state */
  DELETE_CHATHISTORY_ITEM(state, chatIid) {
    state.chat.deleteChatHistoryItem(chatIid);
  },

  /** @param {state} state */
  SET_EDIT_CHAT_SETTINGS_STATE(state, data) {
    state.chat.setEditChatSettings(data);
  },

  /** @param {state} state */
  SET_IS_UPDATE_REQUEST_TIME(state, data) {
    state.chat.updateTimeStamp(data);
  },

  /** @param {state} state */
  SET_REGENERATE_CHATHISTORY(state, data) {
    state.chat.reGenerateChatHistory(data);
  },
};

export default createStore({
  state,
  mutations,
});
