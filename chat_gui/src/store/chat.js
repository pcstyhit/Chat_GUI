import { marked, textToHtml } from "../helper/formatHelper.js";

/**
 * 表示聊天信息存储的对象。
 */
export const ChatState = {
  /**
   * 当前对话的参数
   * @type {object}
   */
  chatParams: {
    chatName: "",
    modelType: "",
    modelName: "",
    modelList: [],
    maxTokens: 0,
    promptTemplate: [
      {
        role: "system",
        content: "You are GPT-4o a large language model of OpenAI.",
      },
    ],
    promptTemplateTokens: 0,
    passedMsgLen: 20,
    maxResponseTokens: 2000,
    temperature: 0.7,
    topP: 0.95,
    frequecyPenaty: 0,
    presentPenaty: 0,
    stopSequence: [],
    chatWithGptTimeout: 10,
    webRenderStrLen: 20,
    isUseProxy: false,
    proxyURL: "",
    isGhostChat: false,
  },

  /**
   * 当前对话消耗的 tokens 数量。
   * @type {number}
   */
  tokens: 0,

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
   * @type {number} 0表示没有在对话, 1表示在对话, 2/-2表示流更新回答
   */
  isChatting: 0,

  /**
   * 是否处于编辑聊天参数的状态。
   * @type {number}: 1表示正在修改, 0表示修改结束无更改, -1表示修改结束但是有更改
   */
  isEditChatSettings: 0,

  /**
   * 请求得到响应的时间
   * @type {number}
   */
  requestTime: 0,

  /**
   * 当前时间戳
   * @type {number}
   */
  timeStamp: 0,

  /**
   * 设置对话历史。
   * @param {Array<Object>} data - 对话历史。
   */
  setChatHistory(data) {
    this.chatHistory = data;
  },

  /**
   * 重置当前的对话历史
   * @param {Array<Object>} data - 要更新的数据
   */
  resetChatHistory(data) {
    this.chatHistory = [];
    data.forEach((element) => {
      this.chatHistory.push({
        chatIid: element.chatIid,
        role: element.role,
        content: element.content,
        text:
          element.role == "user"
            ? textToHtml(element.content)
            : marked.render(element.content),
      });
    });
  },

  /**
   * 重置当前的对话的参数信息
   * @param {object} data - 要更新的数据
   */
  resetChatParams(data) {
    // 循环键值对赋值,更新对话的参数
    Object.keys(this.chatParams).forEach((key) => {
      this.chatParams[key] = data[key];
    });
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
   * @param {Object} chatItemObj - 存入chatItem的对象。
   */
  changeSpecChatItemHistory(chatItemObj) {
    this.chatHistory.forEach((item) => {
      if (item.chatIid == chatItemObj.chatIid) {
        item.content = chatItemObj.content;
        item.text =
          chatItemObj.role == "user"
            ? textToHtml(chatItemObj.content)
            : marked.render(chatItemObj.content);
      }
    });
  },

  /**
   * 设置对话状态。
   * @param {number} data - 新的对话状态。
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
   * @param {number} chatIid - 要删除的对象的唯一序号标志
   */
  deleteChatHistoryItem(chatIid) {
    const index = this.chatHistory.findIndex(
      (item) => item.chatIid === chatIid
    );

    this.chatHistory.splice(index, 1);
  },

  /**
   * 设置是否处于编辑聊天参数的状态。
   * @param {number} data - 新的编辑状态。
   */
  setEditChatSettings(data) {
    this.isEditChatSettings = data;
  },

  /**
   * 更新时间戳
   * @param {boolean} isUpdateRequestTime - 是否更新请求时间
   */
  updateTimeStamp(isUpdateRequestTime) {
    const currentTime = new Date().getTime();
    if (isUpdateRequestTime) {
      this.requestTime = Math.abs(currentTime - this.timeStamp);
    }
    this.timeStamp = currentTime;
  },

  /**
   * 定制化的重新生成内容的API, 根据chatIid和role判断怎么刷新store的chatHistory
   * @param {Object} chatItemObj - 存入chatItem的对象。
   */
  reGenerateChatHistory(chatItemObj) {
    const index = this.chatHistory.findIndex(
      (item) => item.chatIid === chatItemObj.chatIid
    );
    if (index !== -1) {
      // 删除这个序号后面的全部元素
      if (chatItemObj.role == "user") this.chatHistory.splice(index + 1);
      else this.chatHistory.splice(index);
    }
  },
};
