from flask import Flask, render_template, Response
import cv2
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

# Initialize the camera
camera = cv2.VideoCapture(0)

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define the pins for motor driver
Motor1A = 24
Motor1B = 23
Motor2A = 27
Motor2B = 22

# Set up motor pins
GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor2A, GPIO.OUT)
GPIO.setup(Motor2B, GPIO.OUT)

def forward():
    GPIO.output(Motor1A, GPIO.HIGH)
    GPIO.output(Motor1B, GPIO.LOW)
    GPIO.output(Motor2A, GPIO.HIGH)
    GPIO.output(Motor2B, GPIO.LOW)

def backward():
    GPIO.output(Motor1A, GPIO.LOW)
    GPIO.output(Motor1B, GPIO.HIGH)
    GPIO.output(Motor2A, GPIO.LOW)
    GPIO.output(Motor2B, GPIO.HIGH)

def stop():
    GPIO.output(Motor1A, GPIO.LOW)
    GPIO.output(Motor1B, GPIO.LOW)
    GPIO.output(Motor2A, GPIO.LOW)
    GPIO.output(Motor2B, GPIO.LOW)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/forward')
def move_forward():
    forward()
    return '', 204

@app.route('/backward')
def move_backward():
    backward()
    return '', 204

@app.route('/stop')
def move_stop():
    stop()
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
