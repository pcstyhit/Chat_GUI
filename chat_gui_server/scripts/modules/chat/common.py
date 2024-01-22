from openai import AzureOpenAI
from scripts.libs import ACCT


async def chatByText(msg: str, acct: dict = ACCT) -> None:
    client = AzureOpenAI(
        azure_endpoint=acct['end_point'],
        api_key=acct['api_key'],
        api_version=acct['api_version']
    )

    response = client.chat.completions.create(
        model=acct['deployment'],
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': msg},
        ]
    )

    return response.choices[0].message.content
