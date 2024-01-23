'''
chat内的公共方法,用于记录token的使用情况
之前版本的response是没有token的记录的,现在的是有的因此函数更简单了
https://github.com/Chanzhaoyu/chatgpt-web/issues/464
'''

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

def resetTokens(maxValue:int, modelType:str='32k'):
    '''重置全部的tokens'''
    global PROMPT_TOKENS, COMPLETION_TOKENS, TOTAL_TOKENS
    setModelMaxToken(maxValue, modelType)
    PROMPT_TOKENS = 0
    COMPLETION_TOKENS = 0
    TOTAL_TOKENS = 0




