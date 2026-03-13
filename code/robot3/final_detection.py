import cv2
import numpy as np
import os
import serial
import time

# ---------------- Paths ----------------
folder = os.path.dirname(os.path.abspath(__file__))
proto_path = os.path.join(folder, "packages/deploy.prototxt")
model_path = os.path.join(folder, "packages/res10_300x300_ssd_iter_140000_fp16.caffemodel")
eye_cascade_path = os.path.join(folder, "packages/haarcascade_eye.xml")

# ---------------- Load models ----------------
face_model = cv2.dnn.readNetFromCaffe(proto_path, model_path)
eye_cascade = cv2.CascadeClassifier(eye_cascade_path)

# ---------------- Camera setup ----------------
cap = cv2.VideoCapture(1, cv2.CAP_V4L2)
#cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Camera failed to open")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

CONF_THRESH = 0.5

# ---------------- Serial setup ----------------

arduino = serial.Serial('/dev/ttyACM2', 9600, timeout=1)
#arduino = serial.Serial(

#'/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_0353638323635141C072-if00',
#9600,
#timeout=1
#)
arduino.setDTR(False)
time.sleep(3)  # wait for Arduino bootloader to finish
arduino.flushInput()  # clear any startup messages
SEND_DELAY = 4  # seconds between serial writes
last_send_time = 0

print("Face detection running. Ctrl+C to quit.")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        h, w = frame.shape[:2]

        # ---------------- DNN Face Detection ----------------
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
                                     (104.0, 177.0, 123.0))
        face_model.setInput(blob)
        detections = face_model.forward()

        motor_active = False
        eye_count = 0

        if detections.shape[2] > 0 and detections[0, 0, :, 2].max() > CONF_THRESH:
            i = detections[0, 0, :, 2].argmax()
            confidence = detections[0, 0, i, 2]

            if confidence > CONF_THRESH:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                x1, y1, x2, y2 = box.astype(int)
                face_roi = frame[y1:y2, x1:x2]

                eyes = eye_cascade.detectMultiScale(face_roi)
                eye_count = len(eyes)
                motor_active = eye_count < 2

        else:
            motor_active = False

        # ---------------- SERIAL OUTPUT every SEND_DELAY ----------------
        now = time.time()
        if now - last_send_time >= SEND_DELAY:
            if motor_active:
                arduino.write(b"PRESS\n")
                print(f"{time.strftime('%H:%M:%S')} TRUE (motor ON) sent to Arduino")
            else:
                arduino.write(b"FALSE\n")
                print(f"{time.strftime('%H:%M:%S')} FALSE (motor OFF)")
            last_send_time = now


        time.sleep(0.3)  # reduce CPU usage

except KeyboardInterrupt:
    print("\nExiting program.")

finally:
    cap.release()
    arduino.close()
