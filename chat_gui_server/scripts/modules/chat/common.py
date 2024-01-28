'''
用来处理一些简单的响应式的回答.
'''
from openai import AzureOpenAI
from scripts.libs import CONF

from .messages import updateMessage, writeMessageToFile
from .tokens import accont, writeTokenToFile


def chatCore(msg: str, name='test', acct: dict = CONF) -> str:
    '''结合上下文进行对话的核心函数
        https://zhuanlan.zhihu.com/p/618911413
    '''
    client = AzureOpenAI(
        azure_endpoint=acct['end_point'],
        api_key=acct['api_key'],
        api_version=acct['api_version']
    )

    # 增加上下文信息
    messgaes = updateMessage('user', msg)
    response = client.chat.completions.create(
        model=acct['deployment'], messages=messgaes)
    ans = response.choices[0].message.content
    usage = accont(response)
    updateMessage('assistant', response.choices[0].message.content)
    writeMessageToFile(name)
    writeTokenToFile(name)
    # 返回文本信息
    return {'ans': ans, 'usage': usage}


async def chatByText(name: str, msg: str) -> str:
    '''将核心函数变成异步的'''
    return chatCore(msg, name)


async def chatStream(msg: str, name='test', acct: dict = CONF) -> str:
    '''结合上下文进行对话的核心函数
        https://zhuanlan.zhihu.com/p/618911413
    '''
    client = AzureOpenAI(
        azure_endpoint=acct['end_point'],
        api_key=acct['api_key'],
        api_version=acct['api_version']
    )

    # 增加上下文信息
    messgaes = updateMessage('user', msg)
    response = client.chat.completions.create(model=acct['deployment'], messages=messgaes,       stream=True,
                                              temperature=0,)
    all_content = ''
    async for chunk in response:
        # TBD: [DONE]在chunk中的准确位置
        if chunk == '[DONE]':
            # stream结束，复写Messages变量，Messages文件，Token文件
            updateMessage('assistant', all_content)
            writeMessageToFile(name)
            writeTokenToFile(name)
            # No need to start new yield
            # yield {'done': True}
        else:
            content = chunk.choices[0].delta.content
            if content:
                all_content += content
                # TBD: usage在chunk中的准确位置
                usage = accont(chunk)
                yield {'ans': content, 'usage': usage}
