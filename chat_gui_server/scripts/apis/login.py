import fastapi
from pydantic import BaseModel

from scripts.modules.umm import authenticateUser, login, logout

LOGIN_OUT_ROUTER = fastapi.APIRouter()


class LoginAndLogoutRequest(BaseModel):
    '''login和logout的请求体'''
    data: str
    timeout: int


class LoginAndLogoutResponse(BaseModel):
    '''login和logout的应答体'''
    flag: bool = False
    msg: str = 'Password error'
    chatWsid: str = ''


@LOGIN_OUT_ROUTER.post('/login')
async def loginAPI(_: LoginAndLogoutRequest,
                   user: str = fastapi.Depends(authenticateUser)):
    '''插件模式 fastapi.Deepends添加对身份信息的验证
    实际上 可以写成 @LOGINANLOGOUTROUTER.post('/login', dependencies=[fastapi.Depends(authenticateUser)])
    只是如果再想获取headers内的身份会再次调用fastapi.Depends(authenticateUser)
    '''
    rea = LoginAndLogoutResponse()
    # 能够执行到函数体说明身份是正确的, 判断在线情况
    rea.flag, rea.msg, rea.chatWsid = login(user)
    # FastAPI 可以直接返回 rea，它将会自动的转换为 JSON格式
    return rea


@LOGIN_OUT_ROUTER.post('/logout')
async def logoutAPI(_: LoginAndLogoutRequest,
                    user: str = fastapi.Depends(authenticateUser)):
    rea = LoginAndLogoutResponse()
    rea.flag, rea.msg = logout(user)
    return rea
