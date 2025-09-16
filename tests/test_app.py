import pytest


@pytest.mark.asyncio
async def test_uses_qna_cache(
    async_client,
    cache_client,
    _clear_cache,
):
    question = "What is the cross product of [1, 2, 3] and [4, 5, 6]?"

    resp = await async_client.get("/get_answer", params={"question": question})
    assert resp.status_code == 200
    answer = resp.json()["answer"]

    resp = await async_client.get("/get_answer", params={"question": question})
    assert resp.status_code == 200
    assert resp.json()["answer"] == answer

    assert cache_client.method_calls == [
        ("get", question),
        ("set", (question, answer, 60)),
        ("get", question),
    ]
