## app.py
import streamlit as st
import cv2
import numpy as np
import os
import sys
import pyautogui
import time
from hand_tracking import HandTracker

def perform_media_action(finger_count):
    if finger_count == 1:
        pyautogui.press('right')  # Skip forward 10 seconds
        return "Skip Forward 10s"
    elif finger_count == 2:
        pyautogui.press('left')  # Skip backward 10 seconds
        return "Skip Backward 10s"
    elif finger_count == 3:
        pyautogui.press('up')  # Volume up
        return "Volume Up"
    elif finger_count == 4:
        pyautogui.press('down')  # Volume down
        return "Volume Down"
    elif finger_count == 5:
        pyautogui.press('space')  # Play/Pause
        return "Play/Pause"
    return "No Action"

def main():
    st.title("Hand Tracking Media Control App")

    # Set a fixed window size
    window_size = (400, 400)
    tracker = HandTracker(window_size)
    
    # Initialize session state
    if 'prev_count' not in st.session_state:
        st.session_state.prev_count = -1
    if 'action_start_time' not in st.session_state:
        st.session_state.action_start_time = 0
    if 'current_action' not in st.session_state:
        st.session_state.current_action = "No Action"

    # Streamlit layout
    col1, col2 = st.columns(2)

    with col1:
        run = st.checkbox('Run Hand Tracking')
        FRAME_WINDOW = st.image([])
        
    with col2:
        st.subheader("Detected Gesture")
        gesture_text = st.empty()
        st.subheader("Media Action")
        action_text = st.empty()
        st.subheader("Countdown")
        countdown_text = st.empty()

    cap = cv2.VideoCapture(0)

    ACTION_DELAY = 1  

    while run:
        ret, frame = cap.read()
        if not ret:
            st.write("Failed to capture frame from camera. Check camera connection.")
            break

        # Process the frame
        processed_frame, finger_count, hand_detected = tracker.process_frame(frame)

        current_time = time.time()

        if hand_detected:
            gesture_text.text(f"Fingers Detected: {finger_count}")

            if st.session_state.prev_count != finger_count:
                st.session_state.action_start_time = current_time
                st.session_state.prev_count = finger_count
                st.session_state.current_action = "No Action"

            time_elapsed = current_time - st.session_state.action_start_time
            time_remaining = max(0, ACTION_DELAY - time_elapsed)
            
            if time_remaining > 0:
                countdown_text.text(f"Action in: {time_remaining:.1f}s")
            else:
                countdown_text.text("Action ready!")

            if time_elapsed >= ACTION_DELAY and st.session_state.current_action == "No Action":
                action = perform_media_action(finger_count)
                st.session_state.current_action = action

            action_text.text(st.session_state.current_action)

        else:
            gesture_text.text("No Hand Detected")
            action_text.text("No Action")
            countdown_text.text("")
            st.session_state.prev_count = -1
            st.session_state.current_action = "No Action"

        # Convert the frame to RGB for Streamlit
        processed_frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)

        # Display the processed frame
        FRAME_WINDOW.image(processed_frame_rgb)

    cap.release()

if __name__ == '__main__':
    main()
