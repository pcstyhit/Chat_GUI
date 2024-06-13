'''
从core中引入ChatHandle并且将其中的实现转换为FastAPI操作的异步方法
'''
import json
import typing
from .core import ChatHandle
from .params import Params

from scripts.libs import oruuid
from scripts.modules.sql import UserSQL, ChatSQL, getUserSQLHandle, getChatSQLHandle


class ChatAPI(ChatHandle):
    def __init__(self, user='test_user') -> None:
        super().__init__()

        self.userName = user                        # 当前的用户名
        self.chatCid = ''                           # chatCid 表示这一个对话的唯一ID
        self.userSql: UserSQL = getUserSQLHandle()  # 操作用户行为的数据库
        self.chatSql: ChatSQL = getChatSQLHandle()  # 操作对话数据的处理器
        self.chatParams = Params()                  # 存放当前对话的所有配置参数
        self.chatPrompts = []                       # 存放当前对话要发送的提示消息
        self.chatTokens = 0                         # 当前消息消耗的令牌数量统计

        self.chatIid = -1                           # chatIid 表示对话中每条消息的ID，也是数据库中存放元素的ID

    async def azureChatStreamAPI(self):
        '''进行流式对话,不需要接受meesgae, 这个函数是setUserMsg之后调用的, 此时已经从数据库获取prompt'''
        self.chatIid = oruuid()
        response = self.azureChatStream(self.chatPrompts,
                                        max_tokens=self.chatParams.maxResponseTokens,
                                        temperature=self.chatParams.temperature,
                                        top_p=self.chatParams.topP,
                                        stop=self.chatParams.stopSequence,
                                        frequency_penalty=self.chatParams.frequecyPenaty,
                                        presence_penalty=self.chatParams.presentPenaty,
                                        timeout=self.chatParams.chatWithGptTimeout)

        allMessages = []

        for chunk in response:
            try:
                choice = chunk.choices
                if choice == []:
                    continue

                chunkMsg = chunk.choices[0].delta.content

                # 过滤掉为None的信息, 然后拼接
                if chunkMsg != None:
                    allMessages.append(chunkMsg)
                    chunkToken = self.chatParams.getTokens(chunkMsg)
                    self.chatTokens += chunkToken

                    yield chunkMsg, self.chatTokens, self.chatIid

            except Exception as e:
                print(f'azureChatStream error >>> {e}')
                continue

        # 更新数据库的值
        await self.setMessageWithTokens(Params.ASS, ''.join([m if m else '' for m in allMessages]), self.chatTokens)

    async def azureChatSyncAPI(self):
        '''获取非流式的API对话返回结果, 这个函数是setUserMsg之后调用的, 此时已经从数据库获取prompt'''
        self.chatIid = oruuid()
        outgoingMsg, outgoingTokens = self.azureChatSync(self.chatPrompts,
                                                         max_tokens=self.chatParams.maxResponseTokens,
                                                         temperature=self.chatParams.temperature,
                                                         top_p=self.chatParams.topP,
                                                         stop=self.chatParams.stopSequence,
                                                         frequency_penalty=self.chatParams.frequecyPenaty,
                                                         presence_penalty=self.chatParams.presentPenaty,
                                                         timeout=self.chatParams.chatWithGptTimeout)

        yield outgoingMsg, self.chatTokens+outgoingTokens, self.chatIid
        await self.setMessageWithTokens(Params.ASS, outgoingMsg, outgoingTokens)

    async def getAllHistory(self):
        '''返回当前用户下的全部chat的关系, chat数据库的id和chat名称的关系是一个元组
         元组格式位(cid, cname)
        '''
        crlist = self.userSql.getAllChatCidNChatName(self.userName)
        rea = [{'chatCid': cr[0], 'chatName': cr[1]} for cr in crlist]
        return rea

    async def addNewChat(self, chatName) -> str:
        '''根据对话名称创立对话的表, 创建成功会返回一个特意的chatCid给到WEB
         这个chatCid可以用来作为SSE/Websocket请求的URL参数,来做流更新对话的区分
        '''
        allParams = json.dumps(self.chatParams.getCurrentParams())
        # 将最开始的配置参数存入数据库, 其实可以不放入任何内容,但是只是保证操作的统一
        self.chatCid = self.userSql.addChatInfoForSpecUser(
            self.userName, chatName, allParams)

        # 创建一个存放这个新对话的表单到chatSQL里
        self.chatSql.createTableByUserNameNChatCid(self.userName, self.chatCid)

        return self.chatCid

    async def getSpecChatHistory(self, chatCid) -> typing.Tuple[list, int, bool, str]:
        '''根据对话的Cid,也就是这个对话的唯一id, 加载特定的消息
        后面用到的 `msgList` 其中每个msg的格式是元组: `msg = (1, 'TYR_YGHGH', 'user', 'Hello!', 10)`
         - msg[0]是数据库的id位,
         - msg[1]是chatIid
         - msg[2]是角色信息,
         - msg[3]是消息,
         - msg[4]是tokens数量
        '''
        flag = self.userSql.checkChatCidbyUserName(self.userName, chatCid)
        if not flag:
            return [], 0, False, 'Chat has been deleted by others.'

        # 重置当前的chatCid，也就是这个操作表示切换了对话历史
        self.chatCid = chatCid
        msgList = self.chatSql.getAllItemInSpecTable(
            self.userName, self.chatCid)

        # 获取chatHistory
        chatHistoy = []
        tokens = 0
        for lenI in range(0, len(msgList)):
            item = msgList[lenI]
            chatHistoy.append(
                {'chatIid': item[1], 'role': item[2], 'content':  item[3]})

            # 达到可以计算tokens的下标
            if lenI >= len(msgList) - self.chatParams.passedMsgLen:
                tokens += item[4]

        return chatHistoy, tokens, True, 'successfully.'

    async def getChatParams(self, chatCid) -> dict:
        '''根据用户名和唯一的对话ChatCid来从数据库中加载对话的配置'''
        # 新建对话返回默认的值
        if chatCid == "" or chatCid == None:
            return self.chatParams.getDefaultParams()

        strData = self.userSql.getChatParamsByChatCid(chatCid)
        return json.loads(strData)

    async def setChatParams(self, chatCid, data: dict) -> None:
        '''根据用户名和唯一的对话ChatCid来设置数据库中里对应条目的值
        如果chatCid对应是当前的对话,那需要更新当前的self.params的属性
        '''
        self.userSql.setChatParamsForSpecUser(chatCid, json.dumps(data))

        # 是不是要更新当前的配置
        if chatCid == self.chatCid:
            self.chatParams.updateCurrentParams(data)
            # 更新GPT模型参数
            self.updateAzureGPTModel(endPoint=self.chatParams.endPoint,
                                     apiKey=self.chatParams.apiKey,
                                     apiVersion=self.chatParams.apiVersion,
                                     deployment=self.chatParams.deployment)

    async def setUserMsg(self, msg: str) -> tuple:
        '''将用户的消息存入数据库,然后返回对应的item的chatIid'''
        await self.setMessage(Params.USER, msg)
        # 返回一个chatIid
        self.chatIid = oruuid()
        # 判断tokens是不是达到最大了
        flag = await self.getPrompt(self.chatParams.passedMsgLen)
        return flag, self.chatIid, self.chatTokens

    async def getPrompt(self, passedMsgLen) -> bool:
        '''从数据库中存入要发送的消息,并得到prompt
         `msgList` 其中每个msg的格式是元组: `msg = (1, 'TYR_YGHGH', 'user', 'Hello!', 10)`
         - msg[0]是数据库的id位,
         - msg[1]是chatIid
         - msg[2]是角色信息,
         - msg[3]是消息,
         - msg[4]是tokens数量
        '''
        # 获得prompt
        self.chatPrompts = self.chatParams.promptTemplate + []
        self.chatTokens = 0
        msgList = self.chatSql.getLastNItemsInSpecTable(
            self.userName, self.chatCid, passedMsgLen)

        for lenI in range(len(msgList) - 1, -1, -1):
            self.chatPrompts.append(
                {'role': msgList[lenI][2], 'content':  msgList[lenI][3]})
            self.chatTokens += msgList[lenI][4]

        if self.chatTokens > int(self.chatParams.maxTokens):
            if passedMsgLen - 1 > 0:
                passedMsgLen = passedMsgLen - 1
                return await self.getPrompt(passedMsgLen)
            else:
                return False

        return True

    async def setMessage(self, role, msg):
        '''这个函数是将消息存入数据库'''
        tokens = self.chatParams.getTokens(msg)
        self.chatSql.addItemToSpecTable(
            self.userName, self.chatCid, self.chatIid, role, msg, tokens)

    async def setMessageWithTokens(self, role, msg, tokens):
        '''将携带tokens信息的消息存入数据库,省去计算一步'''
        self.chatSql.addItemToSpecTable(
            self.userName, self.chatCid, self.chatIid, role, msg, tokens)

    async def deleteChat(self, chatCid):
        '''根据对话名称删除对话表'''
        try:
            # 删除有关的用户操作的数据
            self.userSql.deleteChatInfoForSpecUser(self.userName, chatCid)
            # 删除存放全部对话列表的表单
            self.chatSql.deleteSpecTable(self.userName, chatCid)
            return True
        except Exception as eMsg:
            print(f'deleteChat error : {eMsg}')
            return False

    async def deleteChatItemByID(self, chatIid: str):
        '''根据用户提供的id信息来删除数据库的那条信息'''
        try:
            self.chatSql.deleteItemInSpecTable(
                self.userName, self.chatCid, chatIid)
            return True
        except Exception as eMsg:
            print(f'deleteChatItem error : {eMsg}')
            return False

    async def editChatItemMsgByID(self, chatIid, msg):
        '''根据提供的chat的id和新消息, 对chatItem表的内容进行更新'''
        tokens = self.chatParams.getTokens(msg)
        try:
            self.chatSql.setItemInSpecTable(
                self.userName, self.chatCid, chatIid, msg, tokens)
            return True
        except Exception as eMsg:
            print(f'deleteChatItem error : {eMsg}')
            return False
