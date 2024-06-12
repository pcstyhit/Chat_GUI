import axios from "axios";
import {
  URL,
  getHeaders,
  updateStreamHistroy,
  addStreamHistroy,
  setIsChattingState,
  setTokens,
  updateTimeStamp,
} from "./common.js";

export async function getAllHistoryAPI() {
  try {
    const response = await axios.get(`${URL}/chat/allHistory`, {
      // headers已经包含了用户的身份
      headers: getHeaders(),
    });
    return response.data;
  } catch (error) {
    if (error.code === "ECONNABORTED") {
      console.error("TIME OVER");
    } else {
      console.error("REQUEST FAILED:", error.message);
    }
    return { data: [] };
  }
}

/** 设置模型的参数 */
export async function addNewChatAPI(chatName) {
  try {
    const response = await axios.post(
      `${URL}/chat/addNewChat`,
      { chatName: chatName },
      {
        headers: getHeaders(),
      }
    );
    return response.data;
  } catch (error) {
    if (error.code === "ECONNABORTED") {
      console.error("TIME OVER");
    } else {
      console.error("REQUEST FAILED:", error.message);
    }
    return { data: "Network Error" };
  }
}

/** 修改对话的参数,可以不是当前的对话 */
export async function setChatParamsAPI(chatCid, paramsData) {
  try {
    const response = await axios.post(
      `${URL}/chat/setChatParams`,
      {
        chatCid: chatCid,
        data: paramsData,
      },
      {
        headers: getHeaders(),
      }
    );
    return response.data;
  } catch (error) {
    if (error.code === "ECONNABORTED") {
      console.error("TIME OVER");
    } else {
      console.error("REQUEST FAILED:", error.message);
    }
    return { data: "Network Error" };
  }
}

export async function getSpecChatHistoryAPI(chatCid) {
  try {
    const response = await axios.post(
      `${URL}/chat/getSpecChatHistory`,
      {
        chatCid: chatCid,
        timeout: 10000,
      },
      {
        headers: getHeaders(),
      }
    );
    return response.data;
  } catch (error) {
    if (error.code === "ECONNABORTED") {
      console.error("TIME OVER");
    } else {
      console.error("REQUEST FAILED:", error.message);
    }
    return { data: "Network Error" };
  }
}

export async function deleteChatAPI(chatCid) {
  try {
    const response = await axios.post(
      `${URL}/chat/deleteChat`,
      {
        chatCid: chatCid,
        timeout: 10000,
      },
      {
        headers: getHeaders(),
      }
    );
    return response.data;
  } catch (error) {
    if (error.code === "ECONNABORTED") {
      console.error("TIME OVER");
    } else {
      console.error("REQUEST FAILED:", error.message);
    }
    return { data: "Network Error" };
  }
}

/** 删除指定chatIid的对话 */
export async function deletChatItemAPI(chatIid) {
  try {
    const response = await axios.post(
      `${URL}/chat/deleteChatItem`,
      {
        chatIid: chatIid,
        timeout: 10000,
      },
      {
        headers: getHeaders(),
      }
    );
    return response.data;
  } catch (error) {
    if (error.code === "ECONNABORTED") {
      console.error("TIME OVER");
    } else {
      console.error("REQUEST FAILED:", error.message);
    }
    return { data: "Network Error" };
  }
}

/** 修改指定chatIid的对话 */
export async function editChatItemAPI(chatIid, msg) {
  try {
    const response = await axios.post(
      `${URL}/chat/editChatItem`,
      {
        chatIid: chatIid,
        msg: msg,
        timeout: 10000,
      },
      {
        headers: getHeaders(),
      }
    );
    return response.data;
  } catch (error) {
    if (error.code === "ECONNABORTED") {
      console.error("TIME OVER");
    } else {
      console.error("REQUEST FAILED:", error.message);
    }
    return { data: "Network Error" };
  }
}

/** 获得用户发出消息的chatIid */
export async function setUserMsgAPI(msg) {
  try {
    const response = await axios.post(
      `${URL}/chat/setUserMsg`,
      {
        msg: msg,
        timeout: 10000,
      },
      {
        headers: getHeaders(),
      }
    );
    return response.data;
  } catch (error) {
    if (error.code === "ECONNABORTED") {
      console.error("TIME OVER");
    } else {
      console.error("REQUEST FAILED:", error.message);
    }
    return { data: "Network Error" };
  }
}

/** 获得当前对话的设置 */
export async function getChatParamsAPI(chatCid) {
  try {
    const response = await axios.post(
      `${URL}/chat/getChatParams`,
      {
        chatCid: chatCid,
        timeout: 10000,
      },
      {
        headers: getHeaders(),
      }
    );
    return response.data;
  } catch (error) {
    if (error.code === "ECONNABORTED") {
      console.error("TIME OVER");
    } else {
      console.error("REQUEST FAILED:", error.message);
    }
    return { data: "Network Error" };
  }
}

/** 通过SSE获取来自SERVER端的响应 */
export const createEventSourceAPI = (chatCid) => {
  let chatRes = "";
  let isAutoToBottomFlag = 2;
  let isValidResponse = true;

  return new Promise((resolve, reject) => {
    const eventSource = new EventSource(`${URL}/chat/sse/${chatCid}`);

    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.flag == 0) {
        // 服务端标志对话结束
        chatRes = "";
        setIsChattingState(0); // 结束处于对话的状态
        isValidResponse = true; // 重置可以更新时间戳的开关量
        setTokens(data.tokens); // 更新最新对话要消耗的tokens数量
        eventSource.close();
        resolve("Connection closed by server request.");
      }

      // 开始对话的标志
      if (data.flag == 1) {
        // 在history数组最后新增一个gpt的元素
        addStreamHistroy({
          chatIid: null,
          id: "assistant",
          text: "Please wait ... ...",
        });
        // 开始流对话
        setIsChattingState(isAutoToBottomFlag * -1);
        chatRes = "";
      }

      if (data.flag == 2) {
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
