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
    # ---------------- Simulating Ambulance Movement -------------------
    if run:
        amb_coords = ambulance_spots[amb_point]
        hos_coords = hospital_spots[hos_point]

        # Calculate Route and Network Slice Data
        route = [amb_coords, ((amb_coords[0] + hos_coords[0]) / 2, (amb_coords[1] + hos_coords[1]) / 2), hos_coords]
        selected_slice = "URLLC" if emergency_level == "Critical" else "eMBB"
        slice_data = SLICES[selected_slice]
        
        # Traffic light (static for demo purposes)
        traffic_light_coords = (12.8220, 80.0400)  # Near the route for demo purposes
        traffic_light_state = "Red"  # Initial state of traffic light
        
        # Map initialization
        st.subheader("📍 Final Route Map with V2X Communication")
        
        # Simulate the ambulance approaching the traffic light
        for i in range(1, 4):
            # Simulate movement
            ambulance_position = (amb_coords[0] + i * (hos_coords[0] - amb_coords[0]) / 4,
                                  amb_coords[1] + i * (hos_coords[1] - amb_coords[1]) / 4)
            
            # Update traffic light state earlier
            if i == 2:  # At the second step, ambulance approaches traffic light
                traffic_light_state = "Green"
            
            # Draw map at each step
            map_step = draw_map(amb_coords, hos_coords, route, "Ambulance route to hospital", traffic_light_coords, traffic_light_state, ambulance_position)
            folium_static(map_step)

            # Generate patient data and update session state
            patient_data = generate_patient_data()
            st.session_state.patient_data = patient_data

            time.sleep(2)  # Simulate a small delay between steps

        # After movement completes, display final map with traffic light in green
        final_map = draw_map(amb_coords, hos_coords, route, "Ambulance route to hospital", traffic_light_coords, "Green", hos_coords)
        folium_static(final_map)

        # Displaying route and network slice data
        st.subheader("🔍 Selected 5G Network Slice")
        st.markdown(f"**Slice Name:** {slice_data['name']}")
        st.markdown(f"**Use Case:** {slice_data['use_case']}")
        st.markdown(f"**Latency:** {slice_data['latency']} ms")
        st.markdown(f"**Bandwidth:** {slice_data['bandwidth']}")
        st.info(f"Network Slicing selected due to {emergency_level} severity.")

        st.markdown("---")
        st.subheader("📡 5G Slicing Explained")

        with st.expander("What is 5G Network Slicing?"):
            st.markdown("""
            **Network Slicing** is a key feature in 5G that lets operators divide their network into slices based on use cases:
            - **eMBB** for high-speed internet
            - **URLLC** for mission-critical tasks like real-time ambulance control
            - **mMTC** for IoT/sensors

            These slices share the same infrastructure but behave like separate networks.
            """)

        with st.expander("Why URLLC for Critical Cases?"):
            st.markdown("""
            In critical emergencies, we use the **URLLC** slice because:
            - It guarantees **low latency** and **high reliability**
            - It can prioritize ambulance vehicle over normal traffic
            - Supports **remote monitoring**, **teleconsultation**, and **priority routing**
            """)

    # ---------------- Display Real-Time Patient Data -------------------
    st.sidebar.subheader("🚑 Patient's Health Data")
    if 'patient_data' in st.session_state:
        patient_data = st.session_state.patient_data
        st.sidebar.write(f"**Heart Rate**: {patient_data['Heart Rate (BPM)']} BPM")
        st.sidebar.write(f"**Blood Oxygen Level**: {patient_data['Blood Oxygen Level (%)']}%")
        st.sidebar.write(f"**Snoring Rate**: {patient_data['Snoring Rate (dB)']} dB")
        st.sidebar.write(f"**Temperature**: {patient_data['Temperature (°C)']}°C")

    st.caption("Prototype simulation developed by Roshan Chaudhary for advanced 5G network applications in smart healthcare.")

elif tabs == "Hospital":
    # Hospital view: Real-time patient data
    st.title("🏥 Hospital Emergency Unit")

    st.subheader("🩺 Real-Time Patient Data Receiving")
    if 'patient_data' in st.session_state:
        patient_data = st.session_state.patient_data
        st.write(f"**Heart Rate**: {patient_data['Heart Rate (BPM)']} BPM")
        st.write(f"**Blood Oxygen Level**: {patient_data['Blood Oxygen Level (%)']}%")
        st.write(f"**Snoring Rate**: {patient_data['Snoring Rate (dB)']} dB")
        st.write(f"**Temperature**: {patient_data['Temperature (°C)']}°C")
        
    st.write("### Emergency Preparation Status:")
    st.write("The hospital is preparing for the patient with critical conditions. Medical staff are alerted.")
    