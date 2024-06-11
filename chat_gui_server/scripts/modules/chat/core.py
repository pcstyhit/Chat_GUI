'''
处理对话的核心类，为每个用户暴露一个实例来操作对话
'''
import httpx
from openai import AzureOpenAI
from openai.types.chat import ChatCompletion
from scripts.libs import CONF


class ChatHandle:
    def __init__(self) -> None:
        '''默认就选用默认的模型参数'''
        self.azureClient = AzureOpenAI(
            azure_endpoint=CONF.default_endPoint,
            api_key=CONF.default_apiKey,
            api_version=CONF.default_apiVersion
        )
        self.deployment = CONF.default_deployment

    def updateAzureGPTModel(self, endPoint, apiKey, apiVersion, deployment):
        '''根据最新的设置切换模型'''
        if CONF.isUseProxy:
            # 使用代理就加上代理的URL, 默认HTTPS和HTTP的代理是一个URL
            self.azureClient = AzureOpenAI(
                azure_endpoint=endPoint,
                api_key=apiKey,
                api_version=apiVersion,
                http_client=httpx.Client(proxies={
                    'http://': CONF.proxyURL,
                    'https://': CONF.proxyURL
                })
            )
        else:
            self.azureClient = AzureOpenAI(
                azure_endpoint=endPoint,
                api_key=apiKey,
                api_version=apiVersion,
            )
        self.deployment = deployment

    def azureChatSync(self, messages: list, max_tokens=2000, temperature=0.7, top_p=0.95, stop=[], frequency_penalty=0, presence_penalty=0, timeout=10) -> tuple:
        '''结合上下文进行对话的核心函数 https://zhuanlan.zhihu.com/p/618911413'''
        # 增加上下文信
        response: ChatCompletion = self.azureClient.chat.completions.create(model=self.deployment,
                                                                            messages=messages,
                                                                            max_tokens=max_tokens,
                                                                            temperature=temperature,
                                                                            top_p=top_p,
                                                                            stop=stop,
                                                                            frequency_penalty=frequency_penalty,
                                                                            presence_penalty=presence_penalty,
                                                                            timeout=timeout)

        # 返回回答的内容中抽出消息和tokens数量
        return response.choices[0].message.content, response.usage.total_tokens

    def azureChatStream(self, messages: list, max_tokens=2000, temperature=0.7, top_p=0.95, stop=[], frequency_penalty=0, presence_penalty=0, timeout=10):
        '''只用于对话使用的流式输出
         [Example of an OpenAI ChatCompletion request with stream=True](https://platform.openai.com/docs/guides/chat)
        '''
        response: ChatCompletion = self.azureClient.chat.completions.create(model=self.deployment,
                                                                            messages=messages,
                                                                            stream=True,  # Set stream=True
                                                                            max_tokens=max_tokens,
                                                                            temperature=temperature,
                                                                            top_p=top_p,
                                                                            stop=stop,
                                                                            frequency_penalty=frequency_penalty,
                                                                            presence_penalty=presence_penalty,
                                                                            timeout=timeout)

        return response
