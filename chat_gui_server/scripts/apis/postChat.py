import fastapi
from pydantic import BaseModel

from scripts.modules.chat import chatByText

CHATROUTER = fastapi.APIRouter()

class Chat(BaseModel):
    '''前端请求体内的参数'''
    data: str
    timeout: int

@CHATROUTER.post("/chat/{parameters}")
async def chat(parameters: str, item: Chat):
    '''聊天功能的主入口'''
    if parameters == 'text':
        # 普通的文本响应式
        rea = await chatByText(item.data)
    return {"name": parameters, "data": rea}
