import fastapi
import asyncio
from pydantic import BaseModel
from scripts.libs import dict2Str, str2Dict
from scripts.modules.umm import authenticateUser, getChatHandle, getUser

CHAT_ROUTE = fastapi.APIRouter()


class AllHistoryRequest(BaseModel):
    '''allHistoryAPI的请求体, 实际上没有内容'''
    pass


class AllHistoryResponse(BaseModel):
    '''allHistoryAPI的应答体, 返回全部的列表即可'''
    data: list = []
    log: str = ''


class NewChatRequest(BaseModel):
    '''newChatAPI请求'''
    chatName: str


class NewChatResponse(BaseModel):
    '''startChat响应内容的格式'''
    flag: bool = False
    chatCid: str = ''    # 用于对话的唯一标志
    log: str = ''


class LoadChatHistoryRequest(BaseModel):
    '''加载对话历史的函数的请求体'''
    chatCid: str  # 对话的名称
    timeout: int


class LoadChatHistoryResponse(BaseModel):
    '''加载对话历史的函数的响应体'''
    history: list = []  # 对话的历史记录
    tokens: int = 0
    flag: bool = False
    log: str = ''


class DeleteChatRequest(BaseModel):
    '''deleteChatAPI前端请求体内的参数'''
    chatCid: str
    timeout: int


class DeleteChatResponse(BaseModel):
    '''deleteChatAPI前端response的参数'''
    flag: bool = False
    log: str = ''


class EditChatItemRequest(BaseModel):
    '''editChatItemAPI前端请求体内的参数'''
    chatIid: str    # 对话每个元素的唯一标志
    msg: str
    timeout: int


class EditChatItemResponse(BaseModel):
    '''editChatItemAPI前端response的参数'''
    flag: bool = False
    log: str = ''


class DeleteChatItemRequest(BaseModel):
    '''deletChatItemAPI前端请求体内的参数'''
    chatIid: str
    timeout: int


class DeleteChatItemResponse(BaseModel):
    '''deletChatItemAPI前端response的参数'''
    flag: bool = False
    log: str = ''


class SetUserMsgRequest(BaseModel):
    '''Chat的中user的消息的请求体, 接受消息存入数据库, 并返回对话的唯一chatIid'''
    msg: str
    timeout: int


class SetUserMsgResponse(BaseModel):
    '''Chat的中user的消息的应答体, 返回对话的唯一chatIid'''
    flag: bool = False
    chatIid: str = ''
    log: str = ''


@CHAT_ROUTE.get('/chat/allHistory')
async def allHistoryAPI(user: str = fastapi.Depends(authenticateUser)):
    '''获取全部的对话历史记录的API'''
    rea = AllHistoryResponse()
    handle = getChatHandle(user)
    rea.data = await handle.getAllHistory()
    return rea


@CHAT_ROUTE.post('/chat/addNewChat')
async def addNewChatAPI(item: NewChatRequest, user: str = fastapi.Depends(authenticateUser)):
    rea = NewChatResponse()
    handle = getChatHandle(user)
    try:
        rea.chatCid = await handle.addNewChat(item.chatName)
        rea.flag = True
    except Exception as e:
        print(f'addNewChatAPI error: {e}')
    return rea


@CHAT_ROUTE.post('/chat/getSpecChatHistory')
async def getSpecChatHistoryAPI(item: LoadChatHistoryRequest, user: str = fastapi.Depends(authenticateUser)):
    rea = LoadChatHistoryResponse()
    handle = getChatHandle(user)
    rea.history, rea.tokens, rea.flag, rea.log = await handle.getSpecChatHistory(item.chatCid)
    return rea


@CHAT_ROUTE.post('/chat/deleteChat')
async def deleteChatAPI(item: DeleteChatRequest, user: str = fastapi.Depends(authenticateUser)):
    rea = DeleteChatResponse()
    handle = getChatHandle(user)
    rea.flag = await handle.deleteChat(item.chatCid)
    return rea


@CHAT_ROUTE.post('/chat/setUserMsg')
async def setUserMsgAPI(item: SetUserMsgRequest, user: str = fastapi.Depends(authenticateUser)):
    rea = SetUserMsgResponse()
    handle = getChatHandle(user)
    try:
        rea.chatIid = await handle.setUserMsg(item.msg)
        rea.flag = True
    except Exception as eMsg:
        print(f"Set User Msg failed! {eMsg}")
    return rea


@CHAT_ROUTE.post('/chat/editChatItem')
async def editChatItemAPI(item: EditChatItemRequest, user: str = fastapi.Depends(authenticateUser)):
    rea = EditChatItemResponse()
    handle = getChatHandle(user)
    rea.flag = await handle.editChatItemMsgByID(item.chatIid, item.msg)
    return rea


