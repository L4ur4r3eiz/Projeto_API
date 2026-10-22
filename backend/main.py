import os  # serve para criar a pasta de uploads se ela não existir
from fastapi import FastAPI, Depends  # <--- Adicionamos o Depends aqui!
from fastapi.staticfiles import StaticFiles  # serve arquivos estáticos (como imagens enviadas)
from fastapi.middleware.cors import CORSMiddleware
from rotas import clientes, senioridade, tatuadores, agendamentos, estilos, usuarios, login
from seguranca import verificar_token

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Garante que a pasta de uploads existe antes de tentar servir arquivos dela
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")  # serve as imagens estáticas

# ─── Registro das Rotas ───
app.include_router(login.router, tags=["Login"])
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuários"])
app.include_router(clientes.router, prefix="/clientes", tags=["Clientes"], dependencies=[Depends(verificar_token)])
app.include_router(senioridade.router, prefix="/senioridade", tags=["Senioridade"], dependencies=[Depends(verificar_token)])
app.include_router(estilos.router, prefix="/estilos", tags=["Estilos"], dependencies=[Depends(verificar_token)])
app.include_router(tatuadores.router, prefix="/tatuadores", tags=["Tatuadores"], dependencies=[Depends(verificar_token)])
app.include_router(agendamentos.router, prefix="/agendamentos", tags=["Agendamentos"], dependencies=[Depends(verificar_token)])




@app.get("/")
def inicio():
    return {"mensagem": "API do estúdio de tatuagem funcionando!"}