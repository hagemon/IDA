import json
import pandas as pd

def converter(s):
    left = s.find('content')
    right = s.find('\n    "figure_type"')
    s = s[:left] + s[left:right].replace('\n', '\\n\\n') + s[right:]
    obj = json.loads(s)
    return obj


def csv2str(url):
    df = pd.read_csv(url)
    return df.to_csv()

if __name__ == '__main__':
    src = 'https://people.sc.fsu.edu/~jburkardt/data/csv/cities.csv'
    print(csv2str(src))