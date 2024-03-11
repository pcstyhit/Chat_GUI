import fastapi
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from .login import LOGIN_OUT_ROUTER
from .chat import CHAT_ROUTE

app = fastapi.FastAPI()

app.include_router(LOGIN_OUT_ROUTER)
app.include_router(CHAT_ROUTE)


def debug():
    '''设置调试模式下的一些web server的配置'''
    # 启用 CORS 中间件, 配置允许跨域请求的来源
    app.add_middleware(CORSMiddleware,
                       allow_origins=["*"],  # 允许所有 跨越URL 方法
                       allow_methods=["*"],  # 允许所有 HTTP 方法
                       allow_headers=["*"],  # 允许所有 HTTP 头部
                       )


def run():
    '''启动fastapi webserver 服务'''
    debug()
    uvicorn.run(app, host="0.0.0.0", port=5001)
