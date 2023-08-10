import cv2 as cv
import mediapipe as mp

# Get mediapipe modules and start detector
handsModule = mp.solutions.hands
drawModule = mp.solutions.drawing_utils
detector = handsModule.Hands(max_num_hands=1, min_detection_confidence=0.7)

def get_landmarks_list(img):
    """Gets list of significant hand landmarks in a given BGR image"""
    rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    results = detector.process(rgb)
    return results.multi_hand_landmarks
