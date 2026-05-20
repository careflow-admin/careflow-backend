from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
from contextlib import asynccontextmanager
import app.api.models
from app.api.routers import (
    auth,
    citas,
    especialidades,
    horarios,
    medicos,
    usuarios,
    historiales_clinicos,
    medicamentos,
    recetas_medicas,
    tipos_medicamento,
)
from app.database.session import Base, engine


origins = [
    "http://localhost:4200",  # Angular
    "http://127.0.0.1:4200",
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="CareFlow API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],  # importante
    allow_headers=["*"],
)

app.include_router(usuarios.router)
app.include_router(auth.router)
app.include_router(especialidades.router)
app.include_router(medicos.router)
app.include_router(citas.router)
app.include_router(horarios.router)
app.include_router(historiales_clinicos.router)
app.include_router(medicamentos.router)
app.include_router(recetas_medicas.router)
app.include_router(tipos_medicamento.router)
