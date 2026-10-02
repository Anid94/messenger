from pathlib import Path

from fastapi import FastAPI
from routes import users, messages

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="Messenger")
app.include_router(users.router)
app.include_router(messages.router)

#Для css
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

@app.get("/", include_in_schema=False)
def index():
    return FileResponse(BASE_DIR / "static" / "index.html")
