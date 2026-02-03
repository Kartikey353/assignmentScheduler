import sys
import os

# Adds the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from db.init_db import initialize_databases 
from src.module.router.user_router import router as user_router
from src.module.router.target_router import router as target_router

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await initialize_databases()

@app.get("/healthCheckup")
def read_main():
    return {"message": "Service is running and UP"}


app.include_router(user_router, prefix="/api/v1")
app.include_router(target_router, prefix="/api/v1")

