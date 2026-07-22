from pathlib import Path
import re

from .models import Document
from .normalize import split_references


FIELD_PATTERNS = {
    "version": re.compile(r"^\s*Vers[aã]o\s*:\s*(.+?)\s*$", re.I),
    "status": re.compile(r"^\s*Status\s*:\s*(.+?)\s*$", re.I),
    "category": re.compile(r"^\s*Categoria\s*:\s*(.+?)\s*$", re.I),
    "document_type": re.compile(
        r"^\s*Tipo\s+de\s+documento\s*:\s*(.+?)\s*$",
        re.I,
    ),
    "official_source": re.compile(
        r"^\s*Fonte\s+oficial\s+de\s*:\s*(.+?)\s*$",
        re.I,
    ),
    "superior_documents": re.compile(
        r"^\s*Documentos\s+superiores\s*:\s*(.+?)\s*$",
        re.I,
    ),
    "related_documents": re.compile(
        r"^\s*Documentos\s+relacionados\s*:\s*(.+?)\s*$",
        re.I,
    ),
}


def detect_title(lines: list[str]) -> str:
    for line in lines:
        stripped = line.strip()

        if not stripped:
            continue

        if stripped.startswith("#"):
            title = stripped.lstrip("#").strip()
            if title:
                return title

        if any(pattern.match(stripped) for pattern in FIELD_PATTERNS.values()):
            continue

        if stripped in {"---", "***", "___"}:
            continue

        return stripped

    return ""


def parse_document(path: Path) -> Document:
    text = path.read_text(
        encoding="utf-8-sig",
        errors="replace",
    )

    lines = text.splitlines()
    title = detect_title(lines)

    data: dict[str, object] = {
        "version": None,
        "status": None,
        "category": None,
        "document_type": None,
        "official_source": None,
        "superior_documents": [],
        "related_documents": [],
    }

    for line in lines[:80]:
        for field_name, pattern in FIELD_PATTERNS.items():
            match = pattern.match(line)

            if not match:
                continue

            value = match.group(1).strip()

            if field_name in {
                "superior_documents",
                "related_documents",
            }:
                data[field_name] = split_references(value)
            else:
                data[field_name] = value

            break

    return Document(
        path=path,
        title=title,
        raw_text=text,
        **data,
    )


def discover_documents(
    folder: Path,
    include_txt: bool = False,
) -> tuple[list[Document], list[str]]:
    extensions = {".md"}

    if include_txt:
        extensions.add(".txt")

    documents: list[Document] = []
    untitled_files: list[str] = []

    for path in sorted(folder.rglob("*")):
        if not path.is_file():
            continue

        if path.suffix.lower() not in extensions:
            continue

        document = parse_document(path)

        if document.title:
            documents.append(document)
        else:
            untitled_files.append(str(path))

    return documents, untitled_files