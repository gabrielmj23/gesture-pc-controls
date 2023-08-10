import cv2 as cv
import math
import numpy as np
import pygetwindow as gw
import screen_brightness_control as sbc
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from tracking import get_landmarks_list, drawModule, handsModule

def rescale(img, scale=1.5):
    """Rescale given image by a constant factor"""
    new_width = int(img.shape[1] * scale)
    new_height = int(img.shape[0] * scale)
    return cv.resize(img, (new_width, new_height), interpolation=cv.INTER_AREA)

def is_right_hand(thumb, pinky):
    """Uses thumb and pinky finger landmarks to determine if looking at a right hand or not.

    Only works when palm is shown on a generally normal position, otherwise gives opposite results"""
    return thumb[0] <= pinky[0]

def slope(pt1, pt2):
    """Gets slope of line connecting pt1 and pt2 given as two-value tuples"""
    return abs((pt2[1] - pt1[1]) / (pt2[0] - pt1[0] + 0.1))

def main():
    # Set up audio management
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None
    )
    volume = interface.QueryInterface(IAudioEndpointVolume)
    min_vol, max_vol, _ = volume.GetVolumeRange()
    vol = volume.GetMasterVolumeLevel()

    # Variables for changing windows
    window_change_delay = 0
    window_index = 0

    capture = cv.VideoCapture(0)
    while True:
        if window_change_delay > 0:
            window_change_delay -= 1

        _, frame = capture.read()
        if frame is not None:
            frame = rescale(cv.flip(frame, 1))

            # Write values
            output_volume = int(np.interp(vol, [min_vol, max_vol], [0, 100]))
            cv.putText(frame, f'Volume: {int(output_volume)}', (10, 30), cv.QT_FONT_NORMAL, 1, (0, 0, 0), 2)
            cv.putText(frame, f'Brightness: {sbc.get_brightness()[0]}', (10, 60), cv.QT_FONT_NORMAL, 1, (0, 0, 0), 2)

            hand_landmarks = get_landmarks_list(frame)
            if hand_landmarks is not None and len(hand_landmarks) > 0:
                # Draw landmarks
                for lms in hand_landmarks:
                    drawModule.draw_landmarks(frame, lms, handsModule.HAND_CONNECTIONS)
                # Get significant landmarks
                positions = []
                for hand in hand_landmarks:
                    for lm in hand.landmark:
                        positions.append((int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])))
                thumb, finger, finger_base = positions[4], positions[8], positions[5]
                length = math.hypot(finger[0] - thumb[0], finger[1] - thumb[1])
                
                # Handle volume and brightness with the right hand
                if (is_right_hand(thumb, positions[20])):
                    if (slope(thumb, finger) <= 1):
                        # Control volume
                        vol = np.interp(length, [10, 250], [min_vol, max_vol])
                        volume.SetMasterVolumeLevel(vol, None)
                    else:
                        # Control brightness
                        brightness = np.interp(length, [10, 250], [0, 100])
                        sbc.set_brightness(brightness)
                # Change windows when using left hand
                else:
                    index_slope = slope(finger_base, finger)
                    if window_change_delay == 0 and abs(index_slope) <= 2.5:
                        window_change_delay = 30
                        windows = gw.getAllWindows()
                        if window_index > len(windows):
                            window_index = 0
                        try:
                            windows[window_index].activate()
                        except:
                            windows[window_index].minimize()
                            windows[window_index].restore()
                        if index_slope >= 0:
                            window_index = (window_index + 1) % len(windows)
                        else:
                            window_index = (window_index - 1) % len(windows)
            
            cv.imshow("Video", frame)  # Show video
            if (cv.waitKey(20) & 0xFF) == 27:
                break
    
    # Finish video capture
    capture.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
