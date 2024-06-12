'''
#### 管理一些用户属性的SQL的handle

UserSQL管理两张表: users 和 usersmap, 其中: 

对于users表单的信息 主要管理登录的一些特有的用户属性:
    - id: 数据的主键
    - uid: 用户的唯一身份id, 可以是登录时会分配, uid适合拓展登录情况 没有做, 先埋坑👻
    - userName: 用户名称, 这个也是唯一的

对于usersmap表单,主要存放用户的一些操作行为:
    - id: 数据库的id标志
    - uid 用户的唯一身份信息
    - userName: 用户名称, 唯一的属性
    - chatCid 用户某个对话的唯一id
    - chatName 对话的名称
    - chatParams 对话的参数信息
'''

import sqlite3
from scripts.libs import oruuid, reuuid


class UserSQL:
    def __init__(self, sqlFileName='users.db', logger=None) -> None:
        # 简单的配置
        self.dbName = sqlFileName
        self.logger = logger
        # 初始时,连接数据库
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()

        self.initUsersTable()
        self.initUsersMapTable()

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

    def initUsersMapTable(self):
        '''usersmap表单,主要存放用户的一些操作行为,用uid来挂用户信息
        '''
        # 创建user表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usersmap (
                id INTEGER PRIMARY KEY,
                uid TEXT,
                userName TEXT,
                chatCid TEXT UNIQUE,
                chatName TEXT,
                chatParams TEXT
            )
        ''')

        # 提交修改
        self.conn.commit()

    def addUserLoginInfo(self, userName):
        '''根据用户名创建一个users表来存放相关信息,创建用户记录'''
        uid = reuuid(20)
        self.cursor.execute(
            'SELECT id FROM users WHERE userName=?', (userName,))
        # 获取信息
        existing_user = self.cursor.fetchone()

        if existing_user is None:
            print(f'Add a new user: {userName}.')

        # 存入登录的属性
        self.cursor.execute(
            "INSERT INTO users (userName, uid) VALUES (?,?)", (userName, uid,))

        # 提交修改
        self.conn.commit()

        return uid

    def addChatInfoForSpecUser(self, userName, chatName, chatParams) -> str:
        '''用户操作新建对话,这个时候需要生成一个唯一的chatCid,这个唯一的ChatCid也是生成后面存放具体的对话信息表的名称'''

        chatCid = oruuid(30)
        # 将cid和cname和user存入usersmap
        self.cursor.execute(
            f"INSERT INTO usersmap (userName,chatCid,chatName,chatParams) VALUES (?,?,?,?)", (userName, chatCid, chatName, chatParams,))
        print(
            f'User: {userName} has created a chat channel: {chatCid}')

        # 提交更改
        self.conn.commit()

        # 返回唯一的对话表的名称
        return chatCid

    def deleteChatInfoForSpecUser(self, userName, chatCid):
        '''删除指定用户和聊天表'''
        self.cursor.execute("DELETE FROM usersmap WHERE chatCid=?", (chatCid,))
        print(f'User: {userName} has deleted chat {chatCid} information.')

        # 提交更改并关闭连接
        self.conn.commit()

    def setChatParamsForSpecUser(self, chatCid, chatParams):
        '''根据指定的ID修改对应的chat的设置params内容'''
        self.cursor.execute(
            f"UPDATE usersmap SET chatParams = ? WHERE chatCid = ?", (chatParams, chatCid,))
        self.conn.commit()

    def checkChatCidbyUserName(self, userName, chatCid) -> bool:
        '''判断对应用户名下的ChatCid是不是还存在,有没有被其他用户给删除'''
        self.cursor.execute(
            "SELECT 1 FROM usersmap WHERE userName=? AND chatCid=?", (userName, chatCid))
        bExit = self.cursor.fetchone()

        # 如果查询结果不为空，说明存在相同名称的cid
        if bExit:
            return True
        else:
            return False

    def getChatParamsByChatCid(self, chatCid):
        '''根据对话用户身份和唯一的对话chatCid来找出对话的设置'''
        self.cursor.execute(
            "SELECT chatParams FROM usersmap WHERE chatCid = ?", (chatCid,))
        result = self.cursor.fetchone()
        if result:
            # 实际上要用的时候还要转成dict: json.loads(result[0])
            return result[0]
        else:
            return None

    def getAllChatCidNChatName(self, userName) -> list:
        '''在usermap表下获取指定username的全部cid和cname'''
        self.cursor.execute(
            "SELECT chatCid, chatName FROM usersmap WHERE userName=?", (userName,))
        rea: list = self.cursor.fetchall()
        return rea

    def getUserNameByChatCid(self, chatCid) -> str:
        '''根据chatCid来推到出userName的信息'''
        self.cursor.execute(
            "SELECT userName FROM usersmap WHERE chatCid = ?", (chatCid,))
        result = self.cursor.fetchone()
        if result:
            # 返回userName
            return result[0]
        else:
            return None

    def releaseCursor(self):
        '''释放游标，关闭资源'''
        self.cursor.close()
