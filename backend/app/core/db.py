from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.core.db_init import init_db, close_db

# Import your Beanie documents here (when created)
# from app.models.user import User
# from app.models.payment import Payment
# ... other models

# Global database client
db_client = None

async def connect_to_mongo():
    """Connect to MongoDB and initialize the database."""
    global db_client
    try:
        db_client = await init_db()
        print("Successfully connected to MongoDB")
    except Exception as e:
        print(f"Error connecting to MongoDB: {str(e)}")
        raise

async def close_mongo_connection():
    """Close MongoDB connection."""
    global db_client
    if db_client:
        await close_db(db_client)
        db_client = None
        print("MongoDB connection closed")

def get_database():
    """Get the database instance."""
    if not db_client:
        raise Exception("Database not initialized")
    return db_client[settings.MONGO_DB_NAME]

# Dependency for FastAPI endpoints to get DB access
async def get_db_dependency():
    database = get_database()
    return database
