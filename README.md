# AI Data Analyst

This project implements an AI Data Analyst backend using FastAPI, LangChain, and MongoDB Atlas. It allows users to upload CSV files and ask natural language queries about their data. The AI agent uses PandasTool for data manipulation and ChartTool for generating visualizations.

## Features

* **CSV Uploads:** Users can upload CSV files, which are stored in MongoDB Atlas GridFS.
* **Natural Language Queries:** Users can ask questions about their uploaded datasets using natural language.
* **AI-Powered Analysis:** A LangChain agent with Gemini interprets queries and uses PandasTool for data operations.
* **Structured Responses:** Returns structured JSON with textual insights and analysis results.
* **Scalable Backend:** Built with FastAPI for high performance and asynchronous operations.
* **MongoDB Atlas:** Utilizes MongoDB for dataset storage and GridFS for efficient file storage.

## Project Structure

```
ai-data-analyst/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── deps.py
│   │   ├── routers/
│   │   │   ├── upload.py
│   │   │   ├── analyze.py
│   │   ├── services/
│   │   │   ├── dataset_service.py
│   │   │   ├── agent_service.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── start.sh
├── frontend/
├── README.md
```

## Setup and Installation

### 1. Environment Variables

Create a `.env` file in the `backend/` directory with the following content:

```
MONGO_URI=mongodb+srv://<user>:<pw>@cluster0.mongodb.net/ai_data_analyst?retryWrites=true&w=majority
LLM_PROVIDER=GEMINI
GEMINI_API_KEY=your_gemini_api_key_here
```

* **MONGO_URI**: Your MongoDB Atlas connection string.
* **LLM_PROVIDER**: Set to `GEMINI`.
* **GEMINI_API_KEY**: Your Google Gemini API key.

### 2. Backend Setup

Navigate to the `backend/` directory:

```bash
cd backend
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the FastAPI application:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Alternatively, you can use Docker:

```bash
docker build -t ai-data-analyst-backend .
docker run -p 8000:8000 ai-data-analyst-backend
```

### 3. Frontend

The frontend is a React application deployed on Vercel. It interacts with the backend endpoints:

* **POST `/files/upload`**: Upload CSV file (multipart/form-data)
* **GET `/files/list`**: Get list of uploaded datasets
* **POST `/analyze`**: Query parameters: `dataset_id` and `question` → Returns JSON with `"final_answer"` and analysis results

The frontend:
* Uploads CSV files and displays the list of datasets
* Provides a question input interface
* Displays analysis results and insights

## Deployment

* **Backend**: Deployed on Render using Docker
* **Frontend**: Deployed on Vercel
* **Database**: MongoDB Atlas
* Uses environment variables for configuration
* CORS enabled for cross-origin requests

## API Endpoints

* `GET /` - Health check
* `GET /health` - Health status
* `POST /files/upload` - Upload CSV file
* `GET /files/list` - List all uploaded datasets
* `POST /analyze?dataset_id=<id>&question=<query>` - Analyze dataset with natural language query
* `GET /analyze?dataset_id=<id>&question=<query>` - Alternative GET method for analysis

## Example Usage

1. Upload a CSV file using the frontend interface
2. Select the uploaded dataset from the list
3. Ask a question like "What are the top 10 customers by sales?"
4. The backend:
   * Loads the dataset into a Pandas DataFrame
   * Uses Gemini LLM to interpret the query
   * Executes data analysis using PandasTool
   * Returns structured insights
5. The frontend displays the analysis results