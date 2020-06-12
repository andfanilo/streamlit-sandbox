import sqlite3

import pandas as pd
import sqlalchemy
import streamlit as st
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.properties import ColumnProperty
from sqlalchemy.orm.query import Query


Base = declarative_base()


class Company(Base):
    __tablename__ = "company"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)


@st.cache(allow_output_mutation=True)
def get_session(path: str):
    e = create_engine(f"sqlite:///{path}")
    Session = sessionmaker(bind=e)
    session = Session()
    return session


def create_test_db(session: Session):
    """Should create test.db file with "company" table
    Maybe should delete test.db if rerunning the script
    """
    Base.metadata.create_all(session.bind)
    session.add(Company(name="Streamlit", age=42))
    session.add(Company(name="is", age=24))
    session.add(Company(name="awesome", age=3))
    session.commit()


def check_sqlite_table(path: str):
    """Use sqlite3 library to read test.db content. 
    Just to check table creation went well.
    """
    e = sqlite3.connect(path)
    sql = """
    SELECT * FROM company;
    """
    df = pd.read_sql(sql, con=e)
    st.dataframe(df)


def serialize_orm_query(q: Query):
    """Build SQL statement with inlined parameters
    https://stackoverflow.com/questions/5631078/sqlalchemy-print-the-actual-query
    """
    return q.statement.compile(compile_kwargs={"literal_binds": True}).string


@st.cache(
    hash_funcs={
        Session: id,
        Query: serialize_orm_query,  # if we get a query, stringify it with inbound params
        StrSQLCompiler: lambda _: None,  # we don't really care about the compiler
    },
    suppress_st_warning=True,
)
def run_orm_query(q: Query, session: Session):
    st.warning("CACHE MISS")
    return pd.read_sql(q.statement, session.bind)


session: Session = get_session("test.db")
if st.button("Create test table"):
    create_test_db(session)
if st.checkbox("Show sqlite test table using raw sqlite3"):
    check_sqlite_table("test.db")
if st.checkbox("Show sqlite test table using ORM query"):
    param = st.text_input("Input name of company to look for :")
    q: Query = session.query(Company.age).filter(Company.name == param)
    st.write(serialize_orm_query(q))
    df = run_orm_query(q, session)
    st.dataframe(df)
