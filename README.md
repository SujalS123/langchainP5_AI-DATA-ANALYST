# AI Data Analyst

This project implements an AI Data Analyst backend using FastAPI, LangChain, and MongoDB Atlas. It allows users to upload CSV files, authenticate, and then ask natural language queries about their data. The AI agent uses PandasTool for data manipulation and ChartTool for generating visualizations.

## Features

* 
* **CSV Uploads:** Users can upload CSV files, which are stored in MongoDB Atlas GridFS.
* **Natural Language Queries:** Users can ask questions about their uploaded datasets using natural language.
* **AI-Powered Analysis:** A LangChain agent with Gemini (or OpenAI) interprets queries, uses PandasTool for data operations, and optionally ChartTool for visualizations.
* **Structured Responses:** Returns structured JSON with textual insights, step-by-step reasoning, and base64 encoded chart images.
* **Scalable Backend:** Built with FastAPI for high performance and asynchronous operations.
* **MongoDB Atlas:** Utilizes MongoDB for user management and GridFS for efficient file storage.

## Project Structure

```
ai-data-analyst/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── deps.py
│   │   ├── auth.py
│   │   ├── models.py           # pydantic schemas
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── upload.py
│   │   │   ├── analyze.py
│   │   ├── services/
│   │   │   ├── mongo_service.py
│   │   │   ├── dataset_service.py
│   │   │   ├── agent_service.py
│   │   │   ├── tools.py         # PandasTool, ChartTool
│   │   ├── llm/
│   │   │   ├── llm_client.py    # provider adapter (Gemini/OpenAI)
│   │   ├── utils/
│   │   │   ├── base64_utils.py
│   │   │   ├── logging.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── start.sh
├── frontend/ (outline only — React)
├── README.md
```

## Setup and Installation

### 1. Environment Variables

Create a `.env` file in the `ai-data-analyst/` directory with the following content:

```
MONGO_URI=mongodb+srv://<user>:<pw>@cluster0.mongodb.net/ai_data_analyst?retryWrites=true&w=majority
JWT_SECRET=supersecretkey_here_change_me
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
LLM_PROVIDER=GEMINI    # or OPENAI
OPENAI_API_KEY=xxx
GEMINI_API_KEY=xxx
```

* **MONGO_URI**: Your MongoDB Atlas connection string.
* **JWT_SECRET**: A strong secret key for JWT token generation.
* **LLM_PROVIDER**: Specify `GEMINI` or `OPENAI`.
* **OPENAI_API_KEY / GEMINI_API_KEY**: Your respective API keys.

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

### 3. Frontend (Outline)

The frontend is outlined as a React application. It should interact with the backend endpoints as follows:

* **POST `/api/auth/signup`**: Body: `{email, password, display_name}`
* **POST `/api/auth/login`**: Body: `{email, password}` → Returns `{access_token}`
* **POST `/api/files/upload`**: Header: `Authorization: Bearer <token>`, Body: form-data file
* **GET `/api/files/list`**: Header: `Authorization: Bearer <token>`
* **POST `/api/analyze`**: Header: `Authorization: Bearer <token>`, Body JSON: `{dataset_id: "<id>", question: "Which region..."}` → Returns JSON with `"final_answer"`, `"reasoning"`, `"tool_results"`, `"chart_image"`

The frontend should:
* Upload CSV and store `dataset_id`.
* Provide a question input UI.
* Render `final_answer` and `reasoning` as text.
* If `chart_image` is present, display it as `<img src={chart_image} />`.

## Security Considerations

* Ensure `JWT_SECRET` is strong and kept secure.
* Use HTTPS in production environments.
* Implement rate limiting on the `/api/analyze` endpoint to prevent abuse and control LLM costs.
* Validate and limit uploaded file sizes (e.g., 10-50 MB).
* Authorization checks for datasets are based on `datasets.owner_id`.

## Deployment Notes

* Dockerize the backend for easy deployment.
* Use MongoDB Atlas for a production-ready database.
* Securely manage LLM API keys (e.g., Google Cloud Secret Manager).
* Optimize LLM calls by chunking prompts and performing heavy data processing locally with Pandas.

## Testing Strategy

1. Verify file upload and listing functionality, ensuring data is correctly stored in GridFS.
2. Test `dataset_service.load_dataset_to_df` with various CSVs.
3. Manually test PandasTool actions and chart generation to confirm correct output and base64 encoding.
4. Integrate the LLM and iterate on prompt design to ensure reliable JSON plan generation.

## Example Run-through

1. User signs up and logs in, receiving a JWT.
2. User uploads `sales.csv`. The backend stores the file in GridFS and returns a `dataset_id`.
3. User asks: "Which region is declining the fastest and why?"
4. The backend:
   * Loads the dataset into a Pandas DataFrame.
   * Constructs a prompt with column information.
   * The LLM generates a JSON plan (e.g., `group_by`, `correlation`, `plot`).
   * The orchestrator executes the plan using `PandasTool` and `ChartTool`.
   * Returns `final_answer`, `reasoning`, `tool_results`, and `chart_image` (base64).
5. The frontend displays the insights and the generated chart.