# Automated Bible Verse

## Development

### 1. Setup template for environment variables

```sh
$ cp .env.example .env
```

### 2. Setup OpenAI API Key

- set the `OPENAI_API_KEY` env variable in `.env` to the api key of your [openai account](https://platform.openai.com/account/api-keys).

### 3. Install dependencies

```sh
$ python -m venv .venv
$ source .venv/bin/activate # .venv\Scripts\activate.bat (for Windows)
$ pip install -e '.[dev]' # install the current project, along with all it's "dev" dependencies
```

### 4. Start program

```sh
$ python -m src.autoscript
```

#### 4.1 Download YouTube Audio

```sh
$ python -m src.ytdownloader [YouTube Video URL] | ffmpeg -y -v error -i - ./tmp/audio.wav
```

#### 4.2 Split audio into segments

```sh
$ python -m src.splitter ./tmp/audio.wav [--segment-duration=8] [--output-dir=./tmp]
```

#### 4.3 Transcribe audio

```sh
$ python -m src.transcriber --credentials=[OpenAI API Key] --file=./tmp/audio.wav
```

#### 4.4 Extract Scripture References from text transcript

```sh
$ python -m src.extractor --credentials=[OpenAI API Key] --file=/path/to/transcription_file
```
