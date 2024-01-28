import fastapi
from scripts.modules.chat import getAllHistory

CHATGETROUTE = fastapi.APIRouter()

@CHATGETROUTE.get('/chat/{parameters}')
async def getCore(parameters: str):
    rea = None
    if parameters == 'allHistory':
        rea = getAllHistory()
    return {'name': parameters, 'data': rea}
