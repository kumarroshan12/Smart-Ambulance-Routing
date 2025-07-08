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