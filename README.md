Authentication Service with Google OAuth
========================================

This project is an Authentication Service built with FastAPI and integrates with 
Google OAuth 2.0 for user login. It uses JWT for access and refresh tokens, Alembic 
for database migrations, and Poetry as the dependency manager.

The service handles authentication flow by redirecting users to Google for login, 
validating tokens, and issuing application-specific JWTs.

-------------------------------------------------------
1. Register OAuth App in Google Cloud Console
-------------------------------------------------------
To use Google login, you must create OAuth credentials in the Google Cloud Console.

Steps:
1. Go to https://console.cloud.google.com/
2. Create a new project (or use an existing one).
3. Navigate to APIs & Services > OAuth consent screen.
   - Choose External (for general users) or Internal (restricted to org).
   - Fill in app name, support email, and authorized domain.
   - Save and continue until done.
4. Navigate to APIs & Services > Credentials.
   - Click Create Credentials > OAuth client ID.
   - Application type: Web application.
   - Enter a name (e.g., Auth Service).
   - Under Authorized redirect URIs, add your callback endpoint:
     http://localhost:8000/auth/v1/google/callback
   - Save and copy the Client ID and Client Secret.

-------------------------------------------------------
2. Configure Environment Variables
-------------------------------------------------------
Create a `.env` file in the root project directory and provide the required values.

Example `.env`:

ENV=local
SESSION_SECRET_KEY=super-secret-session-key
SECRET_KEY=super-secret-jwt-key
ALGORITHM=HS256

# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/auth_service

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
REDIRECT_URL=http://localhost:8000/auth/v1/google/callback

-------------------------------------------------------
3. Install Dependencies (Poetry)
-------------------------------------------------------
Make sure Poetry is installed. Then run:

poetry install

This will install FastAPI, SQLAlchemy, Alembic, Authlib, and other dependencies.

To install with development dependencies (required for testing):
poetry install --with dev

-------------------------------------------------------
4. Run Database Migration
-------------------------------------------------------
We use Alembic for database migrations.

Apply migrations:
poetry run alembic upgrade head

Generate new migration (if models change):
poetry run alembic revision --autogenerate -m "describe changes"
poetry run alembic upgrade head

-------------------------------------------------------
5. Run the Application
-------------------------------------------------------
Start the FastAPI server:

poetry run uvicorn main:app --reload

You can adjust host and port if needed:
poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload

-------------------------------------------------------
Summary
-------------------------------------------------------
- Register Google OAuth app and set credentials
- Configure `.env` for database and Google settings
- Install dependencies with Poetry (use --with dev for testing)
- Migrate tables with Alembic
- Launch FastAPI with Uvicorn

Your Authentication Service is now ready to integrate with frontend or other
backend services using Google OAuth.
