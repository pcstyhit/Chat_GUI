'''
数据库管理的核心文件
'''
import logging
import sqlite3
import random
import string


class Chat:
    def __init__(self, name=None, logger=None) -> None:
        # 简单的配置
        self.dbName = 'chat.db' if name == None else name
        self.logger = None if logger == None else logger
        # 初始时,连接chat.db数据库
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()
        self.initDB()

    def initDB(self):
        '''创建一个chat.db的数据库来存放user和usermap,如果chat.db存在,不会覆盖它
         users 用来存放对话
         usermap 用来存放关于user和对话之间的关系
        '''
        # 创建user表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE
            )
        ''')

        # 创建usermap表
        self.cursor.execute('''  
            CREATE TABLE IF NOT EXISTS usermap (  
                id INTEGER PRIMARY KEY AUTOINCREMENT,  
                username TEXT,  
                cid INTEGER,  
                cname TEXT  
            )  
        ''')
        # 提交修改
        self.conn.commit()

    def generateCid(self, username, length=8):
        '''随机生成cid'''
        rcid = ''.join(random.choice(string.ascii_letters + string.digits)
                       for _ in range(length))
        bInChat = self.queryIfCidExit(username, rcid)
        if bInChat:
            self.generateCid(username)
        return rcid

    def addUser(self, username):
        '''根据用户名创建一个user表来存放相关信息,如果用户不存在,创建用户记录,存在则无操作'''
        self.cursor.execute(
            'SELECT id FROM users WHERE username=?', (username,))
        # 获取信息
        existing_user = self.cursor.fetchone()

        if existing_user is None:
            self.cursor.execute(
                "INSERT INTO users (username) VALUES (?)", (username,))
            print(f'[ Chat DB Log ]: User {username} created successfully.')
        else:
            print(f'[ Chat DB Log ]: User {username} already exists.')

        # 提交修改
        self.conn.commit()

    def addCID(self, username, cid, cname):
        '''向usermap表内插入指定的user和cid和cname'''
        self.cursor.execute(
            f"INSERT INTO usermap (username,cid,cname) VALUES (?,?,?)", (username, cid, cname))
        print(
            f'[ Chat DB Log ]: Chat Cid: {cid} and cname: {cname} of user: {username} added to usermap.')

        # 提交更改
        self.conn.commit()

    def addChat(self, username, chatname):
        '''根据用户名创建一个chat表来存放相关信息, 如果chat不存在,创建chat记录,存在则无操作'''
        cid = self.generateCid(username)
        # 将cid和cname和user存入usermap
        self.addCID(username, cid, chatname)

        # 存入对话
        self.cursor.execute(
            'SELECT id FROM users WHERE username=?', (username,))
        userID = self.cursor.fetchone()

        if userID is not None:
            userID = userID[0]

            # 创建聊天表
            self.cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {username}_{cid} (
                    id INTEGER PRIMARY KEY,
                    role TEXT,
                    message TEXT,
                    tokens INTEGER
                )
            ''')
            print(
                f'[ Chat DB Log ]: Chat table for user {username} and chat {chatname} created successfully.')
            # 提交更改
            self.conn.commit()
            return cid
        else:
            print(f'[ Chat DB Log ]: User {username} not found.')
            return ''

    def addChatItem(self, username, cid, role, message, tokens):
        '''根据指定的用户名和chat名称, 插入一条chat记录'''
        # 获取用户ID
        self.cursor.execute(
            'SELECT id FROM users WHERE username=?', (username,))
        userID = self.cursor.fetchone()

        if userID is not None:
            userID = userID[0]

            # 插入聊天记录
            self.cursor.execute(
                f"INSERT INTO {username}_{cid} (role,message,tokens) VALUES (?,?,?)", (role, message, tokens))
            print(f'[ Chat DB Log ]: Chat item added to {username}_{cid}.')
        else:
            print(f'[ Chat DB Log ]: User {username} not found.')

        # 提交更改
        self.conn.commit()

    def deleteUser(self, username):
        '''删除指定的user'''
        # 从users表中删除用户记录
        self.cursor.execute("DELETE FROM users WHERE username=?", (username,))
        # 从usermap删除全部的对话信息
        self.cursor.execute(
            "DELETE FROM usermap WHERE username=?", (username,))
        print(f'[ Chat DB Log ]: User {username} deleted.')
        # 提交修改
        self.conn.commit()

    def deleteChat(self, username, cid):
        '''删除指定用户和聊天表'''
        self.cursor.execute(f"DROP TABLE IF EXISTS {username}_{cid}")
        self.cursor.execute("DELETE FROM usermap WHERE cid=?", (cid,))
        print(
            f'[ Chat DB Log ]: Chat table for user {username} and chat {cid} deleted successfully.')

        # 提交更改并关闭连接
        self.conn.commit()

    def deleteNthChaItem(self, username, cid, n):
        '''删除指定用户和对话名称下的第n个记录'''
        # 查询第N个元素的ID
        self.cursor.execute(
            f"SELECT id FROM {username}_{cid} ORDER BY id LIMIT {n - 1},1")
        nth_item_id = self.cursor.fetchone()

        if nth_item_id is not None:
            nth_item_id = nth_item_id[0]

            # 删除第N个元素
            self.cursor.execute(
                f"DELETE FROM {username}_{cid} WHERE id=?", (nth_item_id,))
            print(
                f'[ Chat DB Log ]: Item at position {n} deleted for user {username} and chat {cid}.')
        else:
            print(
                f'[ Chat DB Log ]: No item found at position {n} to delete for user {username} and chat {cid}.')

        # 提交更改并关闭连接
        self.conn.commit()

    def deleteChatItemById(self, username, cid, id):
        self.cursor.execute(
            f"DELETE FROM {username}_{cid} WHERE id = ?", (id,))
        print(
            f'[ Chat DB Log ]: Delete chat item {id} in {username} : {cid} successfully.')
        self.conn.commit()

    def queryAllCidNCname(self, username) -> list:
        '''在usermap表下获取指定username的全部cid和cname'''
        self.cursor.execute(
            "SELECT cid, cname FROM usermap WHERE username=?", (username,))
        cid_cname_list = self.cursor.fetchall()
        return cid_cname_list

    def queryIfCidExit(self, username, cid) -> bool:
        '''判断当前用户下是否已经存在了相同名称的cid'''
        self.cursor.execute(
            "SELECT 1 FROM usermap WHERE username=? AND cid=?", (username, cid))
        bExit = self.cursor.fetchone()

        # 如果查询结果不为空，说明存在相同名称的cid
        if bExit:
            return True
        else:
            return False

    def queryAllChat(self, username) -> list:
        '''获取指定用户下的全部chat表'''
        # 获取用户ID
        self.cursor.execute(
            'SELECT id FROM users WHERE username=?', (username,))
        userID = self.cursor.fetchone()
        chatTableList = []

        if userID is not None:
            userID = userID[0]

            # 查询用户的所有聊天表
            self.cursor.execute(
                f"SELECT name FROM sqlite_master WHERE type='table' AND name LIKE ?", (f'{username}_%',))
            chatTableList = self.cursor.fetchall()
        else:
            print(f'[ Chat DB Log ]: User {username} not found.')

        return chatTableList

    def queryAllUsers(self) -> list:
        '''获取chat.db下的全部用户表'''
        # 查询所有用户
        self.cursor.execute("SELECT username FROM users")
        users = self.cursor.fetchall()
        return users

    def queryAllChatItems(self, username, cid):
        '''查询指定用户和聊天表的所有聊天记录'''
        self.cursor.execute(f"SELECT * FROM {username}_{cid}")
        items = self.cursor.fetchall()
        return items

    def queryLastNChatItems(self, username, cid, n):
        '''查询指定用户和对话名称下的,倒数n个记录'''
        self.cursor.execute(
            f"SELECT * FROM {username}_{cid} ORDER BY id DESC LIMIT ?", (n,))
        lastNitems = self.cursor.fetchall()
        return lastNitems

    def queryFirstChatItem(self, username, cid):
        '''查询指定用户和聊天表的第一个聊天记录'''
        self.cursor.execute(
            f"SELECT * FROM {username}_{cid} ORDER BY id ASC LIMIT 1")
        firstItem = self.cursor.fetchone()
        return firstItem

    def queryIfIDExit(self, username, cid, id):
        self.cursor.execute(
            f"SELECT EXISTS(SELECT 1 FROM {username}_{cid} WHERE id = ?)", (id,))
        result = self.cursor.fetchone()[0]
        self.conn.close()
        return bool(result)

    def changeChatItem(self, username, cid, id, message, tokens):
        '''根据指定的ID修改对应的chat的内容'''
        self.cursor.execute(
            f"UPDATE {username}_{cid} SET message = ?, tokens = ? WHERE id = ?", (message, tokens, id))
        self.conn.commit()

    def releaseCursor(self):
        '''释放游标，关闭资源'''
        self.cursor.close()


