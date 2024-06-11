'''
#### 操作用户用GPT API对话的全部表单

用户创建一个对话 就会生成一张userName_chatCid的表 这个表是唯一的, 表内存放全部对话的消息

对于userName_chatCid的表 管理对话的一些消息属性:
    - id: 数据的主键
    - chatIid: 要表达的意思是对话内的item的id, 一条对话的一个随机的唯一标志
    - role: 角色,分为 user和assistant, system的在usersmap的chatParams里面
    - message: 具体的消息内容
    - tokens: 这个消息的tokens数量
'''
import sqlite3


class ChatSQL:
    def __init__(self, sqlFileName='chats.db', logger=None) -> None:
        # 简单的配置
        self.dbName = sqlFileName
        self.logger = logger
        # 初始时,连接chat.db数据库
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()

    def createTableByUserNameNChatCid(self, userName, chatCid):
        '''根据用户名和唯一的ChatCid属性来创建一个表,
         实际上输入的参数有多余,因为userName和chatCid都是唯一的标志'''
        # 创建聊天表
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {userName}_{chatCid} (
                id INTEGER PRIMARY KEY,
                chatIid TEXT,
                role TEXT,
                message TEXT,
                tokens INTEGER
            )
        ''')
        self.conn.commit()

    def addItemToSpecTable(self, userName, chatCid, chatIid, role, message, tokens):
        '''根据指定的chat table中(由userName_chatCid组成), 插入一条chat记录'''
        self.cursor.execute(
            f"INSERT INTO {userName}_{chatCid} (chatIid,role,message,tokens) VALUES (?,?,?,?)", (chatIid, role, message, tokens,))
        print(f'Chat item added to {userName}_{chatCid} table.')

        # 提交更改
        self.conn.commit()

    def deleteSpecTable(self, userName, chatCid):
        '''删除指定用户和聊天表'''
        self.cursor.execute(f"DROP TABLE IF EXISTS {userName}_{chatCid}")

        print(f'Chat table{userName}_{chatCid} deleted successfully.')
        # 提交更改并关闭连接
        self.conn.commit()

    def deleteItemInSpecTable(self, userName, chatCid, chatIid):
        self.cursor.execute(
            f"DELETE FROM {userName}_{chatCid} WHERE chatIid = ?", (chatIid,))

        print(f'Delete chat item {chatIid} in {userName}_{chatCid} table.')
        self.conn.commit()

    def getAllItemInSpecTable(self, userName, chatCid):
        '''查询指定用户和聊天表的所有聊天记录'''
        self.cursor.execute(f"SELECT * FROM {userName}_{chatCid}")
        items = self.cursor.fetchall()
        return items

    def getLastNItemsInSpecTable(self, userName, chatCid, n):
        '''查询指定用户和对话名称下的,倒数n个记录'''
        self.cursor.execute(
            f"SELECT * FROM {userName}_{chatCid} ORDER BY id DESC LIMIT ?", (n,))
        lastNitems = self.cursor.fetchall()
        return lastNitems

    def setItemInSpecTable(self, userName, chatCid, chatIid, message, tokens):
        '''根据指定的ID修改对应的chat的内容'''
        self.cursor.execute(
            f"UPDATE {userName}_{chatCid} SET message = ?, tokens = ? WHERE chatIid = ?", (message, tokens, chatIid,))
        self.conn.commit()

    def releaseCursor(self):
        '''释放游标，关闭资源'''
        self.cursor.close()
