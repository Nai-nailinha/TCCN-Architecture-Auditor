# 📄 Resolução de Universo v0.1

## Objetivo

O módulo de Resolução de Universo é responsável por localizar, validar e disponibilizar todas as informações necessárias sobre o universo informado no Briefing de Produção.

Seu objetivo é evitar que especialistas precisem conhecer previamente cada universo ou consultar documentos manualmente.

A Resolução de Universo atua como uma camada intermediária entre o Briefing de Produção e os Especialistas.

---

# Responsabilidades

O módulo deve:

- Identificar o universo solicitado.
- Verificar se o universo existe.
- Localizar toda a documentação oficial relacionada.
- Consolidar essas informações em um único contexto.
- Disponibilizar esse contexto para os especialistas.

---

# Fluxo

Demanda
↓
Briefing de Produção
↓
Resolução de Universo
↓
Contexto Consolidado
↓
Especialista

---

# Entrada

O módulo recebe, no mínimo:

- Universo

Opcionalmente:

- Versão
- Idioma
- Configurações específicas

---

# Processo

Ao receber um universo válido, o sistema deve localizar automaticamente toda a documentação oficial relacionada.

Exemplo:

Universo:
TCCN

↓

Documentos encontrados:

- Manifesto (quando aplicável)
- Bíblia do Universo
- Personagens
- Direção de Arte
- Identidade Estratégica
- Biblioteca de Conhecimento
- Glossário
- Regras Narrativas
- Diretrizes Visuais
- Outros documentos oficiais existentes

---

# Contexto Consolidado

Após localizar os documentos, o módulo produz um único contexto lógico contendo todas as informações necessárias para a produção.

Os especialistas não devem consultar documentos individualmente.

Eles trabalham exclusivamente sobre o Contexto Consolidado.

---

# Responsabilidades dos Especialistas

Os especialistas não precisam conhecer universos específicos.

Eles devem assumir que:

- o universo já foi resolvido;
- toda a documentação relevante já foi consolidada;
- o contexto recebido é a única fonte de verdade durante a execução.

---

# Observações

A Resolução de Universo não produz conteúdo.

Seu papel é apenas preparar o ambiente de trabalho dos especialistas.

Esse módulo pertence ao Núcleo Operacional do TCCN AI Studio.