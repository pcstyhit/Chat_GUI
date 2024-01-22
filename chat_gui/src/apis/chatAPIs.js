import axios from "axios";

const PORT = 5001;
const URL = `http://127.0.0.1:${PORT}/chat`;

export async function postChatByText(msg) {
  try {
    const response = await axios.post(`${URL}/text`, {
      data: msg,
      timeout: 10000,
    });
    return response.data
  } catch (error) {
    if (error.code === "ECONNABORTED") {
      console.error("TIME OVER");
    } else {
      console.error("REQUEST FAILED:", error.message);
    }
    return { data: 'Network Error' }
  }
}