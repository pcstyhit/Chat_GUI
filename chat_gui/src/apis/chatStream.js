/**
 * 用websocket来实现流对话
 */

import {
  WSURL,
  getWsid,
  updateStreamHistroy,
  addStreamHistroy,
  setChatState,
  setTokens,
} from "./common.js";

let flag = false;
let wsid = "";
let wsurl = "";
let socket = null;
let connectionPromise = null;
let chatRes = "";

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
        setChatState(false); // 结束处于对话的状态
        setTokens(data.tokens); // 更新最新对话要消耗的tokens数量
      } else {
        // 对话进行中更新
        chatRes += data.data;
        updateStreamHistroy({
          chatIid: data.chatIid,
          id: "gpt",
          text: chatRes,
        });
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
export async function chatStreamAPI(msg) {
  if (!flag) {
    connectionPromise = createWebSocketConnection();
  }

  try {
    await connectionPromise;
    const data = JSON.stringify({ data: msg });
    socket.send(data);
    // 再history数组最后新增一个gpt的元素
    addStreamHistroy({ chatIid: -1, id: "gpt", text: "Please wait ... ..." });
  } catch (error) {
    addStreamHistroy({ chatIid: -1, id: "gpt", text: error.toString() });
  }
}
