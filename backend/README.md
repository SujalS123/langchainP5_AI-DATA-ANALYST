# Backend Documentation

## Architecture Overview

The backend is structured into several key components, each serving a specific purpose in the application. Below is an overview of the architecture:

### 1. Configuration
- The [`Settings`](backend/app/config.py:3-11) class in `config.py` manages application settings using Pydantic.

### 2. Dependencies
- The [`get_mongo_client`](backend/app/deps.py:5-9) function in `deps.py` provides a dependency for accessing the MongoDB client.

### 3. LLM Client
- The [`LLMClient`](backend/app/llm/llm_client.py:6-36) class in `llm_client.py` handles interactions with the language model, including initialization and generating responses.

### 4. Routers
- **`analyze.py`**:
  - The [`/analyze`](backend/app/routers/analyze.py:12-41) endpoint analyzes datasets based on user questions.
- **`upload.py`**:
  - The [`/upload`](backend/app/routers/upload.py:7-15) endpoint handles CSV file uploads.
  - The [`/list`](backend/app/routers/upload.py:17-26) endpoint lists uploaded files.

### 5. Services
- **`agent_service.py`**:
  - The [`analyze_question`](backend/app/services/agent_service.py:14-444) function analyzes questions using a DataFrame and interacts with the LLM client.
  - The [`get_dataset_info`](backend/app/services/agent_service.py:101-118) function retrieves dataset information.
  - The [`safe_json_parse`](backend/app/services/agent_service.py:121-133) function safely parses JSON strings.
  - The [`enhance_answer`](backend/app/services/agent_service.py:281-380) function enhances answers with intermediate steps.
- **`dataset_service.py`**:
  - The [`save_dataset`](backend/app/services/dataset_service.py:9-20) function saves datasets to MongoDB GridFS.
  - The [`load_dataset_to_df`](backend/app/services/dataset_service.py:22-52) function loads datasets into DataFrames.
- **`mongo_service.py`**:
  - The [`get_gridfs_bucket`](backend/app/services/mongo_service.py:11-14) function retrieves the GridFS bucket.
  - The [`upload_file_to_gridfs`](backend/app/services/mongo_service.py:16-20) function uploads files to GridFS.
  - The [`download_file_from_gridfs`](backend/app/services/mongo_service.py:22-27) function downloads files from GridFS.
  - The [`MongoService`](backend/app/services/mongo_service.py:29-46) class manages MongoDB operations, including user management.
- **`query_parser.py`**:
  - The [`parse_chart_query`](backend/app/services/query_parser.py:4-117) function parses chart queries based on available columns.
  - The [`should_use_direct_parsing`](backend/app/services/query_parser.py:119-160) function determines if direct parsing is needed for a question.
- **`tools.py`**:
  - The [`PandasTool`](backend/app/services/tools.py:11-50) class provides utility functions for DataFrame operations.
  - Chart preparation functions include [`df_to_base64_png_plot`](backend/app/services/tools.py:53-66), [`plot_bar_top_n`](backend/app/services/tools.py:69-74), [`plot_line_time`](backend/app/services/tools.py:76-81), [`prepare_bar_chart_data`](backend/app/services/tools.py:84-164), [`prepare_line_chart_data`](backend/app/services/tools.py:166-229), and [`prepare_pie_chart_data`](backend/app/services/tools.py:231-296).

### 6. Utilities
- The `utils` directory contains helper scripts or configurations, such as logging and base64 utilities.

## Code Documentation

### Configuration (`config.py`)
- **`Settings` Class**: Manages application settings using Pydantic's [`BaseSettings`](backend/app/config.py:1-13).

### Dependencies (`deps.py`)
- **`get_mongo_client` Function**: Provides a dependency for accessing the MongoDB client using [`AsyncIOMotorClient`](backend/app/deps.py:5-9).

### LLM Client (`llm_client.py`)
- **`LLMClient` Class**:
  - **Purpose**: Interacts with a language model to generate responses based on prompts.
  - **Key Methods**:
    - [`__init__`](backend/app/llm/llm_client.py:7-20): Initializes the client with configuration settings.
    - [`chat`](backend/app/llm/llm_client.py:23-36): Sends a prompt to the language model and returns the generated response.

### Routers

- **`analyze.py`**:
  - **`/analyze` Endpoint**:
    - **Purpose**: Analyzes a dataset based on a user's question.
    - **Parameters**:
      - `dataset_id` (Query): The ID of the dataset to analyze.
      - `question` (Query): The question to analyze.
    - **Response**: Returns the analysis result based on the dataset and question.
    - **Implementation**: Uses the [`analyze_question`](backend/app/services/agent_service.py:14-444) function to process the request.

