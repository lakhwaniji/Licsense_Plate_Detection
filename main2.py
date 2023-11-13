import cv2
import time
import urllib.request  # url requests (opening urls)
import numpy as np# serial communication with external devices
# URL of the ESP32-Cam's video stream
url = "http://192.168.220.193/cam-mid.jpg"
# 5-second delay before camera turns on
time.sleep(5)
# video capture object
cap = cv2.VideoCapture(url)
# serial connection
ser = serial.Serial('COM9', 9600)
# boolean variable to keep track of detection
detected = False
rotation_active = False  # To track servo rotation is active or not
while True:
    img_resp = urllib.request.urlopen(url)  # retrieve image from feed
    imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)  # convert to numpy array
    frame = cv2.imdecode(imgnp, -1) # decode using opencv's imdecode function
    cv2.imshow("Object Detection", frame)  # display the frame with the detected objects
    if cv2.waitKey(1) & 0xFF == ord('q'):  # loop breaks if the 'q' key is pressed
        break
# Release the video capture object and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
