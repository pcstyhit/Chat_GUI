import StoreHelper from "../storeHelper.js";
import { showMessage, showMessageBox } from "../customMessage.js";
import { textToHtml, marked } from "../formatHelper.js";
import {
  assistantIcon,
  reRequestIcon,
  eidtChatItemIcon,
  copyMarkdownIcon,
  deleteChatItemIcon,
} from "../../assets/styles/chat/svgs.js";
import {
  getChatItemAPI,
  deleteChatItemAPI,
  editChatItemAPI,
  reGenerateContentAPI,
  createEventSourceAPI,
} from "../../apis/chat.js";

class ChatItemHelper {
  constructor() {
    this._chatContainer = this._init();
    this._ctrl = new AbortController();
  }

  _init() {
    if (!this._chatContainer) {
      this._chatContainer = document.getElementById("chat-messages-container");
    }
    return this._chatContainer;
  }

  /** 删除容器下的全部div */
  _removeAllElem() {
    const divs = this._chatContainer.getElementsByTagName("div");
    while (divs.length > 0) {
      divs[0].remove();
    }
  }

  async _copyChatItem(chatIid) {
    var rea = await getChatItemAPI(chatIid);
    if (rea.flag) {
      try {
        await navigator.clipboard.writeText(rea.data);
        showMessage("success", "复制markdown成功");
      } catch (err) {
        showMessage("error", "复制失败(WEB ERROR)");
      }
    }
  }

  async editChatItemCallback(newValue, chatIid, role) {
    var rea = await editChatItemAPI(chatIid, newValue);
    if (rea.flag) {
      var tmpParentElem = this._chatContainer.querySelector(`#${chatIid}`);
      var tmpTextElem = tmpParentElem.querySelector(`.text`);
      if (role === "user") tmpTextElem.innerHTML = textToHtml(newValue);
      if (role === "assistant") tmpTextElem.innerHTML = marked.render(newValue);
    }
  }

  /** 从服务器先获得对话内容的文本 再把它通过事件总线传递给文本编辑的组件 */
  async _editChatItem(chatIid, role) {
    var rea = await getChatItemAPI(chatIid);
    if (!rea.flag) {
      showMessage("error", "服务器获取对话内容失败！");
      return;
    }

    // 向通用的文本编辑组件发送文本和回调函数
    StoreHelper.setTextEditObj({
      data: rea.data,
      options: {
        // 使用箭头函数确保 `this` 指向正确的上下文
        confirmCallback: (newValue) =>
          this.editChatItemCallback(newValue, chatIid, role),
      },
    });
  }

  /** 对于删除操作先确定是否真的删除 然后SERVER删除元素成功之后再删除网页的DIV */
  async _deleteChatItem(chatIid) {
    var flag = await showMessageBox("确定删除吗? (操作不可逆)");
    // 取消删除 退出
    if (!flag) return;

    var rea = await deleteChatItemAPI(chatIid);
    if (!rea.flag) {
      showMessage("error", "服务器删除对话内容失败!");
      return;
    }

    var tmpDeleteElem = this._chatContainer.querySelector(`#${chatIid}`);
    if (tmpDeleteElem) {
      this._chatContainer.removeChild(tmpDeleteElem);
      showMessage("info", "删除成功");
    }
  }

  async _reGenerateMessage(chatIid) {
    var rea = await reGenerateContentAPI(chatIid);
    if (rea.flag) {
      // 删除目标 div 之后的所有 div 元素
      const targetDiv = this._chatContainer.querySelector(`#${chatIid}`);
      if (this._chatContainer && targetDiv) {
        let targetIndex = Array.prototype.indexOf.call(
          this._chatContainer.children,
          targetDiv
        );
        while (this._chatContainer.children.length > targetIndex + 1) {
          this._chatContainer.removeChild(this._chatContainer.lastChild);
        }
      }

      // 重新开始生成Assistant的内容
      const chatCid = StoreHelper.getChatCid();
      this._getAssistantResponse(chatCid);
    }
  }

