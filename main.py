from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#os.environ para despliegue. Descomente cuando ya probó todo local.
#client = MongoClient(os.environ["MONGO_URI"])
# TODO: conectarse al cluster Admonsis  
# client = MongoClient("mongodb://<usuario>:<contraseña>@157.253.236.88:8087")


MONGO_URI = os.environ.get("MONGO_URI")

client = MongoClient(MONGO_URI)
# TODO: conectarse a la base de datos Admonsis  
# db = client["ISIS*******"]
db = client["ISIS2304D28202610"]
comentarios_collection = db["comentarios"]
eventos_collection = db["eventos"]

@app.get("/")
def inicio():
    return {"estado": "API funcionando correctamente"}

@app.get('/bares/{bar_id}/comentarios')
def get_comentarios(bar_id: int):
    comentarios = list(comentarios_collection.find(
        {"bar_id": bar_id},
        {"_id": 0}
    ))
    return comentarios

@app.post('/bares/{bar_id}/comentarios')
def post_comentario(bar_id: int, datos: dict):
    datos['bar_id'] = bar_id
    datos['fecha']  = datetime.now().isoformat()
    comentarios_collection.insert_one(datos)
    return {'mensaje': 'Comentario guardado'}

@app.get("/api/bares/{bar_id}/eventos")
def obtener_eventos(bar_id: int):
    eventos = list(eventos_collection.find(
        {"bar_id": bar_id},
        {"_id": 0}
    ))
    return eventos

@app.post("/api/bares/{bar_id}/eventos")
def crear_evento(bar_id: int, datos: dict):
    datos["bar_id"] = bar_id
    datos["fecha_creacion"] = datetime.now().isoformat()
    eventos_collection.insert_one(datos)
    return {"mensaje": "Evento creado correctamente"}
