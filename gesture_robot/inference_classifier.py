import pickle
import cv2
import mediapipe as mp
import numpy as np
import socket
import time

# ================= MODEL =================
model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

# ================= CAMERA =================
cap = cv2.VideoCapture(0)

# ================= MEDIAPIPE =================
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,   # IMPORTANT: chỉ 1 tay
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# ================= ESP32 =================
ESP32_IP = "192.168.1.134"
PORT = 1234

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.settimeout(5)

try:
    client.connect((ESP32_IP, PORT))
    print("ESP32 Connected")
except Exception as e:
    print("Cannot connect ESP32:", e)

# ================= LABELS =================
labels_dict = {
    '0': 'FORWARD',
    '1': 'BACKWARD',
    '2': 'LEFT',
    '3': 'RIGHT',
    '4': 'STOP'
}

commands = {
    '0': 'F',
    '1': 'B',
    '2': 'L',
    '3': 'R',
    '4': 'S'
}

previous_command = ""
last_send_time = 0
SEND_DELAY = 0.2  # chống spam command

# ================= LOOP =================
while True:

    data_aux = []

    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    H, W, _ = frame.shape

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:

        hand_landmarks = results.multi_hand_landmarks[0]

        mp_drawing.draw_landmarks(
            frame,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS
        )

        x_ = []
        y_ = []

        for lm in hand_landmarks.landmark:
            x_.append(lm.x)
            y_.append(lm.y)

        min_x = min(x_)
        min_y = min(y_)

        for lm in hand_landmarks.landmark:
            data_aux.append(lm.x - min_x)
            data_aux.append(lm.y - min_y)

        # ================= PREDICT =================
        if len(data_aux) == 42:

            prediction = model.predict([np.asarray(data_aux)])
            predicted_character = prediction[0]

            command = commands[predicted_character]

            # ================= SEND =================
            current_time = time.time()

            if command != previous_command and (current_time - last_send_time) > SEND_DELAY:

                try:
                    client.send(command.encode())
                    print("Sent:", command)

                    previous_command = command
                    last_send_time = current_time

                except Exception as e:
                    print("Send error:", e)

            # ================= UI =================
            cv2.putText(
                frame,
                labels_dict[predicted_character],
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.3,
                (0, 255, 0),
                3,
                cv2.LINE_AA
            )

    else:
        # không có tay -> STOP
        try:
            client.send(b"S")
        except:
            pass

    cv2.imshow('Gesture Robot Control', frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

# ================= CLEANUP =================
try:
    client.send(b"S")
except:
    pass

cap.release()
cv2.destroyAllWindows()
client.close()