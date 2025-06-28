# main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import boto3
from dotenv import load_dotenv
import os

load_dotenv()

# 2️⃣ Your AWS S3 configuration
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
BUCKET_NAME = os.getenv("BUCKET_NAME")

# 1️⃣ FastAPI instance
app = FastAPI()

# 3️⃣ Create an S3 client using boto3
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

# 4️⃣ Define an upload endpoint
@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    # 4a. Read the file's contents into memory
    contents = await file.read()

    # 4b. Define the S3 object key (path in bucket)
    s3_key = f"uploads/{file.filename}"

    # 4c. Upload to S3
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=s3_key,
        Body=contents,
        ContentType='audio/mpeg',
    )

    # 4d. Build the public URL
    public_url = f"https://{BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{s3_key}"

    # 4e. Return it in JSON
    return JSONResponse({"url": public_url})

@app.delete("/delete")
async def delete_audio(filename: str):
    """
    Delete an audio file from S3 bucket.
    Expects 'filename' query parameter (e.g., ?filename=uploads/recitation.mp3)
    """
    try:
        s3_client.delete_object(Bucket=BUCKET_NAME, Key=filename)
        return {"message": f"Deleted {filename} from S3"}
    except Exception as e:
        return {"error": str(e)}


