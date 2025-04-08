from fastapi import FastAPI
from app.api.routes import tasks
from app.db.database import engine
from app.db.base import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])

@app.get("/")
def read_root():
    return {"msg": "API funcionando"}



