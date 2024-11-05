from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from typing import List
import boto3
from botocore.exceptions import NoCredentialsError
from pydantic import BaseModel

S3_BUCKET = "vitaliy-serverless-api-files"

router = APIRouter( tags=["File"])

class BucketFile(BaseModel):
    name: str
    url: str

@router.post("/upload", response_model=BucketFile)
async def upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        
        s3_client = boto3.client('s3')
        
        s3_client.put_object(Bucket=S3_BUCKET, Key=file.filename, Body=contents)
        
        return BucketFile(name=file.filename, url=f"https://{S3_BUCKET}.amazonaws.com/{file.filename}")
    except NoCredentialsError:
        return JSONResponse(content={"error": "Credentials not available"}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
    
@router.get("/list", response_model=List[BucketFile])
async def list_files():
    try:
        s3_client = boto3.client('s3')
        
        response = s3_client.list_objects_v2(Bucket=S3_BUCKET)
        files = response.get('Contents', [])
        
        bucket_files = [
            BucketFile(name=file['Key'], url=f"https://{S3_BUCKET}.s3.amazonaws.com/{file['Key']}")
            for file in files
        ]
        
        return bucket_files
    except NoCredentialsError:
        return JSONResponse(content={"error": "Credentials not available"}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
    

