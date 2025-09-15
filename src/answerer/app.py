from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from redis.asyncio import StrictRedis

from answerer import services


@asynccontextmanager
async def lifespan(_app: FastAPI):
    global redis_client
    redis_client = StrictRedis(host="redis", port=6379, decode_responses=True)
    yield
    await redis_client.close()


app = FastAPI(title="Math Problem Solver", lifespan=lifespan)
redis_client: StrictRedis = None  # type: ignore


@app.get("/get_answer")
async def get_answer(question: str) -> services.SolverResponse:
    """
    Solve math questions about cylinder surface area or vector cross products.

    Examples:
    - Vector cross product: "What is the cross product of [1, 2, 3] and [4, 5, 6]?"
    - Cylinder surface area: "What is the surface area of a cylinder with radius 5 meters and height 10 meters?"
    """
    return await services.get_answer(question, redis_client)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8008)
