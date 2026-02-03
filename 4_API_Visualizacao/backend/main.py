from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router

# Inicialização da API
app = FastAPI(
    title="API Operadoras ANS",
    description="API para consulta de dados financeiros e cadastrais.",
    version="1.0.0"
)

# Configuração de CORS (Permite que o Frontend HTML acesse)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra as rotas
app.include_router(router, prefix="/api")

# Para rodar: uvicorn main:app --reload