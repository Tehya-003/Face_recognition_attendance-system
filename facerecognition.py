import tkinter as tk
from tkinter import Label
import cv2
from PIL import Image, ImageTk
import datetime
import boto3
import io
import pyodbc

# MySQL database configuration
db_config = {
    'DRIVER': '{MySQL ODBC 8.0 Driver}',  
    'SERVER': 'localhost',                
    'DATABASE': 'database name',     
    'UID': 'username',               
    'PWD': 'your password'                
}

# Function to recognize face
def recognize_face(image_path):
    try:
        rekognition = boto3.client('rekognition', region_name='us-east-1')
        dynamodb = boto3.client('dynamodb', region_name='us-east-1')

        image = Image.open(image_path)
        stream = io.BytesIO()
        image.save(stream, format="JPEG")
        image_binary = stream.getvalue()

        response = rekognition.search_faces_by_image(
            CollectionId='famouspersons',
            Image={'Bytes': image_binary}
        )

        found = False
        for match in response['FaceMatches']:
            print(match['Face']['FaceId'], match['Face']['Confidence'])

            face = dynamodb.get_item(
                TableName='facerecognition',
                Key={'RekognitionId': {'S': match['Face']['FaceId']}}
            )

            if 'Item' in face:
                person_name = face['Item']['FullName']['S']
                print("Found Person: ", person_name)
                record_attendance(person_name)
                found = True

        if not found:
            print("Person cannot be recognized")
    except Exception as e:
        print("Error in recognize_face:", e)

# Function to record attendance in MySQL database
def record_attendance(name):
    try:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.datetime.now().strftime("%H:%M:%S")

        # Connect to the database
        conn_str = (
            f"DRIVER={db_config['DRIVER']};"
            f"SERVER={db_config['SERVER']};"
            f"DATABASE={db_config['DATABASE']};"
            f"UID={db_config['UID']};"
            f"PWD={db_config['PWD']}"
        )
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

          # Check if the employee exists
        cursor.execute("SELECT id, name FROM employees WHERE name = ?", name)
        employee = cursor.fetchone()

        if not employee:
            print(f"No employee found with name: {name}")
            cursor.close()
            conn.close()
            return

        employee_id = employee[0]
        employee_name = employee[1]

        # Check if the employee is already marked present today
        cursor.execute(
            "SELECT COUNT(*) FROM attendance WHERE employee_id = ? AND date = ?",
            (employee_id, current_date)
        )
        attendance_count = cursor.fetchone()[0]

        if attendance_count == 0:
            # Insert new attendance record for today
            cursor.execute(
                "INSERT INTO attendance (employee_id, employee_name, status, date, time) VALUES (?, ?, ?, ?, ?)",
                (employee_id, employee_name, 'Present', current_date, current_time)
            )
            conn.commit()

        # Count the number of unique days the employee has been marked present
        cursor.execute(
            "SELECT COUNT(DISTINCT date) FROM attendance WHERE employee_id = ?",
            (employee_id,)
        )
        unique_days = cursor.fetchone()[0]

        print(f"Employee {employee_name} (ID: {employee_id}) has been present for {unique_days}/30 days.")

    except pyodbc.Error as e:
        print("Error in database connection or query execution:", e)
    finally:
        # Close the connection
        cursor.close()
        conn.close()    


# Function to open the webcam and display the frames in the UI
def start_webcam():
    global cap
    cap = cv2.VideoCapture(0)
    update_frame()
    
def stop_webcam():
    global cap
    if cap:
        cap.release()
        cap = None
    label.config(image='')  # Clear the label

def update_frame():
    global cap
    if cap:
        ret, frame = cap.read()
        if ret:
            # Convert the frame to RGB (OpenCV uses BGR by default)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convert the frame to a PIL image
            img = Image.fromarray(frame)
            # Convert the PIL image to an ImageTk image
            imgtk = ImageTk.PhotoImage(image=img)
            # Update the label with the new image
            label.imgtk = imgtk
            label.configure(image=imgtk)
        # Call this function again after 10 milliseconds
        label.after(10, update_frame)

def capture_photo():
    global cap
    if cap:
        ret, frame = cap.read()
        if ret:
            # Save the frame as an image with a timestamp
            timestamp_filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.jpg")
            cv2.imwrite(timestamp_filename, frame)
            print(f"Photo saved as {timestamp_filename}")
            
            # Save the frame as "latest.jpg"
            latest_filename = "latest.jpg"
            cv2.imwrite(latest_filename, frame)
            print(f"Photo saved as {latest_filename}")
            
            # Call the recognize_face function with the "latest.jpg" filename
            recognize_face(latest_filename)

# Initialize the main window
window = tk.Tk()
window.title("Attendance System")

# Add a main heading
heading = tk.Label(window, text="Attendance System", font=("Helvetica", 16))
heading.pack(pady=10)

# Create a label to hold the webcam frames
label = Label(window)
label.pack()

# Create a frame for the buttons
button_frame = tk.Frame(window)
button_frame.pack(pady=10)

# Create a button to start the webcam
start_button = tk.Button(button_frame, text="Start Webcam", command=start_webcam)
start_button.pack(side=tk.LEFT, padx=10)

# Create a button to stop the webcam
stop_button = tk.Button(button_frame, text="Stop Webcam", command=stop_webcam)
stop_button.pack(side=tk.LEFT, padx=10)

# Create a button to capture a photo
capture_button = tk.Button(button_frame, text="Capture Photo", command=capture_photo)
capture_button.pack(side=tk.LEFT, padx=10)

# Start the Tkinter event loop
window.mainloop()

