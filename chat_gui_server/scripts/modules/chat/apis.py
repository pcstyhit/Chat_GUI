'''
从core中引入ChatHandle并且将其中的实现转换为FastAPI操作的异步方法
'''
import json
from .core import ChatHandle
from .tokens import Tokens
from .params import Params

from scripts.libs import getAbsPath
from scripts.modules.sql import getChatSQLHandle, releaseChatSQLHandle


class ChatAPI(ChatHandle):
    def __init__(self, user='test_user') -> None:
        super().__init__()
        self.user = user

        self.sql = getChatSQLHandle()
        self.param = Params()
        self.tkl = Tokens()

        self.prompt = []
        self.tokens = 0

        # 创建一个属于该用户的表
        self.initUserDB()
        self.chatCid = ''
        self.chatIid = -1

    async def azureChatStreamAPI(self):
        '''进行流式对话,不需要接受meesgae,从数据库获取prompt'''
        await self.getPrompt()
        response = self.azureChatStream(self.prompt)

        collected_chunks = []
        collected_messages = []
        collected_tokens = 0
        # 每次和websocket/SSE的通讯最好是定长的字符，减少前端VUE的刷新频率
        will_be_send_message = ""

        for chunk in response:
            collected_chunks.append(chunk)
            try:
                choice = chunk.choices
                if choice == []:
                    continue
                chunk_message = chunk.choices[0].delta.content
                chunk_token = self.tkl.getTokens(chunk_message)
                collected_tokens += chunk_token
                # 过滤掉为None的信息
                if chunk_message != None:
                    collected_messages.append(chunk_message)
                    will_be_send_message += chunk_message

                    # 判断长度，查看是否发送, 用字符串切片来做
                    if len(will_be_send_message) >= self.param.strLen:
                        yield will_be_send_message[:self.param.strLen], self.tokens+collected_tokens, self.chatIid
                        will_be_send_message = will_be_send_message[self.param.strLen:]
            except Exception as e:
                print(f'azureChatStream error >>> {e}')
                continue

        # 将剩余的消息全部返回给WEB
        yield will_be_send_message, self.tokens+collected_tokens, self.chatIid
        full_reply_content = ''.join(
            [m if m else '' for m in collected_messages])

        # print(f"Full conversation received: {full_reply_content}")
        # 更新数据库的值
        await self.setMessageWithTokens(Params.ASS, full_reply_content, collected_tokens)
        # return collected_messages

    def initUserDB(self):
        '''用户登录成功之后,肯定会有一个存放数据的表'''
        self.sql.addUser(self.user)

    async def getAllHistory(self):
        '''返回当前用户下的全部chat的关系, chat数据库的id和chat名称的关系是一个元组
         元组格式位(cid, cname)
        '''
        crlist = self.sql.queryAllCidNCname(self.user)
        rea = [{'chatCid': cr[0], 'chatName': cr[1]} for cr in crlist]
        return rea

    async def newChat(self, cname):
        '''根据对话名称创立对话的表'''
        chatCid = self.sql.addChat(self.user, cname)
        if chatCid != '':
            # set current chatCid.
            self.chatCid = chatCid
            return True, self.chatCid
        else:
            return False, ''

    async def loadChatHistory(self, chatCid) -> tuple:
        '''加载消息by chatCid'''
        # check if chatCid is exit.
        flag = self.sql.queryIfCidExit(self.user, chatCid)
        if not flag:
            return [], 0, 0, False, 'Chat has been deleted by others.'

        # reset the chatCid
        self.chatCid = chatCid
        msgList = self.sql.queryAllChatItems(self.user, self.chatCid)

        # reset the prompt
        firstPrompt = self.sql.queryFirstChatItem(self.user, self.chatCid)
        self.param.loadChatPrompt(firstPrompt[1], firstPrompt[2])

        # 复用self.prompt和self.tokens，因为对话时候self.prompt和self.tokens会重新刷新
        self.prompt = []
        self.tokens = 0

        # 排序历史对话
        startSit = len(msgList) - self.param.msgLen if len(msgList) - \
            self.param.msgLen > 0 else 0
        for lenI in range(0, len(msgList)):
            item = msgList[lenI]
            self.prompt.append(
                {'chatIid': item[0], 'role': item[1], 'content':  item[2]})
            if (lenI >= startSit):
                self.tokens += item[3]

        modelTokens = self.tkl.getMaxTokens()

        return self.prompt, self.tokens, modelTokens, True, 'successfully.'

    async def setChatParams(self, model, systemContent, passedMsg):
        '''设置system content promote的参数'''
        self.param.updateChatParam(systemContent, passedMsg)
        await self.setMessage(Params.SYS, systemContent)

    async def setUserMsg(self, msg: str) -> list:
        '''将用户的消息存入数据库,然后返回对应的item的id'''
        # 存入数据
        await self.setMessage(Params.USER, msg)
        # 查询插入的元素的ID，也就是最后一个元素的ID
        item: tuple = self.sql.queryLastNChatItems(self.user, self.chatCid, 1)
        self.chatIid = item[0][0]
        return self.chatIid

    async def getPrompt(self) -> list:
        '''从数据库中存入要发送的消息,并得到prompt
         msgList中的每个msg的格式是元组 msg = (1, 'user', 'Hello!', 10) type is <class 'tuple'> type is <class 'tuple'>
         其中的 msg[0]是数据库的id位, msg[1]是角色信息, msg[2]是消息, msg[3]是tokens数量
        '''
        # 获得prompt
        self.prompt = []
        self.tokens = 0
        msgList = self.sql.queryLastNChatItems(
            self.user, self.chatCid, self.param.msgLen)

        # 提前计算得到chatIid再递增得到数据库下次要存放的数据的chatIid
        self.chatIid += 1

        for lenI in range(len(msgList) - 1, -1, -1):
            self.prompt.append(
                {'role': msgList[lenI][1], 'content':  msgList[lenI][2]})
            self.tokens += msgList[lenI][3]

        # add system prompt
        self.prompt[0] = self.param.prompt

    async def setMessage(self, role, msg):
        '''这个函数是将消息存入数据库'''
        tokens = self.tkl.getTokens(msg)
        self.sql.addChatItem(self.user, self.chatCid,
                             role, msg, tokens)

    async def setMessageWithTokens(self, role, msg, tokens):
        '''将携带tokens信息的消息存入数据库,省去计算一步'''
        self.sql.addChatItem(self.user, self.chatCid, role, msg, tokens)

    async def deleteChat(self, chatCid):
        '''根据对话名称删除对话表'''
        try:
            self.sql.deleteChat(self.user, chatCid)
            return True
        except Exception as eMsg:
            print(f'deleteChat error : {eMsg}')
            return False

    async def deleteChatItemByID(self, iid: str):
        '''根据用户提供的id信息来删除数据库的那条信息'''
        try:
            self.sql.deleteChatItemById(self.user, self.chatCid, iid)
            return True
        except Exception as eMsg:
            print(f'deleteChatItem error : {eMsg}')
            return False

    async def editChatItemMsgByID(self, chatIid, msg):
        '''根据提供的chat的id和新消息, 对chatItem表的内容进行更新'''
        tokens = self.tkl.getTokens(msg)
        try:
            self.sql.changeChatItem(
                self.user, self.chatCid, chatIid, msg, tokens)
            return True
        except Exception as eMsg:
            print(f'deleteChatItem error : {eMsg}')
            return False
