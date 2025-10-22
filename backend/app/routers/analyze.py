from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from ..services.dataset_service import load_dataset_to_df, get_user_datasets
from bson import ObjectId
from ..deps import get_mongo_client

router = APIRouter(prefix="/analyze", tags=["analyze"])

@router.options("/test")
async def options_test():
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

@router.get("/test")
async def test():
    return JSONResponse(
        status_code=200,
        content={"message": "Analyze router is working"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "*"
        }
    )

@router.options("/")
async def options_analyze():
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
            return JSONResponse(
                status_code=200,
                content=result,
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "POST, OPTIONS",
                    "Access-Control-Allow-Headers": "*"
                }
            )
        except Exception as agent_error:
            print(f"Agent service failed: {agent_error}")
            # Fallback to simple response if agent fails
            fallback_result = {
                "final_answer": f"Processed question: {question} for dataset: {dataset_doc.get('filename', 'unknown')}. Dataset has {len(df.columns)} columns: {', '.join(df.columns[:5])}...",
                "chart_image": None,
                "debug": f"Agent service failed: {str(agent_error)}. Showing basic dataset info instead."
            }
            return JSONResponse(
                status_code=200,
                content=fallback_result,
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "POST, OPTIONS",
                    "Access-Control-Allow-Headers": "*"
                }
            )
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        error_response = {"error": f"Analysis failed: {str(e)}"}
        return JSONResponse(
            status_code=500,
            content=error_response,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "*"
            }
        )
