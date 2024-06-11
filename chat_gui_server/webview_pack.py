import webview
import threading

from scripts.libs import CONF
from scripts.apis.core import runWithStatics


def startPywebview():
    webview.create_window('', f"http://{CONF.host}:{CONF.port}")
    webview.start()


if __name__ == "__main__":
    fastapiThread = threading.Thread(target=runWithStatics,)
    fastapiThread.start()
    startPywebview()
