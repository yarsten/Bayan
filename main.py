import streamlit as st
import cv2
import joblib
from datetime import datetime
import numpy as np

# Load the model
@st.cache_resource
def load_model():
    # Replace with your actual model path
    model = joblib.load("path/to/incident_detection_model.pkl")
    return model

model = load_model()

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Incident Reports", "Map View", "Settings"])

    if page == "Dashboard":
        dashboard_page(model)
    elif page == "Incident Reports":
        incident_reports_page()
    elif page == "Map View":
        map_view_page()
    elif page == "Settings":
        settings_page()

def dashboard_page(model):
    st.title("Dashboard - Real-Time Camera Feed")

    # Open video capture (use 0 for webcam or the video stream URL for an IP camera)
    cap = cv2.VideoCapture(0)  # or replace 0 with a video stream URL

    # Placeholder to display alerts
    st.header("Automated Crime Alerts")
    alert_placeholder = st.empty()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.write("Failed to capture video.")
            break

        # Preprocess frame for model (adjust this as needed for your model)
        input_data = preprocess_frame_for_model(frame)

        # Get model prediction
        incident_detected = model.predict([input_data])  # Modify based on model requirements

        # Display alerts if an incident is detected
        if incident_detected:
            alert_text = f"Incident Detected: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            alert_placeholder.warning(alert_text)

        # Display the current frame
        st.image(frame, channels="BGR")

        # Break loop with a stop button
        if st.button("Stop"):
            break

    cap.release()
    cv2.destroyAllWindows()

def preprocess_frame_for_model(frame):
    # Preprocess the frame (e.g., resize, normalize) as needed by your model
    # This is just an example; adjust based on your model's input requirements
    processed_frame = cv2.resize(frame, (224, 224))  # Example size
    processed_frame = processed_frame / 255.0  # Normalize if required
    return processed_frame.flatten()  # Flatten or reshape as needed

# Other page functions (Incident Reports, Map View, Settings) remain the same
def incident_reports_page():
    st.title("Incident Reports")
    st.write("List of all past incidents with more detailed information.")

def map_view_page():
    st.title("Map View")
    st.write("Interactive map of the incidents.")

def settings_page():
    st.title("Settings")
    st.write("Configure various settings here.")

if __name__ == "__main__":
    main()
