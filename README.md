# AI Job Tracker

A Django application for organizing job applications and resumes, with AI-assisted analysis planned for a future phase.

## Core Features

- **Organization**: Centralizing job applications so candidates don't lose track of statuses, dates, and deadlines across different portals.
- **Optimization (The AI factor)**: Using AI (like LLMs) to match a resume against a specific job description, generate tailored cover letters, or extract missing keywords.
- **Analytics**: Providing data on application success rates to help the user figure out which roles or industries are yielding the most interviews.

## Current Progress

- [x] Django project initialized
- [x] User registration and login routes added
- [x] Authenticated dashboard created
- [x] Job application model created
- [x] Create, list, detail, edit, and delete job application flows added
- [x] Per-user access filtering added to job views
- [x] Resume PDF upload and management workflow
- [x] PDF text extraction with PyMuPDF
- [x] AI job and resume analysis workflow
- [ ] Celery tasks for background analysis
- [ ] Automated test coverage for the main user flows
- [ ] Production deployment configuration

## Features

- User accounts with registration and Django authentication
- Dashboard counters for applications, interviews, and selected roles
- Job application tracking with these statuses:
	- Saved
	- Applied
	- Assessment
	- Interview
	- Rejected
	- Selected
- Job descriptions, URLs, dates, and company or position details
- Resume PDF upload, download, deletion, and extracted text viewing
- Per-user ownership checks for job applications and resumes

## Planned Features

- AI analysis of job descriptions and resumes
- Background processing through Celery and Redis
- Broader automated test coverage

## Technology Stack

- Python 3.10 in Docker; Python 3.12 is used by the current local environment
- Django 5.2
- Django REST Framework 3.18
- PyMuPDF for PDF text extraction
- SQLite for the current local development configuration
- PostgreSQL 16, Redis 7, Celery, and Nginx available through Docker Compose

## Project Structure

```text
ai_job_tracker/
├── backend/
│   ├── apps/
│   │   ├── ai_analysis/    # Planned AI analysis domain
│   │   ├── jobs/           # Job application tracking and dashboard
│   │   ├── resumes/        # Resume upload and PDF text extraction
│   │   └── users/          # Registration and user features
│   ├── config/             # Django project configuration
│   ├── templates/          # HTML templates
│   ├── static/             # CSS and JavaScript
│   ├── manage.py
│   └── requirements.txt
├── docker/                 # Docker build configuration
├── nginx/                  # Reverse proxy configuration
├── tests/                  # Project-level tests
├── docker-compose.yml
└── README.md
```

## Local Setup

### 1. Create and activate a virtual environment

From the `backend` directory:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Configure environment variables

The current local settings use SQLite. Docker Compose expects a root `.env` file containing `POSTGRES_DB`, `POSTGRES_USER`, and `POSTGRES_PASSWORD`; copy `.env.example` to `.env` and set those values before starting Docker.

### 4. Apply migrations

```powershell
python manage.py migrate
```

### 5. Start the development server

```powershell
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in a browser.

## Docker Setup

From the project root:

```powershell
docker compose up --build
```

The application is available at `http://localhost/`. The Django development server is also exposed on port `8000`.

To stop the services:

```powershell
docker compose down
```

## Main Routes

| Route | Purpose |
| --- | --- |
| `/` | Authenticated dashboard |
| `/login/` | User login |
| `/logout/` | User logout |
| `/users/register/` | User registration |
| `/jobs/` | List job applications |
| `/jobs/create/` | Add a job application |
| `/jobs/<id>/` | View a job application |
| `/jobs/<id>/edit/` | Edit a job application |
| `/jobs/<id>/delete/` | Delete a job application |
| `/resumes/` | List uploaded resumes |
| `/resumes/upload/` | Upload a PDF resume and extract its text |
| `/resumes/<id>/` | View resume details and extracted text |
| `/resumes/<id>/download/` | Download a resume |
| `/resumes/<id>/delete/` | Delete a resume |
| `/admin/` | Django admin |

## Running Tests

From the `backend` directory:

```powershell
python manage.py test
```

## Development Notes

- Job application and resume views require authentication.
- Users can only view and modify their own job applications and resumes.
- Resume uploads are currently processed as PDFs.
- The AI-analysis app is installed but has no implemented model, view, URL, or task yet.
- Update the checklist in this README as each feature is completed.
