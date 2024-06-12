'''
umm(User Management Module)用户信息管理模块
'''

from .basicAuth import authenticateUser
from .core import login, logout, getChatHandle, getChatHandleByChatCid

__all__ = [
    'authenticateUser',
    'login',
    'logout',
    'getChatHandle',
    'getChatHandleByChatCid'
]
