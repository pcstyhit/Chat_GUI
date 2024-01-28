import json

def dict2Str(dictObj: dict) -> tuple:
    '''Ensure the dict data to be string, It has two return data.
    If it falied, it will return "" and False.
     - (dict) dictObj: The dict data from socket.
    '''
    flag = False
    try:
        rea = json.dumps(dictObj)
        flag = True
    except Exception as eMsg:
        rea = ""
        print('[ERROR] - dict2Str', eMsg)
    return rea, flag


def str2Dict(strObj: str) -> tuple:
    '''Ensure the string data to be dict,.It has two return data. If it falied, it will return "" and False.
     - (string) strObj: The string data from web.
    '''
    flag = False
    if strObj != None:
        strObj = str(strObj)
        try:
            rea = json.loads(strObj)
            flag = True
        except Exception as eMsg:
            rea = {}
            print('[ERROR] - str2Dict', eMsg)
        return rea, flag
    else:
        return {}, True