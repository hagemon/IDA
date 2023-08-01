import pandas as pd
import streamlit as st
import gpt
import tools
from streamlit_option_menu import option_menu
import fetch


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


chats = fetch.get_chats()
if len(chats) > 0:
    st.session_state['idx'] = 0

with st.sidebar:
    if st.button('Add', use_container_width=True):
        fetch.add_chat()
        chats = fetch.get_chats()
        st.session_state['idx'] = 0
    if len(chats) > 0:
        option_menu(None, [c.title for c in chats],
                    manual_select=st.session_state.idx)


if 'idx' in st.session_state:
    chat = chats[st.session_state.idx]
    st.title(chat.title)
    url = st.text_input('Please enter the URL of data file.')
    st.text(chat.url)
    df, df_str = load_data(url)
    if df_str is not None:
        if st.button('General Analysis'):
            general_analysis(st.session_state.selected, df_str)
            for c in chat.contents:
                st.write(c.content)
            st.text_input('Enter commands for further analysis.')
