from fastapi import APIRouter, HTTPException, Query
from ..services.dataset_service import load_dataset_to_df, get_user_datasets
from bson import ObjectId
from ..deps import get_mongo_client

router = APIRouter(prefix="/api/analyze", tags=["analyze"])

@router.get("/test")
async def test():
    return {"message": "Analyze router is working"}

@router.post("/")
async def analyze(dataset_id: str = Query(...), question: str = Query(...)):
    print(f"Analyze endpoint called with dataset_id: {dataset_id}, question: {question}")
    try:
        db = get_mongo_client().ai_data_analyst
        dataset_doc = await db.datasets.find_one({"_id": ObjectId(dataset_id)})
        if not dataset_doc:
            raise HTTPException(status_code=404, detail="Dataset not found")
        
        # Load the dataset
        df = await load_dataset_to_df(dataset_doc)
        
        # Try to use the agent service
        try:
            from ..services.agent_service import analyze_question
            result = await analyze_question(df, question)
            return result
        except Exception as agent_error:
            print(f"Agent service failed: {agent_error}")
            # Fallback to simple response if agent fails
            return {
                "final_answer": f"Processed question: {question} for dataset: {dataset_doc.get('filename', 'unknown')}. Dataset has {len(df.columns)} columns: {', '.join(df.columns[:5])}...",
                "chart_image": None,
                "debug": f"Agent service failed: {str(agent_error)}. Showing basic dataset info instead."
            }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
