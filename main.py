from fastapi import FastAPI, Request
from starlette.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.api.user import auth

templates = Jinja2Templates(directory="templates")
 
app = FastAPI()
app.mount("/static",StaticFiles(directory="static",html=True),name="static")
app.include_router(auth.AUTH)
 
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
 
