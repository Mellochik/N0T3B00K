from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.routers import auth_router, tasks_router


app = FastAPI(
    title="N0T3B00K API",
    description="API для сервиса N0T3B00K",
    version="0.1.0",
    root_path="/api/v1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)


app.include_router(auth_router)
app.include_router(tasks_router)


@app.get("/")
async def root() -> JSONResponse:
    return {
        "message": "Welcome to N0T3B00K API",
        "docs": "/docs"
    }
