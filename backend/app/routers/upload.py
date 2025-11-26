from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from ..services import dataset_service
from bson import ObjectId

router = APIRouter(prefix="/files", tags=["files"])

@router.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV allowed")
    content = await file.read()
    default_user_id = "default_user"
    doc = await dataset_service.save_dataset(default_user_id, content, file.filename)
    return {"status":"ok", "dataset_id": str(doc["_id"]), "filename": file.filename}

@router.get("/list")
async def list_files():
    default_user_id = "default_user"
    ds = await dataset_service.get_user_datasets(default_user_id)
    serializable_datasets = []
    for d in ds:
        serializable_doc = {}
        for key, value in d.items():
            if key == "_id" or key == "file_id":
                serializable_doc[key] = str(value)
            elif hasattr(value, "isoformat"):
                serializable_doc[key] = value.isoformat()
            else:
                serializable_doc[key] = value
        serializable_datasets.append(serializable_doc)
    return {"datasets": serializable_datasets}
