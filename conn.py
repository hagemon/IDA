import streamlit as st
from sqlalchemy import create_engine, func, Integer, cast
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from chat import Chat, ChatContent


@st.cache_resource
def init_connection():
    info = st.secrets["postgres"]
    url = f"postgresql://{info['user']}:{info['password']}@{info['host']}:{info['port']}/{info['dbname']}"
    engine = create_engine(url)
    return engine


engine = init_connection()
Base = declarative_base()  # inherit from this class to create ORM models
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


@st.cache_data(ttl=600)
def run_query():
    return session.query(Chat).order_by(Chat.create_datetime.desc()).all()


# @st.cache_data(ttl=600)
def add_chat(chat):
    session.add(chat)
    session.commit()


# @st.cache_data(ttl=600)
def get_chat_index():
    title = session.query(func.max(Chat.title)).filter(Chat.title.op('~')('^Analysis [1-9]*$')).scalar()
    max_x = int(title.split(' ')[-1])
    return max_x+1