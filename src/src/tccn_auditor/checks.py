from collections import defaultdict
from pathlib import Path

from .models import AuditConfig, AuditResult, Document
from .normalize import normalize_name


def build_document_index(
    documents: list[Document],
    aliases: dict[str, str],
) -> dict[str, Document]:
    index: dict[str, Document] = {}

    for document in documents:
        normalized_title = normalize_name(document.title)
        index[normalized_title] = document

    for alias, official_name in aliases.items():
        normalized_alias = normalize_name(alias)
        normalized_official = normalize_name(official_name)

        if normalized_official in index:
            index[normalized_alias] = index[normalized_official]

    return index


def find_duplicate_titles(
    documents: list[Document],
) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = defaultdict(list)

    for document in documents:
        normalized_title = normalize_name(document.title)
        grouped[normalized_title].append(str(document.path))

    return {
        normalized_title: paths
        for normalized_title, paths in grouped.items()
        if len(paths) > 1
    }


def find_broken_references(
    documents: list[Document],
    document_index: dict[str, Document],
) -> list[dict[str, str]]:
    broken_references: list[dict[str, str]] = []

    for document in documents:
        for reference in document.references:
            normalized_reference = normalize_name(reference)

            if normalized_reference not in document_index:
                broken_references.append(
                    {
                        "document": document.title,
                        "reference": reference,
                    }
                )

    return broken_references


def _matches_value(value: str | None, candidates: list[str]) -> bool:
    if not value:
        return False

    normalized_value = normalize_name(value)
    return normalized_value in {
        normalize_name(candidate)
        for candidate in candidates
    }


def _matches_path(path: Path, patterns: list[str]) -> bool:
    normalized_path = normalize_name(path.as_posix())

    return any(
        normalize_name(pattern) in normalized_path
        for pattern in patterns
    )


def _orphan_exemption_reason(
    document: Document,
    config: AuditConfig,
) -> str | None:
    if _matches_value(
        document.document_type,
        config.orphan_exempt_document_types,
    ):
        return f"tipo permitido: {document.document_type}"

    if _matches_value(
        document.category,
        config.orphan_exempt_categories,
    ):
        return f"categoria permitida: {document.category}"

    if _matches_path(
        document.path,
        config.orphan_exempt_paths,
    ):
        return f"pasta permitida: {document.path.parent.as_posix()}"

    return None


def find_orphan_documents(
    documents: list[Document],
    config: AuditConfig,
) -> tuple[list[str], list[dict[str, str]]]:
    referenced_titles: set[str] = set()
    ignored_titles = {
        normalize_name(title)
        for title in config.ignore_orphan_documents
    }

    for document in documents:
        for reference in document.references:
            referenced_titles.add(normalize_name(reference))

    orphan_documents: list[str] = []
    permitted_orphans: list[dict[str, str]] = []

    for document in documents:
        normalized_title = normalize_name(document.title)

        if normalized_title in ignored_titles:
            continue

        if normalized_title in referenced_titles:
            continue

        exemption_reason = _orphan_exemption_reason(
            document,
            config,
        )

        if exemption_reason:
            permitted_orphans.append(
                {
                    "document": document.title,
                    "reason": exemption_reason,
                }
            )
            continue

        orphan_documents.append(document.title)

    return orphan_documents, permitted_orphans


def find_missing_required_documents(
    document_index: dict[str, Document],
    required_documents: list[str],
) -> list[str]:
    return [
        title
        for title in required_documents
        if normalize_name(title) not in document_index
    ]


def _is_metadata_exempt(
    document: Document,
    config: AuditConfig,
) -> bool:
    return (
        _matches_value(
            document.document_type,
            config.metadata_exempt_document_types,
        )
        or _matches_value(
            document.category,
            config.metadata_exempt_categories,
        )
        or _matches_path(
            document.path,
            config.metadata_exempt_paths,
        )
    )


def find_metadata_warnings(
    documents: list[Document],
    config: AuditConfig,
) -> list[dict[str, str]]:
    warnings: list[dict[str, str]] = []

    required_fields = {
        "version": "Versão",
        "status": "Status",
        "category": "Categoria",
        "document_type": "Tipo de documento",
    }

    for document in documents:
        if _is_metadata_exempt(document, config):
            continue

        for attribute, label in required_fields.items():
            if not getattr(document, attribute):
                warnings.append(
                    {
                        "document": document.title,
                        "warning": f"Metadado ausente: {label}",
                    }
                )

    return warnings


def run_checks(
    documents: list[Document],
    untitled_files: list[str],
    config: AuditConfig,
) -> AuditResult:
    document_index = build_document_index(
        documents,
        config.aliases,
    )

    orphan_documents, permitted_orphans = find_orphan_documents(
        documents,
        config,
    )

    return AuditResult(
        documents=documents,
        untitled_files=untitled_files,
        duplicate_titles=find_duplicate_titles(documents),
        broken_references=find_broken_references(
            documents,
            document_index,
        ),
        orphan_documents=orphan_documents,
        permitted_orphan_documents=permitted_orphans,
        missing_required_documents=find_missing_required_documents(
            document_index,
            config.required_documents,
        ),
        metadata_warnings=find_metadata_warnings(
            documents,
            config,
        ),
    )
