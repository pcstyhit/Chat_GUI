'''
chat内的公共方法,用于记录token的使用情况
之前版本的response是没有token的记录的,现在的是有的因此函数更简单了
https://github.com/Chanzhaoyu/chatgpt-web/issues/464
'''
import os
import json
from scripts.libs import getAbsPath

MAX_TOKENS = 32*1024
PROMPT_TOKENS = 0
COMPLETION_TOKENS = 0
TOTAL_TOKENS = 0

def setModelMaxToken(maxValue:int, modelType:str='32k'):
    global MAX_TOKENS
    if modelType == '8k':
        MAX_TOKENS = maxValue if maxValue <= 8*1024 else 8*1024
    if modelType == '16k':
        MAX_TOKENS = maxValue if maxValue <= 16*1024 else 16*1024
    if modelType == '32k':
        MAX_TOKENS = maxValue if maxValue <= 32*1024 else 32*1024


def accont(response) -> bool:
    '''从GPT返回的内容中计算token,返回内容的格式是固定的'''
    global PROMPT_TOKENS, COMPLETION_TOKENS, TOTAL_TOKENS
    PROMPT_TOKENS = response.usage.prompt_tokens
    COMPLETION_TOKENS = response.usage.completion_tokens
    TOTAL_TOKENS = response.usage.total_tokens

    if TOTAL_TOKENS >= MAX_TOKENS:
        return 0
    else:
        return TOTAL_TOKENS

def resetTokens(maxValue:int=32*1024, modelType:str='32k'):
    '''重置全部的tokens'''
    global PROMPT_TOKENS, COMPLETION_TOKENS, TOTAL_TOKENS
    setModelMaxToken(maxValue, modelType)
    PROMPT_TOKENS = 0
    COMPLETION_TOKENS = 0
    TOTAL_TOKENS = 0

def writeTokenToFile(fileName:str):
    '''将最新的对话写入文件'''
    filePath = getAbsPath('history_path', f'{fileName}.tks')
    with open(filePath, 'w') as f:
        tokens = {'prompt_tokens': PROMPT_TOKENS, 'completion_tokens': COMPLETION_TOKENS, 'total_tokens':TOTAL_TOKENS, 'model_tokens': MAX_TOKENS}
        json.dump(tokens, f)

def deletTokens(fileName):
    '''删除token文件'''
    filePath = getAbsPath('history_path', f'{fileName}.tks')
    try:  
        os.remove(filePath)  
    except OSError as e:  
        print(f"Server deletMessage error: {e.filename}")

def loadTokens(fileName):
    '''读取tks文件并返回,并重置tokens数量'''
    global PROMPT_TOKENS, COMPLETION_TOKENS, TOTAL_TOKENS, MAX_TOKENS
    filePath = getAbsPath('history_path', f'{fileName}.tks')
    rea = {'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens':0, 'model_tokens':0}
    with open(file=filePath, mode='r') as f:
        rea = json.load(f)
    PROMPT_TOKENS = rea['prompt_tokens']
    COMPLETION_TOKENS = rea['completion_tokens']
    TOTAL_TOKENS = rea['total_tokens']
    MAX_TOKENS = rea['model_tokens']
    return rea

async def setPromptToken(name):
    '''创建新对话时候重置token数量'''
    resetTokens()
    writeTokenToFile(name)
    return True

async def loadChatTokens(fileName):
    return loadTokens(fileName)

async def deletChatTokens(fileName):
    return deletTokens(fileName)

