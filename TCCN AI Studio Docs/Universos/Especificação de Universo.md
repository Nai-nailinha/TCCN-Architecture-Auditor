# 📄 Especificação de Universo v0.1

## Objetivo

A Especificação de Universo define o modelo padrão utilizado pelo TCCN AI Studio para representar qualquer universo narrativo.

Seu objetivo é garantir que todos os especialistas recebam informações organizadas e consistentes, independentemente da origem ou da complexidade do universo.

---

# Princípios

1. Todo conteúdo é produzido dentro de um universo.
2. Um universo pode ser permanente ou temporário.
3. Os especialistas não conhecem universos específicos.
4. Os especialistas trabalham apenas com o contexto consolidado fornecido pela Resolução de Universo.
5. Todos os universos devem seguir esta especificação.

---

# Tipos de Universo

## Universo Documentado

Possui documentação oficial armazenada no AI Studio.

Exemplos:

- TCCN
- Universo XPTO
- Universo Medieval

Ao ser selecionado, a Resolução de Universo localiza automaticamente toda sua documentação oficial.

---

## Universo Descrito

Não possui documentação oficial.

O universo é definido diretamente pelo usuário através de uma descrição.

Exemplo:

> Existe uma civilização de homens verdes em Marte que está há 500 anos preparando uma invasão da Terra. Eles utilizam plantas inteligentes como computadores e vivem em cidades subterrâneas.

Nesse caso, a descrição fornecida pelo usuário torna-se a base para construção do contexto do universo durante a produção.

---

# Estrutura Recomendada de um Universo Documentado

Cada universo pode possuir, entre outros, os seguintes documentos:

- Bíblia do Universo
- Personagens
- Direção de Arte
- Identidade Estratégica
- Glossário
- Regras Narrativas
- Biblioteca de Conhecimento
- Outros documentos específicos

Nem todos os universos precisam possuir todos os documentos.

A Resolução de Universo deve utilizar apenas aqueles que existirem.

---

# Resolução de Universo

Quando um universo é informado no Briefing de Produção, o sistema identifica seu tipo.

## Universo Documentado

```text
Briefing
      ↓
Universo: TCCN
      ↓
Localiza documentação oficial
      ↓
Monta Contexto Consolidado
      ↓
Especialista
```

## Universo Descrito

```text
Briefing
      ↓
Descrição do Universo
      ↓
Constrói Contexto Temporário
      ↓
Especialista
```

---

# Contexto Consolidado

Independentemente da origem do universo, o resultado da Resolução de Universo deve ser um único contexto de trabalho contendo todas as informações relevantes para os especialistas.

Os especialistas não devem consultar documentos individualmente.

Eles trabalham exclusivamente sobre o Contexto Consolidado.

---

# Observações

A Especificação de Universo define apenas como um universo é representado dentro do AI Studio.

Ela não descreve nenhum universo específico.

Os universos concretos são implementações desta especificação e devem ser armazenados na pasta **Universos**.