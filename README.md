# AI System Log Analyzer

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [API Overview](#api-overview)
- [Limitations and Improvements](#limitations-and-improvements)


---
## Overview
This project is an AI-powered web application for uploading, storing, and analyzing system logs. Users can create
and account and have access to a dashboard. Here they can upload the raw text of system logs, run an analysis, and 
view the results. These results include the root cause, risk level, any immediate action required, and recommended 
steps to resolve any issues.

---

## Features
- User Auth (via JWT)
- Store System Logs
- AI-Powered Analysis (LLM-Backend)
- Structured Analysis Results
- View Stored logs and analyses
- Delete Logs
---
## Tech Stack

### Backend
- Python
- FastApi
- SQLAlchemy
- SQLite
- JWT Authentication
- LangChain
- Google Gemini

### Frontend
- React
- Axios
- Vite
---
## Architecture

```text
Browser (React)
   ↓ Axios (JWT)
FastAPI Backend
   ↓
SQLite Database
   ↓
LLM Provider (via LangChain)
```
- Authentication handled via JWT

- Each log and analysis is scoped to the authenticated user

- LLM responses are validated using strict Pydantic schemas

## Getting Started

### Prerequisites
- Python 3.12+
- Node.js 20+
- npm
---
### Installation
- Close the GitHub Repository
```shell
git clone https://github.com/cwilly_dev/AI_Log_Analyzer.git
```
#### Quick Start Setup
1. Setup environment and install dependencies:
```sh
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. Create .env file:

```sh

cp .env.example .env

```

3. Edit backend/.env and set required values:

```text

SECRET_KEY=...

GEMINI_API_KEY=...

```

`SECRET_KEY`should be set for consistent JWT behavior\
At least one provider key must be set for analysis: `GEMINI_API_KEY`
4. Run Frontend + Backend
```sh 
npm install
npm run setup
npm run dev
```
- Run via Docker (Optional)
```sh
docker compose up --build
```
---
#### Endpoints
- Frontend: http//localhost:5173
- API: http//localhost:8000
- Swagger UI: http//localhost:8000/docs
---
### Usage

* Register a new user
* Log in
* Paste a raw system log
* Save Log and Analyze
* View structured analysis from Gemini AI
* Select stored logs to view prior analyses
* Delete logs as needed

* The database is preloaded with a test user with example logs ready to analyze:
  * Email: test_user@example.com
  * Password: test_pass_123
---
## API Overview
### Authentication

* `POST /api/auth/register`
* `POST /api/auth/login`
### Logs

* `POST /api/logs/ `– create log
* `POST /api/logs/raw/analyze` – create and analyze
* `POST /api/logs/{id}/analyze` – analyze existing log
* `GET /api/logs/` – list user logs
* `DELETE /api/logs/{id}` – delete log
___
## Limitations and Improvements

* A serverless SQLite database is suitable for this project scope, but is not suitable for a production environment.
  * I would implement a server side database (such as PostgreSQL) to handle high concurrency.
* No background task queue for longer analyses. Current setup waits for the entire analysis response to be generated
before it to load in the UI.
  * I would implement async background processing to provide feedback to the user, improving user experience.
* No role based access (Account User vs. Non-Account User) or rate limiting based on user.
  * I would implement the ability for a user without an account to use the app, where the type of user would reflect in the differed rate limit.

