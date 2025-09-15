import math
import re


def solve(question: str) -> int | list[int] | None:
    """Main solving method"""
    topic = _identify_topic(question)

    if topic == "vector_cross_product":
        vectors = _extract_vector_parameters(question)
        if vectors:
            v1, v2 = vectors
            result = _calculate_vector_cross_product(v1, v2)
            return result

    elif topic == "cylinder_surface_area":
        params = _extract_cylinder_parameters(question)
        if params:
            height, radius = params
            result = _calculate_cylinder_surface_area(height, radius)
            return result

    return None


def _identify_topic(question: str) -> str | None:
    """Determine which topic the question is about"""
    # Check for vector cross product first (higher priority)
    vector_pattern = r"-?\d+\s*,\s*-?\d+\s*,\s*-?\d+"
    if re.search(vector_pattern, question):
        return "vector_cross_product"

    # Check for cylinder surface area
    question_lower = question.lower()
    if "cylind" in question_lower and "surface area" in question_lower:
        return "cylinder_surface_area"

    return None


def _extract_vector_parameters(question: str) -> tuple[list[int], list[int]] | None:
    """Extract two vectors from the question"""
    vector_pattern = r"(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)"
    matches = re.findall(vector_pattern, question)

    if len(matches) >= 2:
        vector1 = [int(x) for x in matches[0]]
        vector2 = [int(x) for x in matches[1]]
        return vector1, vector2

    return None


def _extract_cylinder_parameters(question: str) -> tuple[float, float] | None:
    """Extract height and radius from cylinder question"""

    def convert_special_values(value: str, unit: str) -> float:
        if value.lower() == "single":
            return 1.0
        if unit.lower().startswith("stor"):
            return float(value) if value.isdigit() else 1.0
        return float(value)

    height = None
    radius = None

    # Height extraction patterns (case insensitive)
    height_patterns = [
        r"\bheight(?:[^.,\n\d]*?)(\d+|single)\s*(meter)s?\b",
        r"(\d+|single)\s*(meter)s?\s*(?:tall|in height|high)\b",
        r"(\d+|single)-(meter)s?\s(?:tall|high)\b",
        r"(\d+|single)(?:-|\s)(stor)(?:y|ies|eys?)\b",
    ]

    for pattern in height_patterns:
        match = re.search(pattern, question, re.IGNORECASE)
        if match:
            value, unit = match.groups()
            height = convert_special_values(value, unit)
            break

    # Radius extraction patterns (case insensitive)
    radius_patterns = [
        r"\bradius(?:[^.,\n\d]*?)(\d+|single)\s*(meter)s?\b",
        r"(\d+|single)-(meter)s?\sradius\b",
    ]

    for pattern in radius_patterns:
        match = re.search(pattern, question, re.IGNORECASE)
        if match:
            value, unit = match.groups()
            radius = convert_special_values(value, unit)
            break

    if height is not None and radius is not None:
        return height, radius

    return None


def _calculate_cylinder_surface_area(height: float, radius: float) -> int:
    """Calculate surface area of cylinder: 2πr² + 2πrh"""
    surface_area = 2 * math.pi * radius * radius + 2 * math.pi * radius * height
    return round(surface_area)


def _calculate_vector_cross_product(v1: list[int], v2: list[int]) -> list[int]:
    """Calculate cross product of two 3D vectors"""
    cross_product = [
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0],
    ]
    return cross_product
