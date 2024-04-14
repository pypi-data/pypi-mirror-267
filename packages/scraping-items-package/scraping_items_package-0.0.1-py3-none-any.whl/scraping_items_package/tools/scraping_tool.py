from promptflow import tool
from promptflow.connections import CustomConnection
import anthropic
import create_response

@tool
def find_parts(input1: str, input2: str = None, connection: CustomConnection = None,  model: str = "claude-3-opus-20240229", temperature: int = 0, max_tokens: int = 500) -> str:
    client = anthropic.Anthropic(
        api_key=connection.api_key
    )
    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": input1
                    }
                ]
            }
        ]
    )
    return message.content