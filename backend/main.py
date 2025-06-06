from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

# Crear aplicación FastAPI
app = FastAPI(
    title="API de Clasificación de Mensajes",
    description="Clasifica mensajes en categorías Urgente, Normal o Moderado usando IA",
    version="1.0.0"
)

# Configuración CORS esencial para permitir conexiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración del token de Hugging Face
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
if not HUGGINGFACE_TOKEN:
    raise ValueError("No se encontró el token de Hugging Face. Configura HUGGINGFACE_TOKEN en .env")

# Cargamos el modelo Zero-Shot con autenticación
try:
    classifier = pipeline(
        "zero-shot-classification",
        model="facebook/bart-large-mnli",
        use_auth_token=HUGGINGFACE_TOKEN
    )
except Exception as e:
    raise RuntimeError(f"No se pudo cargar el modelo: {str(e)}")

# Modelo Pydantic para la entrada de datos
class Message(BaseModel):
    text: str
    candidate_labels: List[str] = ["Urgente", "Normal", "Moderado"]

# Endpoint de verificación de salud
@app.get("/")
async def health_check():
    return {
        "status": "API funcionando",
        "model": "facebook/bart-large-mnli",
        "ready": True
    }

# Endpoint de clasificación
@app.post("/classify/")
async def classify_message(message: Message):
    try:
        result = classifier(
            message.text,
            candidate_labels=message.candidate_labels,
            multi_label=False
        )
        
        return {
            "message": message.text,
            "classification": result["labels"][0],
            "confidence": result["scores"][0],
            "all_scores": dict(zip(result["labels"], result["scores"])),
            "success": True
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "success": False
            }
        )

