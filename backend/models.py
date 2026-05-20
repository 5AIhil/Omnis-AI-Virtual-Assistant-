from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

class ReminderRequest(BaseModel):
    task: str
    delay_seconds: int

class ReminderResponse(BaseModel):
    id: str
    task: str
    status: str
    trigger_time: str

class SmartHomeState(BaseModel):
    device_id: str
    state: str

class SmartHomeResponse(BaseModel):
    status: str
    device_id: str
    new_state: str
