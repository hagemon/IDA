import conn
from chat import Chat, ChatContent


def get_chats():
    chats = conn.run_query()
    return chats


def add_chat():
    idx = conn.get_chat_index()
    title = f'Analysis {idx}'
    chat = Chat(
        title=title, url='')
    conn.add_chat(chat=chat)


def add_url(chat, url):
    conn.update_chat(chat, url)


def get_contents(chat):
    return conn.get_chat_content(chat=chat)


def add_content():
    pass


if __name__ == '__main__':
    print(get_chats())
