import os

import speech_recognition as sr
from dotenv import load_dotenv

from . import listen
from .openai_chat_completion_scripture_inferer import (
    OpenAIChatCompletionScriptureInferer,
)
from .openai_whisper_speech_transcriber import OpenAIWhisperSpeechTranscriber


def main():
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    assert api_key is not None

    transcriber = OpenAIWhisperSpeechTranscriber(api_key=api_key)

    scripture_inferer = OpenAIChatCompletionScriptureInferer(api_key=api_key)

    microphone = sr.Microphone()

    try:
        for audio_data in listen(microphone):
            value = transcriber.transcribe(audio_data)
            print(f'Speech "{value}"')
            print(scripture_inferer.infer(value))
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
