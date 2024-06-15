'''
#### base models 新增的 项目的全局基础模型类文件
'''


class APIServicesTypes:
    AZURE = "azure"
    OPENAI = "openai"


class AzureAPIParams:
    def __init__(self) -> None:
        self.serviceType: str = ''
        self.modelType: str = ''
        self.apiKey: str = ''
        self.apiVersion: str = ''
        self.endPoint: str = ''
        self.maxToken: int = 0
        self.deployment: str = ''


class OpenAIAPIParams:
    def __init__(self) -> None:
        self.serviceType: str = ''
        self.modelType: str = ''
        self.apiKey: str = ''
        self.baseUrl: str = ''
        self.maxToken: int = 0
