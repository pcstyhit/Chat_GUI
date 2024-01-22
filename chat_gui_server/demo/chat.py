from openai import AzureOpenAI

from scripts.libs import ACCT


def helloGPT(acct: dict = ACCT) -> None:
    client = AzureOpenAI(
        azure_endpoint=acct['end_point'],
        api_key=acct['api_key'],
        api_version=acct['api_version']
    )

    response = client.chat.completions.create(
        model=acct['deployment'],
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': 'Does Azure OpenAI support customer managed keys?'},
            {'role': 'assistant',
                'content': 'Yes, customer managed keys are supported by Azure OpenAI.'},
            {'role': 'user', 'content': 'Do other Azure AI services support this too?'}
        ]
    )

    print(response.choices[0].message.content)


def sayWithGPT(msg: str, acct: dict = ACCT) -> None:
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

    print(response.choices[0].message.content)


def sayWithGPT_Stream(msg: str, acct: dict = ACCT):
    import time
    import json

    # Assuming you have an AzureOpenAI class defined

    # Instantiate the AzureOpenAI client
    client = AzureOpenAI(
        azure_endpoint=acct['end_point'],
        api_key=acct['api_key'],
        api_version=acct['api_version']
    )

    # Set up parameters
    start_time = time.time()
    delay_time = 0.01  # faster

    # Specify the message and generate chat completion
    msg = "Your user message here"
    response = client.chat.completions.create(
        model=acct['deployment'],
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': msg},
        ],
        stream=True,
        temperature=0,
    )

    # Iterate over the chunks of data received in the streaming response
    for chunk in response.iter_content(chunk_size=None):
        # Parse the chunk (assuming it's in JSON format)
        data = json.loads(chunk)

        # Check if 'choices' is present in the chunk
        if 'choices' in data:
            choices = data['choices']
            print(choices)

    # Note: This is a simplified example. You might need to adjust it based on the actual structure of the streaming response.
