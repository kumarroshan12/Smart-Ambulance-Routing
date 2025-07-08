# 🚑 Smart Ambulance Routing with V2X & 5G Network Slicing

A Streamlit-based simulation platform that demonstrates **smart ambulance routing** using **Vehicle-to-Everything (V2X)** communication and **5G Network Slicing** technologies. Built by **Roshan Chaudhary** to showcase advanced use cases in emergency healthcare and real-time data communication.

---

## 📌 Features

- 🗺️ Interactive **Folium map** showing ambulance routes with traffic light control
- 📡 Realistic simulation of **5G network slicing** (eMBB, URLLC, mMTC)
- 💉 Live **patient health data monitoring** (heart rate, SpO₂, snoring, temperature)
- 🚦 Simulated **traffic light switching** based on ambulance proximity
- 🏥 Dual view for **Ambulance Driver** and **Hospital Emergency Unit**
- ⏱️ Real-time emergency severity-based routing
- 🔄 Uses **geodesic calculations** for dynamic vehicle movement

---

## 🛠️ Tech Stack

| Component        | Technology       |
|------------------|------------------|
| Frontend         | Streamlit        |
| Maps             | Folium + Leaflet |
| Distance Calc    | Geopy             |
| UI Interactivity | streamlit-folium |
| Language         | Python            |

---

## 🔧 Installation

1. **Clone the repo**:

```bash
git clone https://github.com/kumarroshan12/smart-ambulance-routing.git
cd smart-ambulance-routing
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Example requirements.txt:

nginx
Copy
Edit
streamlit
folium
streamlit-folium
geopy
Run the app:

bash
Copy
Edit
streamlit run app.py
📷 Screenshots
🚑 Ambulance Routing Simulation

🏥 Hospital Dashboard

🧠 Concept Overview
This project demonstrates smart healthcare infrastructure leveraging:

URLLC (Ultra-Reliable Low Latency Communication) slice of 5G for emergency response

V2I communication to change traffic lights when ambulance approaches

Real-time data like vitals shared with hospital during transit

🧪 Simulation Settings
Choose ambulance starting point

Select hospital destination

Choose emergency severity (Critical / Moderate)

Select network type (4G / 5G)

View real-time routing, patient data, and hospital preparedness

📚 5G Slicing Types Used
Slice	Latency	Bandwidth	Use Case
eMBB	~30ms	High	HD video, Moderate emergencies
URLLC	~5ms	Moderate	Critical emergency routing
mMTC	~100ms	Low	IoT & sensors

👨‍💻 Author
Roshan Kumar Chaudhary
B.Tech CSE, SRM Institute of Science and Technology
Email: roshanchaudhary.dev@gmail.com
GitHub: @kumarroshan12

🏁 Future Scope
Live GPS integration with real ambulance feeds

Integration with Google Maps API

Emergency response optimization algorithms

Cloud deployment (Streamlit Cloud / Render)

📄 License
This project is licensed under the MIT License — feel free to use, modify, and share.

⭐ Give a Star!
If you found this project useful, feel free to give it a ⭐ on GitHub. It motivates further development!

yaml
Copy
Edit

---