import hashlib

from fastapi import HTTPException
from pydantic import BaseModel
from redis.asyncio import StrictRedis
from starlette import status

from answerer.solver import solve


class RedisQnaCache:
    """Redis-based question answer cache"""

    def __init__(self, host: str, port: int = 6379):
        self._redis_client = StrictRedis(host=host, port=port)

    async def get(self, question: str) -> str | None:
        key = self._generate_cache_key(question)
        answer_bytes = await self._redis_client.get(key)
        if answer_bytes:
            return answer_bytes.decode("utf-8")
        return None

    async def set(self, question: str, answer: str, expiration_sec: int = 86_400) -> None:
        key = self._generate_cache_key(question)
        value = answer.encode("utf-8")
        await self._redis_client.setex(name=key, value=value, time=expiration_sec)

    async def aclose(self):
        await self._redis_client.aclose()

    @staticmethod
    def _generate_cache_key(question: str) -> bytes:
        return hashlib.md5(question.encode("utf-8")).digest()


class SolverResponse(BaseModel):
    answer: str


async def get_answer(
    question: str,
    cache: RedisQnaCache,
) -> SolverResponse:
    # Check cache first
    cached_answer = await cache.get(question)
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
    await cache.set(question=question, answer=string_result, expiration_sec=60)

    return SolverResponse(answer=string_result)
