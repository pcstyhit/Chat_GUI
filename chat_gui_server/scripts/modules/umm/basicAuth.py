from fastapi import Depends, HTTPException, status  
from fastapi.security import HTTPBasic, HTTPBasicCredentials  
import secrets  

from scripts.libs import CONF
security = HTTPBasic()

def authenticateUser(credentials: HTTPBasicCredentials = Depends(security)):
    '''校验得到的basic auth的身份是否满足要求'''
    flag = False
    for item in CONF['userList']:
        username = secrets.compare_digest(credentials.username, item['user'])  
        password = secrets.compare_digest(credentials.password, item['pwd'])  
        flag = username and password
        # 验证成功跳出循环, 并得到用户名
        if(flag):
            return item['user']
    
    # 校验失败返回401
    raise HTTPException(  
        status_code=status.HTTP_401_UNAUTHORIZED,  
        detail="Incorrect username or password",  
        headers={"WWW-Authenticate": "Basic"},  
    )