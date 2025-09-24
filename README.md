# Visionary_squad_project
Freshathon 2025 project
# 🔍 Reunify – AI-Powered Lost Person Finder

**Reunify** is a disaster response system that helps reunite missing individuals with their families using **facial recognition AI**, **metadata tagging**, and a **smart offline-ready architecture**. Designed by Dharanish, Dhaarani, Jayashree, Manoj (First Year AIML students), it’s a proof of concept for building scalable, humane tech in times of crisis.

---

## 🚀 Project Features

- 🔎 **Facial Recognition Matching**  
  Match uploaded images using DeepFace or FaceNet to identify lost or found individuals.

- 🧠 **AI-Generated Metadata**  
  Automatically extract data like estimated age, gender, emotion, and appearance from the uploaded image.

- 📝 **User-Submitted Metadata**  
  Users can input key information: Name, Parent’s Name, Contact, Last Seen Location, etc.

- 🌐 **Web Application**  
  A user-friendly interface to upload, match, and view person records.

- 📡 **Offline Data Transmission (LoRa Concept)**  
  Conceptual integration of **LoRaWAN** to enable metadata transmission in areas with no internet access.

---

## 🧱 Tech Stack

- **Frontend**: Vue.js / HTML / CSS  
- **Backend**: Python (Flask or FastAPI)  
- **Facial Recognition**: DeepFace / FaceNet  
- **Database**: MongoDB
- **Optional Tooling**: OpenCV, Pretrained ML for age/gender/emotion

---

## 🔁 Offline Flow (LoRa Concept)

While actual LoRa hardware is not developed, the architecture includes:

- 📷 Image + metadata collected by volunteer device
- 🛰️ Metadata (age, gender, GPS, etc.) transmitted via LoRa
- 🤝 Matching happens locally or once synced with the server

*Note: Hardware transmission is theoretical in this phase; only the concept and data structure are included.*

---

## 📂 Folder Structure

Reunify/
│
├── frontend/                  # VueJS frontend for UI
│   ├── public/                # Static assets (images, icons)
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   ├── pages/             # Home, UploadForm, MatchResult, etc.
│   │   ├── services/          # API calls to backend
│   │   ├── App.js             # Main app component
│   │   └── index.js           # React entry point
│   └── package.json           # Frontend dependencies
│
├── backend/                   # Backend logic (API + AI)
│   ├── api/                   # Flask or FastAPI routes
│   ├── models/                # Face recognition + metadata model code
│   ├── utils/                 # Image preprocessing, encoding, helpers
│   ├── database/              # MongoDB schema or Firestore config
│   ├── main.py                # Entry point (Flask or FastAPI)
│   └── requirements.txt       # Backend dependencies
│
├── data_samples/              # Sample image data for testing
│   ├── lost/                  # Example: uploaded by family
│   └── found/                 # Example: uploaded by volunteers
│
├── offline_mock/              # LoRa integration concept
│   ├── lora_flow_diagram.png  # Flowchart for offline flow
│   ├── payload_format.json    # Sample metadata structure
│   └── lora_notes.txt         # Architecture explanation
│
├── docs/                      # Project docs, research papers, references
│   ├── research_summary.md
│   └── system_architecture.md
│
├── .gitignore
├── README.md                  # our GitHub README file
