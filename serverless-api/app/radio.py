import asyncio
import httpx
from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(tags=["Radio"])

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

@router.get("/stations", response_model=List[RadioStation])
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