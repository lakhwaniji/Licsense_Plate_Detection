import time

from django.shortcuts import render
import threading
import json
from django.http import StreamingHttpResponse
import urllib.request  # url requests (opening urls)
from django.http import JsonResponse
import cv2
import numpy as np
import imutils
import easyocr
from .models import Registered_Vehicles,Entry_Exit
from datetime import datetime
from pyfirmata import Arduino, SERVO, util
from time import sleep
import paho.mqtt.publish as publish

IP="192.168.225.13"

# Create your views

def get_number_plate():
    img = cv2.imread("sample7.jpg")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bfilter = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(bfilter, 30, 200)
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    location = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 10, True)
        if (len(approx) == 4):
            location = approx
            break
    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [location], 0, 255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)
    (x, y) = np.where(mask == 255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    cropped_image = gray[x1:x2 + 1, y1:y2 + 1]
    reader = easyocr.Reader(['en'])
    result = reader.readtext(cropped_image)
    return (result[1][1])


def index(request):
    '''    try:
        # Assuming MQTT broker is running on localhost, change this accordingly
        mqtt_broker = "192.168.238.13"
        publish.single("start_rfid_scan", 180, hostname=mqtt_broker)
    except Exception as e:
        print(f"Error sending message to topic ")
    '''
    return render(request, 'index.html')


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture("http://192.168.225.193/cam-hi.jpg")
        img_resp = urllib.request.urlopen("http://192.168.225.193/cam-hi.jpg")  # retrieve image from feed
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        self.frame = cv2.imdecode(imgnp, -1)
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            img_resp = urllib.request.urlopen("http://192.168.225.193/cam-hi.jpg")  # retrieve image from feed
            imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
            self.frame = cv2.imdecode(imgnp, -1)


def detection(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass
    return render(request, 'detection.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def capture_image(request):
    img_resp = urllib.request.urlopen("http://192.168.225.193/cam-hi.jpg")
    imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
    frame = cv2.imdecode(imgnp, -1)
    cv2.imwrite("Vehicle.jpg", frame)
    result = get_number_plate()
    number = result.replace(" ", "")
    resp = check_number_plate(number)
    request.session["vehicle_number"]=number
    request.session["event"]=0
    return JsonResponse({'message': resp})


def check_number_plate(vehicle_number):
    results = Registered_Vehicles.objects.raw("select * from Car_Identification_registered_vehicles")
    for result in results:
        if result.vehicle_number == vehicle_number:
            vehicle_data = f"""Name -- > {result.first}
Vehicle_number -- > {result.vehicle_number}
Email -- > {result.email}
Unique Id -- >{result.uid}"""

            return vehicle_data
    return "No Data Found"


def visitor_vehicle(request):
    img_resp = urllib.request.urlopen("http://192.168.225.193/cam-hi.jpg")
    imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
    frame = cv2.imdecode(imgnp, -1)
    cv2.imwrite("visitor_vehicle.jpg", frame)
    result = get_number_plate()
    number = result.replace(" ", "")
    resp = f"{number} data is created"
    request.session["vehicle_number"]=number
    request.session["event"]=1
    return JsonResponse({'message': resp})


def rotateservo(pin, angle) :
    pass

def open():
    try:
        # Assuming MQTT broker is running on localhost, change this accordingly
        mqtt_broker = IP
        publish.single("servo", 90, hostname=mqtt_broker)
    except Exception as e:
        print(f"Error sending message to topic ")

def close():
    try:
        # Assuming MQTT broker is running on localhost, change this accordingly
        mqtt_broker = "192.168.225.13"
        publish.single("servo", 180, hostname=mqtt_broker)
    except Exception as e:
        print(f"Error sending message to topic ")

def opening_gate(request):
        number = request.session["vehicle_number"]
        e=request.session["event"]
        Entry_Exit.objects.create(vehicle_number=number, date_created=datetime.now(), event=e)
        open()
        time.sleep(5)
        close()
        return JsonResponse({'message': "The vehicle Entry is Successfull"})
    #arduino function for gate
