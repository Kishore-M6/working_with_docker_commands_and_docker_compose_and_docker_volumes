import os

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from redis.asyncio import Redis
from redis.exceptions import RedisError

# Reading environment variables
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
COUNTER_KEY = os.getenv("COUNTER_KEY", "hello-user:endpoint-hits")


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = Redis.from_url(REDIS_URL, decode_responses=True)
    try:
        # await app.state.redis.ping()  # redis.exceptions.ConnectionError: Error Multiple exceptions: [Errno 111] Connect call failed ('::1', 6379, 0, 0), [Errno 111] Connect call failed ('127.0.0.1', 6379) connecting to localhost:6379.
        yield
    finally:
        await app.state.redis.aclose()


app = FastAPI(title="Hello User Counter", lifespan=lifespan)


@app.get("/")
async def hello_user(request: Request) -> dict[str, str | int]:
    try:
        count = await request.app.state.redis.incr(COUNTER_KEY)
    except RedisError as error:
        raise HTTPException(
            status_code=503,
            detail="Redis is unavailable",
        ) from error

    return {
        "message": f"hello dockers, you accessed this endpoint {count} many times",
        "count": count,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("hello_user_counter_app:app", host="0.0.0.0", port=8000)
