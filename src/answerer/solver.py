import math
import re
from collections.abc import Sequence
from enum import Enum
from typing import Iterable

_VECTOR_PATTERN = re.compile(r"(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)")
_HEIGHT_PATTERNS = tuple(
    re.compile(pattern=p, flags=re.IGNORECASE)
    for p in [
        # language=pythonregexp
        r"\bheight[^.,\n\d]*?(\d+|single)\s*(meter)s?\b",
        # language=pythonregexp
        r"(\d+|single)\s*(meter)s?\s*(?:tall|in height|high)\b",
        # language=pythonregexp
        r"(\d+|single)-(meter)s?\s(?:tall|high)\b",
        # language=pythonregexp
        r"(\d+|single)(?:-|\s)(stor)(?:y|ies|eys?)\b",
    ]
)
_RADIUS_PATTERNS = tuple(
    re.compile(pattern=p, flags=re.IGNORECASE)
    for p in [
        # language=pythonregexp
        r"\bradius[^.,\n\d]*?(\d+|single)\s*(meter)s?\b",
        # language=pythonregexp
        r"(\d+|single)-(meter)s?\sradius\b",
    ]
)
_KNOWN_UNITS_TO_METERS = {
    "meter": 1.0,
    "stor": 1.0,  # "storey"
}
_KNOWN_SPECIAL_VALUES = {
    "single": 1.0,
}


class _Topic(str, Enum):
    VECTOR_CROSS_PRODUCT = "vector_cross_product"
    CYLINDER_SURFACE_AREA = "cylinder_surface_area"


def solve(question: str) -> int | list[int] | None:
    """Main solving method"""
    result = None
    match _identify_topic(question):
        case _Topic.VECTOR_CROSS_PRODUCT:
            if vectors := _extract_vector_parameters(question):
                result = _calculate_vector_cross_product(*vectors)

        case _Topic.CYLINDER_SURFACE_AREA:
            if params := _extract_cylinder_parameters(question):
                height, radius = params
                result = _calculate_cylinder_surface_area(height, radius)

    return result


def _identify_topic(question: str) -> _Topic | None:
    """Determine which topic the question is about"""
    if _VECTOR_PATTERN.search(question):
        return _Topic.VECTOR_CROSS_PRODUCT

    question_lower = question.lower()
    if "cylind" in question_lower and "surface area" in question_lower:
        return _Topic.CYLINDER_SURFACE_AREA

    return None


def _extract_vector_parameters(question: str) -> tuple[list[int], list[int]] | None:
    """Extract two vectors from the question"""

    def _deduplicate(values: Iterable[tuple[str, ...]]) -> list[tuple[str, ...]]:
        seen = set()
        dedup = []
        for value in values:
            if value not in seen:
                seen.add(value)
                dedup.append(value)
        return dedup

    matches = _VECTOR_PATTERN.findall(question)
    if len(matches) > 2:
        matches = _deduplicate(matches)

    try:
        vec1, vec2 = matches
    except ValueError:
        return None

    vector1 = list(map(int, vec1))
    vector2 = list(map(int, vec2))
    return vector1, vector2


def _extract_cylinder_parameters(question: str) -> tuple[float, float] | None:
    """Extract height and radius from cylinder question"""

    def convert_to_meters(value: str, unit: str) -> float:
        numeric_value = _KNOWN_SPECIAL_VALUES.get(value.lower()) or float(value)
        meters = _KNOWN_UNITS_TO_METERS[unit.lower()]
        return numeric_value * meters

    def extract_value(question: str, patterns: Sequence[re.Pattern]) -> str | None:
        for pattern in patterns:
            if not (match := pattern.search(question)):
                continue
            value, unit = match.groups()
            return convert_to_meters(value, unit)
        return None

    height = extract_value(question, _HEIGHT_PATTERNS)
    radius = extract_value(question, _RADIUS_PATTERNS)

    if height is not None and radius is not None:
        return height, radius

    return None


def _calculate_cylinder_surface_area(height: float, radius: float) -> int:
    """Calculate surface area of cylinder: 2πr² + 2πrh"""
    surface_area = 2 * math.pi * radius * (radius + height)
    # floor, а не round, т.к. это даёт большую долю совпадений с ответом из `train.json`
    return math.floor(surface_area)


def _calculate_vector_cross_product(v1: list[int], v2: list[int]) -> list[int]:
    """Calculate cross product of two 3D vectors"""
    cross_product = [
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0],
    ]
    return cross_product
