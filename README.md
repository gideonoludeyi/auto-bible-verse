# Automated Bible Verse (Speech-To-Text)

## Getting Started

1. Setup template for environment variables

```sh
$ cp .env.example .env
```

2. Setup OpenAI API Key

- set the `OPENAI_API_KEY` env variable in `.env` to the api key for your [openai account](https://platform.openai.com/account/api-keys).

3. Install dependencies

```sh
$ poetry install
```

5. Start program

```sh
$ poetry run start
```

## Download YouTube Audio

```sh
$ poetry run download [YouTube Video URL] | ffmpeg -y -v error -i - audio.wav
```

## Split audio into segments

```sh
$ poetry run split /path/to/audio [--segment-duration=8] [--output-dir=./out]
```

## Transcribe audio

```sh
$ poetry run transcribe --credentials=[OpenAI API Key] --file=/path/to/audio
```

## Extract Scripture References from text transcript

```sh
$ poetry run extract --credentials=[OpenAI API Key] "TEXT"
```
