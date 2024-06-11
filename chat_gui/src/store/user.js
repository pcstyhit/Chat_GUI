export const UserState = {
  /**
   * 当前的用户名称
   * @type {string}
   */
  name: "",
  /**
   * 简单的base64加密的认证字符
   * @type {string}
   */
  basicAuth: "",
  /**
   * 是否处于登录状态
   * @type {boolean}
   */
  isLogged: false,

  /**
   * 设置用户名
   * @param {string} data - name。
   */
  setUserName(data) {
    this.name = data;
  },

  /**
   * 设置base64认证的值
   * @param {string} data - 密文。
   */
  setBasicAuth(data) {
    this.basicAuth = data;
  },

  /**
   * 设置当前登录的状态
   * @param {boolean} data - 状态
   */
  setLoginState(data) {
    this.isLogged = data;
  },
};
