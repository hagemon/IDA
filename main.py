import pandas as pd
import streamlit as st
import gpt
import tools
from streamlit_option_menu import option_menu
import conn

@st.cache_data(show_spinner='Downloading')
def load_data(src):
    if src:
        x = pd.read_csv(src)
        x.columns = [c.replace('"', '').strip() for c in x.columns]
        st.dataframe(x)
        return x, x.to_csv()
    return None, None


@st.cache_data(show_spinner='Analyzing')
def general_analysis(_, s):
    resp = gpt.chat(gpt.general_analysis_prompt(s))
    content, _, op = gpt.format(resp)
    fig = eval(op)
    st.subheader('General Analysis')
    for c in content.split('\n'):
        st.write(c)
    st.pyplot(fig=fig)
    

if 'chats' not in st.session_state:
    st.session_state['chats'] = []
elif len(st.session_state['chats']) > 0:
    st.session_state['selected'] = st.session_state.chats[0]

with st.sidebar:
    if st.button('Add', use_container_width=True):
        st.session_state['chats'] =[f'Analysis {tools.get_new_idx(st.session_state.chats)}'] + st.session_state['chats']
        st.session_state['selected'] = st.session_state.chats[0]
    if len(st.session_state.chats) > 0:
        selected = option_menu(None, st.session_state.chats, icons=[None for _ in st.session_state.chats])
        st.session_state['selected'] = selected


if 'selected' in st.session_state:
    st.title(st.session_state.selected)
    url = st.text_input('Please enter the URL of data file.')
    st.text('https://people.sc.fsu.edu/~jburkardt/data/csv/homes.csv')
    df, df_str = load_data(url)
    if df_str is not None:
        if st.button('General Analysis'):
            general_analysis(st.session_state.selected, df_str)
            # for c in st.session_state['chats']:
            #     st.write('Hi')
            st.text_input('Enter commands for further analysis.')
