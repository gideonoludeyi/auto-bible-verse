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
$ pdm install
```

5. Start program

```sh
$ pdm run start
```

## Download YouTube Audio

```sh
$ pdm run download [YouTube Video URL] | ffmpeg -y -v error -i - audio.wav
```

## Split audio into segments

```sh
$ pdm run split /path/to/audio [--segment-duration=8] [--output-dir=./out]
```

## Transcribe audio

```sh
$ pdm run transcribe --credentials=[OpenAI API Key] --file=/path/to/audio
```

## Extract Scripture References from text transcript

```sh
$ pdm run extract --credentials=[OpenAI API Key] --text="TEXT"
```
