# 🚀 Quran Platform API - Postman Testing Guide

## 📋 Quick Start

1. **Import the Collection**: Import `postman_collection.json` into Postman
2. **Set Environment Variables**: 
   - `base_url`: `http://localhost:8000`
   - `recitation_id`: Will be set after uploading a recitation
3. **Start the Server**: Run `python main.py`
4. **Test the API**: Follow the testing sequence below

## 🔧 Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Copy `env.example` to `.env` and update with your credentials:
```bash
cp env.example .env
```

### 3. Setup Database (Optional)
```bash
python scripts/setup_database.py
```

### 4. Start the Server
```bash
python main.py
```

The server will start at `http://localhost:8000`

## 🧪 Testing Sequence

### Step 1: Health Check
- **Request**: `GET /api/v1/health`
- **Purpose**: Verify the API is running
- **Expected Response**: 
```json
{
  "status": "healthy",
  "message": "Quran Platform API is running"
}
```

### Step 2: Upload a Recitation
- **Request**: `POST /api/v1/upload`
- **Headers**: `Authorization: Bearer dummy_token`
- **Body**: Form-data with:
  - `title`: "Beautiful Recitation of Al-Fatiha"
  - `reciter_name`: "Sheikh Abdul Rahman Al-Sudais"
  - `masjid_name`: "Masjid Al-Haram"
  - `masjid_location`: "Mecca, Saudi Arabia"
  - `surah_name`: "Al-Fatiha"
  - `surah_number`: "1"
  - `ayah_start`: "1"
  - `ayah_end`: "7"
  - `description`: "A beautiful recitation of the opening chapter of the Quran"
  - `tags`: "fatiha,opening,beautiful"
  - `audio_file`: [Upload any audio file]

**Note**: For testing without S3, you can use any audio file. The system will attempt to upload to S3, but if credentials aren't configured, it will fail gracefully.

### Step 3: Get All Recitations
- **Request**: `GET /api/v1/recitations?page=1&limit=10`
- **Headers**: `Authorization: Bearer dummy_token`
- **Purpose**: View all approved recitations

### Step 4: Get My Recitations
- **Request**: `GET /api/v1/recitations?mine=true&page=1&limit=10`
- **Headers**: `Authorization: Bearer dummy_token`
- **Purpose**: View only your uploaded recitations

### Step 5: Get Specific Recitation
- **Request**: `GET /api/v1/recitations/{recitation_id}`
- **Headers**: `Authorization: Bearer dummy_token`
- **Purpose**: Get details of a specific recitation
- **Note**: Copy the `id` from the upload response and set it as the `recitation_id` variable

### Step 6: Like a Recitation
- **Request**: `POST /api/v1/likes`
- **Headers**: `Authorization: Bearer dummy_token`
- **Body**: 
```json
{
  "recitation_id": "your_recitation_id_here"
}
```

### Step 7: Get Recommendations
- **Request**: `GET /api/v1/recommendations?limit=10`
- **Headers**: `Authorization: Bearer dummy_token`
- **Purpose**: Get personalized recommendations based on your likes

### Step 8: Search Recitations
- **Request**: `GET /api/v1/search?reciter_name=Sheikh&surah_name=Al-Fatiha`
- **Headers**: `Authorization: Bearer dummy_token`
- **Purpose**: Search recitations by various criteria

### Step 9: Update Recitation
- **Request**: `PUT /api/v1/recitations/{recitation_id}`
- **Headers**: `Authorization: Bearer dummy_token`
- **Body**:
```json
{
  "title": "Updated Title",
  "description": "Updated description",
  "tags": ["updated", "tags"]
}
```

### Step 10: Delete Recitation
- **Request**: `DELETE /api/v1/recitations/{recitation_id}`
- **Headers**: `Authorization: Bearer dummy_token`
- **Purpose**: Delete your own recitation

## 🔍 API Documentation

Once the server is running, you can view the interactive API documentation at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🛠️ Troubleshooting

### Common Issues:

1. **Connection Error**: Make sure the server is running on port 8000
2. **Authentication Error**: Use `Bearer dummy_token` for development
3. **Upload Fails**: Check if S3 credentials are configured in `.env`
4. **Database Error**: Ensure MongoDB is running and accessible

### Development Mode Features:

- **Dummy Authentication**: Use `Bearer dummy_token` for testing
- **Local MongoDB**: Defaults to `mongodb://localhost:27017`
- **CORS**: Configured for localhost frontend development

## 📊 Expected Responses

### Successful Upload Response:
```json
{
  "id": "507f1f77bcf86cd799439011",
  "title": "Beautiful Recitation of Al-Fatiha",
  "reciter_name": "Sheikh Abdul Rahman Al-Sudais",
  "masjid_name": "Masjid Al-Haram",
  "masjid_location": "Mecca, Saudi Arabia",
  "surah_name": "Al-Fatiha",
  "surah_number": 1,
  "ayah_start": 1,
  "ayah_end": 7,
  "description": "A beautiful recitation of the opening chapter of the Quran",
  "tags": ["fatiha", "opening", "beautiful"],
  "uploader_id": "dummy_user_id",
  "audio_url": "https://bucket.s3.region.amazonaws.com/recitations/...",
  "status": "pending",
  "likes_count": 0,
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

### Error Response:
```json
{
  "detail": "Error message here"
}
```

## 🎯 Next Steps

After testing with Postman:
1. Set up Firebase Authentication
2. Configure AWS S3 credentials
3. Set up MongoDB Atlas
4. Build the frontend application

Happy Testing! 🚀 