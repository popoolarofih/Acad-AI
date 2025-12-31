# Exam System API

## Overview

This is a comprehensive Django-based REST API for an online exam system. It provides a secure platform for students to take exams, submit answers, and receive automated grading feedback. The system supports multiple question types and integrates with AI for intelligent text answer evaluation.

## Features

- **Secure Exam Management**: Create and manage exams with multiple question types (multiple choice and text-based)
- **Automated Grading**: AI-powered grading for text answers using Groq LLM, exact matching for multiple choice
- **User Authentication**: Token-based authentication with session fallback for secure access
- **Role-based Access Control**: Different data visibility for students vs administrators
- **API Documentation**: Interactive Swagger UI and Redoc documentation
- **Database Integration**: PostgreSQL database with Supabase hosting
- **Comprehensive Testing**: Full test coverage including unit tests and integration tests
- **RESTful Design**: Clean API design following REST principles

## Architecture and Design

The application follows Django REST Framework best practices with a modular architecture:

### Project Structure
```
exam_system/
├── api/                    # Main application
│   ├── models.py          # Data models (Exam, Question, Submission)
│   ├── views.py           # API endpoints logic
│   ├── serializers.py     # Data serialization
│   ├── permissions.py     # Custom permissions
│   ├── grading.py         # Grading logic
│   ├── urls.py           # API routing
│   └── tests.py          # Test cases
├── exam_system/           # Django project settings
│   ├── settings.py       # Configuration
│   ├── urls.py           # Main routing
│   └── wsgi.py           # WSGI application
└── requirements.txt      # Dependencies
```

### Key Components

- **Models**: Define the core data entities and relationships
- **Views**: Handle HTTP requests using generic class-based views
- **Serializers**: Convert model instances to/from JSON with role-based field filtering
- **Permissions**: Custom permission classes for fine-grained access control
- **Grading Service**: Separate module handling automated grading logic

## Data Models

### Exam Model
Represents an exam with its metadata and associated questions.

| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Primary key |
| `title` | CharField | Exam title (max 255 chars) |
| `duration` | IntegerField | Duration in minutes |
| `course` | CharField | Associated course name |
| `metadata` | JSONField | Additional exam metadata (optional) |
| `questions` | RelatedManager | Related Question objects |

### Question Model
Represents individual questions within an exam.

| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Primary key |
| `exam` | ForeignKey | Related Exam |
| `question_text` | TextField | The question content |
| `question_type` | CharField | 'multiple_choice' or 'text' |
| `expected_answer` | TextField | Correct answer for grading |

### Submission Model
Represents a student's exam submission.

| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Primary key |
| `student` | ForeignKey | Related User (student) |
| `exam` | ForeignKey | Related Exam |
| `answers` | JSONField | Dictionary of question_id: answer pairs |
| `submitted_at` | DateTimeField | Auto-generated submission timestamp |
| `grade` | FloatField | Calculated grade (0.0 to 1.0 scale) |

## API Endpoints

### Authentication
The API uses token authentication. Include the token in the Authorization header:
```
Authorization: Token <your-token>
```

### Authentication Endpoints

#### User Registration
- **URL**: `POST /api/v1/auth/register/`
- **Description**: Register a new user account
- **Authentication**: Not required
- **Request Body**:
```json
{
  "username": "student1",
  "email": "student@example.com",
  "password": "securepassword123"
}
```
- **Response**: User data with authentication token

#### User Login
- **URL**: `POST /api/v1/auth/login/`
- **Description**: Authenticate user and get token
- **Authentication**: Not required
- **Request Body**:
```json
{
  "username": "student1",
  "password": "securepassword123"
}
```
- **Response**: User data with authentication token

### Exams Endpoints

#### List Exams
- **URL**: `GET /api/v1/exams/`
- **Description**: Retrieve all available exams with filtering and search
- **Authentication**: Required
- **Query Parameters**:
  - `course`: Filter by course name
  - `search`: Search in title and course fields
- **Response**: Paginated list of exams with questions (expected answers hidden for students)

#### Get Exam Details
- **URL**: `GET /api/v1/exams/<id>/`
- **Description**: Retrieve detailed information for a specific exam
- **Authentication**: Required
- **Response**: Single exam object with full details

### Submissions Endpoints

