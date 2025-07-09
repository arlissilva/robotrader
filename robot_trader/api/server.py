from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List
import jwt
import time
import uvicorn

app = FastAPI()

# CORS liberado para frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔐 Configurações de autenticação
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
SECRET_KEY = "segredo123"
ALGORITHM = "HS256"

# 🧪 Usuário fictício para testes
fake_user = {
    "username": "admin",
    "password": "admin123"
}

# 🧠 Banco de dados em memória
ordens_executadas = []
ativos_configurados = []

# 📦 Modelos de dados
class Ordem(BaseModel):
    ativo: str
    tipo: str
    preco: float
    timestamp: str

class AtivoConfig(BaseModel):
    simbolos: List[str]

# 🔑 Login
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != fake_user["username"] or form_data.password != fake_user["password"]:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    payload = {
        "sub": form_data.username,
        "exp": time.time() + 3600  # 1 hora
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

# 🔒 Dependência para validar token
def validar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")

# 🔐 Rota protegida de teste
@app.get("/dados")
def dados(usuario: str = Depends(validar_token)):
    return {"mensagem": f"Olá, {usuario}! Acesso autorizado à rota protegida."}

# 🔒 Rotas de ordens protegidas
@app.get("/ordens", response_model=List[Ordem])
def listar_ordens(usuario: str = Depends(validar_token)):
    return ordens_executadas

@app.post("/ordens")
def adicionar_ordem(ordem: Ordem, usuario: str = Depends(validar_token)):
    ordens_executadas.append(ordem)
    return {"status": "sucesso", "mensagem": "Ordem registrada"}

# 🔒 Rotas de ativos protegidas
@app.get("/ativos", response_model=List[str])
def listar_ativos(usuario: str = Depends(validar_token)):
    return ativos_configurados

@app.post("/ativos")
def configurar_ativos(config: AtivoConfig, usuario: str = Depends(validar_token)):
    ativos_configurados.clear()
    ativos_configurados.extend(config.simbolos)
    return {"status": "sucesso", "mensagem": "Ativos configurados"}
    
def iniciar_api(sinais_externos):
    global sinais_recebidos
    sinais_recebidos = sinais_externos

    uvicorn.run(app, host="0.0.0.0", port=8000)
