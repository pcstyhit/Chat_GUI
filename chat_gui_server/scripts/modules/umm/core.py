'''
FastAPI管理用户的核心文件
'''
from scripts.modules.chat import ChatAPI
from .fastapiWsid import addWsid
from scripts.modules.sql import UserSQL, getUserSQLHandle, releaseUserSQLHandle
ONLINELIST = {}


def login(user):
    '''判断要登录的用户是否在线, 已经在线的用户无法继续登录,'''
    userSQLHandler: UserSQL = getUserSQLHandle()
    flag = True
    msg = 'Login Success!'
    chatWsid = ''

    if user in list(ONLINELIST.keys()):
        flag = False
        msg = 'The user is already online.'
    else:
        # 申请对话的资源
        userSQLHandler.addUserLoginInfo(user)
        ONLINELIST[user] = ChatAPI(user)
        chatWsid = addWsid(user, 'chat')

    releaseUserSQLHandle(userSQLHandler)

    return flag, msg, chatWsid


def getChatHandle(user: str) -> ChatAPI:
    '''通过用户名获得操作对话的实力'''
    return ONLINELIST[user]


def logout(user):
    '''退出登录,删除资源'''
    del ONLINELIST[user]
    return True, 'Logout Success'
