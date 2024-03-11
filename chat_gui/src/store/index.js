import { createStore } from "vuex";

const state = {
  user: "",
  basicAuth: "",
  loginState: false,
  tokens: 0, // 根据上下文记录当前对话一次要消耗的tokens数量
  chatWsid: "", // 流对话的websocket的id
  chatCid: "", // 对话过程中的唯一标志，用这个访问数据库
  chatHistory: [], // 响应式存储对话，方便websocket流接收消息
  chatState: false, // 是否处于对话状态的开过量，控制对话发送功能
};

const mutations = {
  SET_USER_NAME(state, data) {
    state.user = data;
  },
  SET_BASIC_AUTH(state, data) {
    state.basicAuth = data;
  },
  SET_LOGIN_STATE(state, data) {
    state.loginState = data;
  },
  SET_CHATWSID_STATE(state, data) {
    state.chatWsid = data;
  },
  SET_CHATHISTORY_STATE(state, data) {
    state.chatHistory = data;
  },
  PUSH_CHATHISTORY_STATE(state, data) {
    state.chatHistory.push(data);
  },
  CHANGE_CHATHISTORY_STATE(state, data, sit) {
    state.chatHistory[sit] = data;
  },
  SET_CHATSTATE_STATE(state, data) {
    state.chatState = data;
  },
  SET_TOKENS_STATE(state, data) {
    state.tokens = data;
  },
  SET_CHATCID_STATE(state, data) {
    state.chatCid = data;
  },
  DELETE_CHATHISTORY_ITEM(state, index) {
    state.chatHistory.splice(index, 1);
  },
  EDIT_CHATHISTORY_ITEM(state, data) {
    state.chatHistory[data.index].text = data.data;
  },
};

export default createStore({
  state,
  mutations,
});
