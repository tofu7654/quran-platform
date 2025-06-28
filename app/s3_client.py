import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from app.config import settings
import logging
from typing import Optional
import uuid
from datetime import datetime
import os

logger = logging.getLogger(__name__)

class S3Manager:
    def __init__(self):
        self.s3_client = None
        self.bucket_name = settings.bucket_name
    
    def initialize(self):
        """Initialize S3 client"""
        try:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.aws_access_key_id,
                aws_secret_access_key=settings.aws_secret_access_key,
                region_name=settings.aws_region
            )
            logger.info("S3 client initialized successfully")
        except NoCredentialsError:
            logger.error("AWS credentials not found")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize S3 client: {e}")
            raise
    
    def upload_file(self, file_data: bytes, file_extension: str, user_id: str) -> Optional[str]:
        """Upload file to S3 and return the URL"""
        if not self.s3_client:
            self.initialize()
        
        try:
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            filename = f"recitations/{user_id}/{timestamp}_{unique_id}.{file_extension}"
            
            # Upload file
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=filename,
                Body=file_data,
                ContentType=f'audio/{file_extension}',
                ACL='public-read'
            )
            
            # Generate public URL
            url = f"https://{self.bucket_name}.s3.{settings.aws_region}.amazonaws.com/{filename}"
            logger.info(f"File uploaded successfully: {url}")
            return url
            
        except ClientError as e:
            logger.error(f"Failed to upload file to S3: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error uploading file: {e}")
            return None
    
    def upload_audio_file(self, file_data: bytes, filename: str) -> Optional[str]:
        """Upload audio file to S3 (simplified method)"""
        if not self.s3_client:
            self.initialize()
        
        try:
            # Define the S3 object key (path in bucket)
            s3_key = f"uploads/{filename}"
            
            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=file_data,
                ContentType='audio/mpeg',
                ACL='public-read'
            )
            
            # Build the public URL
            public_url = f"https://{self.bucket_name}.s3.{settings.aws_region}.amazonaws.com/{s3_key}"
            logger.info(f"Audio file uploaded successfully: {public_url}")
            return public_url
            
        except ClientError as e:
            logger.error(f"Failed to upload audio file to S3: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error uploading audio file: {e}")
            return None
    
    def delete_file(self, file_url: str) -> bool:
        """Delete file from S3"""
        if not self.s3_client:
            self.initialize()
        
        try:
            # Extract key from URL
            key = file_url.split(f"{self.bucket_name}.s3.{settings.aws_region}.amazonaws.com/")[1]
            
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=key
            )
            logger.info(f"File deleted successfully: {key}")
            return True
            
        except ClientError as e:
            logger.error(f"Failed to delete file from S3: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error deleting file: {e}")
            return False
    
    def delete_audio_file(self, filename: str) -> bool:
        """Delete audio file from S3 (simplified method)"""
        if not self.s3_client:
            self.initialize()
        
        try:
            s3_key = f"uploads/{filename}"
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=s3_key)
            logger.info(f"Audio file deleted successfully: {s3_key}")
            return True
            
        except ClientError as e:
            logger.error(f"Failed to delete audio file from S3: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error deleting audio file: {e}")
            return False

# Global S3 manager instance
s3_manager = S3Manager() 