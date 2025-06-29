from pymongo import MongoClient
from pymongo.database import Database
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.client: MongoClient = None
        self.db: Database = None
    
    def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = MongoClient(settings.mongodb_uri)
            self.db = self.client.quranApp
            # Test the connection
            self.client.admin.command('ping')
            logger.info("Successfully connected to MongoDB")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB")
    
    def get_db(self) -> Database:
        """Get the database instance"""
        if not self.db:
            self.connect()
        return self.db

# Global database manager instance
db_manager = DatabaseManager() 