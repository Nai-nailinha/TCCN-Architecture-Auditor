# Princípio de Fidelidade Arquitetural

**Versão:** v0.1  
**Status:** Oficial  
**Categoria:** Governança  
**Tipo de documento:** Princípio de Governança  
**Pasta de destino:** 01 - Governança  
**Nome do arquivo:** principio-fidelidade-arquitetural.md

---

**Princípio:** A fidelidade arquitetural prevalece sobre a completude documental.

O processo de migração, consolidação ou atualização da documentação oficial deverá refletir fielmente a arquitetura vigente e o material de origem oficialmente aprovado.

As ferramentas responsáveis pela migração, consolidação ou atualização da documentação oficial atuam como editoras técnicas da documentação, não como autoras da arquitetura.

Durante esses processos, nenhuma ferramenta ou agente poderá:

- criar elementos arquiteturais não definidos;
- inferir informações não aprovadas;
- renomear elementos existentes;
- consolidar elementos sem decisão arquitetural explícita;
- expandir responsabilidades além das previstas na arquitetura;
- complementar informações por interpretação própria.

Quando a arquitetura ou o material de origem indicar a existência de um elemento ainda não suficientemente especificado, esse elemento deverá ser registrado como **Pendente de Definição**, preservando sua posição prevista na arquitetura sem preenchimento por inferência.

Elementos que não estejam previstos pela arquitetura nem pelo material de origem não deverão ser incorporados à documentação oficial.

Em caso de conflito entre a completude documental e a fidelidade arquitetural, deverá prevalecer a fidelidade arquitetural, ainda que isso implique registrar pendências, lacunas ou elementos futuros.

## Regra Permanente para Produção de Documentação Oficial

Todo documento oficial produzido durante a migração, consolidação ou atualização da documentação deverá obrigatoriamente iniciar com o cabeçalho padrão de metadados definido pelo TCCN AI Studio, contendo, no mínimo:

- Título
- Versão
- Status
- Categoria
- Tipo de documento
- Pasta de destino
- Nome do arquivo

A ausência desse cabeçalho caracteriza uma migração documental incompleta.