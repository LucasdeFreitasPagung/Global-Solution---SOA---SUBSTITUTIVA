from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

# --- MOCK DE BANCO DE DADOS DE USUÁRIOS E TOKENS ---
# Na vida real, validaríamos um token JWT gerado após o login. 
# Aqui, simulamos tokens fixos documentados para a banca conseguir testar.
USUARIOS_MOCK = {
    "token-cidadao-123": {"id": 1, "nome": "João", "role": "cidadao"},
    "token-operador-456": {"id": 2, "nome": "Maria", "role": "operador"},
    "token-admin-789": {"id": 3, "nome": "Carlos", "role": "administrador"}
}

# Configura o FastAPI para buscar o token no cabeçalho (Header) "Authorization"
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

# --- MIDDLEWARE DE AUTENTICAÇÃO ---
async def obter_usuario_atual(api_key: str = Security(api_key_header)):
    """Verifica se o usuário enviou um token válido (Autenticação)."""
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação ausente."
        )
    
    # Remove prefixo 'Bearer ' caso o cliente envie por padrão
    token_limpo = api_key.replace("Bearer ", "") if "Bearer" in api_key else api_key
    
    usuario = USUARIOS_MOCK.get(token_limpo)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou acesso não reconhecido."
        )
    return usuario

# --- MIDDLEWARE DE AUTORIZAÇÃO (PERFIS) ---
def exigir_perfil(perfis_permitidos: list):
    """Fábrica de dependências para verificar a role do usuário (Autorização)."""
    def validador_perfil(usuario: dict = Security(obter_usuario_atual)):
        if usuario["role"] not in perfis_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acesso negado. Seu perfil ({usuario['role']}) não tem permissão para esta ação."
            )
        return usuario
    return validador_perfil