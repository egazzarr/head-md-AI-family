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
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

CONF_THRESH = 0.5

# ---------------- Serial setup ----------------
arduino = serial.Serial(
'/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_0353638323635141C072-if00',
9600,
timeout=1
)
time.sleep(2)

last_send_time = 0
SEND_DELAY = 5  # seconds
motor_was_active = False  # track state

while True:

    ret, frame = cap.read()
    if not ret:
        continue

    h, w = frame.shape[:2]

    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))
    face_model.setInput(blob)
    detections = face_model.forward()

    motor_active = False
    eye_count = 0

    # ---------------- Face detection ----------------
    if detections.shape[2] > 0 and detections[0, 0, :, 2].max() > CONF_THRESH:
        i = detections[0, 0, :, 2].argmax()
        confidence = detections[0, 0, i, 2]

        if confidence > CONF_THRESH:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            x1, y1, x2, y2 = box.astype(int)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            face_roi = frame[y1:y2, x1:x2]

            eyes = eye_cascade.detectMultiScale(face_roi)
            eye_count = len(eyes)

            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(face_roi, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 1)

            # -------- LOGIC --------
            motor_active = eye_count < 2  # TRUE if 0 or 1 eyes, FALSE if 2+ eyes

    # ---------------- SERIAL OUTPUT ON CHANGE ----------------
    now = time.time()

    if motor_active and not motor_was_active:
        # only send once when motor becomes active
        arduino.write(b"PRESS\n")
        print("PRESS sent (face turned away)")
        last_send_time = now

    motor_was_active = motor_active  # track previous state

    # ---------------- DISPLAY ----------------
    text = "TRUE" if motor_active else "FALSE"
    cv2.putText(frame, f"{text}  eyes:{eye_count}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    cv2.imshow("Face + Eye Detection", frame)
    key = cv2.waitKey(1)
    if key == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
