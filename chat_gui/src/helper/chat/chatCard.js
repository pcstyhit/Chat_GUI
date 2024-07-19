import ChatItemHelper from "./chatItem.js";
import StoreHelper from "../storeHelper.js";
import { showMessage } from "../customMessage.js";
import {
  addNewChatAPI,
  setUserMsgAPI,
  setChatParamsAPI,
  getSpecChatHistoryAPI,
} from "../../apis/chat.js";

class ChatCardHelper extends ChatItemHelper {
  // 单例
  static instance = null;
  constructor() {
    super();
    if (ChatCardHelper.instance) {
      throw new Error("我是单例 用 ChatCardHelper.getInstance() 来调我");
    }
    this._isListenerActive = false;
  }

  static getInstance() {
    if (!ChatCardHelper.instance) {
      ChatCardHelper.instance = new ChatCardHelper();
    }
    return ChatCardHelper.instance;
  }

  _mouseMoveLister = (event) => {
    const targetClass = event.target.closest(
      ".user-content, .assistant-content"
    );
    if (targetClass) {
      const optionButtons = targetClass.querySelectorAll(".options-button");
      optionButtons.forEach((div) => {
        div.classList.add("active");
      });
    }
  };

  _mouseOutLister = () => {
    const activeOptionButtons = document.querySelectorAll(
      ".options-button.active"
    );
    activeOptionButtons.forEach((div) => {
      div.classList.remove("active");
    });
  };

  async _newChat() {
    var tmpChatCid = StoreHelper.getChatCid();
    var chatCid = tmpChatCid !== "" ? tmpChatCid : "";

    // 没有新建对话需要新建对话
    if (chatCid == "") {
      showMessage("info", "默认参数开始对话, 初始化数据库 ... ...");
      var rea = await addNewChatAPI();
      if (!rea.flag) return false;

      // 得到chatCid
      chatCid = rea.chatCid;
      //  切换chatCid的时候 已经从SERVER更新过参数了
      var chatParams = StoreHelper.getChatParams();
      rea = await setChatParamsAPI(chatCid, chatParams);
      if (!rea.flag) return false;

      // 🎉 有效的ChatCid, 新建对话成功！ 存入store
      StoreHelper.setChatCid(chatCid);
      StoreHelper.pushChatName(chatCid, chatParams.chatName);
    }

    return chatCid;
  }

  /** 给显示对话消息的界面增加鼠标移动事件的监听器, 单例 必须保证事件监听器的开关是挂锁的 */
  addListener = () => {
    if (!this._init()) return;
    if (this._isListenerActive) return;
    this._chatContainer.addEventListener("mouseover", this._mouseMoveLister);
    this._chatContainer.addEventListener("mouseout", this._mouseOutLister);
    this._isListenerActive = true;
  };

  /** 移除对话消息的界面的鼠标移动事件监听器*/
  removeListener = () => {
    if (!this._init()) return;
    if (!this._isListenerActive) return;
    this._chatContainer.removeEventListener("mouseover", this._mouseMoveLister);
    this._chatContainer.removeEventListener("mouseout", this._mouseOutLister);
    this._isListenerActive = false;
  };

  /** 初始化时候从SERVER加载的对话历史渲染消息到`ChatCard.vue`上 */
  initChatHistory = async (chatCid) => {
    if (!this._init()) return;
    this._removeAllElem();
    // 新对话 清空DIV就返回了
    if (chatCid === "") return;
    this.addListener();
    var rea = await getSpecChatHistoryAPI(chatCid);
    if (rea.flag) {
      rea.history.forEach((item) => {
        if (item.role == "user")
          this._addUserQHTMLElem(item.chatIid, item.content);
        else this._addAssAHTMLElem(item.chatIid, item.content);
      });
      return rea.tokens;
    }
    return 0;
  };

  async sendChat(msg) {
    this.removeListener();
    var chatCid = await this._newChat();
    // 发送消息
    var rea = await setUserMsgAPI(msg);
    if (rea.flag) {
      // 更新UI
      this._addUserQHTMLElem(rea.chatIid, msg);
      // 更新tokens
      StoreHelper.setTokens(rea.tokens);
      // 开始更新Assistant的回答
      console.log("chatCid: ", chatCid);
      await this._getAssistantResponse(chatCid);
    } else {
      showMessage("error", "GPT API tokens error");
    }
    this.addListener();
  }
}

// 单例
const chatCardHandler = ChatCardHelper.getInstance();
export default chatCardHandler;
