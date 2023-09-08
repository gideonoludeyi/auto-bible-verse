# Automated Bible Verse (Speech-To-Text)

## Getting Started

1. Setup template for environment variables

```sh
$ cp .env.example .env
```

2. Setup Google Service Account Credentials

- create a `secrets` directory and place the Google Service Account Credentials JSON file in there
- set the `GOOGLE_APPLICATION_CREDENTIALS_FILEPATH` env variable in `.env` to the path to the Google Service Account Credentials JSON file

3. Install dependencies

```sh
$ poetry install
```

5. Start program

```sh
$ poetry run start
```
