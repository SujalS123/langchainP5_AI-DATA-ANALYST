from dotenv import load_dotenv
from fastapi import FastAPI
from app.routers import upload, analyze

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

app.include_router(upload.router)
app.include_router(analyze.router)

def main():
    print("Hello from backend!")

if __name__ == "__main__":
    main()
