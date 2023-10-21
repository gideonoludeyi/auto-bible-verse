import argparse

from scripture_extract.openai_chat_completion_scripture_inferer import (
    OpenAIChatCompletionScriptureInferer
)


parser = argparse.ArgumentParser(
    prog="Scripture Reference Extractor",
    description="Extract a list of scripture references from a text transcription")
parser.add_argument(
    "text", help="transcription from which to extract scripture references", type=str)
parser.add_argument("-c", "--credentials", dest="credentials",
                    help="OpenAI api key", required=True, type=str)


def main():
    args = parser.parse_args()

    text = args.text

    inferer = OpenAIChatCompletionScriptureInferer(
        api_key=args.credentials)

    result = inferer.infer(text)
    print(result)
