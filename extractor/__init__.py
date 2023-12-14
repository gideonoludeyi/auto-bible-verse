import sys
import os
import argparse

from scripture_extract.openai_chat_completion_scripture_inferer import (
    OpenAIChatCompletionScriptureInferer,
)


parser = argparse.ArgumentParser(
    prog="Scripture Reference Extractor",
    description="Extract a list of scripture references from text",
)
parser.add_argument(
    "-t",
    "--text",
    dest="text",
    help="transcription from which to extract scripture references",
    type=str,
)
parser.add_argument(
    "-c",
    "--credentials",
    dest="credentials",
    help="OpenAI api key",
    type=str,
    default=os.getenv("OPENAI_API_KEY"),
)


def main():
    args = parser.parse_args()

    assert args.credentials is not None

    if args.text is not None:
        text = args.text
    else:
        text = "".join(sys.stdin)

    inferer = OpenAIChatCompletionScriptureInferer(api_key=args.credentials)

    result = inferer.infer(text)
    print(result)
