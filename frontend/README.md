# Frontend Documentation

## Architecture Overview

The frontend is structured into several key components and pages, each serving a specific purpose in the application. Below is an overview of the architecture:

### 1. Components
- **`ChartRenderer.jsx`**:
  - **Purpose**: Renders charts based on a provided specification.
  - **Props**:
    - `chartSpecification`: The specification for the chart to render.
    - `className`: Optional CSS class name for styling.
  - **Functionality**:
    - Defines default chart options, including plugins (e.g., title, tooltip) and scales (e.g., x, y).
    - Merges default options with the provided chart specification.
    - Renders the chart using a charting library (e.g., Chart.js).

- **`Layout.jsx`**:
  - **Purpose**: Provides a layout structure for the application.
  - **Props**:
    - `children`: The content to be rendered inside the layout.
  - **Functionality**:
    - Defines the structure of the layout, including headers, footers, and main content areas.
    - Renders the children components within the layout.

- **`UploadPage.jsx`**:
  - **Purpose**: Provides a page for uploading files.
  - **Functionality**:
    - Includes a form for users to upload files.
    - Handles file uploads and displays upload status or errors.

### 2. Pages
- **`AnalyzePage.jsx`**:
  - **Purpose**: Allows users to analyze datasets.
  - **Functionality**:
    - Fetches available datasets using the [`fetchDatasets`](frontend/src/pages/AnalyzePage.jsx:14-33) function.
    - Handles analysis requests using the [`handleAnalyze`](frontend/src/pages/AnalyzePage.jsx:38-68) function.
    - Sends analysis requests to the backend API.

- **`DashboardPage.jsx`**:
  - **Purpose**: Provides a dashboard for managing datasets.
  - **Functionality**:
    - Fetches datasets using the [`fetchDatasets`](frontend/src/pages/DashboardPage.jsx:10-24) function.
    - Displays dataset information and management options.

- **`HomePage.jsx`**:
  - **Purpose**: The main home page of the application.
  - **Functionality**:
    - Renders the main content of the home page.

### 3. Context
- The `context` directory does not exist or cannot be accessed. Context files may be located elsewhere or not present in the project.

### 4. API
- The `api` directory likely contains utility scripts or configurations for API interactions.

## Code Documentation

### Components

- **`ChartRenderer.jsx`**:
  - **Purpose**: Renders charts based on a provided specification.
  - **Props**:
    - `chartSpecification`: The specification for the chart to render.
    - `className`: Optional CSS class name for styling.
  - **Functionality**:
    - Defines default chart options, including plugins (e.g., title, tooltip) and scales (e.g., x, y).
    - Merges default options with the provided chart specification.
    - Renders the chart using a charting library (e.g., Chart.js).

- **`Layout.jsx`**:
  - **Purpose**: Provides a layout structure for the application.
  - **Props**:
    - `children`: The content to be rendered inside the layout.
  - **Functionality**:
    - Defines the structure of the layout, including headers, footers, and main content areas.
    - Renders the children components within the layout.

- **`UploadPage.jsx`**:
  - **Purpose**: Provides a page for uploading files.
  - **Functionality**:
    - Includes a form for users to upload files.
    - Handles file uploads and displays upload status or errors.

### Pages

- **`AnalyzePage.jsx`**:
  - **Purpose**: Allows users to analyze datasets.
  - **Functionality**:
    - Fetches available datasets using the [`fetchDatasets`](frontend/src/pages/AnalyzePage.jsx:14-33) function.
    - Handles analysis requests using the [`handleAnalyze`](frontend/src/pages/AnalyzePage.jsx:38-68) function.
    - Sends analysis requests to the backend API.

- **`DashboardPage.jsx`**:
  - **Purpose**: Provides a dashboard for managing datasets.
  - **Functionality**:
    - Fetches datasets using the [`fetchDatasets`](frontend/src/pages/DashboardPage.jsx:10-24) function.
    - Displays dataset information and management options.

- **`HomePage.jsx`**:
  - **Purpose**: The main home page of the application.
  - **Functionality**:
    - Renders the main content of the home page.

## Components and Pages Documentation

### Components

- **`ChartRenderer.jsx`**:
  - **Purpose**: Renders charts based on a provided specification.
  - **Props**:
    - `chartSpecification`: The specification for the chart to render.
    - `className`: Optional CSS class name for styling.
  - **Functionality**:
    - Defines default chart options, including plugins (e.g., title, tooltip) and scales (e.g., x, y).
    - Merges default options with the provided chart specification.
    - Renders the chart using a charting library (e.g., Chart.js).

- **`Layout.jsx`**:
  - **Purpose**: Provides a layout structure for the application.
  - **Props**:
    - `children`: The content to be rendered inside the layout.
  - **Functionality**:
    - Defines the structure of the layout, including headers, footers, and main content areas.
    - Renders the children components within the layout.

- **`UploadPage.jsx`**:
  - **Purpose**: Provides a page for uploading files.
  - **Functionality**:
    - Includes a form for users to upload files.
    - Handles file uploads and displays upload status or errors.

### Pages

- **`AnalyzePage.jsx`**:
  - **Purpose**: Allows users to analyze datasets.
  - **Functionality**:
    - Fetches available datasets using the [`fetchDatasets`](frontend/src/pages/AnalyzePage.jsx:14-33) function.
    - Handles analysis requests using the [`handleAnalyze`](frontend/src/pages/AnalyzePage.jsx:38-68) function.
    - Sends analysis requests to the backend API.

- **`DashboardPage.jsx`**:
  - **Purpose**: Provides a dashboard for managing datasets.
  - **Functionality**:
    - Fetches datasets using the [`fetchDatasets`](frontend/src/pages/DashboardPage.jsx:10-24) function.
    - Displays dataset information and management options.

- **`HomePage.jsx`**:
  - **Purpose**: The main home page of the application.
  - **Functionality**:
    - Renders the main content of the home page.
