from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from starlette.responses import HTMLResponse
from starlette.middleware.base import BaseHTTPMiddleware
from .routers import upload, analyze
from .config import settings
import uvicorn

app = FastAPI(title="AI Data Analyst", redirect_slashes=False)

# Custom CORS middleware to ensure headers are always added
class ExplicitCORSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "*"
        response.headers["Access-Control-Expose-Headers"] = "*"
        return response

app.add_middleware(ExplicitCORSMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600
)

app.include_router(upload.router)
app.include_router(analyze.router)
app.include_router(analyze.api_router)

@app.get("/")
async def root():
    return {"status": "ok", "message": "AI Data Analyst API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url=app.openapi_url, title=app.title + " - Swagger UI")

@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(openapi_url=app.openapi_url, title=app.title + " - ReDoc")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
