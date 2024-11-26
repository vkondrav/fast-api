from pydantic import BaseModel
from typing import Optional 
import requests
import json

class ModerationResponse(BaseModel):
    passing: bool
    message: Optional[str] = None

def moderate_message(message: str, moderator_url: str) -> ModerationResponse:
    
    try:
        params = {'message': message}
        worker_response = requests.get(moderator_url, params=params)
        
        if worker_response.status_code == 200:
            
            moderation_response = json.loads(worker_response.json().get('response'))
            
            return ModerationResponse(**moderation_response)
        else:
            raise Exception("Worker returned an error.")
        
    except Exception as e:
        
        print(f"An error occurred: {str(e)}")
        response = ModerationResponse(
            passing=False, message="An error occurred while processing the message."
        )
        
    return response