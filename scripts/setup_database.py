#!/usr/bin/env python3
"""
Database setup script for Quran Platform
Creates necessary collections and indexes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import db_manager
from pymongo import ASCENDING, DESCENDING, TEXT
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_database():
    """Setup database collections and indexes"""
    try:
        # Connect to database
        db = db_manager.get_db()
        
        # Create collections
        collections = ['recitations', 'likes', 'users']
        
        for collection_name in collections:
            if collection_name not in db.list_collection_names():
                db.create_collection(collection_name)
                logger.info(f"Created collection: {collection_name}")
        
        # Create indexes for recitations collection
        recitations = db.recitations
        
        # Text search indexes
        recitations.create_index([("title", TEXT), ("reciter_name", TEXT), ("surah_name", TEXT)])
        recitations.create_index([("reciter_name", ASCENDING)])
        recitations.create_index([("surah_name", ASCENDING)])
        recitations.create_index([("uploader_id", ASCENDING)])
        recitations.create_index([("status", ASCENDING)])
        recitations.create_index([("created_at", DESCENDING)])
        recitations.create_index([("likes_count", DESCENDING)])
        
        # Compound indexes for better query performance
        recitations.create_index([("status", ASCENDING), ("created_at", DESCENDING)])
        recitations.create_index([("uploader_id", ASCENDING), ("status", ASCENDING)])
        
        logger.info("Created indexes for recitations collection")
        
        # Create indexes for likes collection
        likes = db.likes
        likes.create_index([("user_id", ASCENDING), ("recitation_id", ASCENDING)], unique=True)
        likes.create_index([("recitation_id", ASCENDING)])
        likes.create_index([("user_id", ASCENDING)])
        
        logger.info("Created indexes for likes collection")
        
        # Create indexes for users collection (if needed)
        users = db.users
        users.create_index([("email", ASCENDING)], unique=True)
        users.create_index([("created_at", DESCENDING)])
        
        logger.info("Created indexes for users collection")
        
        logger.info("Database setup completed successfully!")
        
    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        raise

if __name__ == "__main__":
    setup_database() 