#### Submit Answers
- **URL**: `POST /api/v1/submissions/`
- **Description**: Submit answers for an exam (automatically triggers grading)
- **Authentication**: Required
- **Request Body**:
```json
{
  "exam": 1,
  "answers": {
    "1": "4",
    "2": "This is my answer to the text question"
  }
}
```
- **Response**: Created submission object with grade

#### Get Submission Details
- **URL**: `GET /api/v1/submissions/<id>/`
- **Description**: Retrieve submission details (owner only)
- **Authentication**: Required
- **Permission**: Submission owner only
- **Response**: Submission object with answers and grade

#### List My Submissions
- **URL**: `GET /api/v1/my-submissions/`
- **Description**: Retrieve all submissions for the authenticated user
- **Authentication**: Required
- **Response**: List of user's submissions with grades

### Documentation Endpoints

#### Swagger UI
- **URL**: `GET /swagger/`
- **Description**: Interactive API documentation
- **Authentication**: Not required

#### Redoc
- **URL**: `GET /redoc/`
- **Description**: Alternative API documentation
- **Authentication**: Not required

## Authentication and Permissions

### Authentication Methods
1. **Token Authentication**: Primary method using API tokens
2. **Session Authentication**: Fallback for web interface

### Permission Classes
- **IsAuthenticated**: Default permission requiring user authentication
- **IsOwner**: Custom permission allowing only submission owners to view their submissions

### Data Visibility
- **Students**: Cannot see expected answers in exam questions
- **Administrators**: Have full access to all data including expected answers

## Grading System

The system supports two grading methods based on question type:

### Multiple Choice Questions
- **Method**: Exact string matching
- **Scoring**: 1.0 for correct, 0.0 for incorrect
- **Case Sensitivity**: Exact match required

### Text-Based Questions
- **Method**: AI-powered semantic similarity using Groq LLM
- **Scoring**: Float between 0.0 and 1.0 based on semantic similarity
- **Model**: Uses Groq's language model for intelligent evaluation

### Overall Grade Calculation
- **Formula**: Average of individual question scores
- **Scale**: 0.0 to 1.0 (can be converted to percentage by multiplying by 100)

## Requirements

- Python 3.8+
- Pip package manager
- Supabase account for PostgreSQL database
- Groq account for LLM-based grading

## Installation and Setup

### 1. Clone the Repository
```bash
git clone <repository_url>
cd <repository_directory>
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the project root:
```
DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<name>
GROQ_API_KEY=<your_groq_api_key>
```

### 5. Database Setup
```bash
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```
The API will be available at `http://127.0.0.1:8000/`.

## Testing

### Running Tests
Execute the complete test suite:
```bash
python manage.py test
```

### Test Coverage
The test suite includes:
- **API Endpoint Tests**: Verify all CRUD operations work correctly
- **Authentication Tests**: Ensure proper access control
- **Permission Tests**: Validate role-based access
- **Grading Tests**: Test both multiple choice and text grading logic
- **Security Tests**: Confirm data privacy and access restrictions

### Test Database
Tests use SQLite for isolation and speed, separate from the main PostgreSQL database.

## Deployment

### Production Configuration
1. **Debug Mode**: Set `DEBUG = False` in settings.py
2. **Allowed Hosts**: Configure `ALLOWED_HOSTS` with your domain
3. **Environment Variables**: Use secure environment variables for secrets
4. **Database**: Configure production PostgreSQL database
5. **Static Files**: Set up static file serving (nginx, cloud storage, etc.)
6. **HTTPS**: Enable SSL/TLS encryption
7. **Security Headers**: Configure security middleware

### Example Production Settings
```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}
```

## Contributing

We welcome contributions to improve the Exam System API!

### Development Workflow
1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/your-feature-name`
3. **Write** comprehensive tests for new functionality
4. **Implement** your changes following Django/DRF best practices
5. **Run** the full test suite: `python manage.py test`
6. **Commit** your changes with clear messages
7. **Push** to your fork and create a pull request

### Code Standards
- Follow PEP 8 style guidelines
- Write comprehensive docstrings
- Maintain test coverage above 80%
- Use meaningful variable and function names
- Keep functions small and focused

### Reporting Issues
- Use GitHub issues for bug reports and feature requests
- Provide detailed steps to reproduce bugs
- Include relevant error messages and stack traces
- Specify your environment (OS, Python version, etc.)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Check the API documentation at `/swagger/` or `/redoc/`
- Review the test cases for usage examples
- Create an issue on GitHub for bugs or feature requests
