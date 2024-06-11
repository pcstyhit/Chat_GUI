/**
 * 用websocket来实现流对话
 */

import {
  WSURL,
  getWsid,
  updateStreamHistroy,
  addStreamHistroy,
  setIsChattingState,
  setTokens,
  updateTimeStamp,
} from "./common.js";

let flag = false;
let wsid = "";
let wsurl = "";
let socket = null;
let connectionPromise = null;
let chatRes = "";

let isAutoToBottomFlag = 2;
let isValidResponse = true;

function createWebSocketConnection() {
  return new Promise((resolve, reject) => {
    wsid = getWsid();

    // 无效的身份
    if (wsid === "") {
      reject(new Error("Invalid identity"));
    }

    wsurl = `${WSURL}/chat/${wsid}`;
    socket = new WebSocket(wsurl);

    // WebSocket连接打开
    socket.onopen = function () {
      flag = true; // 设置标志为true，表示连接已经建立
      resolve();
    };

    // 当接收到来自服务器的消息时，处理消息
    socket.onmessage = function (event) {
      // TODO: 数据量太大时候，这个可能不是一个很好的解决办法
      const data = JSON.parse(event.data);
      if (data.flag) {
        // 服务端标志对话结束
        chatRes = "";
        setIsChattingState(0); // 结束处于对话的状态
        isValidResponse = true; // 重置可以更新时间戳的开关量
        setTokens(data.tokens); // 更新最新对话要消耗的tokens数量
      } else {
        // 对话进行中更新
        chatRes += data.data;
        updateStreamHistroy({
          chatIid: data.chatIid,
          id: "assistant",
          text: chatRes,
        });
        // 更新流对话的一个开关
        isAutoToBottomFlag = isAutoToBottomFlag * -1;
        setIsChattingState(isAutoToBottomFlag);

        // 更新时间戳
        if (isValidResponse) {
          updateTimeStamp(true);
          isValidResponse = false;
        }
      }
    };

    // 当发生错误时，记录错误
    socket.onerror = function (error) {
      console.error("WebSocket error:", error);
      reject(error);
    };
  });
}

/**
 * 向fastapi的服务端发送websocket的消息
 */
export async function chatStreamAPI(isStreamResponse) {
  if (!flag) {
    connectionPromise = createWebSocketConnection();
  }

  try {
    await connectionPromise;
    const data = JSON.stringify({ data: isStreamResponse });
    socket.send(data);
    // 再history数组最后新增一个gpt的元素
    addStreamHistroy({
      chatIid: -1,
      id: "assistant",
      text: "Please wait ... ...",
    });
    // 开始流对话
    setIsChattingState(isAutoToBottomFlag * -1);
  } catch (error) {
    addStreamHistroy({ chatIid: -1, id: "assistant", text: error.toString() });
  }
}
