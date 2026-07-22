from collections import defaultdict

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


def find_orphan_documents(
    documents: list[Document],
    ignored_documents: list[str],
) -> list[str]:
    referenced_titles: set[str] = set()
    ignored_titles = {
        normalize_name(title)
        for title in ignored_documents
    }

    for document in documents:
        for reference in document.references:
            referenced_titles.add(normalize_name(reference))

    orphan_documents: list[str] = []

    for document in documents:
        normalized_title = normalize_name(document.title)

        if normalized_title in ignored_titles:
            continue

        if normalized_title not in referenced_titles:
            orphan_documents.append(document.title)

    return orphan_documents


def find_missing_required_documents(
    document_index: dict[str, Document],
    required_documents: list[str],
) -> list[str]:
    return [
        title
        for title in required_documents
        if normalize_name(title) not in document_index
    ]


def find_metadata_warnings(
    documents: list[Document],
) -> list[dict[str, str]]:
    warnings: list[dict[str, str]] = []

    required_fields = {
        "version": "Versão",
        "status": "Status",
        "category": "Categoria",
        "document_type": "Tipo de documento",
    }

    for document in documents:
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

    return AuditResult(
        documents=documents,
        untitled_files=untitled_files,
        duplicate_titles=find_duplicate_titles(documents),
        broken_references=find_broken_references(
            documents,
            document_index,
        ),
        orphan_documents=find_orphan_documents(
            documents,
            config.ignore_orphan_documents,
        ),
        missing_required_documents=find_missing_required_documents(
            document_index,
            config.required_documents,
        ),
        metadata_warnings=find_metadata_warnings(documents),
    )