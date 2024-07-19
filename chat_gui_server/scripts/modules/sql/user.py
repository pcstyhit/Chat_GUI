'''
#### 管理一些用户属性的SQL的handle

UserSQL管理两张表: users, users_settings_table 和 users_chats_table, 其中: 

对于users表单的信息 主要管理登录的一些特有的用户属性:
    - id: 数据的主键
    - uid: 用户的唯一身份id, 可以是登录时会分配, uid适合拓展登录情况 没有做, 先埋坑👻
    - userName: 用户名称, 这个也是唯一的

对于 users_settings_table 表单, 主要存放用户的默认设置信息:
    - id: 数据库的id标志
    - userName: 用户名称, 唯一的属性
    - chatSettings 用户某个对话的唯一id
    - proxySettings 对话的参数信息

对于 users_chats_table 表单,主要存放用户的一些操作行为:
    - id: 数据库的id标志
    - uid 用户的唯一身份信息
    - userName: 用户名称, 唯一的属性
    - chatCid 用户某个对话的唯一id
    - chatParams 对话的参数信息
'''

import sqlite3
from typing import List, Optional, Tuple
from scripts.libs import LOGGER
from scripts.libs.cuuid import oruuid, reuuid


class UserSQL:
    def __init__(self, sqlFileName='users.db') -> None:
        # 简单的配置
        self.dbName = sqlFileName
        # 初始时,连接数据库
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()

        self.initUsersTable()
        self.initUsersChatsTable()
        self.initUsersSettingsTable()

    def initUsersTable(self):
        '''users表用来存放登录后的一些特有的用户属性
        '''
        # 创建user表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                uid TEXT UNIQUE,
                userName TEXT
            )
        ''')

        # 提交修改
        self.conn.commit()

    def initUsersSettingsTable(self):
        '''users_settings_table 表单,主要存放用户的一些操作行为,用uid来挂用户信息
        '''
        # 创建user表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users_settings_table (
                id INTEGER PRIMARY KEY,
                userName TEXT UNIQUE,
                chatSettings TEXT,
                proxySettings TEXT
            )
        ''')

        # 提交修改
        self.conn.commit()

    def print_all_user_settings(self):
        # 执行查询语句，获取表中的所有内容
        self.cursor.execute('SELECT * FROM users_settings_table')
        rows = self.cursor.fetchall()

        # 打印表中的所有内容
        if rows:
            for row in rows:
                print(row)
        else:
            print("No records found in users_settings_table.")

    def initUsersChatsTable(self):
        '''users_chats_table 表单,主要存放用户的一些操作行为,用uid来挂用户信息
        '''
        # 创建user表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users_chats_table (
                id INTEGER PRIMARY KEY,
                uid TEXT,
                userName TEXT,
                chatCid TEXT UNIQUE,
                chatParams TEXT
            )
        ''')

        # 提交修改
        self.conn.commit()

    def addUserLoginInfo(self, userName) -> str:
        '''根据用户名创建一个users表来存放相关信息,创建用户记录'''
        self.cursor.execute('SELECT id FROM users WHERE userName=?', (userName,))
        existingUser = self.cursor.fetchone()

        # 不存在的用户 创建新的条目
        if existingUser is None:
            uid = reuuid(20)
            LOGGER.info(f'SERVER add a new user: {userName}.')
            # 存入登录的属性
            self.cursor.execute("INSERT INTO users (userName, uid) VALUES (?,?)", (userName, uid,))
            self.cursor.execute(
                "INSERT INTO users_settings_table (userName,chatSettings,proxySettings) VALUES (?,?,?)", (userName, None, None))

            # 提交修改
            self.conn.commit()

            return uid
        else:
            self.cursor.execute('SELECT uid FROM users WHERE userName=?', (userName,))
            uid = self.cursor.fetchone()[0]
            LOGGER.info(f'User: {userName}. has already in USER SQL; uid: {uid}')
            return uid

    def addChatInfoForSpecUser(self, userName: str, chatParams: str) -> str:
        '''用户操作新建对话,这个时候需要生成一个唯一的chatCid,这个唯一的ChatCid也是生成后面存放具体的对话信息表的名称'''

        chatCid = oruuid(30)
        # 将cid和cname和user存入 users_chats_table
        self.cursor.execute(
            f"INSERT INTO users_chats_table (userName,chatCid,chatParams) VALUES (?,?,?)", (userName, chatCid, chatParams,))
        LOGGER.info(f'User: {userName} has created a chat channel: {chatCid}')

        # 提交更改
        self.conn.commit()

        # 返回唯一的对话表的名称
        return chatCid

    def deleteChatInfoForSpecUser(self, userName, chatCid) -> bool:
        '''删除指定用户和聊天表'''
        self.cursor.execute("DELETE FROM users_chats_table WHERE chatCid=?", (chatCid,))
        LOGGER.info(f'User: {userName} has deleted chat {chatCid} information.')

        # 提交更改并关闭连接
        self.conn.commit()

    def setChatParamsForSpecUser(self, chatCid, chatParams) -> bool:
        '''根据指定的ID修改对应的chat的设置params内容'''
        self.cursor.execute(
            f"UPDATE users_chats_table SET chatParams = ? WHERE chatCid = ?", (chatParams, chatCid,))
        self.conn.commit()

    def checkChatCidbyUserName(self, userName, chatCid) -> bool:
        '''判断对应用户名下的ChatCid是不是还存在,有没有被其他用户给删除'''
        self.cursor.execute(
            "SELECT 1 FROM users_chats_table WHERE userName=? AND chatCid=?", (userName, chatCid))
        bExit = self.cursor.fetchone()

        # 如果查询结果不为空，说明存在相同名称的cid
        if bExit:
            return True
        else:
            return False

    def getChatParamsByChatCid(self, chatCid) -> Optional[str]:
        '''根据对话用户身份和唯一的对话chatCid来找出对话的设置'''
        self.cursor.execute(
            "SELECT chatParams FROM users_chats_table WHERE chatCid = ?", (chatCid,))
        result = self.cursor.fetchone()
        if result:
            # 实际上要用的时候还要转成dict: json.loads(result[0])
            return result[0]
        else:
            return None

    def getAllChatCidNChatParams(self, userName) -> List[Tuple[str, str]]:
        '''在usermap表下获取指定username的全部cid和cname'''
        self.cursor.execute("SELECT chatCid, chatParams FROM users_chats_table WHERE userName=?", (userName,))
        rea: list = self.cursor.fetchall()
        return rea

    def getUserNameByChatCid(self, chatCid) -> str:
        '''根据chatCid来推到出userName的信息'''
        self.cursor.execute("SELECT userName FROM users_chats_table WHERE chatCid = ?", (chatCid,))
        result = self.cursor.fetchone()
        if result:
            # 返回userName
            return result[0]
        else:
            return None

    def setChatSettingsForSpecUser(self, userName: str, chatParams: str) -> str:
        '''将用户的默认的对话参数 存入数据库'''
        self.cursor.execute(f"UPDATE users_settings_table SET proxySettings=? WHERE userName=?", (chatParams, userName,))
        # 提交更改
        self.conn.commit()

    def getChatSettingsForSpecUser(self, userName: str) -> str:
        '''根据对话用户身份得到默认的对话的设置'''
        self.cursor.execute("SELECT chatSettings FROM users_settings_table WHERE userName = ?", (userName,))
        result = self.cursor.fetchone()
        if result:
            # 实际上要用的时候还要转成dict: json.loads(result[0])
            return result[0]
        else:
            return None

    def setProxySettingsForSpecUser(self, userName: str, proxySettings: str) -> str:
        '''将用户的默认的对话参数 存入数据库'''
        self.cursor.execute("UPDATE users_settings_table SET proxySettings=? WHERE userName=?", (proxySettings, userName))
        # 提交更改
        self.conn.commit()

    def getProxySettingsForSpecUser(self, userName: str) -> str:
        '''根据对话用户身份得到默认的对话的设置'''
        self.cursor.execute(
            "SELECT proxySettings FROM users_settings_table WHERE userName = ?", (userName,))
        result = self.cursor.fetchone()
        if result:
            # 实际上要用的时候还要转成dict: json.loads(result[0])
            return result[0]
        else:
            return None

    def releaseCursor(self):
        '''释放游标，关闭资源'''
        self.cursor.close()
