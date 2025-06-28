from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from fastapi.responses import JSONResponse
from typing import List, Optional
from app.auth import verify_token
from app.services import recitation_service
from app.s3_client import s3_manager
from app.models import (
    RecitationCreate, RecitationUpdate, RecitationResponse, 
    LikeCreate, LikeResponse, SearchFilters, PaginationParams, RecitationStatus
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
    s3_url: str = Form(...),
    user_id: str = Depends(verify_token)
):
    """Upload a new recitation with S3 URL"""
    try:
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
        
        # Create recitation with S3 URL
        result = await recitation_service.create_recitation_with_url(
            recitation_data, s3_url, user_id
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

@router.post("/s3/upload")
async def upload_audio_to_s3(file: UploadFile = File(...)):
    """Upload audio file directly to S3"""
    try:
        # Read the file's contents into memory
        contents = await file.read()
        
        # Upload to S3 using the simplified method
        public_url = s3_manager.upload_audio_file(contents, file.filename)
        
        if not public_url:
            raise HTTPException(status_code=500, detail="Failed to upload file to S3")
        
        return {"url": public_url}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"S3 upload error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/s3/delete")
async def delete_audio_from_s3(filename: str):
    """Delete an audio file from S3 bucket"""
    try:
        success = s3_manager.delete_audio_file(filename)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete file from S3")
        
        return {"message": f"Deleted {filename} from S3"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"S3 delete error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Quran Platform API is running"}

@router.put("/admin/recitations/{recitation_id}/status")
async def update_recitation_status(
    recitation_id: str,
    status: RecitationStatus = Form(...),
    reason: Optional[str] = Form(None),
    user_id: str = Depends(verify_token)
):
    """Admin endpoint to update recitation status"""
    try:
        # For now, allow any authenticated user to be admin
        # In production, you'd check if user_id has admin role
        result = await recitation_service.update_recitation_status(
            recitation_id, status, reason, user_id
        )
        
        if not result:
            raise HTTPException(status_code=404, detail="Recitation not found")
        
        return {"message": f"Recitation status updated to {status.value}", "recitation": result}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update status error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/admin/recitations/pending")
async def get_pending_recitations(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    user_id: str = Depends(verify_token)
):
    """Admin endpoint to get pending recitations for review"""
    try:
        recitations = await recitation_service.get_recitations_by_status(
            RecitationStatus.PENDING, page, limit
        )
        return recitations
    except Exception as e:
        logger.error(f"Get pending recitations error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error") 