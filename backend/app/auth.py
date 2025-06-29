import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import settings
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Initialize Firebase Admin SDK
def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate({
                "type": "service_account",
                "project_id": settings.firebase_project_id,
                "private_key_id": settings.firebase_private_key_id,
                "private_key": settings.firebase_private_key.replace('\\n', '\n'),
                "client_email": settings.firebase_client_email,
                "client_id": settings.firebase_client_id,
                "auth_uri": settings.firebase_auth_uri,
                "token_uri": settings.firebase_token_uri,
                "auth_provider_x509_cert_url": settings.firebase_auth_provider_x509_cert_url,
                "client_x509_cert_url": settings.firebase_client_x509_cert_url
            })
            firebase_admin.initialize_app(cred)
            logger.info("Firebase Admin SDK initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Firebase Admin SDK: {e}")
        # For development, we'll allow dummy auth
        logger.warning("Using dummy authentication for development")

# Security scheme
security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Verify Firebase ID token and return user ID"""
    try:
        # For development, allow dummy token
        if settings.app_env == "development" and credentials.credentials == "dummy_token":
            return "dummy_user_id"
        
        # Verify with Firebase
        decoded_token = auth.verify_id_token(credentials.credentials)
        user_id = decoded_token['uid']
        logger.info(f"Token verified for user: {user_id}")
        return user_id
        
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials"
        )

# Initialize Firebase on module import
initialize_firebase() 