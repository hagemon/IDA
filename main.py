import pandas as pd
import numpy as np
import streamlit as st
import gpt

@st.cache_data(show_spinner='Downloading')
def load_data(src):
    if src:
        x = pd.read_csv(src)
        x.columns = [c.replace('"', '').strip() for c in x.columns]
        st.dataframe(x)
        return x, x.to_csv()
    return None, None


@st.cache_data(show_spinner='Analyzing')
def general_analysis(s):
    resp = gpt.chat(gpt.general_analysis_prompt(s))
    content, _, op = gpt.format(resp)
    fig = eval(op)
    st.subheader('General Analysis')
    for c in content.split('\n'):
        st.write(c)
    st.pyplot(fig=fig)


st.title('Interaction Data Analysis')
url = st.text_input('Please enter the URL of data file.')
st.text('https://people.sc.fsu.edu/~jburkardt/data/csv/homes.csv')
df, df_str = load_data(url)
if df_str is not None:
    if st.button('General Analysis'):
        general_analysis(df_str)
        st.text_input('Enter commands for further analysis.')
