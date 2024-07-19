'''
FastAPI管理用户的核心文件
'''
import sys
import json
from typing import List
from dataclasses import dataclass
from scripts.modules.sql import *
from scripts.libs import LOGGER
from scripts.libs.arsm import LoginAndLogoutResponse
from scripts.modules.chat import ChatAPI
from scripts.modules.network import HttpxProxy


@dataclass
class OnlineUserHandles:
    userName: str = ''
    uid: str = ''
    chat: ChatAPI = None
    httpxp: HttpxProxy = None
    userSql: UserSQL = None
    chatSql: ChatSQL = None


class UserManage:
    '''管理项目的用户状态'''

    ONLINELIST: List[OnlineUserHandles] = []

    @classmethod
    def init(cls):
        cls.initSqlite3()

    @classmethod
    def initSqlite3(cls):
        '''因为sqlite3初始化很慢 可以在启动时候 开辟一次 后面再申请hanlder就很快'''
        try:
            tmpUser: UserSQL = getUserSQLHandle()
            tmpChat: ChatSQL = getChatSQLHandle()
            releaseChatSQLHandle(tmpChat)
            releaseUserSQLHandle(tmpUser)
            LOGGER.info(f"initialize sqlit3 data base success!")
        except Exception as e:
            print(e)
            sys.exit(1)

    @classmethod
    def isUserOnline(cls, name):
        '''判断用户是不是在线了'''
        for user in cls.ONLINELIST:
            if user.userName == name:
                return True
        return False

    @classmethod
    async def addOnlineUser(cls, userName) -> OnlineUserHandles:
        '''新建一个用户 并且初始化它内部的元素'''
        user = OnlineUserHandles()

        tmpUh = getUserSQLHandle()
        tmpCh = getChatSQLHandle()
        tmpHp = HttpxProxy()

        # 用userSqlHandler向数据库存入用户信息 同时也把这个数据库操作的句柄作为这个用户的单例
        user.userName = userName
        user.uid = tmpUh.addUserLoginInfo(userName)
        user.userSql = tmpUh
        user.chatSql = tmpCh
        user.httpxp = tmpHp
        user.chat = ChatAPI(userName, tmpUh, tmpCh, tmpHp)
        await cls.initUserSettings(user)
        return user

    @classmethod
    async def initUserSettings(cls, userHandler: OnlineUserHandles) -> None:
        '''登录的用户 初始化一下默认的配置参数'''
        print("xxxxxxxxxxxxxxx", userHandler.userName)
        tmpCsStr = userHandler.userSql.getChatSettingsForSpecUser(userHandler.userName)
        if tmpCsStr != None:
            # 已经存在就更新
            tmpCsDict: dict = json.loads(tmpCsStr)
            await userHandler.chat.setChatDefaultParams(tmpCsDict)
        else:
            # 不存在需要新设置
            tmpCsDict: dict = await userHandler.chat.getChatDefaultParams()
            tmpCsStr = json.dumps(tmpCsDict)
            userHandler.userSql.setChatParamsForSpecUser(userHandler.userName, tmpCsStr)

        # 对于其他设置也是一样的
        tmpCsStr = userHandler.userSql.getProxySettingsForSpecUser(userHandler.userName)
        if tmpCsStr != None:
            # 已经存在就更新
            tmpCsDict: dict = json.loads(tmpCsStr)
            userHandler.httpxp.setHttpxClient(tmpCsDict)
            await userHandler.chat.updateHttpx(userHandler.httpxp)
        else:
            # 不存在需要新设置
            tmpCsDict: dict = await userHandler.httpxp.getHttpxInfo()
            tmpCsStr = json.dumps(tmpCsDict)
            userHandler.userSql.setProxySettingsForSpecUser(userHandler.userName, tmpCsStr)

    @classmethod
    async def loginAPI(cls, userName) -> LoginAndLogoutResponse:
        '''登录成功的操作 也就是开辟各种handler'''
        rea = LoginAndLogoutResponse()

        if cls.isUserOnline(userName):
            rea.msg = 'The user is already online.'
            return rea

        user = await cls.addOnlineUser(userName)
        cls.ONLINELIST.append(user)

        rea.flag = True
        rea.msg = "Login success!"
        return rea

    @classmethod
    def getChatHandle(cls, uid) -> ChatAPI:
        '''根据用户的唯一标识 找到能够操作对话的句柄'''
        for user in cls.ONLINELIST:
            if user.userName == uid:
                return user.chat

    @classmethod
    def _getUserHandle(cls, uid) -> OnlineUserHandles:
        '''根据用户的唯一标识 找到能够操作用户全部内容的句柄'''
        for user in cls.ONLINELIST:
            if user.userName == uid:
                return user

    @classmethod
    async def getUserChatDefParamsAPI(cls, userName) -> dict:
        '''获得用户默认的对话参数'''
        userHandler = cls._getUserHandle(userName)
        rea = await userHandler.chat.getChatDefaultParams()
        return rea

    @classmethod
    async def setUserChatDefParamsAPI(cls, userName, data) -> bool:
        '''修改掉这个用户的对话handle的默认参数'''
        userHandler = cls._getUserHandle(userName)
        userHandler.userSql.setChatParamsForSpecUser(userName, json.dumps(data))
        await userHandler.chat.setChatDefaultParams(data)
        return True

    @classmethod
    async def getUserSettingsAPI(cls, userName) -> dict:
        '''获得用户的默认设置参数, 目前只有代理的信息'''
        userHandler = cls._getUserHandle(userName)
        rea = await userHandler.httpxp.getHttpxInfo()
        return rea

    @classmethod
    async def setUserSettingsAPI(cls, userName, data) -> bool:
        '''修改用户的默认参数, 目前只有代理的信息'''
        print(">>>>> data: ", data)
        userHandler = cls._getUserHandle(userName)
        userHandler.httpxp.setHttpxClient(data)
        userHandler.userSql.setProxySettingsForSpecUser(userName, json.dumps(data))
        await userHandler.chat.updateHttpx(userHandler.httpxp)
        return True
