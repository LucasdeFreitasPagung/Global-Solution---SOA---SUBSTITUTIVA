from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional
from datetime import datetime

# --- ENUMS (Regras de Domínio) ---
class TipoOcorrencia(str, Enum):
    BURACO = "buraco na via"
    ILUMINACAO = "iluminação pública"
    ALAGAMENTO = "alagamento"
    ARVORE = "queda de árvore"
    SEMAFORO = "semáforo com defeito"
    LIXO = "lixo acumulado"
    CALCADA = "calçada danificada"

class StatusOcorrencia(str, Enum):
    ABERTA = "ABERTA"
    EM_ANALISE = "EM_ANALISE"
    EM_ATENDIMENTO = "EM_ATENDIMENTO"
    RESOLVIDA = "RESOLVIDA"
    CANCELADA = "CANCELADA"

class PrioridadeOcorrencia(str, Enum):
    BAIXA = "BAIXA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"
    CRITICA = "CRITICA"

# --- SCHEMAS (Validação de Entrada e Saída da API) ---

# Schema para o Payload (o que o Cidadão envia no POST)
class OcorrenciaCreate(BaseModel):
    titulo: str = Field(..., min_length=3, max_length=100, example="Buraco enorme na rua principal")
    descricao: str = Field(..., min_length=10, example="Há um buraco muito fundo causando acidentes na via.")
    tipo: TipoOcorrencia
    localizacao: str = Field(..., example="Rua das Flores, 123 - Centro")

# Schema para a Resposta (o que a API devolve, adicionando ID, status, etc.)
class OcorrenciaResponse(OcorrenciaCreate):
    id: str
    prioridade: PrioridadeOcorrencia
    status: StatusOcorrencia
    data_abertura: str
    responsavel: Optional[str] = None
    
    class Config:
        orm_mode = True

# Schema para atualizar o status (o que o Operador envia no PATCH)
class OcorrenciaUpdateStatus(BaseModel):
    novo_status: StatusOcorrencia
    responsavel: Optional[str] = Field(None, example="Equipe Alpha")