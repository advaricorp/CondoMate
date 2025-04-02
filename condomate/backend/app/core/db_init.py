from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings
from app.models.user import User
from app.models.tenant import Tenant
from datetime import datetime
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def init_db():
    """Initialize database connection and create required collections/indexes."""
    try:
        # Create MongoDB client
        client = AsyncIOMotorClient(settings.MONGO_DB_URL)
        
        # Get database
        db = client[settings.MONGO_DB_NAME]
        
        # Initialize Beanie with the document models
        await init_beanie(
            database=db,
            document_models=[
                User,
                Tenant,
            ]
        )
        
        # Create indexes
        await create_indexes(db)
        
        # Create initial admin tenant if it doesn't exist
        await create_initial_admin_tenant(db)
        
        # Create demo tenant (Hogwarts)
        await create_demo_tenant(db)
        
        return client
        
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        raise

async def create_indexes(db):
    """Create required indexes for collections."""
    # Users collection indexes
    await db.users.create_index("email", unique=True)
    await db.users.create_index("tenant_id")
    await db.users.create_index([("tenant_id", 1), ("email", 1)], unique=True)
    
    # Tenants collection indexes
    await db.tenants.create_index("name", unique=True)
    await db.tenants.create_index("is_active")

async def create_initial_admin_tenant(db):
    """Create initial admin tenant if it doesn't exist."""
    admin_tenant = await db.tenants.find_one({"name": "Admin"})
    if not admin_tenant:
        admin_tenant = Tenant(
            name="Admin",
            description="System Administration Tenant",
            is_active=True,
            max_users=100,
            features=["all"],
            tenant_id="admin",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            current_users=0
        )
        await admin_tenant.insert()

async def create_demo_tenant(db):
    """Create demo tenant (Hogwarts) if it doesn't exist."""
    hogwarts_tenant = await db.tenants.find_one({"name": "Hogwarts School of Witchcraft and Wizardry"})
    if not hogwarts_tenant:
        hogwarts_tenant = Tenant(
            name="Hogwarts School of Witchcraft and Wizardry",
            description="A magical school for wizards and witches",
            is_active=True,
            max_users=1000,
            features=["all"],
            tenant_id="hogwarts",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            current_users=0
        )
        await hogwarts_tenant.insert()
        
        # Create demo users for Hogwarts
        demo_users = [
            User(
                email="dumbledore@hogwarts.wiz",
                full_name="Albus Dumbledore",
                hashed_password=pwd_context.hash("Phoenix123!"),
                role="admin",
                tenant_id="hogwarts",
                is_active=True,
                is_superuser=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            User(
                email="minerva@hogwarts.wiz",
                full_name="Minerva McGonagall",
                hashed_password=pwd_context.hash("Transfiguration123!"),
                role="manager",
                tenant_id="hogwarts",
                is_active=True,
                is_superuser=False,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            User(
                email="harry@hogwarts.wiz",
                full_name="Harry Potter",
                hashed_password=pwd_context.hash("Quidditch123!"),
                role="user",
                tenant_id="hogwarts",
                is_active=True,
                is_superuser=False,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        ]
        
        # Insert demo users
        for user in demo_users:
            await user.insert()
        
        # Update tenant user count
        await hogwarts_tenant.update({"$inc": {"current_users": len(demo_users)}})

async def close_db(client):
    """Close database connection."""
    if client:
        client.close() 