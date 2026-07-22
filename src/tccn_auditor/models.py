from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class Document:
    path: Path
    title: str
    version: str | None = None
    status: str | None = None
    category: str | None = None
    document_type: str | None = None
    official_source: str | None = None
    superior_documents: list[str] = field(default_factory=list)
    related_documents: list[str] = field(default_factory=list)
    raw_text: str = ""

    @property
    def references(self) -> list[str]:
        return [*self.superior_documents, *self.related_documents]


@dataclass(slots=True)
class AuditConfig:
    required_documents: list[str] = field(default_factory=list)
    aliases: dict[str, str] = field(default_factory=dict)
    ignore_orphan_documents: list[str] = field(default_factory=list)


@dataclass(slots=True)
class AuditResult:
    documents: list[Document]
    untitled_files: list[str] = field(default_factory=list)
    duplicate_titles: dict[str, list[str]] = field(default_factory=dict)
    broken_references: list[dict[str, str]] = field(default_factory=list)
    orphan_documents: list[str] = field(default_factory=list)
    cycles: list[list[str]] = field(default_factory=list)
    missing_required_documents: list[str] = field(default_factory=list)
    metadata_warnings: list[dict[str, Any]] = field(default_factory=list)

    @property
    def error_count(self) -> int:
        return (
            len(self.untitled_files)
            + len(self.duplicate_titles)
            + len(self.broken_references)
            + len(self.cycles)
            + len(self.missing_required_documents)
        )

    @property
    def warning_count(self) -> int:
        return len(self.orphan_documents) + len(self.metadata_warnings)