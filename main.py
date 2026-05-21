from fastapi import FastAPI
from routers import auth, notas, ia

app = FastAPI(
    title="Notas IA API",
    description="API de notas con autenticación JWT y endpoints para agentes de IA",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(notas.router)
app.include_router(ia.router)


@app.get("/")
def raiz():
    return {
        "nombre": "Notas IA API",
        "version": "1.0.0",
        "docs": "/docs"
    }