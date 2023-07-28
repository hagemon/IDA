import streamlit as st
import psycopg2

@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()
    
def run_executes(query):
    if type(query) != list:
        query = [query]
    with conn.cursor() as cur:
        for q in query:
            cur.execute(q)
