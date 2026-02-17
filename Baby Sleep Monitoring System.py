import cv2
import csv
from datetime import datetime
import time
import pygame
from twilio.rest import Client

pygame.mixer.init()

def send_msg():
    account_sid = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    auth_token = 'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='whatsapp:+ZZZZZZZZZ',
        to='whatsapp:+XYXYXYXYXY',
        body='The baby just woke up!'        
    )

    print(message.sid)

def play_alert():
    pygame.mixer.music.load(r"D:\Project\Baby Sleep Monitor System\alert.wav")
    pygame.mixer.music.play()

def sleep_baby(st, sp):
    with open(r"D:\Project\Baby Sleep Monitor System\sleep_data.csv", 'a', newline='') as file:
        duration = round(sp - st)
        start_time = datetime.fromtimestamp(st).strftime('%H:%M:%S')
        end_time = datetime.fromtimestamp(sp).strftime('%H:%M:%S')
        write = csv.writer(file)
        write.writerow([start_time, end_time, f"{duration} seconds"])
        
        print(f"Baby slept from {start_time} to {end_time} for {duration} seconds")

face_cascade = cv2.CascadeClassifier(r"D:\Project\Baby Sleep Monitor System\haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(r"D:\Project\Baby Sleep Monitor System\haarcascade_eye.xml")

webcam = cv2.VideoCapture(0)

sleeping = False
sleep_st = None
wake_ct = 0
state = None
last_state = None


while 1:
    _, imageFrame = webcam.read()
    gray = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=1, minSize=(30,30))
    
    state = 'unknown'
    face_detected = False
    
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+h]
        roi_color = gray[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)

        if len(eyes) > 2:
            state = 'awake'
        else:
            state = 'sleeping'
        break
    
    curr_time = time.time()
    
    if state == 'sleeping':
        if not sleeping:
            sleeping = True
            sleep_st = curr_time
            
        elif sleeping and curr_time - sleep_st > 5 and last_state != "sleeping":
            last_state = 'sleeping'
            print("Baby is sleeping")
            
    elif state == 'awake':
        if sleeping:
            sleeping = False
            wake_time = curr_time
            duration = wake_time - sleep_st
            
            if duration > 5:
                sleep_baby(sleep_st, wake_time)
                print("Baby is awake")
                play_alert()
                send_msg()
                
            else:
                    print("Blinking")
                    
            last_state = 'awake'
            
        elif last_state != 'awake':
                print("Baby is awake")
                last_state = 'awake'
                
    else:
        if state == 'unknown' and not face_detected:
            print("Baby not in frame")
            last_state = "unknown"

                
    cv2.imshow("Baby Sleep Monitoring System", imageFrame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        webcam.release()
        cv2.destroyAllWindows()
        break