import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from answerer import services


@asynccontextmanager
async def lifespan(_app: FastAPI):
    global cache_client
    cache_client = services.RedisQnaCache(
        host=os.environ["REDIS_HOST"],
        port=os.getenv("REDIS_PORT", 6379),
    )
    yield
    await cache_client.aclose()


app = FastAPI(title="Math Problem Solver", lifespan=lifespan)
cache_client: services.RedisQnaCache = None  # type: ignore


@app.get("/get_answer")
async def get_answer(question: str) -> services.SolverResponse:
    """
    Solve math questions about cylinder surface area or vector cross products.

    Examples:
    - Vector cross product: "What is the cross product of [1, 2, 3] and [4, 5, 6]?"
    - Cylinder surface area: "What is the surface area of a cylinder with radius 5 meters and height 10 meters?"
    """
    return await services.get_answer(question, cache_client)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8008)
