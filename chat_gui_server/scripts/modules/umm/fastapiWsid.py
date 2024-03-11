'''
管理用户的websocket的值
'''
import secrets

'''
一个wsid的实例形如:
{
    '9c8b3efdaef7dd8d':      # id
    {
        'user':'test1',      # 用户名
        'type':'chat',       # 用途
    }

}
'''
WSIDS = {}


def generateWsid():
    '''生成随机的八位的wsid'''
    tks = secrets.token_hex(8)
    if tks not in WSIDS.keys():
        return tks
    else:
        generateWsid()


def addWsid(user: str, type: str) -> str:
    '''一个wsid对应一个用户, 创建websocket和用户的对应关系
     - type (str): 作为保留关键字,不限定用户可以有多个websocket
    '''
    wsid = generateWsid()
    WSIDS[wsid] = {'user': user, 'type': type}
    return wsid


def getUser(wsid):
    '''根据wsid查询用户身份'''
    info: dict = WSIDS.get(wsid)
    if info == None:
        return info
    return info.get('user')


def getType(wsid):
    '''根据wsid获得websocket的用途类型'''
    info: dict = WSIDS.get(wsid)
    if info == None:
        return info
    return info.get('type')


def delWsid(wsid):
    '''删除一个wsid对应的信息'''
    del WSIDS[wsid]
