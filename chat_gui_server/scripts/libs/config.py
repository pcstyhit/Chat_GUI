import os
import configparser
import json

CONF = dict()
DIR_LOOP = 3


def getMyAccountInfo():
    '''配置个人私钥'''
    cf = configparser.ConfigParser()
    absPath = os.path.dirname(os.path.dirname(
        os.path.abspath(os.path.dirname(__file__))))
    cf.read(f'{absPath}/config.cfg', encoding='utf-8')

    endPoint = cf.get('my_account', 'end_point')
    apiKey = cf.get('my_account', 'api_key')
    deployment = cf.get('my_account', 'deployment')
    apiVersion = cf.get('my_account', 'api_version')

    return {'end_point': endPoint, 'api_key': apiKey, 'deployment': deployment, 'api_version': apiVersion}


def updateConfigurations():
    global CONF
    '''更新项目配置'''
    CONF = getMyAccountInfo()

    project_path = os.path.abspath(__file__)
    for _ in range(DIR_LOOP):
        project_path = os.path.dirname(project_path)

    configFile = f'{project_path}/config.json'
    with open(file=configFile, mode='r') as f:
        configurations = json.load(f)
        configurations['project_path'] = project_path

    CONF.update(configurations)

    return CONF


def getAbsPath(pathKey: str, fileName: str = None):
    '''获取某些绝对路径'''
    if fileName == None:
        return f"{CONF['project_path']}/{CONF[pathKey]}"
    else:
        return f"{CONF['project_path']}/{CONF[pathKey]}/{fileName}"


def joinAbsPath(pathKey: str, floderName: str = None, fileName: str = None):
    '''拼接绝对路径'''
    if floderName == None:
        if fileName == None:
            return f"{CONF['project_path']}/{CONF[pathKey]}"
        else:
            return f"{CONF['project_path']}/{CONF[pathKey]}/{fileName}"
    else:
        if fileName == None:
            return f"{CONF['project_path']}/{CONF[pathKey]}/{floderName}"
        else:
            return f"{CONF['project_path']}/{CONF[pathKey]}/{floderName}/{fileName}"


CONF = updateConfigurations()
