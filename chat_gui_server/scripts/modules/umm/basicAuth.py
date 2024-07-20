from .core import UserManage
from scripts.libs.consts import APIAuth
from fastapi import Depends, HTTPException, status
from fastapi.requests import Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security = HTTPBasic()


def authenticateUser(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    '''校验得到的请求的身份是否满足要求'''
    print("cookies: ", request.cookies)
    print("credentials.username: ", credentials.username)

    ssid = request.cookies.get(APIAuth.SESSIONKEY, None)
    userName = UserManage.getUserBySession(ssid)
    if userName:
        print("session userName >>> ", userName)
        return userName

    # 如果是无效的session 用basic判断用户名是不是对的
    if credentials.username != 'undefined':
        flag = secrets.compare_digest(credentials.username, credentials.password)
        # 随机测试的用户只要保证用户名和密码是一样的由Test+number组成即可
        if (flag):
            print("basic auth userName >>> ", credentials.username)
            return credentials.username

    # 如果连正确的basic auth都是错误的 那表示WEB都没有点击login按钮 失败返回401
    return None
