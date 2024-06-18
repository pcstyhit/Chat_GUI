import fastapi
import asyncio
from pydantic import BaseModel
from scripts.libs import dict2Str, str2Dict, CONF
from scripts.modules.umm import authenticateUser, getChatHandle, getChatHandleByChatCid

CHAT_ROUTE = fastapi.APIRouter()


# ==================================================
# 📜 allHistoryAPI 从数据库拿当前用户的全部对话记录
# 一条对话记录包括对话的名称,以及它的唯一的chatCid
# ==================================================

class AllHistoryResponse(BaseModel):
    '''allHistoryAPI的应答体, 返回全部的列表即可'''
    data: list = []
    log: str = ''


@CHAT_ROUTE.get('/chat/allHistory')
async def allHistoryAPI(user: str = fastapi.Depends(authenticateUser)):
    '''获取全部的对话历史记录的API'''
    rea = AllHistoryResponse()
    handle = getChatHandle(user)
    rea.data = await handle.getAllHistory()
    return rea


# ==================================================
# ➕ addNewChatAPI 根据新的对话名称创建一个对话表
# 对话名称可以重复因为对话表的唯一标识是chatCid
# 直接在数据库创建一张存对话记录的表
# 返回这个新建对话的chatCid
# ==================================================

class NewChatRequest(BaseModel):
    '''newChatAPI请求'''
    chatName: str


class NewChatResponse(BaseModel):
    '''startChat响应内容的格式'''
    flag: bool = False
    chatCid: str = ''    # 用于对话的唯一标志
    log: str = ''


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


# ==================================================
# 📖 getSpecChatHistoryAPI 从数据库拿当前用户的唯一chatCid的全部对话历史记录
# 根据指定的chatCid来获取具体的内容
# 返回的response会携带下次要发送的消息消耗的tokens数量
# ==================================================

class GetSpecChatHistoryRequest(BaseModel):
    '''加载对话历史的函数的请求体'''
    chatCid: str  # 对话的名称


class GetSpecChatHistoryResponse(BaseModel):
    '''加载对话历史的函数的响应体'''
    history: list = []  # 对话的历史记录
    tokens: int = 0
    flag: bool = False
    log: str = ''


@CHAT_ROUTE.post('/chat/getSpecChatHistory')
async def getSpecChatHistoryAPI(item: GetSpecChatHistoryRequest, user: str = fastapi.Depends(authenticateUser)):
    rea = GetSpecChatHistoryResponse()
    handle = getChatHandle(user)
    rea.history, rea.tokens, rea.flag, rea.log = await handle.getSpecChatHistory(item.chatCid)
    return rea


# ==================================================
# ❌ deleteChatAPI 删除当前用户的指定chatCid的对话内容
# 根据chatCid直接删除这张对话的表
# ==================================================

class DeleteChatRequest(BaseModel):
    '''deleteChatAPI前端请求体内的参数'''
    chatCid: str


class DeleteChatResponse(BaseModel):
    '''deleteChatAPI前端response的参数'''
    flag: bool = False
    log: str = ''


@CHAT_ROUTE.post('/chat/deleteChat')
async def deleteChatAPI(item: DeleteChatRequest, user: str = fastapi.Depends(authenticateUser)):
    rea = DeleteChatResponse()
    handle = getChatHandle(user)
    rea.flag = await handle.deleteChat(item.chatCid)
    return rea


# ==================================================
# ✉️ setUserMsgAPI 向数据库存入用户的提问
# 向chat hanlder里设置最新的用户提示的内容
# 因为整个prompt是被存在数据库的,设置成功之后, Assistant的请求就不需要携带message了
# ==================================================

class SetUserMsgRequest(BaseModel):
    '''Chat的中user的消息的请求体, 接受消息存入数据库, 并返回对话的唯一chatIid'''
    msg: str


