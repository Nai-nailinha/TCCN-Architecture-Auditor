from pathlib import Path

from .models import AuditResult


def _section(title: str) -> list[str]:
    return [
        "",
        f"## {title}",
        "",
    ]


def generate_markdown_report(result: AuditResult) -> str:
    lines: list[str] = [
        "# Relatório de Auditoria do TCCN AI Studio",
        "",
        "## Resumo",
        "",
        f"- Documentos encontrados: {len(result.documents)}",
        f"- Erros encontrados: {result.error_count}",
        f"- Avisos encontrados: {result.warning_count}",
    ]

    lines.extend(_section("Arquivos sem título"))

    if result.untitled_files:
        for path in result.untitled_files:
            lines.append(f"- `{path}`")
    else:
        lines.append("Nenhum arquivo sem título encontrado.")

    lines.extend(_section("Títulos duplicados"))

    if result.duplicate_titles:
        for normalized_title, paths in result.duplicate_titles.items():
            lines.append(f"### {normalized_title}")
            lines.append("")

            for path in paths:
                lines.append(f"- `{path}`")
    else:
        lines.append("Nenhum título duplicado encontrado.")

    lines.extend(_section("Referências quebradas"))

    if result.broken_references:
        for item in result.broken_references:
            lines.append(
                f"- **{item['document']}** referencia "
                f"`{item['reference']}`, que não foi encontrado."
            )
    else:
        lines.append("Nenhuma referência quebrada encontrada.")

    lines.extend(_section("Documentos órfãos"))

    if result.orphan_documents:
        for title in result.orphan_documents:
            lines.append(f"- {title}")
    else:
        lines.append("Nenhum documento órfão encontrado.")

    lines.extend(_section("Dependências circulares"))

    if result.cycles:
        for cycle in result.cycles:
            lines.append(f"- {' → '.join(cycle)}")
    else:
        lines.append("Nenhuma dependência circular encontrada.")

    lines.extend(_section("Documentos obrigatórios ausentes"))

    if result.missing_required_documents:
        for title in result.missing_required_documents:
            lines.append(f"- {title}")
    else:
        lines.append("Nenhum documento obrigatório ausente.")

    lines.extend(_section("Avisos de metadados"))

    if result.metadata_warnings:
        for item in result.metadata_warnings:
            lines.append(
                f"- **{item['document']}**: {item['warning']}"
            )
    else:
        lines.append("Nenhum aviso de metadados encontrado.")

    return "\n".join(lines).strip() + "\n"


def save_markdown_report(
    result: AuditResult,
    output_path: Path,
) -> None:
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    report = generate_markdown_report(result)

    output_path.write_text(
        report,
        encoding="utf-8",
    )