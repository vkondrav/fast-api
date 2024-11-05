from fastapi import APIRouter, Query, Response, Cookie
from pydantic import BaseModel
from typing import List, Optional
import boto3
import uuid
from datetime import datetime, timezone
from botocore.exceptions import NoCredentialsError
from fastapi.responses import JSONResponse
import random
import string
from ably import AblyRealtime
import os
from dotenv import load_dotenv

dynamodb = None
table = None
ably = None
channel = None

router = APIRouter(tags=["Chat"])

def get_dynamodb_resources():
    global dynamodb, table
    
    if dynamodb is None:
        dynamodb = boto3.resource('dynamodb')
        
    if table is None:
        table = dynamodb.Table("messages")

def generate_random_code(length=5):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

class Message(BaseModel):
    user: str
    date: str
    text: str
    id: str
        
@router.get("/messages", response_model=List[Message])
async def get_messages(sort_order: Optional[str] = Query("asc", enum=["asc", "dsc"])):
    
    global dynamodb, table
    
    try:
        get_dynamodb_resources()
            
        response = table.scan()
        items = response.get('Items', [])
        messages = [Message(**item) for item in items]
        sorted_messages = sorted(messages, key=lambda x: x.date, reverse=(sort_order == "dsc"))
        
        return sorted_messages
    except NoCredentialsError:
        return JSONResponse(content={"error": "Credentials not available"}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
 
async def publish_message(id):
    
    global ably, channel
    
    load_dotenv()
    
    ably_api_key = os.getenv('ABLY_API_KEY')
    
    if not ably_api_key:
        print("Ably API key not available")
        return
    
    if ably is None:
        ably = AblyRealtime(ably_api_key)
        await ably.connection.once_async('connected')
    
    if channel is None:
        channel = ably.channels.get('messages')

    await channel.publish('id', id)
    
def save_message(message):
    global table
    
    get_dynamodb_resources()
        
    table.put_item(Item=message.model_dump())
    
@router.post("/messages", response_model=Message)
async def create_message(
    response: Response, 
    text: str,
    user_id: Optional[str] = Cookie(None)):
    
    try:
        
        if not user_id:
            user_id = generate_random_code()
            
            days_30 = 30*24*60*60
            
            response.set_cookie(
                key="user_id",
                value=user_id,
                max_age=days_30
            )
        
        message_id = str(uuid.uuid4())
        current_time = datetime.now(timezone.utc).isoformat()
        
        message = Message(
            user=user_id,
            date=current_time,
            text=text,
            id=message_id
        )
        
        await publish_message(message_id)
        
        save_message(message)
        
        return message
    except NoCredentialsError:
        return JSONResponse(content={"error": "Credentials not available"}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)