@CHAT_ROUTE.post('/chat/deleteChatItem')
async def deleteChatItemAPI(item: DeleteChatItemRequest, user: str = fastapi.Depends(authenticateUser)):
    rea = DeleteChatItemResponse()
    handle = getChatHandle(user)
    rea.flag = await handle.deleteChatItemByID(item.chatIid)
    return rea


# ==================================================
# ✨ Chat Stream / 普通对话的API操作函数, 没有用SSE直接用websocket来操作
# ==================================================

class ChatResponse(BaseModel):
    '''Chat对话的应答体'''
    flag: bool = False  # 是否输出完成的开关量
    data: str = ''  # 具体的内容
    tokens: int = 0
    chatIid: str = ''  # 对话对象的唯一标志


@CHAT_ROUTE.websocket('/chat/{wsid}')
async def websocket_endpoint(websocket: fastapi.WebSocket,
                             wsid: str):
    '''websocket是一个长连接,理论上希望创建成功之后,同一个用户就不应该再调用这个接口创建新的,
    通过维护一个映射关系, 来判断用户身份
    用户登录时,分配websocket的wsid值
    同时对于asyncio.sleep(0)有解释：
        - await asyncio.sleep(0)在Python的异步编程中通常用于“让出控制权”。当你在协程中使用await asyncio.sleep(0)时,你实际上是在告诉事件循环：“我现在没有什么要做的,你可以去处理其他的任务。”

        - 在你的情况中,这些“其他的任务”可能包括处理WebSocket的数据发送。当你调用websocket.send_text(resp)时,你并不是立即发送数据,而是将数据放入一个发送缓冲区,等待事件循环在适当的时候发送它。当你使用await asyncio.sleep(0)时,你给了事件循环一个机会去处理这个发送任务。

        - 但请注意,这只是一个可能的解释,实际效果可能会因为具体情况而有所不同。在某些情况下,使用await asyncio.sleep(0)可能并不会产生预期的效果。比如,如果事件循环有其他更高优先级的任务要处理,那么即使你使用了await asyncio.sleep(0),事件循环也可能选择先处理那些任务。
    '''

    await websocket.accept()
    user = getUser(wsid)
    connection_closed = False
    while True:
        try:
            data = await websocket.receive_text()
        except Exception:
            # 客户端断开连接，退出循环
            connection_closed = True
            break

        item = str2Dict(data)
        # 如果正常通讯, 暂时不对消息内容进行判断，后续可以通过字符来判断是否要主动关闭ws
        isStreamResponse = item.get('data')
        rea = ChatResponse()
        handle = getChatHandle(user)

        async for (chunk, tokens, chatIid) in handle.azureChatAPI(isStreamResponse):
            rea.data = f'{chunk}'
            rea.tokens = tokens
            rea.chatIid = chatIid
            resp, _ = dict2Str(rea.__dict__)
            try:
                if not connection_closed:
                    await websocket.send_text(resp)
                await asyncio.sleep(0)
            except Exception:
                # 客户端断开连接，退出循环
                connection_closed = True
                break

        rea.flag = True
        resp, _ = dict2Str(rea.__dict__)
        try:
            if not connection_closed:
                await websocket.send_text(resp)
            await asyncio.sleep(0)
        except Exception:
            # 客户端断开连接，退出循环
            connection_closed = True
            break


# ''' '''
# 根据对话的唯一标识 chatCid来从数据库获得配置
# ''' '''
class GetChatParamsRequest(BaseModel):
    '''getChatParamsAPI请求体的格式'''
    chatCid: str  # 用于对话的唯一标志


class GetChatParamsResponse(BaseModel):
    '''getChatParamsAPI返回的response的格式'''
    flag: bool = False
    log: str = ''
    data: dict = {}


@CHAT_ROUTE.post('/chat/getChatParams')
async def getChatParamsAPI(item: GetChatParamsRequest, user: str = fastapi.Depends(authenticateUser)):
    rea = GetChatParamsResponse()
    handle = getChatHandle(user)
    rea.data = await handle.getChatParams(item.chatCid)
    rea.flag = True
    return rea


'''
## SetChatParams的请求
## 根据对话的唯一标识 chatCid来对当前的对话的设置进行修改
## 注意这个函数的数据 非常需要前后端的变量名一致
'''


class SetChatParamsRequest(BaseModel):
    '''getChatParamsAPI请求体的格式'''
    chatCid: str  # 用于对话的唯一标志
    data: dict  # 具体的数据


class SetChatParamsResponse(BaseModel):
    '''getChatParamsAPI返回的response的格式'''
    flag: bool = False
    log: str = ''


@CHAT_ROUTE.post('/chat/setChatParams')
async def setChatParamsAPI(item: SetChatParamsRequest, user: str = fastapi.Depends(authenticateUser)):
    rea = SetChatParamsResponse()
    handle = getChatHandle(user)
    try:
        await handle.setChatParams(item.chatCid, item.data)
        rea.flag = True
    except Exception as e:
        print(f"Get chat: {item.chatCid} error: {e}")

    return rea
