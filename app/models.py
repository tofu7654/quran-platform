from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class RecitationStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    FACT_CHECK = "fact_check"

class RecitationBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    reciter_name: str = Field(..., min_length=1, max_length=100)
    masjid_name: Optional[str] = Field(None, max_length=100)
    masjid_location: Optional[str] = Field(None, max_length=200)
    surah_name: str = Field(..., min_length=1, max_length=100)
    surah_number: Optional[int] = Field(None, ge=1, le=114)
    ayah_start: Optional[int] = Field(None, ge=1)
    ayah_end: Optional[int] = Field(None, ge=1)
    description: Optional[str] = Field(None, max_length=500)
    tags: Optional[List[str]] = Field(default_factory=list)

class RecitationCreate(RecitationBase):
    pass

class RecitationResponse(RecitationBase):
    id: str
    uploader_id: str
    audio_url: str
    status: RecitationStatus
    likes_count: int = 0
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class RecitationUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    reciter_name: Optional[str] = Field(None, min_length=1, max_length=100)
    masjid_name: Optional[str] = Field(None, max_length=100)
    masjid_location: Optional[str] = Field(None, max_length=200)
    surah_name: Optional[str] = Field(None, min_length=1, max_length=100)
    surah_number: Optional[int] = Field(None, ge=1, le=114)
    ayah_start: Optional[int] = Field(None, ge=1)
    ayah_end: Optional[int] = Field(None, ge=1)
    description: Optional[str] = Field(None, max_length=500)
    tags: Optional[List[str]] = None

class LikeCreate(BaseModel):
    recitation_id: str

class LikeResponse(BaseModel):
    id: str
    user_id: str
    recitation_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: str
    email: Optional[str] = None
    display_name: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class SearchFilters(BaseModel):
    reciter_name: Optional[str] = None
    masjid_location: Optional[str] = None
    surah_name: Optional[str] = None
    tags: Optional[List[str]] = None
    status: Optional[RecitationStatus] = RecitationStatus.APPROVED

class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(20, ge=1, le=100) 