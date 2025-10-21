from fastapi import FastAPI
from app.routes import (
    files as files_router
)

app = FastAPI()

# Attach roouters
app.include_router(files_router.router)

@app.get("/api")
def root():
    return {"message": "Hello from FastAPI!"}