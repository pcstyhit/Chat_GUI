'''
chat内的成员,用于更新对话时候的参数
封装成类,方便支持多个user使用
'''


class Params:
    SYS = 'system'
    USER = 'user'
    ASS = 'assistant'
    PROMPTTEMP = {'role': 'system',
                  'content': 'You are Chat GPT-4 a large language model of OpenAI.'}

    def __init__(self) -> None:
        self.msgLen = 20                # 上下文长度，默认是10
        self.tempure = 10
        self.prompt = 'You are Chat GPT-4 a large language model of OpenAI.'
        self.maxResponse = 800          # 最大响应
        self.temperature = 0.7
        self.topP = 0.95
        self.frequecyPenaty = 0
        self.presentPenaty = 0
        self.stopSequence = ""
        self.passedMsg = 10             # 默认的上下文长度
        self.timeout = 10000

    def updateChatParam(self, systemContent, passedMsg):
        '''设置或更新对话的参数'''
        self.prompt = {'role': self.SYS, 'content': systemContent}
        self.msgLen = passedMsg
        # self.maxResponse = maxResponse
        # self.temperature = temperature
        # self.topP = topP
        # self.frequecyPenaty= frequecyPenaty
        # self.presentPenaty = presentPenaty
        # self.stopSequence = stopSequence

    def loadChatPrompt(self, role, content):
        '''Check the message from chat data base if is the system prompt'''
        if role != self.SYS:
            self.prompt = self.PROMPTTEMP
        else:
            self.prompt = {'role': self.SYS, 'content': content}
