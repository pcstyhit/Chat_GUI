/**
 * 表示聊天信息存储的对象。
 */
export const ChatState = {
  /**
   * 当前对话消耗的 tokens 数量。
   * @type {number}
   */
  tokens: 0,

  /**
   * 流对话的 WebSocket ID。
   * @type {string}
   */
  chatWsid: "",

  /**
   * 对话过程中的唯一标志，用于访问数据库。
   * @type {string}
   */
  chatCid: "",

  /**
   * 响应式存储对话历史，方便 WebSocket 流接收消息。
   * @type {Array<Object>}
   */
  chatHistory: [],

  /**
   * 是否处于对话状态的开关，控制对话发送功能。
   * @type {boolean}
   */
  isChatting: false,

  /**
   * 是否处于编辑聊天参数的状态。
   * @type {boolean}
   */
  isEditChatSettings: true,

  /**
   * 设置流对话的 WebSocket ID。
   * @param {string} data - WebSocket ID。
   */
  setChatWsid(data) {
    this.chatWsid = data;
  },

  /**
   * 设置对话历史。
   * @param {Array<Object>} data - 对话历史。
   */
  setChatHistory(data) {
    this.chatHistory = data;
  },

  /**
   * 将新消息添加到对话历史。
   * @param {Object} data - 要添加的消息。
   */
  pushChatHistory(data) {
    this.chatHistory.push(data);
  },

  /**
   * 更改对话历史中的特定消息。
   * @param {Object} data - 新的消息数据。
   * @param {number} index - 要更改的消息索引。
   */
  changeChatHistory(data, index) {
    this.chatHistory[index] = data;
  },

  /**
   * 设置对话状态。
   * @param {boolean} data - 新的对话状态。
   */
  setIsChattingState(data) {
    this.isChatting = data;
  },

  /**
   * 设置当前对话消耗的 tokens 数量。
   * @param {number} data - tokens 数量。
   */
  setTokens(data) {
    this.tokens = data;
  },

  /**
   * 设置对话的唯一标志。
   * @param {string} data - 对话标志 ID。
   */
  setChatCid(data) {
    this.chatCid = data;
  },

  /**
   * 删除对话历史中的某条消息。
   * @param {number} index - 要删除的消息索引。
   */
  deleteChatHistoryItem(index) {
    this.chatHistory.splice(index, 1);
  },

  /**
   * 编辑对话历史中的特定消息。
   * @param {Object} data - 新的消息数据。
   * @param {number} data.index - 要编辑的消息索引。
   * @param {string} data.data - 新的消息文本。
   */
  editChatHistoryItem(data) {
    this.chatHistory[data.index].text = data.data;
  },

  /**
   * 设置是否处于编辑聊天参数的状态。
   * @param {boolean} data - 新的编辑状态。
   */
  setEditChatSettings(data) {
    this.isEditChatSettings = data;
  },
};
