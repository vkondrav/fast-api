from fastapi import FastAPI
from mangum import Mangum
from chat import router as chat_router
from radio import router as radio_router
from file import router as file_router
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Serverless Lambda")

app.include_router(radio_router, prefix="/radio")
app.include_router(chat_router, prefix="/chat")
app.include_router(file_router, prefix="/file")

app.mount("/", StaticFiles(directory="static", html=True), name="static")

handler = Mangum(app)

