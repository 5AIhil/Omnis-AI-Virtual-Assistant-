import streamlit as st
import requests
import datetime
import time

# Configuration
API_URL = "http://localhost:8000"

st.set_page_config(page_title="Virtual Assistant", page_icon="🤖", layout="wide")

st.title("🤖 AI Virtual Assistant")
st.markdown("A decoupled architecture powered by FastAPI and Streamlit.")

# Tabs for main interface
tab1, tab2, tab3 = st.tabs(["Chat", "Reminders", "Smart Home"])

# --- TAB 1: Chat Interface ---
with tab1:
    st.header("Chat with your Assistant")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("What is up?"):
        # Display user message
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Send to API
        try:
            response = requests.post(f"{API_URL}/api/chat", json={"message": prompt})
            if response.status_code == 200:
                reply = response.json().get("reply", "No reply received.")
            else:
                reply = f"Error: API returned status code {response.status_code}"
        except requests.exceptions.ConnectionError:
            reply = "Error: Could not connect to the backend API. Is FastAPI running?"

        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

# --- TAB 2: Reminders ---
with tab2:
    st.header("Manage Reminders")
    
    # Create Reminder Form
    with st.form("reminder_form"):
        st.subheader("Add a new reminder")
        task = st.text_input("Task Description")
        delay = st.number_input("Delay (in seconds)", min_value=1, max_value=86400, value=10)
        submitted = st.form_submit_button("Schedule Reminder")
        
        if submitted:
            try:
                res = requests.post(f"{API_URL}/api/reminders", json={"task": task, "delay_seconds": delay})
                if res.status_code == 200:
                    st.success(f"Reminder '{task}' scheduled successfully!")
                else:
                    st.error(f"Failed to schedule reminder: {res.text}")
            except requests.exceptions.ConnectionError:
                st.error("Connection error. Is FastAPI running?")

    st.divider()
    
    # View Active Reminders
    st.subheader("Current Reminders")
    if st.button("Refresh Reminders"):
        pass # Streamlit reruns on button click anyway
        
    try:
        reminders_res = requests.get(f"{API_URL}/api/reminders")
        if reminders_res.status_code == 200:
            reminders = reminders_res.json()
            if not reminders:
                st.info("No active reminders.")
            else:
                for rem_id, rem_data in reminders.items():
                    status_color = "green" if rem_data["status"] == "executed" else "orange"
                    st.markdown(f"**Task:** {rem_data['task']} | **Status:** :{status_color}[{rem_data['status']}] | **Trigger Time:** {rem_data['trigger_time']}")
        else:
            st.error("Failed to fetch reminders.")
    except requests.exceptions.ConnectionError:
         st.error("Connection error. Is FastAPI running?")

# --- TAB 3: Smart Home ---
with tab3:
    st.header("Smart Home Controls")
    
    try:
        sh_res = requests.get(f"{API_URL}/api/smart-home")
        if sh_res.status_code == 200:
            devices = sh_res.json()
            
            # Display devices in columns
            cols = st.columns(len(devices))
            for i, (device_id, device_info) in enumerate(devices.items()):
                with cols[i]:
                    st.subheader(device_info["name"])
                    current_state = device_info["state"]
                    
                    if device_id == "living_room_light":
                        # Toggle Switch for Light
                        is_on = current_state == "on"
                        new_on = st.toggle("Power", value=is_on, key=device_id)
                        new_state = "on" if new_on else "off"
                        if new_state != current_state:
                            requests.post(f"{API_URL}/api/smart-home", json={"device_id": device_id, "state": new_state})
                            st.rerun()
                            
                    elif device_id == "thermostat":
                        # Slider for Thermostat
                        new_temp = st.slider("Temperature (°F)", min_value=50, max_value=90, value=int(current_state), key=device_id)
                        if str(new_temp) != current_state:
                            requests.post(f"{API_URL}/api/smart-home", json={"device_id": device_id, "state": str(new_temp)})
                            
                    elif device_id == "front_door_lock":
                        # Radio buttons for Lock
                        options = ["locked", "unlocked"]
                        idx = options.index(current_state) if current_state in options else 0
                        new_state = st.radio("Lock Status", options, index=idx, key=device_id)
                        if new_state != current_state:
                            requests.post(f"{API_URL}/api/smart-home", json={"device_id": device_id, "state": new_state})
                            st.rerun()
                            
                    st.caption(f"Current State: {current_state.upper()}")
        else:
            st.error("Failed to fetch smart home state.")
    except requests.exceptions.ConnectionError:
        st.error("Connection error. Is FastAPI running?")
