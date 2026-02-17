# 👶 Baby Sleep Monitoring System  
Real-time infant sleep monitoring using **Python**, **OpenCV**, and **Twilio WhatsApp API**.

This project detects a baby's sleep/awake state by analyzing eye activity using Haar Cascade models, and triggers alerts (local alarm + WhatsApp message) when the baby wakes up. Designed to be lightweight, affordable, and deployable on laptops or Raspberry Pi devices.

---

## 📌 Features
- **Real-time face & eye detection** using OpenCV Haar Cascades  
- **Sleep vs Awake classification** using threshold-based logic  
- **WhatsApp alerts** via Twilio API  
- **Local alarm sound** using the Winsound module  
- **Lightweight system** suitable for low-cost hardware  
- **Full project report included**  

---

## 🧠 How It Works
1. The webcam captures a video feed.  
2. Haar Cascade models detect the baby's **face** and **eyes**.  
3. Eye-open / eye-closed durations are tracked using counters.  
4. If eyes remain closed → **Sleeping**  
5. If eyes remain open for long → **Awake**  
6. When baby wakes up:  
   - A **local alarm** is triggered  
   - A **WhatsApp alert message** is sent to the caregiver  

---

## 🛠️ Tech Stack
- **Python 3.x**  
- **OpenCV**  
- **NumPy**  
- **Twilio WhatsApp API**  
- **Winsound (Windows alarm)**  

---
🎯 Future Improvements

Use deep learning (CNNs / Mediapipe) for better eye detection

Add cry detection using audio analysis

Add night vision support (IR cameras)

Build a mobile app dashboard

Add cloud logging + sleep analytics

🙌 Acknowledgements

OpenCV open-source community

Twilio API

Academic mentors and documentation resources
