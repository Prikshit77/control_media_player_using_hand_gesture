import cv2
import mediapipe as mp
import numpy as np

class HandTracker:
    def __init__(self, window_size=(400, 400)):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1)
        self.mp_drawing = mp.solutions.drawing_utils
        self.prev_count = -1
        self.window_size = window_size

    def count_fingers(self, landmarks):
        cnt = 0
        thresh = (landmarks.landmark[0].y * 100 - landmarks.landmark[9].y * 100) / 2

        if (landmarks.landmark[5].y * 100 - landmarks.landmark[8].y * 100) > thresh:
            cnt += 1
        if (landmarks.landmark[9].y * 100 - landmarks.landmark[12].y * 100) > thresh:
            cnt += 1
        if (landmarks.landmark[13].y * 100 - landmarks.landmark[16].y * 100) > thresh:
            cnt += 1
        if (landmarks.landmark[17].y * 100 - landmarks.landmark[20].y * 100) > thresh:
            cnt += 1
        if (landmarks.landmark[5].x * 100 - landmarks.landmark[4].x * 100) > 6:
            cnt += 1
        return cnt

    def process_frame(self, frame):
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(frame_rgb)

        # Resize the frame to the fixed window size
        frame_resized = cv2.resize(frame, self.window_size)

        if result.multi_hand_landmarks:
            hand_landmarks = result.multi_hand_landmarks[0]
            
            # Draw landmarks on the resized frame
            self.mp_drawing.draw_landmarks(frame_resized, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

            finger_count = self.count_fingers(hand_landmarks)
            
            return frame_resized, finger_count, True
        else:
            return frame_resized, -1, False