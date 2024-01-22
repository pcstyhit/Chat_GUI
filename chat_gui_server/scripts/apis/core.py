import fastapi
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from .postChat import CHATROUTER

app = fastapi.FastAPI()

app.include_router(CHATROUTER)

def debug():
    '''设置调试模式下的一些web server的配置'''
    # 配置允许跨域请求的来源
    origins = [
        "http://127.0.0.1:8080",
        "http://localhost:8080",
        "http://192.168.125.150:8080"
    ]

    # 启用 CORS 中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],  # 允许所有 HTTP 方法
        allow_headers=["*"],  # 允许所有 HTTP 头部
    )

def run():
    '''启动fastapi webserver 服务'''
    debug()
    uvicorn.run(app, host="0.0.0.0", port=5001)
