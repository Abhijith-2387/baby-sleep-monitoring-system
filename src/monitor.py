import cv2
import numpy as np
import os
from twilio.rest import Client
import winsound
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twilio Credentials
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH_TOKEN")
WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")
WHATSAPP_TO = os.getenv("MY_WHATSAPP_TO")

# Load Haar Cascade Models
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

# WhatsApp Alert Function
def send_whatsapp_alert():
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH)
        message = client.messages.create(
            body="⚠️ Baby is Awake! Immediate attention required.",
            from_=WHATSAPP_FROM,
            to=WHATSAPP_TO
        )
        print("WhatsApp alert sent!")
    except Exception as e:
        print("Error sending WhatsApp message:", e)

# Local Alarm Function
def sound_alarm():
    freq = 2500  # Hz
    dur = 700    # milliseconds
    winsound.Beep(freq, dur)

# Start Webcam
cap = cv2.VideoCapture(0)

eye_open_count = 0
eye_closed_count = 0

ALERT_THRESHOLD = 20  # number of frames to confirm 'awake'

alert_sent = False

print("Starting Baby Sleep Monitoring System...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    eye_detected = False

    for (x, y, w, h) in faces:
        face_roi = gray[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(face_roi)

        if len(eyes) > 0:
            eye_detected = True

    # Update counters
    if eye_detected:
        eye_open_count += 1
        eye_closed_count = 0
    else:
        eye_closed_count += 1
        eye_open_count = 0

    # State Logic
    if eye_closed_count > ALERT_THRESHOLD:
        state = "Sleeping"
        alert_sent = False  # reset alert
    elif eye_open_count > ALERT_THRESHOLD:
        state = "Awake"
        if not alert_sent:
            sound_alarm()
            send_whatsapp_alert()
            alert_sent = True
    else:
        state = "Analyzing..."

    # UI Display
    cv2.putText(frame, f"State: {state}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow("Baby Sleep Monitoring System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
