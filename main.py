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
def general_analysis(_chat, df, s):
    if _chat.empty:
        resp = gpt.chat(gpt.general_analysis_prompt(s))
        content, _, draw_op, transform_op, _ = gpt.format(resp)
    else:
        content = _chat.general.content
        transform_op = (
            _chat.transform_op
        )  # this operation contains the usage of parameter `x`
        draw_op = _chat.general.draw_op
    exec(transform_op)
    fig = eval(draw_op)
    st.subheader("General Analysis")
    for c in content.split("\n"):
        st.write(c)
    st.dataframe(df, use_container_width=True)
    st.pyplot(fig=fig, clear_figure=True)
    if _chat.empty:
        fetch.add_content(_chat, content, draw_op, transform_op, gen=True)
    return df


@st.cache_data(show_spinner="Analyzing")
def followup_analysis(_chat, df, s, cmd):
    resp = gpt.chat(gpt.followup_analysis_prompt(s, cmd))
    content, _, draw_op, transform_op, title = gpt.format(resp)
    exec(transform_op)
    fig = eval(draw_op)
    st.subheader(title)
    for c in content.split("\n"):
        st.write(c)
    st.dataframe(df, use_container_width=True)
    st.pyplot(fig=fig, clear_figure=True)
    fetch.add_content(_chat, content, draw_op, transform_op, title=title, gen=False)
    return df


def show_content(chat, df):
    exec(chat.transform_op)
    fig = eval(chat.draw_op)
    st.subheader(chat.title)
    st.write(chat.content)
    st.dataframe(df, use_container_width=True)
    st.pyplot(fig=fig)


def enable_gen_btn(flag):
    st.session_state["gen_btn"] = flag


def submit(chat_id):
    st.session_state[chat_id] = st.session_state.widget
    st.session_state["widget"] = ""


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
        if (
            st.button(
                "General Analysis",
                disabled=not st.session_state.gen_btn,
            )
            and chat.empty
        ):
            enable_gen_btn(False)
            df = general_analysis(chat, df, df_str)
        else:
            for c in chat.contents:
                show_content(c, df)
        if not chat.empty:
            text_id = f"{chat.id}_text"
            if text_id not in st.session_state:
                st.session_state[text_id] = ""
            st.text_input(
                "Enter commands for further analysis.",
                key="widget",
                on_change=submit,
                args=[text_id],
            )
            if st.session_state[text_id]:
                followup_analysis(chat, df, df.to_csv(), st.session_state[text_id])