from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from datetime import datetime
import uuid
import logging

# Importando os arquivos que criamos anteriormente
from models import OcorrenciaCreate, OcorrenciaUpdateStatus
from security import obter_usuario_atual, exigir_perfil

# Importando o módulo de serviços (que contém as regras de negócio e o "banco de dados")
import services

# =====================================================================
# 1. CONFIGURAÇÃO DA APLICAÇÃO E OBSERVABILIDADE (LOGS)
# =====================================================================
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - [%(correlation_id)s] - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Plataforma de Monitoramento de Infraestrutura Urbana",
    description="API REST para registro e acompanhamento de ocorrências urbanas.",
    version="1.0.0"
)

# Middleware para injetar Correlation ID (Rastreabilidade - Requisito da GS)
@app.middleware("http")
async def add_correlation_id(request: Request, call_next):
    correlation_id = str(uuid.uuid4())
    
    # Injeta o correlation ID no gerador de logs
    old_factory = logging.getLogRecordFactory()
    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.correlation_id = correlation_id
        return record
    logging.setLogRecordFactory(record_factory)
    
    logger.info(f"Recebendo requisição: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Finalizando requisição com status {response.status_code}")
    return response

# =====================================================================
# 2. TRATAMENTO DE ERROS PADRONIZADO (Requisito da GS)
# =====================================================================
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    # Diferenciando tipo de erro baseado no status code HTTP
    tipo_erro = "BUSINESS_ERROR"
    if exc.status_code == 404:
        tipo_erro = "NOT_FOUND"
    elif exc.status_code in [401, 403]:
        tipo_erro = "UNAUTHORIZED"

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "timestamp": datetime.now().isoformat(),
            "status": exc.status_code,
            "error": tipo_erro,
            "message": exc.detail,
            "path": request.url.path
        }
    )

# =====================================================================
# 3. ENDPOINTS DA API REST
# =====================================================================

@app.get("/health", tags=["Observabilidade"])
def health_check():
    """Endpoint de Health Check para monitoramento básico."""
    return {"status": "UP", "timestamp": datetime.now().isoformat()}


@app.post("/ocorrencias", status_code=201, tags=["Ocorrências"])
def criar_ocorrencia(
    payload: OcorrenciaCreate, 
    usuario: dict = Depends(obter_usuario_atual) # Qualquer usuário autenticado pode criar
):
    """Cadastra uma nova ocorrência urbana (Ex: buraco, alagamento)."""
    logger.info(f"Usuário {usuario['nome']} solicitou criação de ocorrência.")
    nova_ocorrencia = services.criar_ocorrencia(payload.dict())
    return nova_ocorrencia


@app.get("/ocorrencias", tags=["Ocorrências"])
def listar_ocorrencias(usuario: dict = Depends(obter_usuario_atual)):
    """Lista todas as ocorrências ativas no sistema."""
    logger.info(f"Usuário {usuario['nome']} consultou a lista de ocorrências.")
    return services.listar_todas_ocorrencias()


@app.get("/ocorrencias/{ocorrencia_id}", tags=["Ocorrências"])
def buscar_ocorrencia(ocorrencia_id: str, usuario: dict = Depends(obter_usuario_atual)):
    """Busca os detalhes de uma ocorrência específica pelo seu ID."""
    return services.buscar_ocorrencia_por_id(ocorrencia_id)


@app.patch("/ocorrencias/{ocorrencia_id}/status", tags=["Gestão Interna"])
def atualizar_status(
    ocorrencia_id: str, 
    payload: OcorrenciaUpdateStatus, 
    # Autorização: Apenas Operadores e Administradores podem mudar o status!
    usuario: dict = Depends(exigir_perfil(["operador", "administrador"]))
):
    """Atualiza o status de uma ocorrência (Ex: ABERTA para RESOLVIDA)."""
    logger.info(f"Operador {usuario['nome']} alterando status da ocorrência {ocorrencia_id}.")
    ocorrencia_atualizada = services.atualizar_status(ocorrencia_id, payload.novo_status.value)
    return ocorrencia_atualizada


@app.delete("/ocorrencias/{ocorrencia_id}", status_code=204, tags=["Gestão Interna"])
def deletar_ocorrencia(
    ocorrencia_id: str, 
    # Autorização: Apenas Administradores podem deletar
    usuario: dict = Depends(exigir_perfil(["administrador"]))
):
    """Realiza a exclusão (remoção lógica) de uma ocorrência."""
    logger.warning(f"Administrador {usuario['nome']} está deletando a ocorrência {ocorrencia_id}.")
    services.remover_ocorrencia(ocorrencia_id)
    return None # 204 No Content não retorna corpo