class SetUserMsgResponse(BaseModel):
    '''Chat的中user的消息的应答体, 返回对话的唯一chatIid'''
    flag: bool = False
    chatIid: str = ''
    tokens: int = 0
    log: str = ''


@CHAT_ROUTE.post('/chat/setUserMsg')
async def setUserMsgAPI(item: SetUserMsgRequest, user: str = fastapi.Depends(authenticateUser)):
    rea = SetUserMsgResponse()
    handle = getChatHandle(user)
    rea.flag, rea.chatIid, rea.tokens = await handle.setUserMsg(item.msg)
    return rea


# ==================================================
# ✏️ editChatItemAPI 修改数据库里面对应的消息的内容
# 根据指定的chatIid来修改对应的内容
# ==================================================

class EditChatItemRequest(BaseModel):
    '''editChatItemAPI前端请求体内的参数'''
    chatIid: str    # 对话每个元素的唯一标志
    msg: str


class EditChatItemResponse(BaseModel):
    '''editChatItemAPI前端response的参数'''
    flag: bool = False
    log: str = ''


@CHAT_ROUTE.post('/chat/editChatItem')
async def editChatItemAPI(item: EditChatItemRequest, user: str = fastapi.Depends(authenticateUser)):
    rea = EditChatItemResponse()
    handle = getChatHandle(user)
    rea.flag = await handle.editChatItemMsgByID(item.chatIid, item.msg)
    return rea


# ==================================================
# ❌ deleteChatItemAPI 从数据库删除指定的对话元素的API
# 根据指定的chatIid来删除对应的元素
# 注意 如果API返回的message是报错的,那么这个chatIid是无效的, 但是不会影响这里的接口
# ==================================================

class DeleteChatItemRequest(BaseModel):
    '''deletChatItemAPI前端请求体内的参数'''
    chatIid: str


class DeleteChatItemResponse(BaseModel):
    '''deletChatItemAPI前端response的参数'''
    flag: bool = False
    log: str = ''


@CHAT_ROUTE.post('/chat/deleteChatItem')
async def deleteChatItemAPI(item: DeleteChatItemRequest, user: str = fastapi.Depends(authenticateUser)):
    rea = DeleteChatItemResponse()
    handle = getChatHandle(user)
    rea.flag = await handle.deleteChatItemByID(item.chatIid)
    return rea


# ==================================================
# ⚙️ getChatParams 获取对话的参数信息的API
# 根据对话的唯一标识 chatCid来从数据库获得配置, 如果是无效的chatCid就返回默认值
# ==================================================

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


# ==================================================
# 🛠️ SetChatParams的请求
# 根据对话的唯一标识 chatCid来对当前的对话的设置进行修改
# 注意这个函数的数据 非常需要前后端的变量名一致
# ==================================================

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


# ==================================================
# ✨ 📡Chat SSE API 的应答体
# 关键点在于用WEB的eventSource来创建SSE是不能携带header信息
# 通过url挂着chatCid来做用户身份判断
# ==================================================

class ChatSSEResponse(BaseModel):
    '''Chat对话的应答体'''
    flag: int = 0       # SSE对话开始/进行中/结束的标识, 开始是1, 进行中是2, 结束是0
    data: str = ''      # 具体的内容
    tokens: int = 0
    chatIid: str = ''   # 对话对象的唯一标志


