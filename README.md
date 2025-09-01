# FitByte Project

A FitByte API Project for tracking fitness activities.

## Features

- **FastAPI Framework**: Latest stable version with async support
- **PostgreSQL Database**: Full database integration with SQLAlchemy
- **Docker Support**: Containerized deployment
- **Auto-Generated Documentation**: Interactive Swagger UI and ReDoc
- **Versioned API**: Organized routing structure
- **Security Features**: Password hashing
- **Database Operations**: CRUD operations with PostgreSQL

## Quick Start

### Prerequisites
- **PostgreSQL Database**: Set up PostgreSQL externally (see Database Setup section below)

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd fastapi-project
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your PostgreSQL configuration
   ```

3. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - API: http://localhost:8000
   - Swagger Documentation: http://localhost:8000/docs
   - ReDoc Documentation: http://localhost:8000/redoc

### Local Development

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env
   ```

3. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── security.py
│   │   └── database.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── api.py
│   │       └── endpoints/
│   │           └── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   └── schemas/
│       ├── __init__.py
│       ├── token.py
│       └── user.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Configuration

Environment variables in `.env`:

- `SECRET_KEY`: Application secret key
- `DEBUG`: Debug mode
- `DATABASE_URL`: PostgreSQL connection string

### PostgreSQL Configuration
- `POSTGRES_SERVER`: PostgreSQL server hostname (default: localhost)
- `POSTGRES_USER`: PostgreSQL username
- `POSTGRES_PASSWORD`: PostgreSQL password
- `POSTGRES_DB`: PostgreSQL database name

## Database Setup

The application uses PostgreSQL as the database backend. You need to set up PostgreSQL separately (externally) as the application does not include a database service in Docker Compose.


### Database Migration

The application uses SQLAlchemy with automatic table creation. Tables are created automatically when the application starts.

### Database Connection

The application connects to PostgreSQL using the connection string format:
```
postgresql://username:password@host:port/database
```

Update the `DATABASE_URL` in your `.env` file to match your PostgreSQL setup.

## Development

### Adding New Endpoints

1. Create endpoint file in `app/api/v1/endpoints/`
2. Import and include in `app/api/v1/api.py`
3. Add Pydantic schemas in `app/schemas/`
4. Update models if needed

### Database Integration

The project includes full PostgreSQL integration with SQLAlchemy:

1. Database models are defined in `app/models/`
2. Database connection is configured in `app/core/database.py`
3. Dependency injection provides database sessions to endpoints
4. Tables are automatically created on application startup

## License

MIT License