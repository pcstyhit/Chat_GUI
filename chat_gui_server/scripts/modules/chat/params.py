'''
### chat内的成员, 用于更新对话时候的这一个对话通道的参数
封装成类, 方便支持多个user使用
'''

import tiktoken
from scripts.libs import CONF


class Params:
    # GPT对话的几个角色
    SYS = 'system'
    USER = 'user'
    ASS = 'assistant'
    # 最简单prompt的模板
    PROMPTTEMP = {'role': 'system',
                  'content': 'You are GPT-4o a large language model of OpenAI.'}
    # 数据的默认值
    DEFAULT_VALUE = {
        "chatName": "New Chat",
        "isUseProxy": False,
        "proxyURL": '',
        'modelList': [],
        'apiKey': "",
        'apiVersion': "",
        'maxTokens': 0,
        'deployment': "",
        'endPoint': "",
        'promptTemplate': [{'role': 'system', 'content': 'You are GPT-4o a large language model of OpenAI.'}],
        'promptTemplateTokens': 15,
        'passedMsgLen': 20,
        'maxResponseTokens': 2000,
        'temperature': 0.7,
        'topP': 0.95,
        'frequecyPenaty': 0,
        'presentPenaty': 0,
        'stopSequence': [],
        'chatWithGptTimeout': 10,
        'webRenderStrLen': 20
    }

    NOTEXPOSETOWEB = ['encoding', 'apiKey',
                      'apiVersion', 'deployment', 'endPoint']

    def __init__(self) -> None:
        '''OpenAI GPT 对话的默认几个参数'''
        # 模型的标签信息
        self.chatName = ''
        self.isUseProxy = False,
        self.proxyURL = '',
        self.modelType = ''             # 当前模型的类型（gpt-n)
        self.modelName: str = ''
        self.modelList: list = []       # 可以用的模型列表

        # HTTP 访问 Azure API 的身份信息
        self.apiKey: str = ""           # 不暴露给WEB
        self.apiVersion: str = ""       # 不暴露给WEB
        self.maxTokens: int = 0         # 模型最大支持的对话的tokens数量
        self.deployment: str = ""       # 不暴露给WEB
        self.endPoint: str = ""         # 不暴露给WEB

        # 和GPT进行对话的prompt的模板信息
        self.promptTemplate: list = [
            {'role': 'system', 'content': 'You are GPT-4o a large language model of OpenAI.'}
        ]
        # 就当前的提示的template而言的prompt的tokens数量
        self.promptTemplateTokens: int = 15

        # 和GPT进行对话的参数
        self.passedMsgLen: str = 20                    # 上下文长度，默认是20
        self.maxResponseTokens: int = 2000             # 最大响应的tokens
        self.temperature: float = 0.7
        self.topP: float = 0.95
        self.frequecyPenaty: float = 0
        self.presentPenaty: float = 0
        self.stopSequence: list = []
        self.chatWithGptTimeout: int = 10               # 对话超过多少时间停止它

        '''下面的参数是针对这个项目体验设计的'''
        self.webRenderStrLen: int = 20                  # 设置字符长度大于20才yeild出内容，减少web渲染次数
        '''辅助配置Chat功能设置的方法或者对象'''
        # 默认3.5 -> 4.0-* 用的计算方法都是一样的 cl100k_base 这里就不改了
        self.encoding = tiktoken.encoding_for_model('gpt-4')

        # 初始化操作
        self.useDefaultParams()

    def useDefaultParams(self):
        '''使用默认值'''
        for key in Params.DEFAULT_VALUE:
            self.__dict__[key] = Params.DEFAULT_VALUE.get(key)
        # 更新当前模型的信息
        self.useDefaultModelParams()

    def getCurrentParams(self) -> dict:
        '''获得当前用户对这个chat的配置信息,需要和前端约定,用的变量名字是一样的 这样省去了key和value分离的麻烦'''
        reaDictData = {}
        for key in self.__dict__:
            if key in Params.NOTEXPOSETOWEB:
                continue
            reaDictData[key] = self.__dict__[key]
        return reaDictData

    def getDefaultParams(self) -> dict:
        '''特殊函数,如果说chatCid是空的话,那表示正在创建对话,重置参数并返回结果给到WEB'''
        self.useDefaultParams()
        return self.getCurrentParams()

    def updateModelType(self) -> bool:
        '''根据选中的模型名字来重新选中模型的参数, 例如从GPT4切换到GPT3更新这些参数'''
        modelDictData = CONF.modelList[self.modelName]
        for key in modelDictData:
            self.__dict__[key] = modelDictData[key]

    def updateCurrentParams(self, data: dict):
        '''根据data里面包含了哪些参数就把当前实例的属性给更新'''
        for key in data:
            self.__dict__[key] = data[key]
        # 设置信息自带了模型的选项,更新模型
        self.updateModelType()

    def useDefaultModelParams(self):
        '''从CONF拿全局的变量,更新当前的一些模型的信息'''
        self.modelList = []
        for key in CONF.modelList:
            self.modelList.append(
                {'label': key, 'value': CONF.modelList[key]['maxToken'], 'mtype': CONF.modelList[key]['modelType']})

        self.modelName = CONF.default_modelName
        self.modelType = CONF.default_modelType
        self.maxTokens = CONF.default_maxToken
        # 不暴露给WEB的属性
        self.apiKey = CONF.default_apiKey
        self.apiVersion = CONF.default_apiVersion
        self.deployment = CONF.default_deployment
        self.endPoint = CONF.default_endPoint

        self.isUseProxy = CONF.isUseProxy
        self.proxyURL = CONF.proxyURL

    def getPromptTemplate(self) -> list:
        '''获得出当前设置的prompt的template'''
        return self.promptTemplate

    def getTokens(self, msg) -> int:
        '''从消息中计算这次消息要耗的tokens数量'''
        tokenArray = self.encoding.encode(f'{msg}')
        return len(tokenArray)

    def checkTokens(self, msgList: list) -> bool:
        '''特定的函数,针对存在chat数据库的对话信息item来判断,
        这个数值的消息是否满足tokens数量要求可以被发送

        `msgList` 其中每个msg的格式是元组: `msg = (1, 'TYR_YGHGH', 'user', 'Hello!', 10)`
         - msg[0]是数据库的id位,
         - msg[1]是chatIid
         - msg[2]是角色信息,
         - msg[3]是消息,
         - msg[4]是tokens数量
        '''
        allTokens = sum(msg[4] for msg in msgList)
        if allTokens < self.maxTokens:
            return True
        return False
