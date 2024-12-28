import cv2
import numpy as np
from mss import mss
import time
import pytesseract

monitor_area = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

output_file = "capture.avi"

# Video settings
fps = 30
codec = cv2.VideoWriter_fourcc(*'XVID')
output = cv2.VideoWriter(output_file, codec, fps, (monitor_area['width'], monitor_area['height']))
duration = 20

frame_count = 0
start_time = time.time()

frames_to_capture = fps * duration

with mss() as sct:
    while frame_count < frames_to_capture:

        screenshot = sct.grab(monitor_area)
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

        if frame_count % 60 == 0:
            text = pytesseract.image_to_string(frame, lang='pol')
            print("Wykryty tekst:", text)

        output.write(frame)

        frame_count += 1

output.release()
cv2.destroyAllWindows()