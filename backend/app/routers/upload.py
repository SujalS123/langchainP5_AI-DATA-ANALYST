from fastapi import APIRouter, UploadFile, File, HTTPException
from ..services import dataset_service
from bson import ObjectId

router = APIRouter(prefix="/files", tags=["files"])

@router.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV allowed")
    content = await file.read()
    # Use a default user ID since authentication is removed
    default_user_id = "default_user"
    doc = await dataset_service.save_dataset(default_user_id, content, file.filename)
    return {"status":"ok", "dataset_id": str(doc["_id"]), "filename": file.filename}

@router.get("/list")
async def list_files():
    # Use a default user ID since authentication is removed
    default_user_id = "default_user"
    ds = await dataset_service.get_user_datasets(default_user_id)
    # convert objectids
    for d in ds:
        d["_id"] = str(d["_id"])
        d["file_id"] = str(d["file_id"])
    return {"datasets": ds}
