import cv2 as cv
import math
import numpy as np
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from tracking import get_landmarks_list, drawModule, handsModule

def rescale(img, scale=1.5):
    """Rescale given image by a constant factor"""
    new_width = int(img.shape[1] * scale)
    new_height = int(img.shape[0] * scale)
    return cv.resize(img, (new_width, new_height), interpolation=cv.INTER_AREA)

def main():
    # Set up audio management
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None
    )
    volume = interface.QueryInterface(IAudioEndpointVolume)
    min_vol, max_vol, _ = volume.GetVolumeRange()

    capture = cv.VideoCapture(0)
    while True:
        _, frame = capture.read()
        if frame is not None:
            frame = rescale(cv.flip(frame, 1))
            # Show volume
            cur_volume = np.interp(volume.GetMasterVolumeLevel(), [min_vol+15, max_vol], [0, 100])
            cv.putText(frame, f"Volumen: {int(cur_volume)}", (10, 30), cv.QT_FONT_NORMAL, 1, (255, 0, 0), 4)
            
            hand_landmarks = get_landmarks_list(frame)
            positions = get_landmarks_list(frame, format=True)
            
            if hand_landmarks is not None and len(hand_landmarks) > 0:
                # Draw landmarks
                for lms in hand_landmarks:
                    drawModule.draw_landmarks(frame, lms, handsModule.HAND_CONNECTIONS)
                # Get significant landmarks
                thumb, finger = positions[4], positions[8]
                length = math.hypot(finger[1] - thumb[1], finger[2] - thumb[2])
                # Control volume
                vol = np.interp(length, [10, 250], [min_vol, max_vol])
                volume.SetMasterVolumeLevel(vol, None)
            cv.imshow("Video", frame)  # Show video
            if (cv.waitKey(20) & 0xFF) == 27:
                break
    
    # Finish video capture
    capture.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
