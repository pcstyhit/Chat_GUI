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
   * 用户的全部对话
   * @type {Array}
   */
  chatList: [],

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

  /**
   * 直接强制更新对话, 清空或者初始化用
   * @param {list} data
   */
  sethChat(data) {
    this.chatList = data;
  },

  /**
   * 新增对话
   * @param {object} data - 对话的对象 包括名称和chatCid
   */
  pushChat(data) {
    this.chatList.push(data);
  },

  /**
   * 根据chatCid删除对话
   * @param {str} data - 状态
   */
  deleteChatByChatCid(data) {
    const index = this.chatList.findIndex((item) => item.chatCid === data);

    if (index !== -1) {
      this.chatList.splice(index, 1);
    }
  },
};
