# 📸Face Recognition Attendance System
> Welcome to the Face Recognition Attendance System! This innovative project leverages Amazon Rekognition, a live webcam feed, and MySQL to create a seamless and efficient attendance recording system.

# 🚀 Features
-Real-time Face Recognition: Capture photos in real-time using your webcam.
-AWS Rekognition Integration: Identify faces using Amazon Rekognition.
-Automated Attendance Recording: Store attendance records in a MySQL database.
-Attendance Calculation: Calculate attendance based on a default 30-day period.
-User-friendly Interface: Simple and intuitive Tkinter GUI.

# 📋 Table of Contents
-Requirements
-Installation
-Usage
-Database Setup
-Configuration
-License

# 🛠 Requirements
-Python 3.7+
-Tkinter
-OpenCV
-Pillow
-Boto3
-PyODBC
-MySQL
-MySQL ODBC 8.0 Driver
-AWS Account with Rekognition and DynamoDB configured

# 📦 Installation:

# Install Python Dependencies:

bash
Copy code
pip install -r requirements.txt

# Install MySQL ODBC Driver:
Download and install the MySQL ODBC 8.0 Driver from MySQL's official website.

# 🎮 Usage
Start the Application:

bash
Copy code
python facerecognition.py

# Interact with the GUI:

Start Webcam: Opens the webcam and starts the live feed.
Stop Webcam: Stops the webcam feed.
Capture Photo: Captures a photo, recognizes the face, and records attendance.

# 🗄️ Database Setup
Create the Necessary Tables:

sql
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
Insert Employee Data:
Populate the employees table with employee names and IDs.

# ⚙️ Configuration
AWS Configuration:
Ensure AWS credentials are set up and that you have created a Rekognition collection named famouspersons and a DynamoDB table named facerecognition.

MySQL Configuration:
Update the db_config dictionary in g.py with your MySQL database credentials.

python
Copy code
db_config = {
    'DRIVER': '{MySQL ODBC 8.0 Driver}',
    'SERVER': 'localhost',
    'DATABASE': 'your_database_name',
    'UID': 'your_username',
    'PWD': 'your_password'
}
# 📊 Attendance Calculation
Attendance is calculated based on a default 30-day period. If an employee is present, their attendance is recorded as a fraction (e.g., 1/30) and updated each day they are recognized.

# Breaking Down the Repo
At first glance, the files in the repo may look intimidating and overwhelming. To avoid that, here is a quick guide:

-.gitignore: Specifies which files/folders to ignore when committing.
-facerecognition.py: The main script that runs the face recognition and attendance system.
-requirements.txt: List of Python dependencies needed for the project.
-README.md: This readme file.

# How it Works
Start the Application:

Run python g.py to launch the application.
Use the buttons in the GUI to start/stop the webcam and capture photos.
Capture and Recognize:

When you capture a photo, the image is saved locally and analyzed by AWS Rekognition.
The system checks if the recognized face matches any employee in the database.
Attendance is recorded in the MySQL database with the employee's ID, name, status, date, and time.
Attendance Calculation:

Attendance is tracked over a 30-day period.
Each presence is recorded as a fraction of the total period (e.g., 1/30).
Daily attendance is updated automatically.

# Contributors
Your Name: Tehya-003
Made with ❤️ by Yellapu Tehya Poorna Seetu Akshaya
