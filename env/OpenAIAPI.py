import openai
import Config
from validation import validate_text


class API:
    openai.api_key = Config.API_KEY

    @classmethod
    def send_request(cls, system: str, content: str) -> str:
        validate_text(system)
        validate_text(content)
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
            messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": content}
            ])
        return completion.choices[0].message.content