@CHAT_ROUTE.get("/chat/sse/{chatCid}")
async def sseAPI(chatCid: str):
    '''
    SSE方式向WEB端发送消息,通过chatCid来找到用户
    对于asyncio.sleep(0)有解释：
        - await asyncio.sleep(0)在Python的异步编程中通常用于“让出控制权”。当你在协程中使用await asyncio.sleep(0)时,你实际上是在告诉事件循环：“我现在没有什么要做的,你可以去处理其他的任务。”

        - 在你的情况中,这些“其他的任务”可能包括处理WebSocket的数据发送。当你调用websocket.send_text(resp)时,你并不是立即发送数据,而是将数据放入一个发送缓冲区,等待事件循环在适当的时候发送它。当你使用await asyncio.sleep(0)时,你给了事件循环一个机会去处理这个发送任务。

        - 但请注意,这只是一个可能的解释,实际效果可能会因为具体情况而有所不同。在某些情况下,使用await asyncio.sleep(0)可能并不会产生预期的效果。比如,如果事件循环有其他更高优先级的任务要处理,那么即使你使用了await asyncio.sleep(0),事件循环也可能选择先处理那些任务。
    '''
    async def sseEventGenerator():
        rea = ChatSSEResponse()
        handle = getChatHandleByChatCid(chatCid)
        try:
            # 开始请求GPT API
            rea.flag = 1
            resp, _ = dict2Str(rea.__dict__)

            # 包装成符合SSE接收的消息的格式
            yield f"data: {resp}\n\n"

            async for (chunk, tokens, chatIid) in handle.chatStreamAPI():
                rea.flag = 2
                rea.data = f'{chunk}'
                rea.tokens = tokens
                rea.chatIid = chatIid
                resp, _ = dict2Str(rea.__dict__)
                # 持续对话中
                yield f"data: {resp}\n\n"
                # ⭐ 必须 await asyncio.sleep
                await asyncio.sleep(0)

            # 对话结束
            rea.flag = 0
            rea.data = ""
            resp, _ = dict2Str(rea.__dict__)
            yield f"data: {resp}\n\n"

        except asyncio.CancelledError:
            print("WEB Close the sse connection")
        except Exception as e:
            rea.flag = 0
            rea.data = "API tokens error! Please delete some chat item."
            resp, _ = dict2Str(rea.__dict__)
            yield f"data: {resp}\n\n"
            raise fastapi.HTTPException(
                status_code=500, detail="Server error!"
            )

    return fastapi.responses.StreamingResponse(sseEventGenerator(), media_type="text/event-stream")


# ==================================================
# 🔄 ReGenerateChatItemContent的请求参数信息
# 根据对话内每条消息的唯一标识 chatIid 来删除后面的全部数据然后重新生成
# 不同的角色会影响是不是要删除当前这条消息的记录
# 注意这个函数的数据 非常需要前后端的变量名一致
# ==================================================

class ReGenerateContentRequest(BaseModel):
    '''ReGenerateContentAPI请求体的格式'''
    chatIid: str  # 对话具体内容的唯一标志
    role: str  # 角色的信息


class ReGenerateContentResponse(BaseModel):
    '''ReGenerateContentAPI返回的response的格式'''
    flag: bool = False
    tokens: int = 0
    log: str = ''


@CHAT_ROUTE.post('/chat/reGenerateContent')
async def reGenerateContentAPI(item: ReGenerateContentRequest, user: str = fastapi.Depends(authenticateUser)):
    rea = ReGenerateContentResponse()
    handle = getChatHandle(user)
    rea.flag, rea.tokens, rea.log = await handle.reGenerateContent(item.role, item.chatIid)
    return rea


# ==================================================
# 📥 downloadChatHistory的请求参数信息
# 这个没有啥介绍的, 主要是设计上不给prompts的信息
# ==================================================

class DownloadChatHistoryRequest(BaseModel):
    '''DownloadChatHistoryAPI请求体的格式'''
    chatCid: str  # 对话的唯一标志


class DownloadChatHistoryResponse(BaseModel):
    '''DownloadChatHistoryAPI返回的response的格式'''
    flag: bool = False
    data: list = []
    log: str = ''


@CHAT_ROUTE.post('/chat/downloadChatHistory')
async def downloadChatHistoryAPI(item: DownloadChatHistoryRequest, user: str = fastapi.Depends(authenticateUser)):
    rea = DownloadChatHistoryResponse()
    handle = getChatHandle(user)
    rea.flag = True
    rea.data = await handle.downloadChatHistory(item.chatCid)
    return rea


