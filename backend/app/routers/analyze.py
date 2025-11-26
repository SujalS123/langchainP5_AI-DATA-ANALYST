from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from ..services.dataset_service import load_dataset_to_df, get_user_datasets
from bson import ObjectId
from ..deps import get_mongo_client

# Create routers for both /analyze and /api/analyze
router = APIRouter(prefix="/analyze", tags=["analyze"])
api_router = APIRouter(prefix="/api/analyze", tags=["analyze"])

# Add route without trailing slash to prevent 307 redirects
@router.post("")
@router.get("")
async def analyze_no_slash(dataset_id: str = Query(...), question: str = Query(...)):
    return await analyze(dataset_id, question)

@router.get("/test")
async def test():
    return {"message": "Analyze router is working"}

@router.post("/")
@router.get("/")
async def analyze(dataset_id: str = Query(...), question: str = Query(...)):
    print(f"Analyze endpoint called with dataset_id: {dataset_id}, question: {question}")
    try:
        db = get_mongo_client().ai_data_analyst
        dataset_doc = await db.datasets.find_one({"_id": ObjectId(dataset_id)})
        if not dataset_doc:
            raise HTTPException(status_code=404, detail="Dataset not found")
        
        df = await load_dataset_to_df(dataset_doc)
        
        try:
            from ..services.agent_service import analyze_question
            result = await analyze_question(df, question)
            return result
        except Exception as agent_error:
            error_msg = str(agent_error)
            print(f"Agent service failed: {agent_error}")
            
            # Check for quota errors
            if "429" in error_msg or "quota" in error_msg.lower() or "ResourceExhausted" in error_msg:
                return {
                    "final_answer": "⚠️ API Quota Exceeded\n\nThe Gemini API has reached its quota limit. This typically resets daily for free tier accounts.\n\nSolutions:\n• Wait for the quota to reset (usually 24 hours)\n• Use a different API key\n• Upgrade your Gemini API plan\n\nDataset Info:\n" + f"• File: {dataset_doc.get('filename', 'unknown')}\n• Columns: {', '.join(df.columns[:10])}{'...' if len(df.columns) > 10 else ''}\n• Rows: {len(df)}",
                    "error": "quota_exceeded",
                    "debug": "Gemini API quota exceeded"
                }
            
            return {
                "final_answer": f"Processed question: {question} for dataset: {dataset_doc.get('filename', 'unknown')}. Dataset has {len(df.columns)} columns: {', '.join(df.columns[:5])}...",
                "chart_image": None,
                "debug": f"Agent service failed: {str(agent_error)}. Showing basic dataset info instead."
            }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@api_router.get("/test")
async def api_test():
    return {"message": "API Analyze router is working"}

@api_router.post("/")
@api_router.get("/")
async def api_analyze(dataset_id: str = Query(...), question: str = Query(...)):
    print(f"API Analyze endpoint called with dataset_id: {dataset_id}, question: {question}")
    return await analyze(dataset_id, question)