  _addUserQHTMLElem = (chatIid, text) => {
    if (!this._init()) return;
    const userDiv = document.createElement("div");
    userDiv.classList.add("user");
    userDiv.id = chatIid;

    const userContentDiv = document.createElement("div");
    userContentDiv.classList.add("user-content");

    const textDiv = document.createElement("div");
    textDiv.classList.add("text");
    textDiv.innerHTML = textToHtml(text);

    const optionsDiv = document.createElement("div");
    optionsDiv.classList.add("options");

    const reGenerateButtonDiv = document.createElement("div");
    reGenerateButtonDiv.classList.add("options-button");
    reGenerateButtonDiv.innerHTML = reRequestIcon;
    optionsDiv.appendChild(reGenerateButtonDiv);

    reGenerateButtonDiv.addEventListener("click", async () => {
      await this._reGenerateMessage(userDiv.id);
    });

    const editButtonDiv = document.createElement("div");
    editButtonDiv.classList.add("options-button");
    editButtonDiv.innerHTML = eidtChatItemIcon;
    optionsDiv.appendChild(editButtonDiv);

    editButtonDiv.addEventListener("click", async () => {
      await this._editChatItem(userDiv.id, "user");
    });

    const deleteButtonDiv = document.createElement("div");
    deleteButtonDiv.classList.add("options-button");
    deleteButtonDiv.innerHTML = deleteChatItemIcon;
    optionsDiv.appendChild(deleteButtonDiv);

    deleteButtonDiv.addEventListener("click", () => {
      this._deleteChatItem(userDiv.id);
    });

    userContentDiv.appendChild(textDiv);
    userContentDiv.appendChild(optionsDiv);
    userDiv.appendChild(userContentDiv);
    this._chatContainer.appendChild(userDiv);
  };

  _addAssAHTMLElem = (chatIid, text) => {
    if (!this._init()) return;
    const assistantDiv = document.createElement("div");
    assistantDiv.classList.add("assistant");
    //  注意 这里只是把从历史记录拿的消息和从SSE拿的逻辑统一了一下 存在这个判断条件
    if (chatIid !== "") {
      assistantDiv.id = chatIid;
    }

    const assistantIconDiv = document.createElement("div");
    assistantIconDiv.classList.add("assistant-icon");
    assistantIconDiv.innerHTML = assistantIcon;

    const assistantContentDiv = document.createElement("div");
    assistantContentDiv.classList.add("assistant-content");

    const textDiv = document.createElement("div");
    textDiv.classList.add("text");
    textDiv.innerHTML = marked.render(text);

    const optionsDiv = document.createElement("div");
    optionsDiv.classList.add("options");

    const editButtonDiv = document.createElement("div");
    editButtonDiv.classList.add("options-button");
    editButtonDiv.innerHTML = eidtChatItemIcon;
    optionsDiv.appendChild(editButtonDiv);
    editButtonDiv.addEventListener("click", async () => {
      await this._editChatItem(assistantDiv.id, "assistant");
    });

    const copyMarkdownButtonDiv = document.createElement("div");
    copyMarkdownButtonDiv.classList.add("options-button");
    copyMarkdownButtonDiv.innerHTML = copyMarkdownIcon;
    optionsDiv.appendChild(copyMarkdownButtonDiv);
    copyMarkdownButtonDiv.addEventListener("click", async () => {
      await this._copyChatItem(assistantDiv.id);
    });

    const deleteButtonDiv = document.createElement("div");
    deleteButtonDiv.classList.add("options-button");
    deleteButtonDiv.innerHTML = deleteChatItemIcon;
    optionsDiv.appendChild(deleteButtonDiv);
    deleteButtonDiv.addEventListener("click", () => {
      this._deleteChatItem(assistantDiv.id);
    });

    assistantContentDiv.appendChild(textDiv);
    assistantContentDiv.appendChild(optionsDiv);
    assistantDiv.appendChild(assistantIconDiv);
    assistantDiv.appendChild(assistantContentDiv);
    this._chatContainer.appendChild(assistantDiv);

    return assistantDiv;
  };

  async _getAssistantResponse(chatCid) {
    // 从服务端获得输出,并创建一个HTMLElement来缓存值
    const assHTMLElem = this._addAssAHTMLElem(
      "",
      "Connect to WEB server... ..."
    );
    await createEventSourceAPI(chatCid, assHTMLElem, this._ctrl);
  }
}

export default ChatItemHelper;
