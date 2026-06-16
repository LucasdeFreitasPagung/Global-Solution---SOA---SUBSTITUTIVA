graph TD
    %% Atores
    User1((Cidadão))
    User2((Operador / Admin))
    
    %% API e Segurança
    Gateway[API REST / FastAPI]
    Security{Módulo de Segurança \n Auth / JWT}
    
    %% Módulos do Sistema
    ModOcorrencia[Módulo de Ocorrências \n Gestão e Status]
    ModPrioridade[Módulo de Prioridade \n Regras de Negócio]
    ModNotificacao[Módulo de Notificação \n Eventos e Alertas]
    
    %% Banco de Dados
    DB[(Mock Database \n Memória)]

    %% Fluxo de Comunicação
    User1 -->|POST / GET| Gateway
    User2 -->|PUT / GET| Gateway
    
    Gateway -->|Intercepta| Security
    Security -->|Valida| ModOcorrencia
    
    ModOcorrencia -->|Consulta Regra \n Síncrono| ModPrioridade
    ModOcorrencia -.->|Dispara Evento \n Assíncrono| ModNotificacao
    
    ModOcorrencia <-->|Leitura / Escrita| DB
    
    %% Estilização
    classDef module fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef db fill:#fff3e0,stroke:#e65100,stroke-width:2px;
    classDef core fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px;
    
    class ModOcorrencia,ModPrioridade,ModNotificacao module;
    class DB db;
    class Gateway,Security core;
