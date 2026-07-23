# Melhoria: regras semânticas de auditoria

Esta atualização evita tratar todo arquivo Markdown como se tivesse a mesma função arquitetural.

## Arquivos para substituir

- `src/tccn_auditor/models.py`
- `src/tccn_auditor/config.py`
- `src/tccn_auditor/checks.py`
- `src/tccn_auditor/report.py`
- `audit-config.json`

## O que muda

- Documentos não referenciados podem ser permitidos por tipo, categoria ou pasta.
- Documentos permitidos deixam de contar como aviso.
- Eles passam a aparecer numa seção informativa do relatório.
- Artefatos de produção podem ser dispensados dos metadados arquiteturais.
- As regras antigas continuam compatíveis.

## Depois de substituir

Execute o auditor normalmente e compare o novo relatório.

Sugestão de commit:

```bash
git add -A
git commit -m "feat: adiciona regras semânticas para órfãos e metadados"
git push origin main
```