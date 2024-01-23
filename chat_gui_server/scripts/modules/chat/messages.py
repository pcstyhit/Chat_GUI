'''
chat内的公共方法,用于更新对话的
'''

import json
from scripts.libs import getAbsPath

SYSTEMMSG = 'You are a helpful assistant.'
MESSAGES = [
    {'role': 'system', 'content': SYSTEMMSG}
]

def updateMessage(role:str, msg:str):
    global MESSAGES
    '''更新上下文
     - role (str): 应该为 user 或者是 assistant.
    '''
    MESSAGES.append({"role": role, "content": msg})
    return MESSAGES

def resetMessage():
    '''token数量耗尽,重置上下文'''
    global MESSAGES
    MESSAGES = [
        {'role': 'system', 'content': SYSTEMMSG}
    ]

def changeTemplate(content):
    '''修改template,然后重置全部的上下文'''
    global SYSTEMMSG, MESSAGES
    SYSTEMMSG = content
    resetMessage()

def writeToFile(fileName:str):
    '''将最新的对话写入文件'''
    filePath = getAbsPath('history_path', f'{fileName}.json')
    with open(filePath, 'w') as f:  
        json.dump(MESSAGES, f) 