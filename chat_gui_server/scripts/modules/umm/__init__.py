'''
umm(User Management Module)用户信息管理模块
'''

from .basicAuth import authenticateUser
from .core import UserManage

__all__ = [
    'UserManage',
    'authenticateUser',
]
