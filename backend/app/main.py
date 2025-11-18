from fastapi import FastAPI
from .routes import (
    users as users_router,
    auth as auth_router,
    files as files_router,
    fileversion_routes as fileversion_router,
    log_routes as logbook_router
)
from .routes import (
    file_routes as file,
    log_routes as log
)
from .db import init_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating database and tables...")
    await init_db()
    yield
    print("Application shutdown.")

app = FastAPI(lifespan=lifespan)

# Attach roouters
app.include_router(users_router.router)
app.include_router(auth_router.router)
app.include_router(files_router.router)

@app.get("/api")
def root():
    return {"message": "Hello from FastAPI!"}