import cv2 as cv
import math
import numpy as np
import screen_brightness_control as sbc
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from tracking import get_landmarks_list, drawModule, handsModule

def rescale(img, scale=1.5):
    """Rescale given image by a constant factor"""
    new_width = int(img.shape[1] * scale)
    new_height = int(img.shape[0] * scale)
    return cv.resize(img, (new_width, new_height), interpolation=cv.INTER_AREA)

def is_horizontal_enough(pt1, pt2):
    """Checks if line defined by pt1 and pt2 is horizontal enough to control volume.\n
    Points are given as two-value tuples"""
    m = abs((pt2[1] - pt1[1]) / (pt2[0] - pt1[0] + 0.1))
    return m < 1

def main():
    # Set up audio management
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None
    )
    volume = interface.QueryInterface(IAudioEndpointVolume)
    min_vol, max_vol, _ = volume.GetVolumeRange()

    capture = cv.VideoCapture(0)
    vol = volume.GetMasterVolumeLevel()
    while True:
        _, frame = capture.read()
        if frame is not None:
            frame = rescale(cv.flip(frame, 1))

            # Write values
            output_volume = int(np.interp(vol, [min_vol, max_vol], [0, 100]))
            cv.putText(frame, f'Volume: {int(output_volume)}', (10, 30), cv.QT_FONT_NORMAL, 1, (0, 0, 0), 2)
            cv.putText(frame, f'Brightness: {sbc.get_brightness()[0]}', (10, 60), cv.QT_FONT_NORMAL, 1, (0, 0, 0), 2)

            hand_landmarks = get_landmarks_list(frame)
            positions = get_landmarks_list(frame, format=True)
            
            if hand_landmarks is not None and len(hand_landmarks) > 0:
                # Draw landmarks
                for lms in hand_landmarks:
                    drawModule.draw_landmarks(frame, lms, handsModule.HAND_CONNECTIONS)
                # Get significant landmarks
                thumb, finger = positions[4], positions[8]
                length = math.hypot(finger[0] - thumb[0], finger[1] - thumb[1])
                # Check horizontal-ness
                if (is_horizontal_enough(thumb, finger)):
                    # Control volume
                    vol = np.interp(length, [10, 250], [min_vol, max_vol])
                    volume.SetMasterVolumeLevel(vol, None)
                else:
                    # Control brightness
                    brightness = np.interp(length, [10, 250], [0, 100])
                    sbc.set_brightness(brightness)
            cv.imshow("Video", frame)  # Show video
            if (cv.waitKey(20) & 0xFF) == 27:
                break
    
    # Finish video capture
    capture.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
