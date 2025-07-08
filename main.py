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
# ---------------- Map Visualization -------------------
def draw_map(start, end, route, reason, traffic_light_position, traffic_light_state, ambulance_position):
    m = folium.Map(location=start, zoom_start=14)
    
    # Mark Ambulance and Hospital
    folium.Marker(start, tooltip="🚑 Ambulance Start", icon=folium.Icon(color="red")).add_to(m)
    folium.Marker(end, tooltip="🏥 Hospital", icon=folium.Icon(color="green")).add_to(m)
    
    # Draw Route
    folium.PolyLine(route, color="blue", weight=6, tooltip=reason).add_to(m)

    # Add Traffic Light with dynamic state change
    traffic_light_icon = "green" if traffic_light_state == "Green" else "red"
    folium.Marker(traffic_light_position, tooltip=f"Traffic Light: {traffic_light_state}",
                  icon=folium.Icon(color=traffic_light_icon)).add_to(m)

    # Update Ambulance position
    folium.Marker(ambulance_position, tooltip="🚑 Ambulance", icon=folium.Icon(color="blue")).add_to(m)

    return m
# ---------------- Streamlit UI -------------------
st.set_page_config("Smart Ambulance Routing with V2X", layout="wide")
st.title("🚑 Smart Ambulance Routing with V2X Communication")

# Create tabs for the Ambulance and Hospital views
tabs = st.radio("Select View", ("Ambulance", "Hospital"))

if tabs == "Ambulance":
    # ---------------- Sidebar Configuration -------------------
    with st.sidebar:
        st.header("Simulation Settings")
        ambulance_spots = {
            "SRM Tech Park": (12.8251, 80.0460),
            "Medical Hostel": (12.8235, 80.0434),
            "Gate 1": (12.8232, 80.0445)
        }
        hospital_spots = {
            "SRM Hospital": (12.8199, 80.0382),
            "Chengalpattu GH": (12.6927, 79.9706)
        }

        amb_point = st.selectbox("Ambulance Location", list(ambulance_spots.keys()))
        hos_point = st.selectbox("Hospital Destination", list(hospital_spots.keys()))
        emergency_level = st.radio("Emergency Severity", ["Critical", "Moderate"])
        net_type = st.radio("Network Type", ["5G", "4G/LTE"])
        run = st.button("Run Smart Routing Simulation")
