'''
用来处理一些简单的响应式的回答.
'''
import json
from typing import Union  
from openai import AzureOpenAI
from scripts.libs import CONF

from .messages import updateMessage, writeToFile
from .tokens import accont

def chatCore(msg:str, acct:dict = CONF) -> str:
    '''结合上下文进行对话的核心函数
        https://zhuanlan.zhihu.com/p/618911413
    '''
    client = AzureOpenAI(
        azure_endpoint=acct['end_point'],
        api_key=acct['api_key'],
        api_version=acct['api_version']
    )

    # 增加上下文信息
    messgaes = updateMessage('user', msg)
    response = client.chat.completions.create(model=acct['deployment'], messages=messgaes)
    ans = response.choices[0].message.content
    usage = accont(response)
    updateMessage('assistant', response.choices[0].message.content)
    writeToFile('test')
    # 返回文本信息
    return {'ans':ans, 'usage':usage}

async def chatByText(msg: str) -> str:
    '''将核心函数变成异步的'''
    return chatCore(msg)
