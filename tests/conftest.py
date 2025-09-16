from typing import Any

import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from answerer.services import RedisQnaCache


class CacheWrapper:
    method_calls: list[tuple[str, Any]]

    def __init__(self, wrapped_cache: RedisQnaCache):
        self.method_calls = []
        self._wrapped_cache = wrapped_cache

    async def get(self, question: str) -> str | None:
        self.method_calls.append(("get", question))
        return await self._wrapped_cache.get(question)

    async def set(self, question: str, answer: str, expiration_sec: int = 86_400) -> None:
        self.method_calls.append(("set", (question, answer, expiration_sec)))
        return await self._wrapped_cache.set(question, answer, expiration_sec)

    async def aclose(self):
        return await self._wrapped_cache.aclose()


@pytest_asyncio.fixture
def app_module():
    import answerer.app

    return answerer.app


@pytest_asyncio.fixture
async def async_client(app_module):
    transport = ASGITransport(app=app_module.app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        yield client


@pytest_asyncio.fixture
async def __cache_wrapper():
    cache_wrapper = CacheWrapper(
        RedisQnaCache(
            host="localhost",
            port=6379,
        )
    )
    yield cache_wrapper
    await cache_wrapper.aclose()


@pytest_asyncio.fixture
async def cache_client(__cache_wrapper, app_module, monkeypatch):
    monkeypatch.setattr(app_module, "cache_client", __cache_wrapper)
    return __cache_wrapper


@pytest_asyncio.fixture
def _clear_cache(cache_client):
    cache_client._wrapped_cache._redis_client.flushdb()
    cache_client.method_calls.clear()
