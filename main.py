import pandas as pd
import streamlit as st
import gpt
import streamlit_antd_components as sac
import fetch


@st.cache_data(show_spinner="Downloading")
def load_data(src):
    if src:
        try:
            x = pd.read_csv(src)
        except Exception:
            st.error("Something wrong with the given url.")
            return None, None
        print(x.columns)
        x.columns = [c.replace('"', "").strip() for c in x.columns]
        st.dataframe(x, use_container_width=True)
        return x, x.to_csv()
    return None, None


@st.cache_data(show_spinner="Analyzing")
def general_analysis(_chat, s):
    if _chat.empty:
        resp = gpt.chat(gpt.general_analysis_prompt(s))
        content, _, op = gpt.format(resp)
    else:
        content = _chat.general.content
        op = _chat.general.operation
    fig = eval(op)
    st.subheader("General Analysis")
    for c in content.split("\n"):
        st.write(c)
    st.pyplot(fig=fig)
    if _chat.empty:
        fetch.add_content(_chat, content, op, gen=True)


def enable_gen_btn(flag):
    st.session_state["gen_btn"] = flag


chats = fetch.get_chats()
if len(chats) > 0:
    st.session_state["idx"] = 0

with st.sidebar:
    if st.button("Add", use_container_width=True):
        fetch.add_chat()
        chats = fetch.get_chats()
        st.session_state["idx"] = 0
    if len(chats) > 0:
        idx = sac.menu([c.title for c in chats], return_index=True)
        st.session_state["idx"] = idx


if "idx" in st.session_state:
    chat = chats[st.session_state.idx]
    enable_gen_btn(True)
    st.title(chat.title)
    url = st.text_input(
        "Please enter the URL of data file.", value=chat.url, key=chat.id
    )
    if url != chat.url:
        fetch.add_url(chat, url)
    df, df_str = load_data(url)
    if df_str is not None:
        if st.button(
            "General Analysis",
            disabled=st.session_state.gen_btn,
        ) and chat.empty:
            enable_gen_btn(False)
            general_analysis(chat, df_str)
        else:
            for c in chat.contents:
                fig = eval(c.operation)
                st.write(c.content)
                st.pyplot(fig=fig)
        st.text_input("Enter commands for further analysis.")
