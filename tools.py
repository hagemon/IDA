import json
import pandas as pd
import re

def converter(s):
    left = s.find('content')
    right = s.find('\n    "figure_type"')
    s = s[:left] + s[left:right].replace('\n', '\\n\\n') + s[right:]
    obj = json.loads(s)
    return obj


def csv2str(url):
    df = pd.read_csv(url)
    return df.to_csv()


def get_new_idx(chats):
    p = r'^Analysis (\d$)'
    matches = [re.findall(p, c) for c in chats]
    matches = [int(m[0]) for m in matches if m]
    idx = max(matches)+1 if matches else 1
    return idx

if __name__ == '__main__':
    # src = 'https://people.sc.fsu.edu/~jburkardt/data/csv/cities.csv'
    # print(csv2str(src))
    ch = ['Analysis 1', 'A 2', 'aaa', 'AAA4', 'Analysis 4', 'Analysis 6 Ana', 'aaAnalysis 8']
    print(get_new_idx(ch))