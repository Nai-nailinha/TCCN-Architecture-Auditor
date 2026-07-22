import re
import unicodedata


GENERIC_SUFFIXES = (
    "do tccn ai studio",
    "tccn ai studio",
)


def strip_accents(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(ch for ch in normalized if not unicodedata.combining(ch))


def normalize_name(value: str) -> str:
    value = value.strip().strip(".")
    value = re.sub(r"\s+", " ", value)
    lowered = strip_accents(value).casefold()

    for suffix in GENERIC_SUFFIXES:
        normalized_suffix = strip_accents(suffix).casefold()
        if lowered.endswith(normalized_suffix):
            lowered = lowered[: -len(normalized_suffix)].strip(" -–—")

    lowered = re.sub(r"[^a-z0-9]+", " ", lowered)
    return re.sub(r"\s+", " ", lowered).strip()


def split_references(value: str) -> list[str]:
    if not value.strip():
        return []

    parts = re.split(r"\s*;\s*|\s*\|\s*", value)
    return [part.strip().strip(".") for part in parts if part.strip()]