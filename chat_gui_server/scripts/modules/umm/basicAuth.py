from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

from scripts.libs import CONF
security = HTTPBasic()


def authenticateUser(credentials: HTTPBasicCredentials = Depends(security)):
    '''校验得到的basic auth的身份是否满足要求'''
    flag = secrets.compare_digest(credentials.username, credentials.password)
    # 随机测试的用户只要保证用户名和密码是一样的由Test+number组成即可
    if (flag):
        return credentials.username

    # 校验失败返回401
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Basic"},
    )
