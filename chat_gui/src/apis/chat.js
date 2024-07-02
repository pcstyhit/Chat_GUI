import {
  URL,
  apiRequest,
  updateStreamHistroy,
  addStreamHistroy,
  setIsChattingState,
  setTokens,
  updateTimeStamp,
  getWebRenderLen,
} from "./common.js";
import { marked } from "../helper/formatHelper.js";

/** 📜 获取所有历史记录 */
export const getAllHistoryAPI = () => apiRequest("get", "/chat/allHistory");

/** ➕ 设置模型的参数 */
export const addNewChatAPI = (chatName) =>
  apiRequest("post", "/chat/addNewChat", { chatName });

/** 🛠️ 修改对话的参数,可以不是当前的对话 */
export const setChatParamsAPI = (chatCid, paramsData) =>
  apiRequest("post", "/chat/setChatParams", { chatCid, data: paramsData });

/** 📖 获取指定对话的历史记录 */
export const getSpecChatHistoryAPI = (chatCid) =>
  apiRequest("post", "/chat/getSpecChatHistory", { chatCid });

/** ❌ 删除对话 */
export const deleteChatAPI = (chatCid) =>
  apiRequest("post", "/chat/deleteChat", { chatCid });

/** ❌ 删除指定chatIid的对话 */
export const deleteChatItemAPI = (chatIid) =>
  apiRequest("post", "/chat/deleteChatItem", { chatIid });

/** ✏️ 修改指定chatIid的对话 */
export const editChatItemAPI = (chatIid, msg) =>
  apiRequest("post", "/chat/editChatItem", { chatIid, msg });

/** ✉️ 设置用户消息 */
export const setUserMsgAPI = (msg) =>
  apiRequest("post", "/chat/setUserMsg", { msg });

/** ⚙️ 获得当前对话的设置 */
export const getChatParamsAPI = (chatCid) =>
  apiRequest("post", "/chat/getChatParams", { chatCid });

/** 🔄 重新生成内容 */
export const reGenerateContentAPI = (role, chatIid) =>
  apiRequest("post", "/chat/reGenerateContent", { role, chatIid });

/** 📥 下载对话的全部消息 */
export const downloadChatHistory = (chatCid) =>
  apiRequest("post", "/chat/downloadChatHistory", { chatCid });

/** 📤 上传json数据然后开始对话 */
export const uploadChatHistory = (jsonData) =>
  apiRequest("post", "/chat/uploadChatHistory", { data: jsonData });

/** 👻 新建一个幽灵对话 */
export const newGhostChatAPI = (data) =>
  apiRequest("post", "/chat/newGhostChat", { data });

/** 🔊 对话的语音播报 */
export const chatAudioAPI = (data) =>
  apiRequest("post", "/chat/chatAudio", { data });

/** 📡 通过SSE获取来自SERVER端的响应 */
export const createEventSourceAPI = (chatCid) => {
  let chatRes = "";
  let isAutoToBottomFlag = 2;
  let isValidResponse = true;
  const webRenderLen = getWebRenderLen();

  return new Promise((resolve, reject) => {
    const eventSource = new EventSource(`${URL}/chat/sse/${chatCid}`);

    // 在history数组最后新增一个gpt的元素 等待连接与返回消息
    addStreamHistroy({
      chatIid: null,
      role: "assistant",
      content: "",
      text: "Please wait ... ...",
    });
    // 开始流对话
    setIsChattingState(isAutoToBottomFlag * -1);

    // 处理收到的消息
    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      chatRes += data.data;

      // 服务端标志对话结束
      if (data.flag == 0) {
        // 如果残留的字符没有更新,需要更新最后的字符
        updateStreamHistroy({
          chatIid: data.chatIid,
          role: "assistant",
          content: chatRes,
          text: marked.render(chatRes),
        });
        // 更新流对话的一个开关
        isAutoToBottomFlag = isAutoToBottomFlag * -1;
        setIsChattingState(isAutoToBottomFlag);

        // 会话结束重置一些操作
        chatRes = "";
        setIsChattingState(0); // 结束处于对话的状态
        isValidResponse = true; // 重置可以更新时间戳的开关量
        setTokens(data.tokens); // 更新最新对话要消耗的tokens数量
        eventSource.close();
        resolve("Connection closed by server request.");
      }

      // 开始对话的标志
      if (data.flag == 1) {
        chatRes = "";
      }

      if (data.flag == 2) {
        // 网页自身控制render的频率
        if (chatRes.length > webRenderLen) {
          updateStreamHistroy({
            chatIid: data.chatIid,
            role: "assistant",
            content: chatRes,
            text: marked.render(chatRes),
          });
          // 更新流对话的一个开关
          isAutoToBottomFlag = isAutoToBottomFlag * -1;
          setIsChattingState(isAutoToBottomFlag);
          setTokens(data.tokens);
        }

        // 更新时间戳
        if (isValidResponse) {
          updateTimeStamp(true);
          isValidResponse = false;
        }
      }
    };

    eventSource.onerror = (event) => {
      if (eventSource.readyState === EventSource.CLOSED) {
        console.log("EventSource closed by the server.");
        eventSource.close();
        reject(new Error("EventSource closed by the server."));
      } else if (eventSource.readyState === EventSource.CONNECTING) {
        console.log("EventSource is reconnecting...");
      } else {
        console.log("EventSource encountered an error:", event);
        reject(new Error("EventSource encountered an error."));
      }
    };

    eventSource.onopen = () => {
      // console.log("EventSource connection opened:", event);
    };
  });
};
