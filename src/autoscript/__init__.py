from typing import Generator, Any

import speech_recognition as sr


def listen(microphone: sr.Microphone, phrase_time_limit=5, timeout=10) -> Generator[sr.AudioData, Any, Any]:
    recognizer = sr.Recognizer()

    print("A moment of silence...")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
    print(f"Set minimum energy threshold to {recognizer.energy_threshold}")

    while True:
        with microphone as source:
            print("listening...")
            yield recognizer.listen(
                source, phrase_time_limit=phrase_time_limit, timeout=timeout
            )
