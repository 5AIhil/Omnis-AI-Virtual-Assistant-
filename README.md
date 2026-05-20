# AI Virtual Assistant (Omnis)

A decoupled, full-stack Virtual Assistant application built with a **FastAPI** backend and a **Streamlit** frontend. 

It features:
- A responsive **Chat Interface** (currently using a mock service, ready for LLM integration).
- A **Task Scheduler** for managing and executing background reminders.
- A **Smart Home Dashboard** to view and control simulated IoT devices.

## 🚀 Quick Start

1. **Create and activate a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application:**
   Start both the backend and frontend simultaneously using the provided launcher script:
   ```bash
   python run.py
   ```
   
   - **Frontend UI:** `http://localhost:8501`
   - **Backend API:** `http://localhost:8000`
   - **Interactive API Docs:** `http://localhost:8000/docs`

## 📚 Documentation

For a comprehensive overview of the architecture, detailed setup instructions, API documentation, and future roadmap, please refer to the main [documentation.md](documentation.md) file.
