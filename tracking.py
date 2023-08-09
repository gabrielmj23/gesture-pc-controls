import cv2 as cv
import mediapipe as mp

# Get mediapipe modules and start detector
handsModule = mp.solutions.hands
drawModule = mp.solutions.drawing_utils
detector = handsModule.Hands(max_num_hands=1, min_detection_confidence=0.7)

def get_landmarks_list(img, format=False):
    """Gets list of significant hand landmarks in a given BGR image"""
    rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    results = detector.process(rgb)
    landmarks_list = results.multi_hand_landmarks
    if not format or landmarks_list is None:
        return landmarks_list  # Return normalized coordinates without landmark id
    formatted_list = []
    for hand in landmarks_list:
        for id, lm in enumerate(hand.landmark):
            formatted_list.append((id, int(lm.x * img.shape[1]), int(lm.y * img.shape[0])))
    return formatted_list
    
