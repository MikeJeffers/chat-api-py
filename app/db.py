import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('POSTGRES_HOST', "localhost")
DB_NAME = os.getenv('POSTGRES_DB', "test")
DB_USER = os.getenv('POSTGRES_USER', "user")
DB_PASS = os.getenv('POSTGRES_PASSWORD', "password")


def db():
    return psycopg2.connect(dbname=DB_NAME, password=DB_PASS, user=DB_USER, host=DB_HOST)
