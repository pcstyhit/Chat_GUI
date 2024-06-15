import os
import sys
import time
import json
import configparser
from .bms import OpenAIAPIParams, AzureAPIParams, APIServicesTypes
from .encrypt import decryptDict


class CaseSensitiveConfigParser(configparser.ConfigParser):
    '''严格区分大小写的configparser'''

    def optionxform(self, optionstr):
        return optionstr  # 保持原样，不转换为小写


class ApiServiceTypesChecker:
    '''用来校验Azure服务内的GPT模型的设置是不是对的'''
    AZUREOBJ = AzureAPIParams()
    OPENAIOBJ = OpenAIAPIParams()

    @classmethod
    def validAzureKeys(cls, data: dict) -> bool:
        return set(cls.AZUREOBJ.__dict__.keys()).issubset(data.keys())

    @classmethod
    def validOpenAiKeys(cls, data: dict) -> bool:
        return set(cls.OPENAIOBJ.__dict__.keys()).issubset(data.keys())


class ProjectConfig:
    '''整个项目的配置文件'''
    DIR_LOOP = 3    # 当前文件相对于项目main.py的层级

    # CFG文件必要的键, 这些键值和当前的文件的实例对象的属性也有关系, 实例对象的属性会在这些键值前面加default字符
    MODELCFGKEYLIST: set = {'modelType', 'apiKey',
                            'apiVersion', 'endPoint', 'maxToken', 'deployment'}

    # 用户配置文件config.json内可以修改的实例对象的属性名
    USERCONFIGFILEKEYLIST: set = {
        'isLoginByTokenKey', 'isUseProxy', 'proxyURL', 'tokenKey', 'dataBasePath', 'host', 'port'}

    # 项目用到的文件夹结构和实例对象的属性是一样的命名
    PROJECTNESSDIR = {'dataBasePath', }

    def __init__(self) -> None:
        self.adminUserPassword: str = 'pldz'                # 默认的管理员密码
        self.isLoginByTokenKey: bool = False                # 是不是用tokenKey进行登录
        self.tokenKey: str = ''                             # 如果是tokenKey运行的值
        self.isUseProxy: bool = False                       # 是否使用代理来连接GPT
        self.proxyURL: str = ''                             # GPT KEY请求的代理链接

        self.host: str = '127.0.0.1'                        # 项目运行的Host address
        self.port: int = 10080                              # 项目运行的port号

        self.dataBasePath: str = '.dbpath'                  # 数据库相对项目的路径
        self.staticsPath: str = 'statics'                   # 静态资源相对项目的路径
        self.apiServiceListFileName = "cfg.json"            # 没有tokenKey情况下的api服务的全部参数配置
        self.systemConfigFileName: str = 'config.cfg'
        self.userConfigFileName: str = 'config.json'

        self.apiDefaultService = APIServicesTypes.OPENAI    # 区别是azure还是openai的服务
        self.apiModelList = {}                              # api的模型列表

        '''项目自己用来实现功能帮助变量'''
        self.projectPath = self._getProjectAbsPath()

        '''从外部依赖文件导入配置, 先加入用户的设置,这个优先级更高, 然后再加载模型的设置'''
        self.updateUserConfig()
        self.checkProjectNecessaryDirectory()

    def _getProjectAbsPath(self,):
        '''获得项目的入口脚本文件夹的绝对路径'''
        return os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

    def getAbsPath(self, path: str, fileName: str = None):
        '''获取任何项目文件的绝对路径'''
        if path is None:
            if fileName is None:
                return self.projectPath
            else:
                return os.path.join(self.projectPath, fileName)
        else:
            if fileName is None:
                return os.path.join(self.projectPath, path)
            else:
                return os.path.join(self.projectPath, path, fileName)

    def updateUserConfig(self):
        '''如果有config.json的话, 用config.json更新用户的配置'''
        userConfigFilePath = self.getAbsPath(self.userConfigFileName)

        if not os.path.exists(userConfigFilePath):
            print(f'Not find the user config file ({userConfigFilePath}) !!!')
            # 终结项目
            sys.exit(1)

        # 读取json文件
        with open(userConfigFilePath, 'r') as file:
            userConfigData: dict = json.load(file)

            # 更新值
            for key in userConfigData:
                if key not in list(self.__dict__.keys()):
                    continue
                self.__dict__[key] = userConfigData[key]

        # 注意 self.isLoginByTokenKey之后, 可以判断tokenKey是不是被嵌入在了config.json里面, 这个是打包成exe用这个项目的特别的行为
        if self.isLoginByTokenKey:
            if self.tokenKey == "":
                # 😋 没有tokenKey那就需要用户用tokenKey来登录了, 这个功能没有用到, 也就不继续写了
                print("You have configured a tokenKey, tokenKey cannot be empty!")
                sys.exit(1)
            else:
                # 解析tokenKey
                self.decryptDictTokenKey()
        else:
            self.loadApiServiceFromCfgFile()

        # 注意 self.isUserProxy之后, self.proxyURL不能为空
        if self.isUseProxy and self.proxyURL == "":
            print("You have configured a proxy, proxy url cannot be empty!")
            exit(1)

    def decryptDictTokenKey(self):
        '''如果配置的是用tokenkey的情况, 解析TokenKey'''
        apiCfgData: dict = {}
        try:
            # 解密
            apiCfgData = decryptDict(self.tokenKey, 'secretkey')
        except:
            print(f'Error tokenKey ... ... exit(1)')
            sys.exit(1)

        # 判断是不是过期的tokenKey
        if (apiCfgData['expiredTime'] <= int(time.time())):
            print(f'Sorry tokenKey is expired!')
            sys.exit(1)

        # 更新全部的模型信息
        apiModelDict = apiCfgData.get("modelList", {})
        for modelName in apiModelDict:
            flag = self.validApiKeyFormat(apiModelDict[modelName])
            if not flag:
                continue

            # 增加元素
            self.apiModelList.update({modelName: apiModelDict[modelName]})

    def loadApiServiceFromCfgFile(self):
        '''如果没有配置self.isLoginByTokenKey,从cfg.json中加载API的服务信息'''
        apiCfgFile = self.getAbsPath(self.apiServiceListFileName)

        if not os.path.exists(apiCfgFile):
            print(f'Not find the api config ({apiCfgFile}) !!!')
            # 终结项目
            sys.exit(1)

        # 读取json文件
        with open(apiCfgFile, 'r') as file:
            apiCfgData: dict = json.load(file)

            # 直接赋值就行了, 也不用做时效判断
            apiModelDict = apiCfgData.get("modelList", {})

            for modelName in apiModelDict:
                flag = self.validApiKeyFormat(apiModelDict[modelName])
                if not flag:
                    continue

                # 增加元素
                self.apiModelList.update({modelName: apiModelDict[modelName]})

    def validApiKeyFormat(self, data: dict) -> bool:
        '''把有效的配置信息的参数才放入最后的self.apiModelList里, 实际上这个检查有点多余, 都是自己写的 也不会出错👻'''
        sType = data.get("serviceType", None)

        if sType == APIServicesTypes.AZURE:
            return ApiServiceTypesChecker.validAzureKeys(data)

        if sType == APIServicesTypes.OPENAI:
            return ApiServiceTypesChecker.validOpenAiKeys(data)

    def checkProjectNecessaryDirectory(self):
        '''判断项目必要的文件目录是不是存在'''
        for key in ProjectConfig.PROJECTNESSDIR:
            nessDirPath = self.getAbsPath(self.__dict__[key])
            if not os.path.exists(nessDirPath):
                os.mkdir(nessDirPath)

    def getDateBaseDirectory(self, fileName: str = None):
        '''获得要用到到的数据库文件的位置'''
        return self.getAbsPath(self.dataBasePath, fileName)

    def getStaticsDirectory(self):
        '''获得静态资源的绝对路径'''
        return self.getAbsPath(self.staticsPath)

    def findDictWithKey1Value(self, targetValue):
        '''快速找到不同模型类型所对应的第一个模型的dict值'''
        for key, subDict in self.apiModelList.items():
            if subDict.get("serviceType") == targetValue:
                return {key: subDict}
        return None


CONF = ProjectConfig()
