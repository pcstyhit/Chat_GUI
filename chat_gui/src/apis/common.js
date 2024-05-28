import axios from "axios";
import store from "../store/index.js";

const PORT = 5001;
export const SHORTTIME = 2000;
export const LONGTIME = 10000;
export const URL = `http://127.0.0.1:${PORT}`;
export const WSURL = `ws://127.0.0.1:${PORT}`;

/** 调用登录的接口
 * Axios中，第一个参数是URL
 *          第二个参数是数据body体，对应fast api封装的class.
 *          第三个参数是 axios 请求的配置选项，例如headers.
 * 比较规范的写法建议是将第二参数的body体内的变量做到与fast api的class格式一一对应.
 * */
export async function logIN() {
  try {
    const response = await axios.post(
      `${URL}/login`,
      {
        data: "login",
        timeout: SHORTTIME,
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

/** 退出登录 */
export async function logOUT() {
  try {
    const response = await axios.post(
      `${URL}/logout`,
      {
        data: {},
        timeout: SHORTTIME,
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

/** 从当前项目的store获得basic auth信息 */
export const getHeaders = () => {
  return {
    "Content-Type": "application/json",
    Authorization: store.state.user.basicAuth,
  };
};

/** 从当前项目的store获得chat给到websocket的ID */
export const getWsid = () => {
  return store.state.chat.chatWsid;
};

/** 更新流对话 */
export async function updateStreamHistroy(data) {
  store.state.chat.chatHistory[store.state.chat.chatHistory.length - 1] = data;
}

/** 新增流对话 */
export async function addStreamHistroy(data) {
  store.state.chat.chatHistory.push(data);
}

/** 控制当前对话是否处于进行状态 */
export async function setChatState(data) {
  store.state.chat.isChatting = data;
}

/** 设置如果按照当前的内容发送一次对话要消耗的tokens数量 */
export async function setTokens(data) {
  store.state.chat.tokens = data;
}
