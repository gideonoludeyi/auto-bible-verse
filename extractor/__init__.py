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
    "-f",
    "--file",
    dest="textfile",
    help="transcription file from which to extract scripture references [default: read from stdin or use `-`]",
    type=argparse.FileType("r"),
    default=sys.stdin,
)
parser.add_argument(
    "-c",
    "--credentials",
    dest="credentials",
    help="OpenAI api key",
    type=str,
    default=os.getenv("OPENAI_API_KEY"),
)


def main() -> int:
    args = parser.parse_args()
    assert args.credentials is not None

    inferer = OpenAIChatCompletionScriptureInferer(api_key=args.credentials)
    with args.textfile as f:
        result = inferer.infer(f.read())

    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
