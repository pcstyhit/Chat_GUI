import { apiRequest } from "./common";

/** 开始登录 */
export const logIN = () => apiRequest("post", "/login", { data: "" });

/** 退出登录 */
export const logOUT = () => apiRequest("post", "/logout");
