from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

_client = None
def get_mongo_client() -> AsyncIOMotorClient:
    global _client
    if not _client:
        _client = AsyncIOMotorClient(settings.MONGO_URI)
    return _client
