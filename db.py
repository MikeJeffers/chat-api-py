import psycopg2
import os
from dotenv import load_dotenv

load_dotenv("../.env")

DB_NAME = os.getenv('POSTGRES_DB')
DB_USER = os.getenv('POSTGRES_USER')
DB_PASS = os.getenv('POSTGRES_PASSWORD')


def db():
    return psycopg2.connect(dbname=DB_NAME, password=DB_PASS, user=DB_USER, host="localhost")
