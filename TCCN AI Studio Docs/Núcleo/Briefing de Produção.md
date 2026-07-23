# 📄 Briefing de Produção v0.1

## Objetivo

O Briefing de Produção é o documento responsável por transformar uma solicitação do usuário em uma configuração estruturada de produção.

Ele representa a entrada padronizada do TCCN AI Studio e fornece aos especialistas todas as informações necessárias para produzir conteúdos consistentes, independentemente do formato, plataforma, universo ou ferramenta utilizada.

O briefing não descreve o conteúdo em si. Seu papel é definir o contexto da produção.

---

# Responsabilidades

O Briefing de Produção deve:

- Padronizar a entrada das demandas.
- Reduzir ambiguidades durante a produção.
- Permitir reutilização entre diferentes especialistas.
- Centralizar decisões que afetam toda a produção.
- Evitar que cada especialista precise interpretar novamente a intenção do usuário.

---

# Princípios

1. O briefing descreve a produção, não o conteúdo.
2. Deve ser reutilizável por qualquer especialista.
3. Deve ser independente do universo utilizado.
4. Sempre que possível, utilizar valores padronizados.
5. Campos ausentes podem ser inferidos ou solicitados ao usuário quando necessários.

---

# Estrutura

## Universo

Define em qual universo a produção ocorrerá.

**Exemplos:**

- TCCN
- Original
- Genérico
- Outro

---

## Plataforma

Define onde o conteúdo será publicado.

**Exemplos:**

- YouTube
- Instagram
- TikTok
- Kwai
- Facebook
- LinkedIn
- Blog
- Site

---

## Formato

Define o tipo de conteúdo solicitado.

**Exemplos:**

- Vídeo
- Carrossel
- Post
- Artigo
- Podcast
- Thumbnail
- Story
- Banner

---

## Orientação

Define o formato visual da produção, quando aplicável.

**Exemplos:**

- Vertical (9:16)
- Horizontal (16:9)
- Quadrado (1:1)
- Personalizado

---

## Objetivo da Produção

Define o principal resultado esperado.

**Exemplos:**

- Alcance
- Engajamento
- Monetização
- Educação
- Branding
- Conversão
- Entretenimento

---

## Duração

Define o tempo aproximado desejado para a produção.

Pode ser informado por categorias ou por intervalo.

### Categorias sugeridas

- Muito curta (até 30 segundos)
- Curta (30–60 segundos)
- Média (1–3 minutos)
- Longa (3–10 minutos)
- Muito longa (10+ minutos)

### Ou duração personalizada

Exemplos:

- 90–120 segundos
- 8–10 minutos

---

## Ferramenta Alvo

Define a ferramenta principal para geração do conteúdo.

**Exemplos:**

- Gemini
- Veo
- Pika
- Runway
- ChatGPT
- Flux
- Midjourney

---

## Estilo Visual

Define a direção artística da produção.

**Exemplos:**

- 2D Vetorial
- Realista
- Anime
- Pixar
- Live Action
- Low Poly
- Pixel Art

---

## Elenco

Define quais personagens participarão da produção.

Pode ser:

- Automático
- Personagens oficiais do universo
- Personagens definidos pelo usuário
- Personagens genéricos

---

## Público-Alvo

Define para quem o conteúdo será produzido, quando necessário.

**Exemplos:**

- Público geral
- Profissionais de TI
- Pessoas autistas
- Pais
- Crianças
- Empresas

---

# Fluxo na Arquitetura

```text
Demanda
      ↓
Briefing de Produção
      ↓
Planejamento
      ↓
Especialistas
      ↓
Produção
```

---

# Observações

O Briefing de Produção não substitui o roteiro, o planejamento, a documentação dos universos nem a direção de arte.

Seu papel é fornecer o contexto necessário para que qualquer especialista do TCCN AI Studio possa executar a produção de forma consistente, reutilizável e alinhada aos objetivos definidos.

O documento foi concebido como um componente central do Núcleo Operacional do TCCN AI Studio e deve ser utilizado como ponto de entrada para qualquer fluxo de produção de conteúdo.