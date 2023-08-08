import cv2 as cv
import mediapipe as mp
from tracking import get_landmarks_list, drawModule, handsModule

def rescale(img, scale=1.5):
    """Rescale given image by a constant factor"""
    new_width = int(img.shape[1] * scale)
    new_height = int(img.shape[0] * scale)
    return cv.resize(img, (new_width, new_height), interpolation=cv.INTER_AREA)

def main():
    capture = cv.VideoCapture(0)
    while True:
        success, frame = capture.read()
        if frame is not None:
            frame = rescale(cv.flip(frame, 1))
            hand_landmarks = get_landmarks_list(frame)
            if hand_landmarks is not None:
                for lms in hand_landmarks:
                    drawModule.draw_landmarks(frame, lms, handsModule.HAND_CONNECTIONS)
            cv.imshow("Video", frame)  # Show video

            if (cv.waitKey(20) & 0xFF) == 27:
                break
    
    # Finish video capture
    capture.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
