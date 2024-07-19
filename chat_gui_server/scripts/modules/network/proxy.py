'''
每个用户会开辟一个操作这个用户是不是要使用网络代理的句柄
'''

import httpx
from scripts.libs import CONF
from httpx._config import DEFAULT_TIMEOUT_CONFIG as HTTPX_DEFAULT_TIMEOUT


class HttpxProxy:
    def __init__(self) -> None:
        self.isUseProxy = CONF.isUseProxy
        self.proxyURL = CONF.proxyURL
        self.client: httpx.Client = None
        self.timeout = HTTPX_DEFAULT_TIMEOUT

        self.updateClient()

    def updateClient(self) -> httpx.Client:
        self.client = None
        if self.isUseProxy and self.proxyURL != '':
            self.client = httpx.Client(
                proxies={'http://': self.proxyURL, 'https://': self.proxyURL})

    def setHttpxClient(self, data: dict):
        isUseProxy = data.get("isUseProxy", False)
        proxyURL = data.get("proxyURL", "")
        self.isUseProxy = isUseProxy
        self.proxyURL = proxyURL
        self.updateClient()

    async def getHttpxInfo(self):
        return {
            "isUseProxy": self.isUseProxy,
            "proxyURL": self.proxyURL
        }
