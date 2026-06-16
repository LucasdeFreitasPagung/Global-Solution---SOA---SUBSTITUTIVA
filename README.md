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


🧠 Decisões Arquiteturais
Arquitetura Base: Monólito Modular. Os módulos (Ocorrências, Segurança, Prioridade e Notificação) estão separados logicamente. Caso o sistema precise escalar no futuro, o módulo de "Notificação" pode ser facilmente extraído para um Microsserviço independente consumindo mensageria (RabbitMQ/Kafka).

Comunicação: O módulo core (Ocorrências) se comunica de forma síncrona com o módulo de Prioridade, e de forma assíncrona (simulada via eventos de log) com o módulo de Notificações, evitando gargalos de I/O na API principal.

Persistência: Foi utilizado um Mock em memória (dicionários) para manter o projeto agnóstico e facilitar a execução pela banca avaliadora, focando na demonstração dos conceitos de SOA e APIs.

🔐 Estratégia de Segurança
Foi implementada uma camada de autenticação e autorização via cabeçalho HTTP (Authorization). Os perfis estão divididos em:

Cidadão (token-cidadao-123): Pode criar e visualizar ocorrências.

Operador (token-operador-456): Pode alterar o status das ocorrências.

Administrador (token-admin-789): Possui acesso total, incluindo a exclusão lógica (soft delete).

🐛 Tratamento de Erros e Observabilidade
Erros Padronizados: Todos os erros HTTP capturados pelo sistema retornam um payload JSON estruturado contendo timestamp, status, error, message e o path da requisição, diferenciando falhas de negócio (BUSINESS_ERROR) de falhas de autorização (UNAUTHORIZED).

Observabilidade: Foi incluído um endpoint /health para monitoramento do status da aplicação. Além disso, as requisições geram logs contendo um correlation_id único, garantindo rastreabilidade das operações críticas ao longo dos módulos.

🚀 Tecnologias Utilizadas
Linguagem: Python 3.x

Framework Web: FastAPI (Alta performance e suporte nativo a operações assíncronas)

Validação de Dados: Pydantic

Servidor ASGI: Uvicorn

Documentação: Swagger UI / OpenAPI (Gerado automaticamente)

⚙️ Como Executar o Projeto
Certifique-se de ter o Python instalado.

Instale as dependências executando:
pip install fastapi uvicorn pydantic

Inicie o servidor:
python -m uvicorn main:app --reload

Acesse a documentação Swagger e teste a API em:
http://localhost:8000/docs
