'''
chat内的公共方法,用于更新对话的
'''

import os
import glob
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

def writeMessageToFile(fileName:str):
    '''将最新的对话写入文件'''
    filePath = getAbsPath('history_path', f'{fileName}.json')
    with open(filePath, 'w') as f:  
        json.dump(MESSAGES, f)

def getAllHistory():
    '''读取当前缓存全部的json文件名称'''
    filePath = getAbsPath('history_path')
    jsonFiles = glob.glob(os.path.join(filePath, '*.json'))  
    fileNames = [os.path.basename(file) for file in jsonFiles]  
    ans = [name.split('.')[0] for name in fileNames]
    return ans

def loadMessage(fileName):
    '''读取json文件并返回,并设置当前的上下文内容'''
    global MESSAGES
    filePath = getAbsPath('history_path', f'{fileName}.json')
    rea = {'role': 'system', 'content': SYSTEMMSG}
    with open(file=filePath, mode='r') as f:
        rea = json.load(f)
    MESSAGES = rea
    return rea

def deletMessage(fileName):
    '''删除message'''
    filePath = getAbsPath('history_path', f'{fileName}.json')
    try:  
        os.remove(filePath)  
    except OSError as e:  
        print(f"Server deletMessage error: {e.filename}")

async def loadChatMessage(fileName):
    '''加载消息'''
    return loadMessage(fileName)

async def setPrompt(name, msg):
    '''设置system content promote'''
    changeTemplate(msg)
    writeMessageToFile(name)
    return True

async def deletChatMessage(fileName):
    return deletMessage(fileName)
