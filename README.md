## Introduction

Interactive data analysis with ChatGPT.

You can input the url of csv data and get some general analysis and figuring.

Further analysis are under construction.

## Usage

### Pre-requirements

```bash
pip install requirements.txt
```

### LLM Configuration

Add an `conf.json` file with following format:

```json
{
    "api_type": "azure",
    "api_base": "https://YOUR_DEPLOYMENT_NAME.openai.azure.com",
    "api_version": "2023-03-15-preview",
    "api_key": "YOUR_API_KEY"
}
```

### Database Configuration

Using `docker` or `orbstack` and run:

```bash
docker pull postgres
docker run --name postgres -e POSTGRES_PASSWORD=PASSWORD -d postgres
```

then create `.streamlit/secret.toml` file:

```toml
# .streamlit/secrets.toml

[postgres]
host = "localhost"
port = 5432
dbname = "dbname"
user = "USERNAME"
password = "PASSWORD"
```

### Run

```bash
streamlit run main.py
```