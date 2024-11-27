from fastapi import APIRouter, Query, Response, Cookie, Depends
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
from ably.realtime.realtime_channel import RealtimeChannel
import os
from dotenv import load_dotenv
from openai import OpenAI
import concurrent.futures

router = APIRouter(tags=["Chat"])
executor = concurrent.futures.ThreadPoolExecutor()


def get_openai_client() -> OpenAI:
    load_dotenv()

    return OpenAI()


def get_dynamodb_resource():
    return boto3.resource("dynamodb")


def get_dynamodb_table(dynamodb=Depends(get_dynamodb_resource)):
    return dynamodb.Table("messages")


async def get_ably() -> Optional[AblyRealtime]:
    load_dotenv()

    ably_api_key = os.getenv("ABLY_API_KEY")

    if not ably_api_key:
        print("Ably API key not available")
        return None

    ably = AblyRealtime(ably_api_key)

    await ably.connection.once_async("connected")

    return ably


def get_ably_channel(
    ably: Optional[AblyRealtime] = Depends(get_ably),
) -> Optional[RealtimeChannel]:

    if not ably:
        print("Ably not available")
        return None

    return ably.channels.get("messages")


async def publish_message(message, channel: Optional[RealtimeChannel]):

    if not channel:
        print("Channel not available")
        return

    await channel.publish("message", message.json())


class Message(BaseModel):
    user: str
    date: str
    text: str
    id: str
    moderation_pass: bool


@router.get("/messages", response_model=List[Message])
async def get_messages(
    sort_order: Optional[str] = Query("asc", enum=["asc", "dsc"]),
    table=Depends(get_dynamodb_table),
):

    try:
        response = table.scan()
        items = response.get("Items", [])
        messages = [Message(**item) for item in items]
        sorted_messages = sorted(
            messages, key=lambda x: x.date, reverse=(sort_order == "dsc")
        )

        return sorted_messages
    except NoCredentialsError:
        return JSONResponse(
            content={"error": "Credentials not available"}, status_code=400
        )
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)


def save_message(message, table):
    table.put_item(Item=message.model_dump())


def generate_user_id(length=5):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def get_user_id(response: Response, user_id: Optional[str] = Cookie(None)):
    if user_id is None:
        user_id = generate_user_id()

        days_30 = 30 * 24 * 60 * 60

        response.set_cookie(key="user_id", value=user_id, max_age=days_30)
    return user_id


class User(BaseModel):
    id: str


@router.get("/user", response_model=User)
async def get_user(response: Response, user_id: Optional[str] = Cookie(None)):
    return User(id=get_user_id(response, user_id))

        
@router.post("/messages", response_model=Message)
async def create_message(
    response: Response,
    text: str,
    moderation_pass: Optional[bool] = True,
    user_id: Optional[str] = Cookie(None),
    messages_table=Depends(get_dynamodb_table),
    messages_channel: Optional[RealtimeChannel] = Depends(get_ably_channel),
):

    try:

        user_id = get_user_id(response, user_id)

        message_id = str(uuid.uuid4())
        current_time = datetime.now(timezone.utc).isoformat()
        
        if moderation_pass:
            message_text = text
        else:
            message_text = f"Removed by moderator: {text}"

        message = Message(
            user=user_id, 
            date=current_time, 
            text=message_text, 
            id=message_id,
            moderation_pass=moderation_pass
        )

        await publish_message(message, messages_channel)

        executor.submit(save_message, message, messages_table)

        return message
    except NoCredentialsError:
        return JSONResponse(
            content={"error": "Credentials not available"}, status_code=400
        )
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)