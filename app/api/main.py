from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.routers import tasks, auth


app = FastAPI(
    title="N0T3B00K API",
    description="API for N0T3B00K",
    version="0.1.0",
    root_path="/api/v1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(tasks.router)
app.include_router(auth.router)


@app.get("/")
async def root() -> JSONResponse:
    return {
        "message": "Welcome to N0T3B00K API",
        "docs": "/docs"
    }
