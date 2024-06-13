'''
FastAPI管理用户的核心文件
'''
from typing import Optional
from scripts.modules.chat import ChatAPI
from scripts.modules.sql import UserSQL, getUserSQLHandle
ONLINELIST = {}

userSQLHandler: Optional[UserSQL] = None


def login(user):
    global userSQLHandler

    # 保证在一个线程内被初始化, not a good desgin
    userSQLHandler = getUserSQLHandle()
    '''判断要登录的用户是否在线, 已经在线的用户无法继续登录,'''
    flag = True
    msg = 'Login Success!'

    if user in list(ONLINELIST.keys()):
        flag = False
        msg = 'The user is already online.'
    else:
        # 申请对话的资源
        userSQLHandler.addUserLoginInfo(user)
        ONLINELIST[user] = ChatAPI(user)

    return flag, msg


def getChatHandle(user: str) -> ChatAPI:
    '''通过用户名获得操作对话的实例'''
    return ONLINELIST[user]


def getChatHandleByChatCid(chatCid: str) -> ChatAPI:
    '''通过chatCid获得操作对话的实例'''
    global userSQLHandler
    userName = userSQLHandler.getUserNameByChatCid(chatCid)
    return ONLINELIST[userName]


def logout(user):
    '''退出登录,删除资源'''
    del ONLINELIST[user]
    return True, 'Logout Success'
