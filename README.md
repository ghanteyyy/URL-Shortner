# URL Shortener

A **production-ready URL shortener API** built with **FastAPI, PostgreSQL, and SQLAlchemy**.
Designed for scalability, clean architecture, and real-world usage.

## Features

- Short URL generation (Base62)
- Fast redirection using indexed lookup
- User-based URL management (optional auth)
- Optional expiration support
- Collision-safe unique code generation
- PostgreSQL + SQLAlchemy ORM
- Clean modular architecture
- Docker-ready

## Tech Stack

- **Backend:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Server:** Uvicorn / Gunicorn
- **Language:** Python 3.13+


## Installation with Docker
**Requirements:** Docker and Docker Compose installed

### 1. Clone the repository

```bash
git clone https://github.com/ghanteyyy/URL-Shortner.git
cd URL-Shortner
```

### 2. Build and start containers
``` bash
docker-compose up --build
```

### 3. Access the application
The backend will be avilable at:

``` bash
http://localhost:8000/
```

### 4. Stop containers
``` bash
docker-compose down
```

## Running without Docker

### 1. Clone Repository

```bash
git clone https://github.com/ghanteyyy/URL-Shortner.git
cd URL-Shortner
```

### 2. Create Virtual Environment
```
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```


### 4. Configure Environment Variables
Create a ```.env``` file

```
DATABASE_URL=postgresql://postgres:admin@localhost/fastapi_url_shortner
BASE_URL=http://localhost:8000
```

### 5. Run Migrations
```
alembic upgrade head
```
