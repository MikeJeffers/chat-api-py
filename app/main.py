from fastapi import FastAPI, HTTPException
from .db import db
from .tokens import store_token
import bcrypt
from pydantic import BaseModel


class UserRequestBody(BaseModel):
    username: str
    password: str


app = FastAPI()
psql = db()


def hash_pass(password: str) -> str:
    salt = bcrypt.gensalt(10)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def check_pass(test_pass: str, hashed_pass: str) -> bool:
    return bcrypt.checkpw(test_pass.encode("utf-8"), hashed_pass.encode("utf-8"))


@app.post("/register")
def register(body: UserRequestBody):
    hashed = hash_pass(body.password)
    with psql.cursor() as cur:
        try:
            cur.execute("INSERT INTO Users (username, password) VALUES (%s, %s) RETURNING id, username",
                        (body.username, hashed))
            id, username = cur.fetchone()
            psql.commit()
            token = store_token(id, username)
            return {"token": token, "user": {"username": username, "id": id}}
        except Exception as e:
            psql.rollback()
            raise HTTPException(500, e.args)


@app.post("/login")
def login(body: UserRequestBody):
    with psql.cursor() as cur:
        try:
            cur.execute("SELECT id, username, password FROM Users WHERE username=%s LIMIT 1",
                        (body.username,))
            data = cur.fetchone()
            if not data:
                raise HTTPException("400", "Wrong username or password")
            id, username, hashed_password = data
            if not check_pass(body.password, hashed_password):
                raise HTTPException("400", "Wrong username or password")
            token = store_token(id, username)
            return {"token": token, "user": {"username": username, "id": id}}
        except Exception as e:
            raise HTTPException(500, e.args)
