from app.database import db_manager
from app.s3_client import s3_manager
from app.models import RecitationCreate, RecitationUpdate, RecitationStatus, LikeCreate
from bson import ObjectId
from datetime import datetime
from typing import List, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class RecitationService:
    def __init__(self):
        self.db = db_manager.get_db()
        self.recitations_collection = self.db.recitations
        self.likes_collection = self.db.likes
    
    async def create_recitation(self, recitation_data: RecitationCreate, audio_file: bytes, 
                              file_extension: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Create a new recitation"""
        try:
            # Upload audio to S3
            audio_url = s3_manager.upload_file(audio_file, file_extension, user_id)
            if not audio_url:
                raise Exception("Failed to upload audio file")
            
            # Create recitation document
            recitation_doc = {
                "title": recitation_data.title,
                "reciter_name": recitation_data.reciter_name,
                "masjid_name": recitation_data.masjid_name,
                "masjid_location": recitation_data.masjid_location,
                "surah_name": recitation_data.surah_name,
                "surah_number": recitation_data.surah_number,
                "ayah_start": recitation_data.ayah_start,
                "ayah_end": recitation_data.ayah_end,
                "description": recitation_data.description,
                "tags": recitation_data.tags or [],
                "uploader_id": user_id,
                "audio_url": audio_url,
                "status": RecitationStatus.PENDING.value,
                "likes_count": 0,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            # Insert into MongoDB
            result = self.recitations_collection.insert_one(recitation_doc)
            recitation_doc["_id"] = result.inserted_id
            
            logger.info(f"Recitation created successfully: {result.inserted_id}")
            return self._format_recitation(recitation_doc)
            
        except Exception as e:
            logger.error(f"Failed to create recitation: {e}")
            return None
    
    async def create_recitation_with_url(self, recitation_data: RecitationCreate, 
                                       audio_url: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Create a new recitation with existing S3 URL"""
        try:
            # Create recitation document
            recitation_doc = {
                "title": recitation_data.title,
                "reciter_name": recitation_data.reciter_name,
                "masjid_name": recitation_data.masjid_name,
                "masjid_location": recitation_data.masjid_location,
                "surah_name": recitation_data.surah_name,
                "surah_number": recitation_data.surah_number,
                "ayah_start": recitation_data.ayah_start,
                "ayah_end": recitation_data.ayah_end,
                "description": recitation_data.description,
                "tags": recitation_data.tags or [],
                "uploader_id": user_id,
                "audio_url": audio_url,
                "status": RecitationStatus.PENDING.value,
                "likes_count": 0,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            # Insert into MongoDB
            result = self.recitations_collection.insert_one(recitation_doc)
            recitation_doc["_id"] = result.inserted_id
            
            logger.info(f"Recitation created successfully: {result.inserted_id}")
            return self._format_recitation(recitation_doc)
            
        except Exception as e:
            logger.error(f"Failed to create recitation: {e}")
            return None
    
    async def get_recitations(self, user_id: Optional[str] = None, 
                            mine: bool = False, page: int = 1, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recitations with optional filtering"""
        try:
            skip = (page - 1) * limit
            
            # Build query
            query = {"status": RecitationStatus.APPROVED.value}
            
            if mine and user_id:
                query["uploader_id"] = user_id
            elif mine and not user_id:
                return []
            
            # Get recitations
            cursor = self.recitations_collection.find(query).sort("created_at", -1).skip(skip).limit(limit)
            recitations = []
            
            for doc in cursor:
                recitation = self._format_recitation(doc)
                # Check if user liked this recitation
                if user_id:
                    like = self.likes_collection.find_one({
                        "user_id": user_id,
                        "recitation_id": str(doc["_id"])
                    })
                    recitation["is_liked"] = like is not None
                else:
                    recitation["is_liked"] = False
                
                recitations.append(recitation)
            
            return recitations
            
        except Exception as e:
            logger.error(f"Failed to get recitations: {e}")
            return []
    
    async def get_recitation_by_id(self, recitation_id: str, user_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get a specific recitation by ID"""
        try:
            doc = self.recitations_collection.find_one({"_id": ObjectId(recitation_id)})
            if not doc:
                return None
            
            recitation = self._format_recitation(doc)
            
            # Check if user liked this recitation
            if user_id:
                like = self.likes_collection.find_one({
                    "user_id": user_id,
                    "recitation_id": recitation_id
                })
                recitation["is_liked"] = like is not None
            else:
                recitation["is_liked"] = False
            
            return recitation
            
        except Exception as e:
            logger.error(f"Failed to get recitation: {e}")
            return None
    
    async def update_recitation(self, recitation_id: str, update_data: RecitationUpdate, 
                              user_id: str) -> Optional[Dict[str, Any]]:
        """Update a recitation"""
        try:
            # Check if user owns the recitation
            recitation = self.recitations_collection.find_one({
                "_id": ObjectId(recitation_id),
                "uploader_id": user_id
            })
            
            if not recitation:
                return None
            
            # Prepare update data
            update_fields = {}
            for field, value in update_data.dict(exclude_unset=True).items():
                if value is not None:
                    update_fields[field] = value
            
            if not update_fields:
                return self._format_recitation(recitation)
            
            update_fields["updated_at"] = datetime.utcnow()
            
            # Update in MongoDB
            result = self.recitations_collection.update_one(
                {"_id": ObjectId(recitation_id)},
                {"$set": update_fields}
            )
            
            if result.modified_count > 0:
                # Get updated document
                updated_doc = self.recitations_collection.find_one({"_id": ObjectId(recitation_id)})
                return self._format_recitation(updated_doc)
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to update recitation: {e}")
            return None
    
    async def delete_recitation(self, recitation_id: str, user_id: str) -> bool:
        """Delete a recitation"""
        try:
            # Check if user owns the recitation
            recitation = self.recitations_collection.find_one({
                "_id": ObjectId(recitation_id),
                "uploader_id": user_id
            })
            
            if not recitation:
                return False
            
            # Delete from S3
            if recitation.get("audio_url"):
                s3_manager.delete_file(recitation["audio_url"])
            
            # Delete likes
            self.likes_collection.delete_many({"recitation_id": recitation_id})
            
            # Delete recitation
            result = self.recitations_collection.delete_one({"_id": ObjectId(recitation_id)})
            
            return result.deleted_count > 0
            
        except Exception as e:
            logger.error(f"Failed to delete recitation: {e}")
            return False
    
    async def like_recitation(self, recitation_id: str, user_id: str) -> bool:
        """Like a recitation"""
        try:
            # Check if recitation exists
            recitation = self.recitations_collection.find_one({"_id": ObjectId(recitation_id)})
            if not recitation:
                return False
            
            # Check if already liked
            existing_like = self.likes_collection.find_one({
                "user_id": user_id,
                "recitation_id": recitation_id
            })
            
            if existing_like:
                # Unlike
                self.likes_collection.delete_one({"_id": existing_like["_id"]})
                self.recitations_collection.update_one(
                    {"_id": ObjectId(recitation_id)},
                    {"$inc": {"likes_count": -1}}
                )
                return True
            else:
                # Like
                like_doc = {
                    "user_id": user_id,
                    "recitation_id": recitation_id,
                    "created_at": datetime.utcnow()
                }
                self.likes_collection.insert_one(like_doc)
                self.recitations_collection.update_one(
                    {"_id": ObjectId(recitation_id)},
                    {"$inc": {"likes_count": 1}}
                )
                return True
                
        except Exception as e:
            logger.error(f"Failed to like/unlike recitation: {e}")
            return False
    
    async def get_recommendations(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get personalized recommendations for a user"""
        try:
            # Get user's liked recitations
            user_likes = list(self.likes_collection.find({"user_id": user_id}))
            liked_recitation_ids = [like["recitation_id"] for like in user_likes]
            
            if not liked_recitation_ids:
                # If no likes, return recent popular recitations
                cursor = self.recitations_collection.find(
                    {"status": RecitationStatus.APPROVED.value}
                ).sort("likes_count", -1).limit(limit)
            else:
                # Get liked recitations to analyze preferences
                liked_recitations = list(self.recitations_collection.find({
                    "_id": {"$in": [ObjectId(rid) for rid in liked_recitation_ids]}
                }))
                
                # Extract preferences
                preferred_reciters = set()
                preferred_surahs = set()
                preferred_tags = set()
                
                for recitation in liked_recitations:
                    preferred_reciters.add(recitation.get("reciter_name", ""))
                    preferred_surahs.add(recitation.get("surah_name", ""))
                    preferred_tags.update(recitation.get("tags", []))
                
                # Find similar recitations
                query = {
                    "status": RecitationStatus.APPROVED.value,
                    "_id": {"$nin": [ObjectId(rid) for rid in liked_recitation_ids]}
                }
                
                # Build recommendation query
                recommendation_conditions = []
                if preferred_reciters:
                    recommendation_conditions.append({"reciter_name": {"$in": list(preferred_reciters)}})
                if preferred_surahs:
                    recommendation_conditions.append({"surah_name": {"$in": list(preferred_surahs)}})
                if preferred_tags:
                    recommendation_conditions.append({"tags": {"$in": list(preferred_tags)}})
                
                if recommendation_conditions:
                    query["$or"] = recommendation_conditions
                
                cursor = self.recitations_collection.find(query).sort("likes_count", -1).limit(limit)
            
            recommendations = []
            for doc in cursor:
                recitation = self._format_recitation(doc)
                recitation["is_liked"] = False
                recommendations.append(recitation)
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Failed to get recommendations: {e}")
            return []
    
    async def search_recitations(self, search_filters: Dict[str, Any], 
                               page: int = 1, limit: int = 20) -> List[Dict[str, Any]]:
        """Search recitations with filters"""
        try:
            skip = (page - 1) * limit
            
            # Build search query
            query = {"status": RecitationStatus.APPROVED.value}
            
            if search_filters.get("reciter_name"):
                query["reciter_name"] = {"$regex": search_filters["reciter_name"], "$options": "i"}
            
            if search_filters.get("masjid_location"):
                query["masjid_location"] = {"$regex": search_filters["masjid_location"], "$options": "i"}
            
            if search_filters.get("surah_name"):
                query["surah_name"] = {"$regex": search_filters["surah_name"], "$options": "i"}
            
            if search_filters.get("tags"):
                query["tags"] = {"$in": search_filters["tags"]}
            
            # Execute search
            cursor = self.recitations_collection.find(query).sort("created_at", -1).skip(skip).limit(limit)
            
            results = []
            for doc in cursor:
                results.append(self._format_recitation(doc))
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to search recitations: {e}")
            return []
    
    async def update_recitation_status(self, recitation_id: str, status: RecitationStatus, 
                                     reason: Optional[str], user_id: str) -> Optional[Dict[str, Any]]:
        """Update recitation status (admin function)"""
        try:
            # Check if recitation exists
            recitation = self.recitations_collection.find_one({"_id": ObjectId(recitation_id)})
            if not recitation:
                return None
            
            # Update status
            update_fields = {
                "status": status.value,
                "updated_at": datetime.utcnow()
            }
            
            if reason:
                update_fields["status_reason"] = reason
            
            # Update in MongoDB
            result = self.recitations_collection.update_one(
                {"_id": ObjectId(recitation_id)},
                {"$set": update_fields}
            )
            
            if result.modified_count > 0:
                # Get updated document
                updated_doc = self.recitations_collection.find_one({"_id": ObjectId(recitation_id)})
                return self._format_recitation(updated_doc)
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to update recitation status: {e}")
            return None
    
    async def get_recitations_by_status(self, status: RecitationStatus, 
                                      page: int = 1, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recitations by status (admin function)"""
        try:
            skip = (page - 1) * limit
            
            # Build query
            query = {"status": status.value}
            
            # Get recitations
            cursor = self.recitations_collection.find(query).sort("created_at", -1).skip(skip).limit(limit)
            recitations = []
            
            for doc in cursor:
                recitation = self._format_recitation(doc)
                recitation["is_liked"] = False  # Admin view doesn't need like status
                recitations.append(recitation)
            
            return recitations
            
        except Exception as e:
            logger.error(f"Failed to get recitations by status: {e}")
            return []
    
    def _format_recitation(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        """Format recitation document for response"""
        return {
            "id": str(doc["_id"]),
            "title": doc["title"],
            "reciter_name": doc["reciter_name"],
            "masjid_name": doc.get("masjid_name"),
            "masjid_location": doc.get("masjid_location"),
            "surah_name": doc["surah_name"],
            "surah_number": doc.get("surah_number"),
            "ayah_start": doc.get("ayah_start"),
            "ayah_end": doc.get("ayah_end"),
            "description": doc.get("description"),
            "tags": doc.get("tags", []),
            "uploader_id": doc["uploader_id"],
            "audio_url": doc["audio_url"],
            "status": doc["status"],
            "likes_count": doc.get("likes_count", 0),
            "created_at": doc["created_at"],
            "updated_at": doc["updated_at"]
        }

# Global service instance
recitation_service = RecitationService() 