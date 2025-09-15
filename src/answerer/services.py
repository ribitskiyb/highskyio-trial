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
    # Check cache first
    cached_answer = await redis_client.get(question)
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
    await redis_client.setex(question, 60, string_result)

    return SolverResponse(answer=string_result)
