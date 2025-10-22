from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from ..services import dataset_service
from bson import ObjectId

router = APIRouter(prefix="/files", tags=["files"])

@router.options("/upload")
async def options_upload():
    return JSONResponse(
        status_code=200,
        content={"message": "OK"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Max-Age": "600"
        }
    )

@router.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV allowed")
    content = await file.read()
    # Use a default user ID since authentication is removed
    default_user_id = "default_user"
    doc = await dataset_service.save_dataset(default_user_id, content, file.filename)
    return JSONResponse(
        status_code=200,
        content={"status":"ok", "dataset_id": str(doc["_id"]), "filename": file.filename},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*"
        }
    )

@router.options("/list")
async def options_list():
    return JSONResponse(
        status_code=200,
        content={"message": "OK"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Max-Age": "600"
        }
    )

@router.get("/list")
async def list_files():
    # Use a default user ID since authentication is removed
    default_user_id = "default_user"
    ds = await dataset_service.get_user_datasets(default_user_id)
    # convert objectids
    for d in ds:
        d["_id"] = str(d["_id"])
        d["file_id"] = str(d["file_id"])
    return JSONResponse(
        status_code=200,
        content={"datasets": ds},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "*"
        }
    )
