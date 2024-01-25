import fastapi
from pydantic import BaseModel

from scripts.libs import str2Dict
from scripts.modules.chat import chatByText, loadChatMessage, loadChatTokens,setPrompt, setPromptToken, deletChatMessage, deletChatTokens

CHATROUTER = fastapi.APIRouter()

class Chat(BaseModel):
    '''前端请求体内的参数'''
    data: str
    timeout: int

@CHATROUTER.post('/chat/{parameters}')
async def postCore(parameters: str, item: Chat):
    rea = None
    if parameters == 'text':
        # 普通的文本响应式
        data, _ = str2Dict(item.data)
        rea = await chatByText(data['name'], data['msg'])
    
    if parameters == 'loadChatHistory':
        rea = await loadChatMessage(item.data)
    
    if parameters == 'loadChatTokens':
        rea = await loadChatTokens(item.data)

    if parameters == 'prompt':
        # 重置system content和tokens数量
        data, _ = str2Dict(item.data)
        await setPrompt(data['name'], data['msg'])
        await setPromptToken(data['name'])
    
    if parameters == 'deleteChat':
        await deletChatMessage(item.data)
        await deletChatTokens(item.data)
    
    return {'name': parameters, 'data': rea}
