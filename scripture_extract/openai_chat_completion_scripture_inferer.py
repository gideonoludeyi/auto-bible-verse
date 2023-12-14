import openai


class OpenAIChatCompletionScriptureInferer:
    def __init__(self, *, api_key: str) -> None:
        self._api_key = api_key

    def infer(self, text: str) -> list[str]:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that is displaying the list of scriptures referenced in a preacher's sermon",
                },
                {
                    "role": "user",
                    "content": "The following transcript was extracted from a preacher's sermon. List the scripture references explicitly mentioned as bullet points in the American System of Biblical References format:",
                },
                {"role": "user", "content": text},
            ],
            api_key=self._api_key,
        )
        content = response["choices"][0]["message"]["content"]
        return [ref.replace("-", "").strip() for ref in content.split("\n")]
