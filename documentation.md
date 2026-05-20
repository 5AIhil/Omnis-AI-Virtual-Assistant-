# AI Virtual Assistant

## 1. Project Overview
The AI Virtual Assistant is a full-stack, decoupled application designed to simulate the core functionalities of a modern smart assistant. It features a responsive chat interface to interact with users, a task scheduler to manage and execute reminders in the background, and a smart home dashboard to monitor and control simulated IoT devices.

## 2. Architecture Diagram

```mermaid
flowchart LR
    subgraph Frontend [Frontend (Streamlit)]
        UI[User Interface]
        Chat[Chat Interface]
        Reminders[Reminder Controls]
        IoT[Smart Home Dashboard]
        
        UI --> Chat
        UI --> Reminders
        UI --> IoT
    end
    
    subgraph Backend [Backend (FastAPI)]
        API[FastAPI Router]
        ChatLogic[Chat Logic (Mock/LLM)]
        DeviceState[(In-Memory Device State)]
        
        API --> ChatLogic
        API --> DeviceState
    end
    
    subgraph Background [Background Worker]
        APS[APScheduler]
        TaskStore[(In-Memory Task Store)]
        
        APS <--> TaskStore
    end

    Chat -- REST POST --> API
    Reminders -- REST POST/GET --> API
    IoT -- REST POST/GET --> API
    API -- Schedules Tasks --> APS
```

## 3. Directory Structure
```text
.
├── documentation.md
├── requirements.txt
├── run.py              # Launcher script for both servers
├── backend/
│   ├── main.py         # FastAPI application and routing
│   └── models.py       # Pydantic data models
└── frontend/
    └── app.py          # Streamlit user interface
```

## 4. Setup & Installation

### Step 1: Clone or Navigate to the Repository
Navigate to the root directory of this project in your terminal.

### Step 2: Create a Virtual Environment
```bash
python -m venv venv
```

### Step 3: Activate the Virtual Environment
- **Mac/Linux:**
  ```bash
  source venv/bin/activate
  ```
- **Windows:**
  ```bash
  venv\Scripts\activate
  ```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Run the Project
Open a terminal, activate the virtual environment, and run the launcher script:
```bash
python run.py
```
This single command will start both:
- **FastAPI Backend Server**: Running on `http://localhost:8000` (API docs at `http://localhost:8000/docs`)
- **Streamlit Frontend App**: Running on `http://localhost:8501`
## 5. API Documentation

| Endpoint | Method | Expected Payload (JSON) | Response Structure (JSON) | Description |
| :--- | :--- | :--- | :--- | :--- |
| `/api/chat` | `POST` | `{"message": "string"}` | `{"reply": "string"}` | Processes user queries and returns a response. |
| `/api/reminders` | `POST` | `{"task": "string", "delay_seconds": integer}` | `{"id": "string", "task": "string", "status": "string", "trigger_time": "string"}` | Creates a new background reminder. |
| `/api/reminders` | `GET` | *None* | `{"id": {"task": "...", "status": "...", "trigger_time": "..."}}` | Retrieves a list of all active/executed reminders. |
| `/api/smart-home` | `GET` | *None* | `{"device_id": {"name": "...", "state": "..."}}` | Retrieves the state of all mocked smart home devices. |
| `/api/smart-home` | `POST`| `{"device_id": "string", "state": "string"}` | `{"status": "string", "device_id": "string", "new_state": "string"}` | Updates the state of a specific smart home device. |

## 6. Future Roadmap
To scale this virtual assistant into a production-ready system, the following enhancements are recommended:
- **WebSocket Integration:** Replace standard REST requests for the chat interface with WebSockets to support real-time streaming of LLM responses and instant push notifications for reminders.
- **Persistent Database:** Migrate the in-memory state (reminders and device states) to a robust relational database like PostgreSQL or a NoSQL solution like MongoDB.
- **Authentication & Security:** Implement OAuth2 with JWT tokens to secure endpoints and support individual user accounts.
- **Message Queue for Workers:** Replace the in-process `APScheduler` with a robust distributed task queue like Celery backed by Redis or RabbitMQ for scalable background task processing.
