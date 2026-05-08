import logging

logger = logging.getLogger(__name__)


def generate_defined_patterns(text: str) -> list[str]:
    return [part.strip() for part in text.split(",")]


def filter_patterns(text: list[str], patterns: list[str]) -> str:
    p = [line for line in text if any(pattern in line for pattern in patterns)]
    return "".join(p)
