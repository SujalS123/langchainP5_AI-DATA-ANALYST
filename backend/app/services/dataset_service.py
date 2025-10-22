from ..services.mongo_service import upload_file_to_gridfs, download_file_from_gridfs, get_gridfs_bucket
from ..deps import get_mongo_client
from bson import ObjectId
import pandas as pd
import io

db = get_mongo_client().ai_data_analyst

async def save_dataset(user_id: str, file_bytes: bytes, filename: str):
    metadata = {"owner_id": user_id, "filename": filename}
    file_id = await upload_file_to_gridfs(file_bytes, filename, metadata)
    doc = {
        "owner_id": user_id,
        "filename": filename,
        "file_id": file_id,
        "created_at": pd.Timestamp.utcnow().to_pydatetime()
    }
    res = await db.datasets.insert_one(doc)
    doc["_id"] = res.inserted_id
    return doc

async def load_dataset_to_df(dataset_doc):
    # dataset_doc contains file_id
    file_id = dataset_doc["file_id"]
    content = await download_file_from_gridfs(file_id)
    # read bytes into pandas
    try:
        # Try different encodings
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        df = None
        last_error = None
        
        for encoding in encodings:
            try:
                decoded_content = content.decode(encoding)
                df = pd.read_csv(io.StringIO(decoded_content))
                break
            except UnicodeDecodeError as e:
                last_error = e
                continue
            except Exception as e:
                # If it's not a Unicode error, re-raise it
                raise e
        
        if df is None:
            raise last_error or Exception("Failed to decode CSV with any encoding")
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise e
    return df

async def get_user_datasets(user_id: str):
    cursor = db.datasets.find({"owner_id": user_id})
    return [doc async for doc in cursor]
