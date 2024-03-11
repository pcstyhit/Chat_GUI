import asyncio
from scripts.modules.chat import ChatAPI

# 身份信息
handle = ChatAPI('test')


async def event_stream():
    for chunk in await handle.azureChatStreamAPI('fastapi如何实现text/event-stream的应答'):
        yield f'{chunk}\t'


async def main():
    async for chunk in event_stream():
        print(chunk, end='')

    print("")


def test_stream():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
