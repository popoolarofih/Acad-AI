# Exam System API
This is a Django-based REST API for an online exam system. It allows students to take exams, submit answers securely, and receive automated grading feedback.

## Features

-   **Database Modeling:** Relational database schema for exams, questions, and submissions using Supabase (PostgreSQL).
-   **Secure Submission Endpoint:** Secure API endpoint for students to submit exam answers, with authentication and permissions to ensure data privacy.
-   **Automated Grading:** Automated grading mechanism using a mock service and integration with the Groq LLM for text-based answers.
-   **API Documentation:** Comprehensive API documentation using Swagger and Redoc.

## Requirements

-   Python 3.8+
-   Pip
-   A Supabase account for the PostgreSQL database.
-   A Groq account for the LLM-based grading.

## Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create a `.env` file:**
    Create a file named `.env` in the project root and add your Supabase database URL and Groq API key:
    ```
    DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<name>
    GROQ_API_KEY=<your_groq_api_key>
    ```

5.  **Run database migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The API will be available at `http://127.0.0.1:8000/`.

## API Endpoints

-   **List Exams:** `GET /api/exams/`
-   **Exam Details:** `GET /api/exams/<id>/`
-   **Submit Answers:** `POST /api/submissions/`
-   **Submission Details:** `GET /api/submissions/<id>/`

### API Documentation

-   **Swagger UI:** `http://127.0.0.1:8000/swagger/`
-   **Redoc:** `http://127.0.0.1:8000/redoc/`

## Running Tests

To run the test suite, use the following command:
```bash
python manage.py test
```
