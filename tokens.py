import redis
import os
import jwt
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv("../.env")

HOST = os.getenv('REDIS_HOST', "localhost")
PORT = os.getenv('REDIS_PORT')
PW = os.getenv('REDIS_PASSWORD')
SCRT = os.getenv('SECRET_JWT', "idk")

red = redis.Redis(host=HOST, port=PORT, password=PW, decode_responses=True)


def store_token(id: int, username: str) -> str:
    token = jwt.encode({"id": f"{id}", "username": username}, SCRT, algorithm="HS256")
    red.setex(f"jwt:{id}", timedelta(hours=1), token)
    return token


def check_token(token: str) -> str | None:
    try:
        data = jwt.decode(token, SCRT, algorithms=["HS256"])
        id = data.get("id", -1)
        value = red.get(f"jwt:{id}")
        if value == token and value is not None:
            return data
    except Exception as e:
        print(e)
    return None