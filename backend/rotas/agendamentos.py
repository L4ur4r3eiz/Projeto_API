# ============================================================
# rotas/agendamentos.py — CRUD de Agendamentos
# Descrição: Endpoints para gerenciar os agendamentos de sessões
#            de tatuagem. Cada agendamento liga um cliente a um
#            tatuador (duas chaves estrangeiras).
# ============================================================

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from database import conectar
import os

router = APIRouter()

def formatar_hora(agendamento):
    total_segundos = int(agendamento["horaagendamento"].total_seconds())
    horas, resto = divmod(total_segundos, 3600)
    minutos, segundos = divmod(resto, 60)
    agendamento["horaagendamento"] = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
    return agendamento

def enviar_desenho(nome_arquivo):
    if not nome_arquivo:
        raise HTTPException(status_code=404, detail="Desenho não encontrado")

    nome_seguro = os.path.basename(nome_arquivo)
    caminho = os.path.join("uploads", nome_seguro)
    if not os.path.isfile(caminho):
        raise HTTPException(status_code=404, detail="Desenho não encontrado")

    return FileResponse(caminho, filename=nome_seguro)

# Modelo de dados — define os campos que o agendamento deve ter
class Agendamento(BaseModel):
    idcliente: int                          # obrigatório — aponta para a tabela cliente
    idtatuador: int                         # obrigatório — aponta para a tabela tatuador
    dataagendamento: str                    # obrigatório
    horaagendamento: str                    # obrigatório
    descricaotatuagem: Optional[str] = None # opcional
    valortatuagem: Optional[float] = None   # opcional
    status: Optional[str] = None            # só é usado ao atualizar (ver Parte 7)

# POST /agendamentos — cadastra um novo agendamento
@router.post("")
def criar_agendamento(agendamento: Agendamento):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO agendamento (idcliente, idtatuador, dataagendamento, horaagendamento, descricaotatuagem, valortatuagem)
           VALUES (%s, %s, %s, %s, %s, %s)""",
        (agendamento.idcliente, agendamento.idtatuador, agendamento.dataagendamento,
         agendamento.horaagendamento, agendamento.descricaotatuagem, agendamento.valortatuagem)
    )
    novo_id = cursor.lastrowid   # o ID que o MySQL gerou sozinho pro novo agendamento (AUTO_INCREMENT)
    conn.commit()
    conn.close()
    return {"mensagem": "Agendamento cadastrado com sucesso", "idagendamento": novo_id}

# GET /agendamentos — lista todos os agendamentos, já com nome do cliente e do tatuador
@router.get("")
def listar_agendamentos():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT agendamento.*, cliente.nome AS cliente, tatuador.nometatuador AS tatuador
        FROM agendamento
        JOIN cliente  ON agendamento.idcliente  = cliente.idcliente
        JOIN tatuador ON agendamento.idtatuador = tatuador.idtatuador
    """)
    agendamentos = cursor.fetchall()
    conn.close()

    # o mysql-connector-python devolve colunas TIME como um "timedelta" (tempo decorrido),
    # não como texto — por isso convertemos aqui pra "HH:MM:SS" antes de mandar pro frontend
    for a in agendamentos:
        formatar_hora(a)

    return agendamentos

# GET /agendamentos/{id} — busca um agendamento pelo ID
@router.get("/{id}")
def buscar_agendamento(id: int):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM agendamento WHERE idagendamento = %s", (id,))
    agendamento = cursor.fetchone()
    conn.close()
    if not agendamento:
        return {"erro": "Agendamento não encontrado"}

    # mesma conversão — sem isso, horaagendamento viria como número de segundos
    return formatar_hora(agendamento)

@router.get("/{id}/desenho")
def baixar_desenho(id: int):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT desenhoaprovado FROM agendamento WHERE idagendamento = %s", (id,))
    agendamento = cursor.fetchone()
    conn.close()
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    return enviar_desenho(agendamento["desenhoaprovado"])

# PUT /agendamentos/{id} — atualiza um agendamento existente
@router.put("/{id}")
def atualizar_agendamento(id: int, agendamento: Agendamento):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE agendamento
           SET idcliente=%s, idtatuador=%s, dataagendamento=%s, horaagendamento=%s,
               descricaotatuagem=%s, valortatuagem=%s, status=%s
           WHERE idagendamento=%s""",
        (agendamento.idcliente, agendamento.idtatuador, agendamento.dataagendamento,
         agendamento.horaagendamento, agendamento.descricaotatuagem,
         agendamento.valortatuagem, agendamento.status, id)
    )
    conn.commit()
    conn.close()
    return {"mensagem": "Agendamento atualizado com sucesso"}

# DELETE /agendamentos/{id} — deleta um agendamento
@router.delete("/{id}")
def deletar_agendamento(id: int):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM agendamento WHERE idagendamento = %s", (id,))
    conn.commit()
    conn.close()
    return {"mensagem": "Agendamento deletado com sucesso"}

# POST /agendamentos/{id}/desenho — recebe a imagem do desenho aprovado e associa ao agendamento
@router.post("/{id}/desenho")
async def upload_desenho(id: int, arquivo: UploadFile = File(...)):
    nome_original = os.path.basename(arquivo.filename or "")
    extensao = os.path.splitext(nome_original)[1].lower()
    if extensao not in (".png", ".jpg", ".jpeg", ".gif", ".webp"):
        raise HTTPException(status_code=400, detail="Envie uma imagem PNG, JPG, GIF ou WEBP")

    nome_arquivo = f"{id}_{nome_original}"   # o id na frente evita nomes repetidos entre agendamentos
    caminho = os.path.join("uploads", nome_arquivo)

    conteudo = await arquivo.read()       # lê o conteúdo do arquivo enviado
    with open(caminho, "wb") as f:        # "wb" = write binary — é uma imagem, não texto
        f.write(conteudo)

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE agendamento SET desenhoaprovado=%s WHERE idagendamento=%s", (nome_arquivo, id))
    conn.commit()
    conn.close()
    return {"mensagem": "Desenho enviado com sucesso", "arquivo": nome_arquivo}