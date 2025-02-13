import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.setup import engine
from api.routers import tasks
from api.models import get_all_bases, users_base, documents_base, tasks_base


logger = logging.getLogger("uvicorn")

async def create_tables():
    try:
        async with engine.begin() as conn:
            logger.info("Successfully connected to the database")
            for base in get_all_bases():
                await base.create_schema(conn)
                logger.info(f"Successfully created schema for '{base.metadata.schema}'")
            for base in get_all_bases():
                for table in base.metadata.sorted_tables:
                    await conn.run_sync(table.create, checkfirst=True)
                    logger.info(f"Successfully created table '{table.name}'")
    except Exception as e:
        logger.error(f"Error creating tables: {e}")


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup", create_tables)

app.include_router(tasks.router)


@app.get("/")
async def root():
    return {"message": "TaskManager"}
