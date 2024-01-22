import os
import configparser


def getMyAccountInfo():
    cf = configparser.ConfigParser()
    absPath = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    cf.read(f'{absPath}/config.cfg', encoding='utf-8')

    endPoint = cf.get('my_account', 'end_point')
    apiKey = cf.get('my_account', 'api_key')
    deployment = cf.get('my_account', 'deployment')
    apiVersion = cf.get('my_account', 'api_version')

    return {'end_point': endPoint, 'api_key': apiKey, 'deployment': deployment, 'api_version': apiVersion}


ACCT = getMyAccountInfo()
