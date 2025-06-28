from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import boto3
from dotenv import load_dotenv
import os

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
BUCKET_NAME = os.getenv("BUCKET_NAME")

router = APIRouter()

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

@router.post("/upload-audio")
async def upload_audio_file(file: UploadFile = File(...)):
    # Only allow .mp3 files
    if not file.filename.endswith(".mp3"):
        raise HTTPException(status_code=400, detail="Only .mp3 files are allowed.")
    contents = await file.read()
    s3_key = f"uploads/{file.filename}"
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=s3_key,
        Body=contents,
        ContentType='audio/mpeg',
    )
    public_url = f"https://{BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{s3_key}"
    return JSONResponse({"url": public_url})

@router.delete("/delete-audio")
async def delete_audio_file(filename: str):
    try:
        s3_client.delete_object(Bucket=BUCKET_NAME, Key=filename)
        return {"message": f"Deleted {filename} from S3"}
    except Exception as e:
        return {"error": str(e)} 