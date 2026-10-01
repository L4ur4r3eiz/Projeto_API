# ============================================================
# rotas/tatuadores.py — CRUD de Tatuadores
# Descrição: Endpoints para gerenciar os tatuadores do estúdio.
#            Cada tatuador pertence a uma senioridade (FK).
# ============================================================

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from database import conectar

router = APIRouter()

# Modelo de dados — define os campos que o tatuador deve ter
class Tatuador(BaseModel):
    nometatuador: str                      # obrigatório
    cpf: str                               # obrigatório
    email: Optional[str] = None            # opcional
    telefone: Optional[str] = None         # opcional
    datacontratacao: Optional[str] = None  # opcional
    idsenioridade: int                     # obrigatório — aponta para a tabela senioridade
