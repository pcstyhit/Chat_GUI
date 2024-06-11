import os
import json
import configparser
from .encrypt import decryptDict


class CaseSensitiveConfigParser(configparser.ConfigParser):
    '''严格区分大小写的configparser'''

    def optionxform(self, optionstr):
        return optionstr  # 保持原样，不转换为小写


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
    PROJECTNESSDIR = {'dataBasePath'}

    DEFAULT_VALUE = {
        'adminUserPassword': 'pldz',
        'isLoginByTokenKey': False,
        'tokenKey': '',
        'isUseProxy': False,
        'proxyURL': '',

        'host': '0.0.0.0',
        'port': 10080,

        'dataBasePath': 'history',
        'staticsPath': 'statics',
        'systemConfigFileName': 'config.cfg',
        'userConfigFileName': 'config.json',

        'modelList': {},

        'default_modelName': '',
        'default_modelType': '',
        'default_apiKey': '',
        'default_apiVersion': '',
        'default_endPoint': '',
        'default_maxToken': '',
        'default_deployment': '',
    }

    def __init__(self) -> None:
        self.adminUserPassword: str = 'pldz'    # 默认的管理员密码
        self.isLoginByTokenKey: bool = False    # 是不是用tokenKey进行登录
        self.tokenKey: str = ''                 # 如果是tokenKey运行的值
        self.isUseProxy: bool = False           # 是否使用代理来连接GPT
        self.proxyURL: str = ''                 # GPT KEY请求的代理链接

        self.host: str = '127.0.0.1'            # 项目运行的Host address
        self.port: int = 10080                  # 项目运行的port号

        self.dataBasePath: str = '.dbpath'      # 数据库相对项目的路径
        self.staticsPath: str = 'statics'       # 静态资源相对项目的路径
        self.systemConfigFileName: str = 'config.cfg'
        self.userConfigFileName: str = 'config.json'

        self.modelList: dict = {}

        self.default_modelName: str = ''         # 配置的默认的模型的名字
        self.default_modelType: str = ''         # 默认模型的类型
        self.default_apiKey: str = ''
        self.default_apiVersion: str = ''
        self.default_endPoint: str = ''
        self.default_maxToken: str = ''
        self.default_deployment: str = ''

        '''项目自己用来实现功能帮助变量'''
        self.projectPath = self._getProjectAbsPath()

        '''从外部依赖文件导入配置, 先加入用户的设置,这个优先级更高, 然后再加载模型的设置'''
        self.updateUserConfig()
        self.updateModelConfig()
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

    def updateModelConfig(self):
        '''如果存在config.cfg就从这个文件读取项目的模型/系统层面的配置信息, 这个文件的格式要求会很严格'''

        systemConfigData: dict = {}   # 创建一个空的字典来存储所有数据

        if not self.isLoginByTokenKey:
            systemConfigFilePath = self.getAbsPath(self.systemConfigFileName)
            if not os.path.exists(systemConfigFilePath):
                print(
                    f'Not find the system config file ({systemConfigFilePath}) skip...')
                exit(1)

            # 读取cfg文件,并要求区分大小写
            cf = CaseSensitiveConfigParser()
            cf.read(systemConfigFilePath, encoding='utf-8')

            # 遍历所有section
            for section in cf.sections():
                # 将section下的所有键值对存储到一个子字典中
                sectionDict = {key: value for key, value in cf.items(section)}
                # 将子字典存储到主字典中，键为section名
                systemConfigData[section] = sectionDict
        else:
            if self.tokenKey == '':
                print(
                    f'Invalid user config (config.json) file. If you set isLoginByTokenKey true, you must privide tokenKey!')
                exit(1)

            # 解密
            try:
                systemConfigData = decryptDict(self.tokenKey, 'secretkey')
            except:
                print(f'Error tokenKey ... ... exit(1)')
                exit(1)

            # 判断是不是过期的tokenKey
            import time
            if (systemConfigData['expiredTime'] <= int(time.time())):
                print(f'Sorry tokenKey is expired!')
                exit(1)

            # 删除多余不必要的tokenKey
            del systemConfigData['expiredTime']
            self.tokenKey = ''

        # 更新模型的配置信息到self.modelList内
        self.checkModelCfgFileFormat(systemConfigData)

        # 如果self.modelList长度大于0, 那就把第一个模型信息作为当前的模型设置
        if (len(self.modelList) > 0):
            self.default_modelName = list(self.modelList.keys())[0]
            defaultModelDictData = self.modelList[self.default_modelName]
            # 赋值
            for key in defaultModelDictData:
                self.__dict__[f'default_{key}'] = defaultModelDictData[key]

    def updateUserConfig(self):
        '''如果有config.json的话, 用config.json更新用户的配置'''
        # 限定几个json包含的关键字
        userConfigFilePath = self.getAbsPath(self.userConfigFileName)

        if not os.path.exists(userConfigFilePath):
            print(
                f'Not find the user config file ({userConfigFilePath}) skip...')
            return

        # 读取json文件
        with open(userConfigFilePath, 'r') as file:
            userConfigData: dict = json.load(file)

            # 更新值
            for key in userConfigData:
                if key not in ProjectConfig.USERCONFIGFILEKEYLIST:
                    print(
                        f"Invalid value: {key}. config.json (user config) file should include the following contents {ProjectConfig.USERCONFIGFILEKEYLIST}")
                    continue
                self.__dict__[key] = userConfigData[key]

        # 注意 self.isUserProxy之后, self.proxyURL不能为空
        if self.isUseProxy and self.proxyURL == "":
            print("You have configured a proxy, but the proxy cannot be empty!")
            exit(1)

    def checkModelCfgFileFormat(self, systemConfigData: dict):
        '''校验config.cfg文件的格式, 必须包括下面keyList能看见的key, 并且存入Dict的key全部带入default
        一组有效的config.cfg文件的格式:
            [modelName<xxx>]
            modelType = xxx
            apiKey = xxx
            apiVersion = xxx
            endPoint = xxx
            maxToken = xxx
            deployment = xxx
        '''
        for modelName in systemConfigData:
            # 具体的模型内的值
            systemConfigData_item: dict = systemConfigData[modelName]

            if not ProjectConfig.MODELCFGKEYLIST.issubset(systemConfigData_item.keys()):
                print(
                    f"config.cfg (system config) file should include the following contents {modelCfgKeyList}")
                break
            else:
                # 将有效的内容存入self.modelList里面 并且加入一个default的修饰符
                self.modelList.update({modelName: systemConfigData_item})

    def resetProjectConfigByDefault(self):
        '''用默认的值来重置项目的设置'''
        for key in ProjectConfig.DEFAULT_VALUE:
            self.__dict__[key] = ProjectConfig.DEFAULT_VALUE[key]

        # 更新目录和外部文件的配置
        self.projectPath = self._getProjectAbsPath()
        self.updateModelConfig()
        self.updateUserConfig()
        self.checkProjectNecessaryDirectory()

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


CONF = ProjectConfig()
