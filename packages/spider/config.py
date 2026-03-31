import libsql
import redis
import os


def init_db():
    url = os.getenv("TURSO_DATABASE_URL")
    auth_token = os.getenv("TURSO_AUTH_TOKEN")

    if not url or not auth_token:
        raise Exception("Missing TURSO_DATABASE_URL or TURSO_AUTH_TOKEN")

    conn = libsql.connect("hello.db", sync_url=url, auth_token=auth_token)
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER);")

    return conn


def init_redis():
    redis_url = os.getenv("REDIS_URL")

    if not redis_url:
        raise Exception("Missing REDIS_URL")

    return redis.Redis.from_url(redis_url)
