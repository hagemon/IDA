import fetch
import streamlit as st


class ChatList:
    def __init__(self, chats) -> None:
        self.chats = chats
        if "index" not in st.session_state:
            self.refresh_idx()
        else:
            self.idx = st.session_state['index']

    def refresh_idx(self):
        if self.empty:
            self.idx = None
        else:
            self.idx = 0
            st.session_state["index"] = 0

    def select_index(self, idx):
        self.idx = idx
        st.session_state["index"] = idx

    def refresh_chats(self):
        self.chats = fetch.get_chats()
        self.refresh_idx()

    """
    Properties
    """

    @property
    def selected_index(self):
        return self.idx

    @property
    def selected_chat(self):
        return self.chats[self.idx]

    @property
    def empty(self):
        return len(self.chats) == 0

    """
    Chat operations
    """

    def add_chat(self):
        fetch.add_chat()
        self.refresh_chats()

    def delete_selected_chat(self):
        chat = self.selected_chat
        fetch.delete_chat(chat=chat)
        self.refresh_chats()
