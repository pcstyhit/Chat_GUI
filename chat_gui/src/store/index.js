import { createStore } from "vuex";
import { ChatState } from "./chat";
import { UserState } from "./user";

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
    console.log("hello");
    state.user.setBasicAuth(data);
  },

  /** @param {state} state */
  SET_LOGIN_STATE(state, data) {
    state.user.setLoginState(data);
  },

  /** @param {state} state */
  SET_CHATWSID_STATE(state, data) {
    state.chat.setChatWsid(data);
  },

  /** @param {state} state */
  SET_CHATHISTORY_STATE(state, data) {
    state.chat.setChatHistory(data);
  },

  /** @param {state} state */
  PUSH_CHATHISTORY_STATE(state, data) {
    state.chat.pushChatHistory(data);
  },

  /** @param {state} state */
  CHANGE_CHATHISTORY_STATE(state, data, sit) {
    state.chat.changeChatHistory(data, sit);
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
  SET_CHATCID_STATE(state, data) {
    state.chat.setChatCid(data);
  },

  /** @param {state} state */
  DELETE_CHATHISTORY_ITEM(state, index) {
    state.chat.deleteChatHistoryItem(index);
  },

  /** @param {state} state */
  EDIT_CHATHISTORY_ITEM(state, data) {
    state.chat.editChatHistoryItem(data);
  },

  /** @param {state} state */
  SET_EDIT_CHAT_SETTINGS_STATE(state, data) {
    state.chat.setEditChatSettings(data);
  },
};

export default createStore({
  state,
  mutations,
});
