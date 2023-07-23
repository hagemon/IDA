import openai
from tools import converter
import json


with open('conf.json') as f:
    obj = json.load(f)
    openai.api_type = obj['api_type']
    openai.api_base = obj['api_base']
    openai.api_version = obj['api_version']
    openai.api_key = obj['api_key']


def general_analysis_prompt(src):
    prompt = '''Here is a csv file string:

{}

Please check this data and do basic analysis, feed back in following json format:
{{
    \"content\": do general analysis on this data and give some implied information, note that you must seperate each sentences with `\\n`.
    \"figure_type\": choose a figure type to supports analysis, with the support from `kind` parameter in `df.plot` function.
    \"operation\": the single line code that return `figure` object using `df.plot.figure`, you can add additional columns for analysing before drawing. Make sure the code could run withour error.
}}
Note that you must only return the json text without any other information!
'''.format(src)
    print(prompt)
    return prompt


def chat(content):
    response = openai.ChatCompletion.create(
            engine="gpt-35-turbo",
            messages = [
                {"role":"system","content":"You are an expert of data analysis, please help me with some data"},
                {'role':'user','content':content}
            ],
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )
    return response['choices'][0]['message']['content']


def format(resp):
    print(resp)
    obj = converter(resp)
    content = obj['content']
    figure_type = obj['figure_type']
    op = obj['operation']
    if not op.endswith('figure'):
        op = op+'.figure'
    return content, figure_type, op


if __name__ == '__main__':
    response = openai.ChatCompletion.create(
            engine="gpt-35-turbo",
            messages = [
                {"role":"system","content":"Greeting!"},
                {'role':'user','content':'Hello!'}
            ],
            temperature=0.7,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )
    print(response)