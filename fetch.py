import conn
from chat import Chat, ChatContent


def get_chats():
    chats = conn.run_query()
    return chats


def add_chat():
    idx = conn.get_chat_index()
    title = f'Analysis {idx}'
    chat = Chat(
        title=title, url='https://people.sc.fsu.edu/~jburkardt/data/csv/homes.csv')
    conn.add_chat(chat=chat)


if __name__ == '__main__':
    add_chat()
    add_chat()
