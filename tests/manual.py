import json
import re
from pathlib import Path
from typing import Iterator

import httpx

from answerer.solver import solve
import pytest

DATA_DIR = Path(__file__).parent


def get_question_answer_pairs() -> Iterator[
    tuple[
        int,
        str,
        str,
        int | list[int],
    ]
]:
    with open(DATA_DIR / "train.json") as f:
        data = json.load(f)

    for item_no, item in enumerate(data, start=1):
        question = item["question"]
        answer_str = item["answer"]
        topic = item["topic"]

        if answer_str.startswith("["):
            answer = json.loads(answer_str)
        elif match := re.match(r"^\d+", answer_str):
            answer = int(match.group())
        else:
            raise ValueError(f"Invalid answer format: {answer_str}")

        yield item_no, topic, question, answer


def get_question_answer_test_params() -> Iterator[pytest.param]:
    for item_no, topic, question, answer in get_question_answer_pairs():
        yield pytest.param(
            question,
            answer,
            id=f"{topic} #{item_no}",
        )


@pytest.mark.parametrize(
    "question, expected",
    get_question_answer_test_params(),
)
def test_question_asnwers(question, expected):
    resp = httpx.get("http://localhost:8008/get_answer", params={"question": question})
    assert resp.status_code == 200
    assert resp.json()["answer"] == str(expected)


if __name__ == "__main__":
    for q_no, _, question, expected in get_question_answer_pairs():
        actual = solve(question)
        if actual == expected:
            print(f"  #{q_no}")
        else:
            print(f'✗ #{q_no}    {actual} != {expected}    Q:"{question[:30]}"')
