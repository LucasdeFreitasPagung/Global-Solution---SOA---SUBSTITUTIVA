from datetime import datetime
from fastapi import HTTPException

# Nosso "Banco de Dados" em memória
db_ocorrencias = {}

def classificar_prioridade(tipo: str) -> str:
    """Módulo de Prioridade: Calcula a prioridade baseada no tipo."""
    criticos = ["buraco na via", "alagamento", "queda de árvore"]
    if tipo.lower() in criticos:
        return "CRITICA"
    return "MEDIA"

def notificar_responsavel(ocorrencia_id: str, mensagem: str):
    """Módulo de Notificação: Simula o envio de um alerta ou evento."""
    print(f"🔔 [NOTIFICAÇÃO ASSÍNCRONA SIMULADA] Ocorrência {ocorrencia_id}: {mensagem}")

def criar_ocorrencia(dados: dict):
    if not dados.get("descricao"):
        raise HTTPException(status_code=400, detail="Descrição é obrigatória.")
    
    ocorrencia_id = str(len(db_ocorrencias) + 1)
    prioridade = classificar_prioridade(dados["tipo"])
    
    nova_ocorrencia = {
        "id": ocorrencia_id,
        "titulo": dados["titulo"],
        "descricao": dados["descricao"],
        "tipo": dados["tipo"],
        "prioridade": prioridade,
        "status": "ABERTA",
        "data_abertura": datetime.now().isoformat(),
        "ativo": True
    }
    
    db_ocorrencias[ocorrencia_id] = nova_ocorrencia
    
    # Integração entre módulos: Se for crítica, dispara notificação
    if prioridade == "CRITICA":
        notificar_responsavel(ocorrencia_id, "Nova ocorrência crítica registrada na sua região!")
        
    return nova_ocorrencia

def listar_todas_ocorrencias():
    # Retorna apenas as ativas (regra de remoção lógica)
    return [oc for oc in db_ocorrencias.values() if oc["ativo"]]

def buscar_ocorrencia_por_id(ocorrencia_id: str):
    ocorrencia = db_ocorrencias.get(ocorrencia_id)
    if not ocorrencia or not ocorrencia["ativo"]:
        raise HTTPException(status_code=404, detail="Ocorrência não encontrada.")
    return ocorrencia

def atualizar_status(ocorrencia_id: str, novo_status: str):
    ocorrencia = buscar_ocorrencia_por_id(ocorrencia_id)
    status_atual = ocorrencia["status"]
    
    if status_atual in ["RESOLVIDA", "CANCELADA"]:
        raise HTTPException(status_code=400, detail=f"Não é possível alterar uma ocorrência {status_atual}.")
    
    ocorrencia["status"] = novo_status
    return ocorrencia

def remover_ocorrencia(ocorrencia_id: str):
    ocorrencia = buscar_ocorrencia_por_id(ocorrencia_id)
    ocorrencia["ativo"] = False # Remoção lógica (Soft Delete)