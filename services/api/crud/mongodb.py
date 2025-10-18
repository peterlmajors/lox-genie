
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from typing import Optional

from services.api.core.config import settings

class MongoDBClient:
    """MongoDB client for async operations."""
    
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.database: Optional[AsyncIOMotorDatabase] = None
    
    async def connect(self) -> None:
        """Connect to MongoDB."""
        connection_string = (
            f"mongodb://{settings.MONGODB_USERNAME}:{settings.MONGODB_PASSWORD}"
            f"@{settings.MONGODB_HOST}:{settings.MONGODB_PORT}/{settings.MONGODB_DATABASE}"
            f"?authSource=admin"
        )
        
        self.client = AsyncIOMotorClient(connection_string)
        self.database = self.client[settings.MONGODB_DATABASE]
    
    async def disconnect(self) -> None:
        """Disconnect from MongoDB."""
        if self.client is not None:
            self.client.close()
    
    def get_collection(self, collection_name: str) -> AsyncIOMotorCollection:
        """Get a collection from the database."""
        if self.database is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self.database[collection_name]

# Global MongoDB client instance
mongodb_client = MongoDBClient()

async def get_mongodb() -> MongoDBClient:
    """Dependency to get MongoDB client."""
    if mongodb_client.client is None:
        await mongodb_client.connect()
    return mongodb_client