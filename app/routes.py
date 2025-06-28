from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from fastapi.responses import JSONResponse
from typing import List, Optional
from app.auth import verify_token
from app.services import recitation_service
from app.models import (
    RecitationCreate, RecitationUpdate, RecitationResponse, 
    LikeCreate, LikeResponse, SearchFilters, PaginationParams
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/upload", response_model=RecitationResponse)
async def upload_recitation(
    title: str = Form(...),
    reciter_name: str = Form(...),
    masjid_name: Optional[str] = Form(None),
    masjid_location: Optional[str] = Form(None),
    surah_name: str = Form(...),
    surah_number: Optional[int] = Form(None),
    ayah_start: Optional[int] = Form(None),
    ayah_end: Optional[int] = Form(None),
    description: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    audio_file: UploadFile = File(...),
    user_id: str = Depends(verify_token)
):
    """Upload a new recitation"""
    try:
        # Validate file type
        if not audio_file.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="File must be an audio file")
        
        # Get file extension
        file_extension = audio_file.filename.split('.')[-1].lower()
        if file_extension not in ['mp3', 'wav', 'm4a', 'aac']:
            raise HTTPException(status_code=400, detail="Unsupported audio format")
        
        # Parse tags
        tag_list = []
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
        
        # Create recitation data
        recitation_data = RecitationCreate(
            title=title,
            reciter_name=reciter_name,
            masjid_name=masjid_name,
            masjid_location=masjid_location,
            surah_name=surah_name,
            surah_number=surah_number,
            ayah_start=ayah_start,
            ayah_end=ayah_end,
            description=description,
            tags=tag_list
        )
        
        # Read file data
        file_data = await audio_file.read()
        
        # Create recitation
        result = await recitation_service.create_recitation(
            recitation_data, file_data, file_extension, user_id
        )
        
        if not result:
            raise HTTPException(status_code=500, detail="Failed to create recitation")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/recitations", response_model=List[RecitationResponse])
async def get_recitations(
    mine: bool = Query(False, description="Get only user's recitations"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    user_id: Optional[str] = Depends(verify_token)
):
    """Get recitations with optional filtering"""
    try:
        recitations = await recitation_service.get_recitations(
            user_id=user_id, mine=mine, page=page, limit=limit
        )
        return recitations
    except Exception as e:
        logger.error(f"Get recitations error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/recitations/{recitation_id}", response_model=RecitationResponse)
async def get_recitation(
    recitation_id: str,
    user_id: Optional[str] = Depends(verify_token)
):
    """Get a specific recitation by ID"""
    try:
        recitation = await recitation_service.get_recitation_by_id(recitation_id, user_id)
        if not recitation:
            raise HTTPException(status_code=404, detail="Recitation not found")
        return recitation
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get recitation error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/recitations/{recitation_id}", response_model=RecitationResponse)
async def update_recitation(
    recitation_id: str,
    update_data: RecitationUpdate,
    user_id: str = Depends(verify_token)
):
    """Update a recitation"""
    try:
        result = await recitation_service.update_recitation(recitation_id, update_data, user_id)
        if not result:
            raise HTTPException(status_code=404, detail="Recitation not found or not owned by user")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update recitation error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/recitations/{recitation_id}")
async def delete_recitation(
    recitation_id: str,
    user_id: str = Depends(verify_token)
):
    """Delete a recitation"""
    try:
        success = await recitation_service.delete_recitation(recitation_id, user_id)
        if not success:
            raise HTTPException(status_code=404, detail="Recitation not found or not owned by user")
        return {"message": "Recitation deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete recitation error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/likes")
async def like_recitation(
    like_data: LikeCreate,
    user_id: str = Depends(verify_token)
):
    """Like or unlike a recitation"""
    try:
        success = await recitation_service.like_recitation(like_data.recitation_id, user_id)
        if not success:
            raise HTTPException(status_code=404, detail="Recitation not found")
        return {"message": "Like toggled successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Like recitation error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/recommendations", response_model=List[RecitationResponse])
async def get_recommendations(
    limit: int = Query(10, ge=1, le=50, description="Number of recommendations"),
    user_id: str = Depends(verify_token)
):
    """Get personalized recommendations"""
    try:
        recommendations = await recitation_service.get_recommendations(user_id, limit)
        return recommendations
    except Exception as e:
        logger.error(f"Get recommendations error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/search", response_model=List[RecitationResponse])
async def search_recitations(
    reciter_name: Optional[str] = Query(None, description="Search by reciter name"),
    masjid_location: Optional[str] = Query(None, description="Search by masjid location"),
    surah_name: Optional[str] = Query(None, description="Search by surah name"),
    tags: Optional[str] = Query(None, description="Search by tags (comma-separated)"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    user_id: Optional[str] = Depends(verify_token)
):
    """Search recitations with filters"""
    try:
        # Parse tags
        tag_list = None
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
        
        # Build search filters
        search_filters = {
            "reciter_name": reciter_name,
            "masjid_location": masjid_location,
            "surah_name": surah_name,
            "tags": tag_list
        }
        
        # Remove None values
        search_filters = {k: v for k, v in search_filters.items() if v is not None}
        
        results = await recitation_service.search_recitations(
            search_filters, page, limit
        )
        return results
    except Exception as e:
        logger.error(f"Search recitations error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Quran Platform API is running"} 