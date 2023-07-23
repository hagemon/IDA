## Introduction

Interactive data analysis with ChatGPT.

You can input the url of csv data and get some general analysis and figuring.

Further analysis are under construction.

## Usage

Add an `conf.json` file with following format:

```json
{
    "api_type": "azure",
    "api_base": "https://YOUR_DEPLOYMENT_NAME.openai.azure.com",
    "api_version": "2023-03-15-preview",
    "api_key": "YOUR_API_KEY"
}
```

You need to install [Streamlit](https://streamlit.io):

```bash
pip install streamlit
```

then run

```bash
streamlit run main.py
```