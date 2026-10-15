from fastapi import FastAPI
from dotenv import loadenv

from routers.RAGService import router as rag_router
from routers.InputService import router as input_router

loadenv()

app = FastAPI()

app.include_router(router = input_router)
app.include_router(router = rag_router)