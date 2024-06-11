import axios from "axios";
import { URL, getHeaders } from "./common.js";

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
