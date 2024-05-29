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
  SET_CHATCID_STATE(state, data) {
    state.chat.setChatCid(data);
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
};

export default createStore({
  state,
  mutations,
});
