'''
chat内的成员,用于记录token的使用情况
之前版本的response是没有token的记录的,现在的是有的因此函数更简单了
https://github.com/Chanzhaoyu/chatgpt-web/issues/464
'''
import tiktoken

MODEL_TOKEN_MAP = {
    '-32k': 32*1024,
    '-8k': 8*1024,
    '-turbo': 128*1024,
}


class Tokens:
    def __init__(self) -> None:
        self.model = 'gpt-4'
        self.encoding = tiktoken.encoding_for_model(self.model)
        self.maxTokens = self.getMaxTokens(self.model)

    def updateModel(self, name):
        '''更新模型的设置'''
        self.model = name
        self.encoding = tiktoken.encoding_for_model(self.model)
        self.maxTokens = self.getMaxTokens(self.model)
        return self.maxTokens

    def getMaxTokens(self, name='gpt4') -> int:
        '''根据模型名称获得最大的tokens数量'''
        for models in MODEL_TOKEN_MAP.keys():
            if name in models:
                return MODEL_TOKEN_MAP[models]
        return 32*1024

    def getTokens(self, msg) -> int:
        '''从消息中得到tokens'''
        tokenArray = self.encoding.encode(f'{msg}')
        return len(tokenArray)

    def checkTokens(self, msgList: list) -> bool:
        '''特定的函数,针对存在chat数据库的对话信息item来判断,这个数值的消息是否满足tokens数量要求可以被发送
         msgList中的每个msg的格式是元组 msg = (1, 'user', 'Hello!', 10) type is <class 'tuple'> type is <class 'tuple'>
         其中的 msg[0]是数据库的id位, msg[1]是角色信息, msg[2]是消息, msg[3]是tokens数量
        '''
        allTokens = sum(msg[3] for msg in msgList)
        if allTokens < self.maxTokens:
            return True
        return False
