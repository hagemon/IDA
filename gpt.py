import openai
from tools import converter
import json

"""
Basic operations
"""

with open("conf.json") as f:
    obj = json.load(f)
    openai.api_type = obj["api_type"]
    openai.api_base = obj["api_base"]
    openai.api_version = obj["api_version"]
    openai.api_key = obj["api_key"]


def format(resp):
    print(resp)
    obj = converter(resp)
    content = obj["content"]
    figure_type = obj["figure_type"]
    draw_op = obj["draw_op"]
    transform_op = obj["transform_op"]
    if not draw_op.endswith("figure"):
        draw_op = draw_op + ".figure"
    title = obj["title"] if "title" in obj else "General"
    return content, figure_type, draw_op, transform_op, title


def chat(content):
    response = openai.ChatCompletion.create(
        engine="gpt-35-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an expert of data analysis, please help me with some data",
            },
            {"role": "user", "content": content},
        ],
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
    )
    return response["choices"][0]["message"]["content"]


"""
Prompt
"""


def general_analysis_prompt(src):
    prompt = """Here is a csv file string:

{}

Please check this data and do basic analysis, feed back in following json format:
{{
    \"content\": give some analysis about given data on their statistic, relations or trends.
    \"figure_type\": choose a figure type to supports analysis, with the support from `kind` parameter in `df.plot` function.
    \"transform_op\": a single line code that having some inplace operation on dataframe `df`, which must supports your analysis. Make sure the code could run without error.
    \"draw_op\": a single line code that returns `figure` object using `df.plot().figure`, the figure can use columns that added in `transform_op`. Make sure the code could run without error.
}}
Note that you must only return the json text without any other information!
""".format(
        src
    )
    print(prompt)
    return prompt


def followup_analysis_prompt(src, cmd):
    prompt = f"""Here is a csv file string:

{src}

Please check this data and do basic analysis, feed back in following json format:
{{
    \"content\": following this command {cmd}, and give more specific analysis about given data on their values, statistic, relations or trends.
    \"figure_type\": choose a figure type to supports analysis, with the support from `kind` parameter in `df.plot` function.
    \"draw_op\": the single line code that return `figure` object using `df.plot.figure`, you can add additional columns for analysing before drawing. Make sure the code could run without error.
    \"transform_op\": the single line code that return `figure` object using `df.plot.figure`, you can add additional columns for analysing before drawing. If there is no neccessity, please return `pass`. Make sure the code could run without error.
    \"title\": a clear title for this analysis.
}}
Note that you must only return the json text without any other information!
"""
    print(prompt)
    return prompt


if __name__ == "__main__":
    response = openai.ChatCompletion.create(
        engine="gpt-35-turbo",
        messages=[
            {"role": "system", "content": "Greeting!"},
            {"role": "user", "content": "Hello!"},
        ],
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
    )
    print(response)
