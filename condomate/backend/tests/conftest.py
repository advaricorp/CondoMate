import pytest
import pytest_asyncio
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.core.db_init import init_db, close_db
from app.core.db import connect_to_mongo, close_mongo_connection, db_client, get_database
from fastapi.testclient import TestClient
from app.main import app
from colorama import init

# Initialize colorama for colored output
init()

def pytest_configure(config):
    """Configure pytest options."""
    config.option.asyncio_mode = "strict"

@pytest_asyncio.fixture(scope="session")
async def db():
    """Create a test database and handle cleanup."""
    # Use a test database
    settings.MONGO_DB_NAME = "test_condomate"
    
    # Initialize the test database
    client = await init_db()
    
    # Wait for the database to be ready
    database = client[settings.MONGO_DB_NAME]
    await database.command("ping")
    
    yield database
    
    # Cleanup: Drop test database and close connection
    if client:
        await client.drop_database(settings.MONGO_DB_NAME)
        await close_db(client)

@pytest.fixture
def client(db):
    """Create a test client."""
    app.dependency_overrides = {}  # Reset any overrides
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(scope="function")
async def test_client():
    """Create a test client for the FastAPI application."""
    # Initialize the database before creating the test client
    await connect_to_mongo()
    
    async with TestClient(app) as client:
        yield client
    
    # Cleanup: Close database connection
    await close_mongo_connection() 