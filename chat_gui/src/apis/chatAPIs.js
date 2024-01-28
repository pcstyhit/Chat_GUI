import axios from "axios";

const PORT = 5001;
const URL = `http://127.0.0.1:${PORT}/chat`;

export async function postChatByText(msg) {
  try {
    const response = await axios.post(`${URL}/text`, {
      data: JSON.stringify(msg),
      timeout: 10000,
    });
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

export async function postChatByStream(msg,streamStartFunc) {
  try {
    const response = await axios.post(`${URL}/stream`, {
      data: JSON.stringify(msg),
      timeout: 10000,
      responseType: 'stream'
    });
    response.data.on('data', (chunk) => {
      // logic to process stream data
      // TBD: chunk的具体格式
      streamStartFunc(chunk)
    });
    response.data.on('end', () => {
      // logic for stream complete
    });

  } catch (error) {
    if (error.code === "ECONNABORTED") {
      console.error("TIME OVER");
    } else {
      console.error("REQUEST FAILED:", error.message);
    }
    return { data: "Network Error" };
  }
}

export async function postPrompt(msg) {
  try {
    const response = await axios.post(`${URL}/prompt`, {
      data: JSON.stringify(msg),
      timeout: 10000,
    });
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

export async function getAllHistory() {
  try {
    const response = await axios.get(`${URL}/allHistory`, {
      data: null,
      timeout: 10000,
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

export async function loadChatHistory(msg) {
  try {
    const response = await axios.post(`${URL}/loadChatHistory`, {
      data: msg,
      timeout: 10000,
    });
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

export async function loadChatTokens(msg) {
  try {
    const response = await axios.post(`${URL}/loadChatTokens`, {
      data: msg,
      timeout: 10000,
    });
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

export async function deleteChat(msg) {
  try {
    const response = await axios.post(`${URL}/deleteChat`, {
      data: msg,
      timeout: 10000,
    });
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
