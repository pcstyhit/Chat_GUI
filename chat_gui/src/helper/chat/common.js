import StoreHelper from "../storeHelper";
import {
  deleteChatAPI,
  setChatNameAPI,
  getAllHistoryAPI,
  getChatParamsAPI,
  // downloadChatHistory,
  getChatModelListAPI,
} from "../../apis/chat.js";
import { showMessage, showMessageBox } from "../customMessage.js";

/** 使用对话功能之前 需要加载对话界面需要的基本参数 */
export const initChatPage = async () => {
  // 获取能够用的全部对话模型列表
  var rea = await getChatModelListAPI();
  if (!rea.flag) {
    showMessage("error", "获取服务器的对话模型API列表失败! 🙃");
    return;
  }
  StoreHelper.setChatModelList(rea.data);

  // 获取服务器的历史对话记录
  rea = await getAllHistoryAPI();
  if (!rea.flag) {
    showMessage("error", "获取用户的对话的全部记录失败! 🙃");
    return;
  }
  StoreHelper.setChatNameList(rea.data);
  // 初始的界面 默认是空白的
  StoreHelper.setChatCid("");
  // 不为空的chatCid代表切换对话就需要更新对话的参数和历史记录
  rea = await getChatParamsAPI("");
  if (rea.flag) StoreHelper.setChatParams(rea.data);
};

/** 根据chatCid来修改对话的名称 */
export const editChatNameByCid = async (chatCid, chatName) => {
  var flag = await showMessageBox(`确定修改对话名称为 【${chatName}】 吗?`);
  // 取消 返回
  if (!flag) return;
  // 确定 调用接口修改SERVER的参数
  var rea = await setChatNameAPI(chatCid, chatName);
  if (!rea.flag) {
    showMessage("error", "服务器修改对话名称失败! 😭");
    return;
  }
  StoreHelper.editChatNameList(chatCid, chatName);
  showMessage("success", "对话名称修改成功. 😀");
};

/** 根据chatCid来删除指定的对话 */
export const deletChatByCid = async (chatCid, chatName) => {
  var flag = await showMessageBox(`确定删除【${chatName}】这个对话吗? `);
  if (!flag) return;

  var rea = await deleteChatAPI(chatCid);
  if (!rea.flag) {
    showMessage("error", `服务器删除【${chatName}】失败! 😭`);
    return;
  }
  StoreHelper.deleteChatName(chatCid);
  showMessage("success", "对话已经删除. 😀");
};
