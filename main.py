import streamlit as st
import folium
from streamlit_folium import folium_static
from geopy.distance import geodesic
import time
import random

# ---------------- Definitions for 5G Network Slicing -------------------
SLICES = {
    "eMBB": {
        "name": "Enhanced Mobile Broadband",
        "desc": "High-speed internet access, useful for high-res streaming and data-heavy operations.",
        "latency": 30,
        "bandwidth": "High",
        "use_case": "Telemedicine video calls"
    },
    "URLLC": {
        "name": "Ultra-Reliable Low Latency Communication",
        "desc": "Mission-critical applications requiring extremely low latency and high reliability.",
        "latency": 5,
        "bandwidth": "Moderate",
        "use_case": "Ambulance routing, real-time commands, remote surgery"
    },
    "mMTC": {
        "name": "Massive Machine Type Communication",
        "desc": "Connects a large number of devices with small data rates.",
        "latency": 100,
        "bandwidth": "Low",
        "use_case": "IoT health monitoring, sensor data upload"
    }
}

# ---------------- Traffic Light Function (for V2I Communication) -------------------
def update_traffic_lights(ambulance_position, traffic_light_position):
    distance = geodesic(ambulance_position, traffic_light_position).meters
    if distance < 500:  # If the ambulance is within 500 meters of the traffic light, make it green earlier
        return "Green"
    return "Red"

# ---------------- Simulate Real-Time Patient Data -------------------
def generate_patient_data():
    # Simulating patient health data
    return {
        "Heart Rate (BPM)": random.randint(80, 130),
        "Blood Oxygen Level (%)": random.randint(90, 100),
        "Snoring Rate (dB)": random.randint(30, 60),
        "Temperature (°C)": round(random.uniform(36.0, 38.0), 1)
    }