def test_chatdb():
    cdb = Chat()
    # 增加用户
    cdb.addUser('user1')
    cdb.addUser('user2')
    cdb.addUser('user3')

    # 查询当前的全部用户[user1, user2 user3]
    users = cdb.queryAllUsers()
    print(f">>> All user: {users}")

    # user1创建两个聊天表
    chat1 = cdb.addChat("user1", "chat1")
    cdb.addChat("user1", "chat2")

    # 查询user1的所有聊天表
    chat_tables = cdb.queryAllChat("user1")
    print(f'>>> Chat tables for user1: {chat_tables}')

    # user1的chat1表内插入对话
    cdb.addChatItem("user1", chat1, "user", "Hello!", 10)
    cdb.addChatItem("user1", chat1, "user", "World!", 20)
    cdb.addChatItem("user1", chat1, "robot", "I!", 30)
    cdb.addChatItem("user1", chat1, "robot", "AM!", 40)
    cdb.addChatItem("user1", chat1, "robot", "Python!", 50)

    # user1和chat1表内的的所有聊天记录
    chat_items = cdb.queryAllChatItems("user1", chat1)
    print(f'>>> Chat items for user1 and chat1: {chat_items}')

    # 删除user1和chat1表内的第3条记录
    cdb.deleteNthChaItem("user1", chat1, 3)
    cdb.addChatItem("user1", chat1, "gpt", "Python!", 50)
    cdb.deleteNthChaItem("user1", chat1, 3)

    # user1和chat1表内的所有聊天记录
    chat_items = cdb.queryAllChatItems("user1", chat1)
    print(f'>>> After delete Chat items for user1 and chat1: {chat_items}')

    # user1和chat1表内的最后和第一个记录
    last_3_items = cdb.queryLastNChatItems("user1", chat1, 3)
    first_item = cdb.queryFirstChatItem("user1", chat1)
    print(
        f'>>> Last 3 chat items and first item  for user1 and chat1: {last_3_items}  {first_item} type is {type(first_item)}')

    # 删除指定用户和聊天表
    cdb.deleteChat("user1", chat1)

    # 查询user1的所有聊天表
    chat_tables = cdb.queryAllChat("user1")
    print(f'>>> Chat tables for user1: {chat_tables}')

    # 删除指定用户的所有表
    cdb.deleteUser("user1")

    # 查询当前的全部用户[user1, user2 user3]
    users = cdb.queryAllUsers()
    print(f">>> All user: {users}")

    cdb.releaseCursor()


if __name__ == '__main__':
    test_chatdb()
