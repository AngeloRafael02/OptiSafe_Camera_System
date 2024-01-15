
from datetime import datetime
from ultralytics import YOLO
import db
import fs
import threading
import socket
import time
import cv2
import os

# Crete temporary directory for screenshots
os.makedirs('screenshots', exist_ok=True)
# Load YOLO model
model = YOLO('best.pt')
# Open camera
cap = cv2.VideoCapture(0)

now = datetime.now()
show_live_camera = True  # Flag to toggle between live camera and uploaded content
last_screenshot_time = time.time()  # Variable to track the last screenshot time
screenshot_interval = 30  # Set the interval for taking screenshots (in seconds)

def generate_frames():
    global last_screenshot_time
    while show_live_camera:
        ret, frame = cap.read()
        if not ret:
            break
        else:
            results = model.track(frame, persist=True)

            if results and results[0].boxes:
                current_time = time.time()
                if current_time - last_screenshot_time >= screenshot_interval:
                    screenshot_thread = threading.Thread(target=take_screenshot, args=(results,))
                    screenshot_thread.start()  # Start a thread to take a screenshot
                    last_screenshot_time = current_time

            frame = results[0].plot()
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jPower Management Unit peg\r\n\r\n' + frame + b'\r\n')

          
def take_screenshot(results):
    '''Takes a Screenshot and saves it to a file server and its metadata in a database'''

    #Setting up screenshot and metadata 
    hostname = socket.gethostname()
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_fileLoc = f'screenshots/{hostname}_{current_time}.jpg' #temporary local storage location
    fileName = screenshot_fileLoc[len('screenshots/'):-len('.jpg')]

    #Create an array storing the frequencies of objects, 
    classArray = results[0].boxes.cls.numpy().copy()

    # Temporarily stores screenshot to local directory
    cv2.imwrite(screenshot_fileLoc, results[0].plot())
    newURL = f'{datetime.now().strftime("%Y-%m-%d")}/{hostname}'

    # Add screenshot to File Server
    fs.putSamba(screenshot_fileLoc, f'{newURL}/{screenshot_fileLoc}')
    
    # Add screenshot metadata to Database
    for value in classArray:
        db.upload_metadata(fileName, newURL, os.getenv('HOSTNAME_ID'), value)
    
    # Delete Photos from temp directory 
    try:
        os.remove(screenshot_fileLoc) #Delete Screenshot in local machine Permanently
        folder_name = "screenshots"
        folder_path = os.path.join(os.path.dirname(__file__), folder_name)
        file_list = os.listdir(folder_path)
        for file_name in file_list:
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Removed: {file_path}")
    except FileNotFoundError:
        print(f"File '{screenshot_fileLoc}' not found. Skipping removal.")
    except Exception as e:
        print(f"An error occurred: {e}")