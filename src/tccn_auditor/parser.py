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
        r"^\s*Fonte\s+oficial(?:\s+de)?\s*:\s*(.+?)\s*$",
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


DOCUMENT_NAME_PATTERN = re.compile(
    r"^\s*(?:Documento|Nome\s+do\s+documento)\s*:\s*(.+?)\s*$",
    re.I,
)


GENERIC_TITLES = {
    "documento",
    "document",
    "nome do documento",
}


def normalize_markdown_line(line: str) -> str:
    """
    Remove formatação Markdown simples usada nos metadados.

    Exemplos:
        **Versão:** 0.1 -> Versão: 0.1
        __Status:__ Oficial -> Status: Oficial
    """
    normalized = line.strip()
    normalized = normalized.replace("**", "")
    normalized = normalized.replace("__", "")
    return normalized.strip()


def clean_value(value: str) -> str:
    """
    Remove formatação Markdown residual de um valor de metadado.
    """
    return value.strip().strip("*_").strip()


def detect_title(lines: list[str]) -> str:
    """
    Detecta o título real do documento.

    Ordem de prioridade:

    1. Campo explícito 'Documento: Nome';
    2. Primeiro heading Markdown que não seja genérico;
    3. Primeira linha válida que não seja metadado ou separador.
    """

    # 1. Prioriza o campo explícito de nome do documento.
    for line in lines[:80]:
        normalized = normalize_markdown_line(line)
        match = DOCUMENT_NAME_PATTERN.match(normalized)

        if not match:
            continue

        title = clean_value(match.group(1))

        if title and title.casefold() not in GENERIC_TITLES:
            return title

    # 2. Procura o primeiro heading Markdown não genérico.
    for line in lines:
        stripped = line.strip()

        if not stripped.startswith("#"):
            continue

        title = stripped.lstrip("#").strip()
        title = clean_value(title)

        if not title:
            continue

        if title.casefold() in GENERIC_TITLES:
            continue

        return title

    # 3. Usa a primeira linha válida como alternativa.
    for line in lines:
        normalized = normalize_markdown_line(line)

        if not normalized:
            continue

        if normalized in {"---", "***", "___"}:
            continue

        if normalized.casefold() in GENERIC_TITLES:
            continue

        if DOCUMENT_NAME_PATTERN.match(normalized):
            continue

        if any(
            pattern.match(normalized)
            for pattern in FIELD_PATTERNS.values()
        ):
            continue

        return clean_value(normalized)

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

    metadata_lines = lines[:80]
    index = 0

    while index < len(metadata_lines):
        normalized = normalize_markdown_line(metadata_lines[index])

        matched_field = None
        matched_value = None

        for field_name, pattern in FIELD_PATTERNS.items():
            match = pattern.match(normalized)

            if match:
                matched_field = field_name
                matched_value = clean_value(match.group(1))
                break

        if matched_field:
            if matched_field in {
                "superior_documents",
                "related_documents",
            }:
                data[matched_field] = split_references(matched_value)
            else:
                data[matched_field] = matched_value

            index += 1
            continue

        # Detecta campos de referência sem conteúdo na mesma linha:
        # "Documentos relacionados:"
        multiline_match = re.match(
            r"^\s*(Documentos\s+superiores|Documentos\s+relacionados)"
            r"\s*:\s*$",
            normalized,
            re.I,
        )

        if multiline_match:
            label = multiline_match.group(1).casefold()

            field_name = (
                "superior_documents"
                if "superiores" in label
                else "related_documents"
            )

            references: list[str] = []
            next_index = index + 1

            while next_index < len(metadata_lines):
                next_line = metadata_lines[next_index]
                next_normalized = normalize_markdown_line(next_line)

                # Ignora linhas vazias imediatamente após o cabeçalho.
                if not next_normalized:
                    next_index += 1
                    continue

                # Captura itens de lista Markdown.
                list_match = re.match(
                    r"^\s*[-*+]\s+(.+?)\s*$",
                    next_line,
                )

                if not list_match:
                    break

                reference = clean_value(list_match.group(1))

                if reference:
                    references.extend(split_references(reference))

                next_index += 1

            data[field_name] = references
            index = next_index
            continue

        index += 1

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

    ignored_filenames = {
        "readme.md",
    }

    ignored_folders = {
        "templates",
    }

    documents: list[Document] = []
    untitled_files: list[str] = []

    for path in sorted(folder.rglob("*")):
        if not path.is_file():
            continue

        if path.suffix.lower() not in extensions:
            continue

        # READMEs descrevem pastas ou o projeto, não são documentos
        # arquiteturais auditáveis.
        if path.name.casefold() in ignored_filenames:
            continue

        # Templates são modelos de criação, não documentos oficiais.
        relative_parts = path.relative_to(folder).parts

        if any(
            part.casefold() in ignored_folders
            for part in relative_parts[:-1]
        ):
            continue

        document = parse_document(path)

        if document.title:
            documents.append(document)
        else:
            untitled_files.append(str(path))

    return documents, untitled_files