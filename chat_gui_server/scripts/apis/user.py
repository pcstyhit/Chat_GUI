import fastapi
from scripts.modules.umm import authenticateUser, UserManage
from scripts.libs.arqm import LoginAndLogoutRequest
from scripts.libs.arsm import LoginAndLogoutResponse
from scripts.libs.arqm import *
from scripts.libs.arsm import *

USER_ROUTE = fastapi.APIRouter()


@USER_ROUTE.post('/login')
async def loginAPI(_: LoginAndLogoutRequest,
                   user: str = fastapi.Depends(authenticateUser)):
    '''插件模式 fastapi.Deepends添加对身份信息的验证
    实际上 可以写成 @LOGINANLOGOUTROUTER.post('/login', dependencies=[fastapi.Depends(authenticateUser)])
    只是如果再想获取headers内的身份会再次调用fastapi.Depends(authenticateUser)
    '''
    rea: LoginAndLogoutResponse = await UserManage.loginAPI(user)
    # FastAPI 可以直接返回 rea，它将会自动的转换为 JSON格式
    return rea


# ==================================================
# ⚙️ 获得用户的默认对话参数
# ==================================================


@USER_ROUTE.get('/user/getUserChatParams')
async def getUserChatParamsAPI(user: str = fastapi.Depends(authenticateUser)):
    rea = GetUserChatParamsResponse()
    rea.data = await UserManage.getUserChatDefParamsAPI(user)
    rea.flag = True
    return rea

# ==================================================
# ✏️ setUserChatParamsAPI 修改用户的默认对话参数
# ==================================================


@USER_ROUTE.post('/user/setUserChatParams')
async def setUserChatParamsAPI(item: SetUserChatParamsAPIRequest, user: str = fastapi.Depends(authenticateUser)):
    rea = SetUserChatParamsResponse()
    rea.flag = await UserManage.setUserChatDefParamsAPI(user, item.data)
    return rea

# ==================================================
# ⚙️ getUserSettingAPI 获得用户的默认设置参数的信息
# ==================================================


@USER_ROUTE.get('/user/getUserSetting')
async def getUserSettingAPI(user: str = fastapi.Depends(authenticateUser)):
    rea = GetUserSettingResponse()
    rea.data = await UserManage.getUserSettingsAPI(user)
    rea.flag = True
    return rea

# ==================================================
# ✏️ setUserSettingAPI 修改用户的默认设置内容
# ==================================================


@USER_ROUTE.post('/user/setUserSetting')
async def setUserSettingAPI(item: SetUserSettingAPIRequest, user: str = fastapi.Depends(authenticateUser)):
    rea = SetUserSettingResponse()
    rea.flag = await UserManage.setUserSettingsAPI(user, item.data)
    return rea
