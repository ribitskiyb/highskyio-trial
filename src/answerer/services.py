import hashlib
from typing import cast

from fastapi import HTTPException
from pydantic import BaseModel
from redis.asyncio import StrictRedis
from starlette import status

from answerer.solver import solve


class SolverResponse(BaseModel):
    answer: str


async def get_answer(
    question: str,
    redis_client: StrictRedis,
) -> SolverResponse:
    cache_key = _generate_cache_key(question)

    # Check cache first
    cached_answer = cast(bytes, await redis_client.get(cache_key)).decode("utf-8")
    if cached_answer:
        return SolverResponse(answer=cached_answer)

    # Solve the problem
    result = solve(question)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The question is not recognized",
        )

    string_result = str(result)

    # Cache the result for 60 seconds
    await redis_client.setex(
        name=cache_key,
        time=60,
        value=string_result.encode("utf-8"),
    )

    return SolverResponse(answer=string_result)


def _generate_cache_key(question: str) -> str:
    return hashlib.md5(question.encode("utf-8")).hexdigest()