- **`upload.py`**:
  - **`/upload` Endpoint**:
    - **Purpose**: Handles CSV file uploads.
    - **Parameters**:
      - `file` (FormData): The CSV file to upload.
    - **Response**: Confirms the file upload and returns the dataset ID.
    - **Implementation**: Saves the file to MongoDB GridFS using the [`save_dataset`](backend/app/services/dataset_service.py:9-20) function.
  - **`/list` Endpoint**:
    - **Purpose**: Lists all uploaded files.
    - **Response**: Returns a list of uploaded files with their metadata.
    - **Implementation**: Retrieves the list of files from MongoDB GridFS.

### Services

- **`agent_service.py`**:
  - **`analyze_question` Function**:
    - **Purpose**: Analyzes a question using a DataFrame and interacts with the LLM client.
    - **Implementation**:
      - Parses the question and dataset.
      - Uses the LLM client to generate a response.
      - Enhances the response with intermediate steps.
  - **`get_dataset_info` Function**:
    - **Purpose**: Retrieves dataset information, such as columns.
    - **Implementation**: Queries the dataset and returns relevant information.
  - **`safe_json_parse` Function**:
    - **Purpose**: Safely parses JSON strings, handling potential issues with extra quotes from the LLM.
  - **`enhance_answer` Function**:
    - **Purpose**: Enhances the final answer with intermediate steps for better clarity.

- **`dataset_service.py`**:
  - **`save_dataset` Function**:
    - **Purpose**: Saves a dataset to MongoDB GridFS.
    - **Implementation**:
      - Accepts file bytes and metadata.
      - Uploads the file to GridFS using [`upload_file_to_gridfs`](backend/app/services/mongo_service.py:16-20).
  - **`load_dataset_to_df` Function**:
    - **Purpose**: Loads a dataset from MongoDB GridFS into a DataFrame.
    - **Implementation**:
      - Downloads the file from GridFS using [`download_file_from_gridfs`](backend/app/services/mongo_service.py:22-27).
      - Converts the file to a DataFrame.

- **`mongo_service.py`**:
  - **`get_gridfs_bucket` Function**:
    - **Purpose**: Retrieves the GridFS bucket for file storage.
  - **`upload_file_to_gridfs` Function**:
    - **Purpose**: Uploads a file to GridFS.
  - **`download_file_from_gridfs` Function**:
    - **Purpose**: Downloads a file from GridFS.
  - **`MongoService` Class**:
    - **Purpose**: Manages MongoDB operations, including user management.
    - **Key Methods**:
      - [`get_user_by_id`](backend/app/services/mongo_service.py:33-36): Retrieves a user by ID.
      - [`update_user`](backend/app/services/mongo_service.py:38-46): Updates user data.

- **`query_parser.py`**:
  - **`parse_chart_query` Function**:
    - **Purpose**: Parses a chart query based on available columns.
    - **Implementation**: Analyzes the query and returns the parsed result.
  - **`should_use_direct_parsing` Function**:
    - **Purpose**: Determines if direct parsing should be used for a question.

- **`tools.py`**:
  - **`PandasTool` Class**:
    - **Purpose**: Provides utility functions for DataFrame operations.
    - **Key Methods**:
      - [`describe`](backend/app/services/tools.py:21-26): Generates descriptive statistics for a DataFrame.
      - [`group_agg`](backend/app/services/tools.py:28-34): Groups and aggregates data.
      - [`filter`](backend/app/services/tools.py:36-41): Filters data based on an expression.
      - [`correlation`](backend/app/services/tools.py:47-50): Calculates correlation between columns.
  - **Chart Preparation Functions**:
    - [`df_to_base64_png_plot`](backend/app/services/tools.py:53-66): Converts a DataFrame to a base64-encoded PNG plot.
    - [`plot_bar_top_n`](backend/app/services/tools.py:69-74): Plots a bar chart for the top N values.
    - [`plot_line_time`](backend/app/services/tools.py:76-81): Plots a line chart over time.
    - [`prepare_bar_chart_data`](backend/app/services/tools.py:84-164): Prepares data for a bar chart.
    - [`prepare_line_chart_data`](backend/app/services/tools.py:166-229): Prepares data for a line chart.
    - [`prepare_pie_chart_data`](backend/app/services/tools.py:231-296): Prepares data for a pie chart.

### Utilities (`utils`)
- The `utils` directory contains helper scripts or configurations, such as logging and base64 utilities.

## Endpoint Documentation

