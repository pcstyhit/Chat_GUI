'''
利用sqlite3库来管理项目的数据
'''
from .core import getChatSQLHandle, releaseChatSQLHandle

__all__ = [
    'getChatSQLHandle',
    'releaseChatSQLHandle',
]