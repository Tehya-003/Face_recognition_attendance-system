# 📸Face Recognition Attendance System
 Welcome to the Face Recognition Attendance System! Face Recognition Attendance System is an advanced end-to-end system that uses AWS Rekognition for face recognition and records attendance in an AWS RDS MySQL database.

The system includes a user-friendly interface built with Tkinter, allowing real-time face recognition using a webcam. Recognized faces are recorded in the attendance database with date and time.

## 🚀 Features
- **Real-time Face Recognition**: Capture photos in real-time using your webcam.
- **AWS Rekognition Integration**: Identify faces using Amazon Rekognition.
- **Automated Attendance Recording**: Attendance recorded in AWS RDS MySQL database.
- **Attendance Calculation**: Calculate attendance based on a default 30-day period.
- **User-friendly Interface**: Simple and intuitive Tkinter GUI.

## 📋 Table of Contents
- Requirements
- Installation
- Usage
- Database Setup
- Configuration
  
## 🛠 Requirements
- Python 3.8+
- Tkinter
- OpenCV
- Pillow
- AWS RDS MySQL database
- Boto3
- PyODBC
- MySQL
- MySQL ODBC 8.0 Driver
- AWS Account with Rekognition and DynamoDB configured

## 📦 Installation:

### Install Python Dependencies:

```bash
pip install -r requirements.txt
```

### Install MySQL ODBC Driver:
 #### Download and install the MySQL ODBC 8.0 Driver from [**MySQL's official website**](https://dev.mysql.com/downloads/connector/odbc/).

## 🎮 Usage
**Start the Application**:

```bash
python facerecognition.py
```

# Interact with the GUI:

- Start Webcam: Opens the webcam and starts the live feed.
- Stop Webcam: Stops the webcam feed.
- Capture Photo: Captures a photo, recognizes the face, and records attendance.

## 🗄️ Database Setup
 1.**Create the Necessary Tables**:
```sql
Copy code
CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    employee_name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);
```
 2.**Insert Employee Data**:
Populate the employees table with employee names and IDs.

## ⚙️ Configuration
 1. **AWS Configuration**:
Ensure AWS credentials are set up and that you have created a Rekognition collection named **famouspersons** and a DynamoDB table named **facerecognition**.Ensure AWS credentials are configured on your machine for accessing Rekognition, DynamoDB, and RDS.

 2. **MySQL Configuration**:
Update the **db_config** dictionary in **facerecognition.py** with your MySQL database credentials.
```ini
    [database]
    DRIVER = {MySQL ODBC 8.0 Driver}
    SERVER = localhost
    DATABASE = your_database_name
    UID = your_username
    PWD = your_password

    [aws]
    REGION = us-east-1
    COLLECTION_ID = famouspersons
```

## 📊 Attendance Calculation
Attendance is calculated based on a default 30-day period. If an employee is present, their attendance is recorded as a fraction (e.g., 1/30) and updated each day they are recognized.

## 📂 Additional Scripts

### putimages.py
This script uploads images to an S3 bucket and assigns metadata to each image.

### lambdafunction.py
This AWS Lambda function indexes faces in the S3 bucket using Rekognition and updates a DynamoDB table with the face ID and full name.

### Breaking Down the Repo
At first glance, the files in the repo may look intimidating and overwhelming. To avoid that, here is a quick guide:

- `facerecognition.py`: The main script that runs the face recognition and attendance system.
- `putimages.py`:Script to upload images to S3 with metadata
- `lambdafunction.py`:AWS Lambda function to index faces and update DynamoDB.
- `requirements.txt`: List of Python dependencies needed for the project.
- `README.md`: This readme file.

## How we built it
### AWS

1. **AWS S3 (Simple Storage Service)**:
* Created an S3 bucket named "famouspersons" to store images of employees.

2. **AWS DynamoDB**:
* Created a DynamoDB table named "facerecognition" to store data related to employee face recognition, such as face IDs and full names.

3. **Lambda Function**:
* Developed a Lambda function named "lambdafunction.py" that is triggered by S3 events.
* Utilized Rekognition to process uploaded images, detect faces, and match them against stored face templates.
* Updated the "facerecognition" DynamoDB table with detected faces.

4. **File Upload Script**:
* Created a Python script named "putimages.py" to directly upload photos from your PC to the S3 bucket "famouspersons".
* This script facilitates the process of uploading employee photos to AWS S3.

### MySQL
5. **Attendance Reporting (SQL Database)**:

1.Two SQL tables have been made:
* Employee Data Table: Contains detailed information about each employee, including their ID, name, and department.
* Attendance Table: Logs attendance records with timestamps, employee names, and their attendance status (present/absent).

### About facerecognition.py
This Python script is an Attendance System that integrates face recognition, image capture from a webcam, and database operations using Tkinter for the GUI, OpenCV for webcam access, Pillow for image processing, Boto3 for AWS services integration (Rekognition and DynamoDB), and pyodbc for MySQL database connectivity.

Here's a breakdown of its functionality:

- **MySQL Database Configuration**: The script initializes a dictionary db_config with MySQL database connection parameters like driver, server, database name, username, and password.

-  **Recognize Face Function**: The recognize_face function takes an image path as input, detects faces in the image using AWS Rekognition, matches them against a database of known faces stored in DynamoDB, and records attendance in the MySQL database for recognized individuals.

- **Record Attendance Function**: The record_attendance function records attendance in the MySQL database for recognized individuals. It checks if the employee is already marked present for the current date and calculates the number of unique days the employee has been present.

- **Webcam Functions**: Functions like start_webcam, stop_webcam, and capture_photo handle webcam access and image capture. They use OpenCV to capture frames from the webcam, convert them to PIL images, and display them in a Tkinter window.

- **Tkinter GUI**: The script creates a simple Tkinter GUI with buttons to start/stop the webcam and capture a photo. It displays the webcam feed and captured images in a Tkinter label.

- **Main Loop**: The main loop (window.mainloop()) runs the Tkinter GUI, allowing users to interact with the webcam and capture photos.


## How it Works
**Start the Application**:

- Run **python facerecognition.py** to launch the application.
- Use the buttons in the GUI to start/stop the webcam and capture photos.
  
**Capture and Recognize**:

- When you capture a photo, the image is saved locally and analyzed by AWS Rekognition.
- The system checks if the recognized face matches any employee in the database.
- Attendance is recorded in the MySQL database with the employee's ID, name, status, date, and time.
  
**Attendance Calculation**:

- Attendance is tracked over a 30-day period.
- Each presence is recorded as a fraction of the total period (e.g., 1/30).
- Daily attendance is updated automatically.

## Contributors
* Your Name: Tehya-003
* Made with ❤️ by Yellapu Tehya Poorna Seetu Akshaya
