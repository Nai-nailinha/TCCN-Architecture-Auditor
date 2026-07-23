from pathlib import Path
import argparse
import sys

from .checks import run_checks
from .config import load_config
from .parser import discover_documents
from .report import save_markdown_report


DEFAULT_CONFIG_PATH = Path("audit-config.json")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Auditor da arquitetura documental do TCCN AI Studio."
    )

    parser.add_argument(
        "documents_folder",
        type=Path,
        help="Pasta que contém os documentos Markdown.",
    )

    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help=(
            "Arquivo JSON de configuração. "
            "Quando omitido, usa audit-config.json da pasta atual, se existir."
        ),
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("audit-report.md"),
        help="Caminho do relatório gerado.",
    )

    parser.add_argument(
        "--include-txt",
        action="store_true",
        help="Inclui arquivos .txt na auditoria.",
    )

    return parser


def resolve_config_path(config_path: Path | None) -> Path | None:
    """
    Usa o arquivo informado por --config.

    Quando o argumento não é fornecido, procura audit-config.json
    na pasta atual. Se ele não existir, mantém a configuração padrão.
    """
    if config_path is not None:
        return config_path

    if DEFAULT_CONFIG_PATH.exists():
        return DEFAULT_CONFIG_PATH

    return None


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.documents_folder.exists():
        print(
            f"Pasta não encontrada: {args.documents_folder}",
            file=sys.stderr,
        )
        return 1

    if not args.documents_folder.is_dir():
        print(
            f"O caminho não é uma pasta: {args.documents_folder}",
            file=sys.stderr,
        )
        return 1

    try:
        config_path = resolve_config_path(args.config)
        config = load_config(config_path)

        documents, untitled_files = discover_documents(
            args.documents_folder,
            include_txt=args.include_txt,
        )

        result = run_checks(
            documents,
            untitled_files,
            config,
        )

        save_markdown_report(
            result,
            args.output,
        )

    except (FileNotFoundError, ValueError, OSError) as error:
        print(
            f"Erro: {error}",
            file=sys.stderr,
        )
        return 1

    print("Auditoria concluída.")
    print(f"Documentos encontrados: {len(result.documents)}")
    print(f"Erros: {result.error_count}")
    print(f"Avisos: {result.warning_count}")
    print(f"Informações: {result.information_count}")

    if config_path is not None:
        print(f"Configuração usada: {config_path}")
    else:
        print("Configuração usada: padrão interno")

    print(f"Relatório salvo em: {args.output}")

    return 0 if result.error_count == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
