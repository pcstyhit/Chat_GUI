'''
处理对话的核心类，为每个用户暴露一个实例来操作对话
'''
from openai import AzureOpenAI
from openai.types.chat import ChatCompletion
from scripts.libs import CONF


class ChatHandle:
    def __init__(self) -> None:
        self.azureClient = AzureOpenAI(
            azure_endpoint=CONF['end_point'],
            api_key=CONF['api_key'],
            api_version=CONF['api_version']
        )
        self.openaiClient = None

    def azureChat(self, messages: list, acct: dict = CONF) -> ChatCompletion:
        '''结合上下文进行对话的核心函数, 响应式
            https://zhuanlan.zhihu.com/p/618911413
        '''
        # 增加上下文信息
        response = self.azureClient.chat.completions.create(model=acct['deployment'],
                                                            messages=messages)
        # 返回回答的内容
        return response

    def getChatCompletionInfo(self, response: ChatCompletion):
        '''从非流式对话中获取单次对话的内容和token的使用情况'''
        content = response.choices[0].message.content
        usage = self.tksHandle.accont(response)
        return {'content': content, 'usage': usage}

    def azureChatStream(self, messages: list, acct: dict = CONF):
        '''只用于对话使用的流式输出'''
        # Example of an OpenAI ChatCompletion request with stream=True
        # https://platform.openai.com/docs/guides/chat
        # send a ChatCompletion request to count to 100
        response = self.azureClient.chat.completions.create(
            model=acct['deployment'],
            messages=messages,
            stream=True  # again, we set stream=True
        )

        return response