# ==================================================
# 📤 uploadChatHistory的请求参数信息
# 这个没有啥介绍的, 使用默认的对话参数创建一个对话,然后返回一个chatCid
# ==================================================

class UploadChatHistoryRequest(BaseModel):
    '''uploadChatHistoryAPI请求体的格式'''
    data: object  # 对话的唯一标志


class UploadChatHistoryResponse(BaseModel):
    '''uploadChatHistoryAPI返回的response的格式'''
    flag: bool = False
    chatCid: str = ''
    history: list = []
    tokens: int = 0
    log: str = ''


@CHAT_ROUTE.post('/chat/uploadChatHistory')
async def uploadChatHistoryAPI(item: UploadChatHistoryRequest, user: str = fastapi.Depends(authenticateUser)):
    rea = UploadChatHistoryResponse()
    handle = getChatHandle(user)
    rea.flag = True
    rea.chatCid, rea.history, rea.tokens = await handle.uploadChatHistory(item.data)
    return rea


# ==================================================
# 👻 newGhostChatAPI的请求参数信息
# 使用默认的对话参数创建一个幽灵对话, 然后WEB 设置对话的固定名称,这个都是很随意的
# 幽灵对话其实是没有上下文记忆的对话
# ==================================================

class NewGhostChatRequest(BaseModel):
    '''newGhostChatAPI请求体的格式'''
    data: str  # 具体的模板是什么


class NewGhostChatResponse(BaseModel):
    '''newGhostChatAPI返回的response的格式'''
    flag: bool = False
    chatCid: str = ''
    chatParams: dict = {}
    tokens: int = 0
    log: str = ''


@CHAT_ROUTE.post('/chat/newGhostChat')
async def newGhostChatAPI(item: NewGhostChatRequest, user: str = fastapi.Depends(authenticateUser)):
    rea = NewGhostChatResponse()
    handle = getChatHandle(user)
    rea.chatCid, rea.chatParams, rea.tokens = await handle.newGhostChat(item.data)
    rea.flag = True
    return rea


# ==================================================
# 🔊 chatAudioAPI 生成语音播报的请求参数信息
# 调用接口 生成一个mp3文件, 然后和SSE请求一样, 用URL内挂chatCid来进行audio的返回
# 📝 TODO: 可以直接用OpenAI client做stream的返回, 但是请求体携带用户信息还没有做考虑
# ==================================================

class ChatAudioRequest(BaseModel):
    '''chatAudioAPI请求体的格式'''
    data: str  # 具体的模板是什么


class ChatAudioResponse(BaseModel):
    '''chatAudioAPI请求体的格式'''
    data: str = ''  # 文件名称
    flag: bool = False
    log: str = ''


@CHAT_ROUTE.post('/chat/chatAudio')
async def chatAudioAPI(item: ChatAudioRequest, user: str = fastapi.Depends(authenticateUser)):
    handle = getChatHandle(user)
    rea = ChatAudioResponse()
    rea.flag = True
    rea.data = await handle.getChatItemAudio(item.data)
    return rea


@CHAT_ROUTE.get("/chat/audio/{fileName}")
async def chatAudioFileAPI(fileName: str):
    '''直接通过文件名来获取音频, 这里不做异常处理了,方便排除错误'''
    def iterfile(filePath: str):
        with open(filePath, mode="rb") as audioChunk:
            yield from audioChunk

    filePath = f"{CONF.getCacheDirectory()}/{fileName}"
    return fastapi.responses.StreamingResponse(iterfile(filePath), media_type="audio/mpeg")


@CHAT_ROUTE.get("/chat/audio/{chatCid}")
async def chatAudioStreamAPI(chatCid: str):
    ''' 📝TODO: 需要传入data进入这个函数才能使用stream的方法'''
    handle = getChatHandleByChatCid(chatCid)
    return fastapi.responses.StreamingResponse(handle.getChatItemStreamAudio(), media_type="audio/mpeg")
