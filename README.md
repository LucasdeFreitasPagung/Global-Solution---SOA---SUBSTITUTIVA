# 🏙️ Plataforma de Monitoramento de Infraestrutura Urbana - Arquitetura SOA

**Aluno:** Lucas de Freitas Pagung  
**RM:** 553242  
**Turma:** 3ESPR  
**Polo:** Av. Paulista  
**Turno:** Noturno  

---

## 📖 Descrição da Solução
Esta aplicação backend é uma solução arquitetural focada no monitoramento de ocorrências urbanas (como buracos em vias, alagamentos e falhas de iluminação). O sistema permite o registro ágil de problemas, acompanhamento de status, classificação automática de prioridade e simulação de notificação de responsáveis.

## 🏗️ Diagrama da Arquitetura
A solução foi desenhada utilizando o padrão **Monólito Modular**, o que garante uma excelente separação de responsabilidades (SoC) enquanto mantém a simplicidade de implantação e testes.

```mermaid
graph TD
    User1((Cidadão))
    User2((Operador / Admin))
    
    Gateway[API REST / FastAPI]
    Security{Módulo de Segurança \n Auth}
    
    ModOcorrencia[Módulo de Ocorrências \n Gestão e Status]
    ModPrioridade[Módulo de Prioridade \n Regras de Negócio]
    ModNotificacao[Módulo de Notificação \n Eventos e Alertas]
    
    DB[(Mock Database \n Memória)]

    User1 -->|POST / GET| Gateway
    User2 -->|PATCH / DELETE| Gateway
    
    Gateway -->|Intercepta| Security
    Security -->|Valida| ModOcorrencia
    
    ModOcorrencia -->|Consulta Regra| ModPrioridade
    ModOcorrencia -.->|Dispara Evento Assíncrono| ModNotificacao
    
    ModOcorrencia <-->|Leitura / Escrita| DB
