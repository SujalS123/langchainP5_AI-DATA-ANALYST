from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket
from ..config import settings
from ..deps import get_mongo_client
from bson import ObjectId
import aiofiles
import io

def get_db():
    return get_mongo_client().ai_data_analyst

def get_gridfs_bucket():
    client: AsyncIOMotorClient = get_mongo_client()
    db = client.ai_data_analyst
    return AsyncIOMotorGridFSBucket(db)

async def upload_file_to_gridfs(file_bytes: bytes, filename: str, metadata: dict):
    bucket = get_gridfs_bucket()
    stream = io.BytesIO(file_bytes)
    file_id = await bucket.upload_from_stream(filename, stream, metadata=metadata)
    return file_id  # ObjectId

async def download_file_from_gridfs(file_id):
    bucket = get_gridfs_bucket()
    out = io.BytesIO()
    await bucket.download_to_stream(file_id, out)
    out.seek(0)
    return out.read()

class MongoService:
    def __init__(self, mongo_client: AsyncIOMotorClient):
        self.client = mongo_client

    async def get_user_by_id(self, user_id: str):
        db = self.client.ai_data_analyst
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        return user

    async def update_user(self, user_id: str, update_data: dict):
        db = self.client.ai_data_analyst
        result = await db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        if result.modified_count == 0:
            return None
        return await self.get_user_by_id(user_id)