### 1. `/analyze` (POST)
- **Purpose**: Analyzes a dataset based on a user's question.
- **Parameters**:
  - `dataset_id` (Query): The ID of the dataset to analyze.
  - `question` (Query): The question to analyze.
- **Response**: Returns the analysis result based on the dataset and question.

### 2. `/upload` (POST)
- **Purpose**: Handles CSV file uploads.
- **Parameters**:
  - `file` (FormData): The CSV file to upload.
- **Response**: Confirms the file upload and returns the dataset ID.

### 3. `/list` (GET)
- **Purpose**: Lists all uploaded files.
- **Response**: Returns a list of uploaded files with their metadata.

## Detailed LangChain Logic

### 1. **LangChain Client (`llm_client.py`)**

The [`LLMClient`](backend/app/llm/llm_client.py:6-36) class is the core component for interacting with the language model. It provides the following functionalities:

- **Initialization (`__init__` Method)**:
  - The [`__init__`](backend/app/llm/llm_client.py:7-20) method initializes the client with configuration settings, such as API keys or model parameters.
  - It sets up the client to communicate with the language model API.

- **Generating Responses (`chat` Method)**:
  - The [`chat`](backend/app/llm/llm_client.py:23-36) method sends a prompt to the language model and returns the generated response.
  - It accepts parameters like `prompt`, `temperature`, and `max_tokens` to customize the response generation.

### 2. **Agent Service (`agent_service.py`)**

The [`agent_service.py`](backend/app/services/agent_service.py) file contains the logic for processing user queries using LangChain. Key functions include:

- **`analyze_question` Function**:
  - **Purpose**: Analyzes a question using a DataFrame and interacts with the LLM client.
  - **Implementation**:
    - Parses the question and dataset.
    - Uses the LLM client to generate a response.
    - Enhances the response with intermediate steps for better clarity.

- **`get_dataset_info` Function**:
  - **Purpose**: Retrieves dataset information, such as columns.
  - **Implementation**: Queries the dataset and returns relevant information.

- **`safe_json_parse` Function**:
  - **Purpose**: Safely parses JSON strings, handling potential issues with extra quotes from the LLM.

- **`enhance_answer` Function**:
  - **Purpose**: Enhances the final answer with intermediate steps for better clarity.

### 3. **Query Parser (`query_parser.py`)**

The [`query_parser.py`](backend/app/services/query_parser.py) file contains functions to parse and process user queries:

- **`parse_chart_query` Function**:
  - **Purpose**: Parses a chart query based on available columns.
  - **Implementation**: Analyzes the query and returns the parsed result.

- **`should_use_direct_parsing` Function**:
  - **Purpose**: Determines if direct parsing should be used for a question.

### 4. **Tools (`tools.py`)**

The [`tools.py`](backend/app/services/tools.py) file provides utility functions for working with DataFrames and generating charts:

- **`PandasTool` Class**:
  - **Purpose**: Provides utility functions for DataFrame operations.
  - **Key Methods**:
    - [`describe`](backend/app/services/tools.py:21-26): Generates descriptive statistics for a DataFrame.
    - [`group_agg`](backend/app/services/tools.py:28-34): Groups and aggregates data.
    - [`filter`](backend/app/services/tools.py:36-41): Filters data based on an expression.
    - [`correlation`](backend/app/services/tools.py:47-50): Calculates correlation between columns.

- **Chart Preparation Functions**:
  - [`df_to_base64_png_plot`](backend/app/services/tools.py:53-66): Converts a DataFrame to a base64-encoded PNG plot.
  - [`plot_bar_top_n`](backend/app/services/tools.py:69-74): Plots a bar chart for the top N values.
  - [`plot_line_time`](backend/app/services/tools.py:76-81): Plots a line chart over time.
  - [`prepare_bar_chart_data`](backend/app/services/tools.py:84-164): Prepares data for a bar chart.
  - [`prepare_line_chart_data`](backend/app/services/tools.py:166-229): Prepares data for a line chart.
  - [`prepare_pie_chart_data`](backend/app/services/tools.py:231-296): Prepares data for a pie chart.

### 5. **Integration with Routers**

The LangChain logic is integrated into the backend routers to handle API requests:

- **`analyze.py`**:
  - The [`/analyze`](backend/app/routers/analyze.py:12-41) endpoint uses the [`analyze_question`](backend/app/services/agent_service.py:14-444) function to process user queries and generate responses.

- **`upload.py`**:
  - The [`/upload`](backend/app/routers/upload.py:7-15) endpoint handles file uploads, which are then processed using LangChain for analysis.