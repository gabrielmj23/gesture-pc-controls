# Control your PC with hand gestures

* Built with OpenCV and Mediapipe on Python 3.9
* Lets you control brightness, volume and active window using simple hand gestures

## Setup
* Run `pip install -r requirements.txt` in project directory
* Run `py main.py` to start the program

## Usage
* The program detects only one hand at a time
* With your right hand, your index finger and thumb control volume and brightness. If they form a line with a horizontal angle greater than 45°, it controls brightness, otherwise, it controls volume. Bring both fingers closer or bring them apart to change these values
* With your left hand, swipe it to change active screens. There's a delay of about a second (though may vary according to your camera FPS)

## Bugs
* The volume level shown on screen is not really accurate. This is due to using the `pycaw` library, which gives a range of volume values on the negatives, not corresponding with \[0-100] and being calculated using numpy's `interp` function on these non-ideal ranges
* Switching active windows may take a while given that `pygetwindow` often detects more windows than those visible to the user
* This is designed to be used while showing your palms to the camera at a relatively normal inclination, so expect undesired results when violating any of these rules
* Only tested on Windows 10!

**Enjoy 🐄**