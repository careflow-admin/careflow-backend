from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
from contextlib import asynccontextmanager
import app.api.models
from app.api.routers import auth, citas, especialidades, horarios, medicos, usuarios
from app.database.session import Base, engine

app = FastAPI(title="CareFlow API")

origins = [
    "http://localhost:4200",  # Angular
    "http://127.0.0.1:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],  # importante
    allow_headers=["*"],
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    Base.metadata.create_all(bind=engine)
    yield

app.include_router(usuarios.router)
app.include_router(auth.router)
app.include_router(especialidades.router)
app.include_router(medicos.router)
app.include_router(citas.router)
app.include_router(horarios.router)
