from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse
from app.s3_client import s3_manager
import logging
from typing import Optional
from datetime import datetime
import uuid

router = APIRouter()
logger = logging.getLogger(__name__)

from app.moderation_app import verify_audio_is_quran

@router.post("/upload-audio")
async def upload_audio_file(
    file: UploadFile = File(...),
    user_id: Optional[str] = Query(None)
):
    # Enforce MP3
    if not file.filename.endswith(".mp3"):
        raise HTTPException(status_code=400, detail="Only .mp3 files are allowed.")

    if not user_id:
        user_id = "anonymous"

    contents = await file.read()

    # ✅ Step: Check if it's Quran
    is_quran = await verify_audio_is_quran(contents)
    if not is_quran:
        raise HTTPException(status_code=400, detail="Audio does not appear to be Quran recitation.")

    # ✅ Upload to S3
    public_url = s3_manager.upload_file(
        file_data=contents,
        file_extension='mp3',
        user_id=user_id
    )

    if not public_url:
        raise HTTPException(status_code=500, detail="Upload failed to S3.")

    return JSONResponse({"url": public_url})



@router.delete("/delete-audio")
async def delete_audio_file(
    file_url: Optional[str] = Query(None, description="Full S3 public URL"),
    s3_key: Optional[str] = Query(None, description="Alternatively, provide the S3 key directly")
):
    """
    Deletes an audio file from S3.
    Accepts either the full public URL or direct S3 key.
    """
    if not file_url and not s3_key:
        raise HTTPException(status_code=400, detail="Provide either file_url or s3_key.")

    if not s3_key:
        # Extract key from the public URL
        try:
            split_part = f"{s3_manager.bucket_name}.s3.{s3_manager.s3_client.meta.region_name}.amazonaws.com/"
            s3_key = file_url.split(split_part, 1)[1]
        except (IndexError, AttributeError):
            raise HTTPException(status_code=400, detail="Invalid file_url format.")

    try:
        s3_manager.initialize()
        s3_manager.s3_client.delete_object(
            Bucket=s3_manager.bucket_name,
            Key=s3_key
        )
    except Exception as e:
        logger.error(f"Failed to delete from S3: {e}")
        raise HTTPException(status_code=500, detail=f"Delete failed: {e}")

    return {"message": f"Deleted {s3_key} from S3"}
