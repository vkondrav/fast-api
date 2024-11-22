from fastapi import FastAPI
from mangum import Mangum
from chat import router as chat_router
from radio import router as radio_router
from file import router as file_router
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Serverless Lambda")

app.include_router(radio_router, prefix="/api/radio")
app.include_router(chat_router, prefix="/api/chat")
app.include_router(file_router, prefix="/api/file")

app.mount("/", StaticFiles(directory="static", html=True), name="static")

handler = Mangum(app)

