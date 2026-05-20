from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
import uuid
import logging

from models import (
    ChatRequest, ChatResponse, 
    ReminderRequest, ReminderResponse, 
    SmartHomeState, SmartHomeResponse
)

# APScheduler for background tasks
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI(title="Virtual Assistant API", version="1.0.0")

# Setup Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory storage for mock data
active_reminders = {}
smart_home_devices = {
    "living_room_light": {"name": "Living Room Light", "state": "off"},
    "thermostat": {"name": "Thermostat", "state": "72"},
    "front_door_lock": {"name": "Front Door Lock", "state": "locked"}
}

# Setup Background Scheduler
scheduler = BackgroundScheduler()
scheduler.start()

def execute_reminder(reminder_id: str, task: str):
    """Callback function triggered when a reminder is due."""
    logger.info(f"REMINDER EXECUTED: {task} (ID: {reminder_id})")
    if reminder_id in active_reminders:
        active_reminders[reminder_id]["status"] = "executed"

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()

@app.post("/api/chat", response_model=ChatResponse)
async def process_chat(request: ChatRequest):
    """
    Process user queries. Currently uses a mock service.
    Replace the mock logic below with an actual LLM integration (e.g., OpenAI, Anthropic).
    """
    query = request.message.lower()
    
    # Mock LLM Logic
    if "hello" in query or "hi" in query:
        reply = "Hello! I am your virtual assistant. How can I help you today?"
    elif "weather" in query:
        reply = "I cannot check live weather yet, but it's always a good idea to bring an umbrella!"
    elif "joke" in query:
        reply = "Why do programmers prefer dark mode? Because light attracts bugs!"
    else:
        reply = f"I understand you said: '{request.message}'. As a mock assistant, I don't have a specific answer for that yet."
        
    return ChatResponse(reply=reply)

@app.post("/api/reminders", response_model=ReminderResponse)
async def create_reminder(request: ReminderRequest):
    """Create and schedule a new reminder."""
    if request.delay_seconds <= 0:
        raise HTTPException(status_code=400, detail="Delay must be greater than 0 seconds.")
        
    reminder_id = str(uuid.uuid4())
    trigger_time = datetime.now() + timedelta(seconds=request.delay_seconds)
    
    active_reminders[reminder_id] = {
        "task": request.task,
        "status": "pending",
        "trigger_time": trigger_time.isoformat()
    }
    
    # Schedule the background job
    scheduler.add_job(
        execute_reminder,
        'date',
        run_date=trigger_time,
        args=[reminder_id, request.task],
        id=reminder_id
    )
    
    return ReminderResponse(
        id=reminder_id,
        task=request.task,
        status="pending",
        trigger_time=trigger_time.isoformat()
    )

@app.get("/api/reminders")
async def get_reminders():
    """View all reminders."""
    return active_reminders

@app.get("/api/smart-home")
async def get_smart_home_state():
    """Get the current state of all smart home devices."""
    return smart_home_devices

@app.post("/api/smart-home", response_model=SmartHomeResponse)
async def update_smart_home_state(request: SmartHomeState):
    """Update the state of a specific smart home device."""
    if request.device_id not in smart_home_devices:
        raise HTTPException(status_code=404, detail="Device not found.")
        
    smart_home_devices[request.device_id]["state"] = request.state
    
    return SmartHomeResponse(
        status="success",
        device_id=request.device_id,
        new_state=request.state
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
