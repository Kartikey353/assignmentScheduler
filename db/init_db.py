import os
from typing import Dict

from dotenv import load_dotenv 
from beanie import init_beanie
from utils.logger import get_logger
from motor.motor_asyncio import AsyncIOMotorClient
from db.tables.user import User
from db.tables.target import Target
from db.tables.schedule import Schedule
from db.tables.history import ExecutionHistory


load_dotenv()
logger = get_logger("DatabaseInit")
db: Dict[str, any] = {}



async def initialize_mongodb():
    MONGO_URL = os.getenv("MONGO_URL")
    if not MONGO_URL:
        logger.error("MONGO_URL is not set in .env file")
        raise RuntimeError("MONGO_URL missing from environment variables")

    db["mongo"] = AsyncIOMotorClient(MONGO_URL)
    await init_beanie(database=db["mongo"].mydb, document_models=[Target, Schedule, User, ExecutionHistory])
    namespace = {
        "User": User,
        "Target": Target,
        "Schedule": Schedule,
        "ExecutionHistory": ExecutionHistory
    }
    User.model_rebuild(_types_namespace=namespace)
    Target.model_rebuild(_types_namespace=namespace)
    Schedule.model_rebuild(_types_namespace=namespace)
    ExecutionHistory.model_rebuild(_types_namespace=namespace)
    logger.info("MongoDB initialized successfully")



async def initialize_databases():
    await initialize_mongodb()

def get_db() -> Dict[str, any]:
    return db