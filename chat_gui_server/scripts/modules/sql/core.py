'''
数据库管理的核心文件
'''
from scripts.libs import getAbsPath
from .chat import Chat

CHAT_DB = getAbsPath('history_path', 'chat.db')

def getChatSQLHandle() -> Chat:
    '''登录成功的用户得到一个访问chatSQL的对象'''
    return Chat(name=CHAT_DB)

def releaseChatSQLHandle(handle: Chat) -> None:
    '''释放游标的资源'''
    handle.releaseCursor()

