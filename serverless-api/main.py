import asyncio
import httpx
from fastapi import FastAPI, Query, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
from mangum import Mangum
import boto3
from botocore.exceptions import ClientError
import uuid
from datetime import datetime, timezone

app = FastAPI(title="Serverless Lambda")

class NowPlaying(BaseModel):
    title: str
    artist: str
    album: str

class RadioStation(BaseModel):
    id: int
    name: str
    tagline: str
    call_letters: str
    now_playing: Optional[NowPlaying] = None

@app.get("/radio-stations", response_model=List[RadioStation], tags=["Seekr"])
async def get_radio_stations(followed_stations: Optional[List[int]] = Query(None, example=[730, 34253, 605])):
    """
    Returns a list of radio stations sorted by followed stations.

    This endpoint retrieves a list of radio stations, each with their current 
    'now playing' data.
    
    Returns:
        json: A JSON object containing a list of radio stations with their 
              respective 'now playing' data.
    """
    
    stations_data, now_playing_data = await asyncio.gather(
        radio_stations(),
        now_playing()
    )

    stations = [RadioStation(**station) for station in stations_data]

    for station in stations:
        for playing in now_playing_data:
            if station.call_letters == playing["call_letters"]:
                station.now_playing = NowPlaying(**playing["now_playing"])

    if followed_stations:
        station_dict = {station.id: station for station in stations}
        followed = [station_dict[station_id] for station_id in followed_stations if station_id in station_dict]
        non_followed = [station for station in stations if station.id not in followed_stations]
        stations = followed + non_followed

    return stations
    
async def radio_stations():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://www.seekyoursound.com/wp-json/ang/v1/radio_stations")
        return response.json()
    
async def now_playing():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("https://radio.rogersdigitalmedia.com/service/now_playing")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching now playing: {e}")
            return []

class Message(BaseModel):
    user: str
    date: str
    text: str
    id: str
        
@app.get("/messages", response_model=List[Message], tags=["Chat"])
async def get_messages():
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('messages')
    
    try:
        response = table.scan()
        items = response.get('Items', [])
        return [Message(**item) for item in items]
    except Exception as e:
        print(f"Error fetching messages: {e}")
        return []
    
@app.post("/messages", response_model=Message, tags=["Chat"])
async def create_message(request: Request, text: str):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('messages')
    
    user_id = request.headers.get('User-Agent', 'unknown')
    message_id = str(uuid.uuid4())
    current_time = datetime.now(timezone.utc).isoformat()
    
    message = Message(
        user=user_id,
        date=current_time,
        text=text,
        id=message_id
    )
    
    try:
        table.put_item(Item=message.model_dump())
        return message
    except Exception as e:
        print(f"Error storing message: {e}")
        raise HTTPException(status_code=500, detail="Error storing message")

handler = Mangum(app)