import sqlite3
from sqlite3 import Connection

import pandas as pd
import streamlit as st

def build_sqlite():
  conn = sqlite3.connect("test.db")
  conn.execute(
      """CREATE TABLE COMPANY
          (ID INT PRIMARY KEY     NOT NULL,
          NAME           TEXT    NOT NULL,
          AGE            INT     NOT NULL,
          ADDRESS        CHAR(50),
          SALARY         REAL);"""
  )
  conn.execute(
      "INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
        VALUES (1, 'Paul', 32, 'California', 20000.00 )"
  )
  conn.execute(
      "INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
        VALUES (2, 'Allen', 25, 'Texas', 15000.00 )"
  )
  conn.execute(
      "INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
        VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )"
  )
  conn.execute(
      "INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
        VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )"
  )
  conn.commit()
  print("Records created successfully")

  conn.close()

@st.cache(allow_output_mutation=True)
def get_connection(path):
    """Put the connection in cache to reuse if path does not change."""
    return sqlite3.connect(path)


@st.cache(hash_funcs={Connection: id})
def get_data(engine):
    """If the Connection.id is the same as before, use the cached dataframe"""
    sql = """
    SELECT * FROM COMPANY;
    """
    df = pd.read_sql(sql, con=engine)
    return df


engine = get_connection("test.db")