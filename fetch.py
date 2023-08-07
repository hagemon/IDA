import conn
from chat import Chat, ChatContent

"""
Querys
"""


def get_chats():
    chats = conn.run_query()
    return chats


def get_contents(chat):
    return conn.get_chat_content(chat=chat)


"""
Creates
"""


def add_chat():
    idx = conn.get_chat_index()
    title = f"Analysis {idx}"
    chat = Chat(title=title, url="")
    conn.add_chat(chat=chat)


def add_url(chat, url):
    conn.update_chat(chat, url)


def add_content(chat, content, operation, gen=False):
    chat_content = ChatContent(chat=chat, content=content, operation=operation, is_general=gen)
    print(chat_content)
    conn.add_chat_content(chat_content)


if __name__ == "__main__":
    print(get_chats())
