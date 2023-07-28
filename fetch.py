import conn


def get_chats():
    conn.run_executes(['''
        create table if not exists chats (
            id uuid PRIMARY KEY,
            title varchar(255) NOT NULL,
        );
        ''','''
        create table if not exists chat_contents (
        
        )
    '''])
    chats = conn.run_query('select * from chats')
    return chats


def get_content(chat_id):
    content = conn.run_query(f'select * from chat_content where id = {chat_id}')
    return content


if __name__ == '__main__':
    print(get_chats())
