from pathlib import Path
import json

from .models import AuditConfig


def load_config(config_path: Path | None) -> AuditConfig:
    if config_path is None:
        return AuditConfig()

    if not config_path.exists():
        raise FileNotFoundError(
            f"Arquivo de configuração não encontrado: {config_path}"
        )

    data = json.loads(
        config_path.read_text(
            encoding="utf-8",
        )
    )

    return AuditConfig(
        required_documents=data.get(
            "required_documents",
            [],
        ),
        aliases=data.get(
            "aliases",
            {},
        ),
        ignore_orphan_documents=data.get(
            "ignore_orphan_documents",
            [],
        ),
    )