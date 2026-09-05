# AI Anti-Glare Headlight System

## Computer Vision Based Adaptive Headlight Control

An AI-powered automotive safety system designed to detect approaching vehicles and bright headlights during night driving and intelligently determine the required headlight response to reduce glare and improve driving visibility.

---

## Project Overview

During night-time driving, high-beam headlights from opposite vehicles can produce intense glare. This glare can temporarily reduce the driver's visibility and make it difficult to identify road conditions, vehicles, pedestrians, and obstacles.

The AI Anti-Glare Headlight System uses Artificial Intelligence and Computer Vision to analyze a night-driving video, detect vehicles and headlights, estimate the glare level, and determine an appropriate adaptive beam-control action.

The current prototype is implemented as a video-based simulation using Python, YOLO, OpenCV, NumPy, Pandas, and Streamlit.

The user uploads a normal-speed night-driving video, and the system processes the video frame by frame.

---

## Problem Statement

Night driving becomes challenging when vehicles approaching from the opposite direction use high-beam headlights.

Excessive headlight brightness can:

- Cause temporary visual discomfort.
- Reduce the driver's visibility.
- Make it difficult to identify road obstacles.
- Increase driver reaction time.
- Increase the possibility of accidents.
- Create dangerous glare on highways and urban roads.
- Distract the driver during night-time driving.

In conventional vehicles, the driver generally has to manually switch between high beam and low beam.

Therefore, an intelligent system is required to automatically identify approaching vehicles, detect their headlights, analyze the glare level, and determine the appropriate headlight response.

---

## Proposed Solution

The proposed system uses a camera-based Artificial Intelligence and Computer Vision approach.

The system processes a night-driving video and performs the following operations:

1. Upload a night-driving video.
2. Read the video frame by frame.
3. Detect vehicles using YOLO.
4. Analyze detected vehicles between consecutive frames.
5. Estimate approaching vehicles.
6. Extract the detected vehicle regions.
7. Detect bright headlight regions using OpenCV.
8. Calculate a glare score.
9. Classify glare as LOW, MEDIUM, or HIGH.
10. Determine the appropriate beam-control action.
11. Generate an annotated anti-glare output video.
12. Generate a CSV report containing frame-by-frame data.
13. Display graphs for system analysis.

---

# System Workflow

```text
                  NIGHT-DRIVING VIDEO
                           |
                           v
                  VIDEO FRAME INPUT
                           |
                           v
                  VEHICLE DETECTION
                        (YOLO)
                           |
                           v
                APPROACHING VEHICLE
                     ANALYSIS
                           |
                           v
                  HEADLIGHT DETECTION
                      (OpenCV)
                           |
                           v
                    GLARE ANALYSIS
                           |
                           v
                  GLARE SCORE
                    CALCULATION
                           |
                           v
                LOW / MEDIUM / HIGH
                           |
                           v
                BEAM CONTROL DECISION
                           |
              +------------+------------+
              |            |            |
              v            v            v
         NORMAL BEAM   REDUCE BEAM   DIM + REDIRECT
              |            |            |
              +------------+------------+
                           |
                           v
                  ANTI-GLARE OUTPUT
                           |
                  +--------+--------+
                  |                 |
                  v                 v
            PROCESSED VIDEO      CSV REPORT
                                      |
                                      v
                              GRAPHICAL ANALYSIS

Main Features
1. Night-Driving Video Upload

The application allows users to upload a night-driving video.

Supported formats:

MP4
AVI
MOV
MKV

The uploaded video is used as the input source for the computer vision pipeline.

2. Vehicle Detection

The system uses YOLO for vehicle detection.

Currently supported vehicle classes include:

Car
Motorcycle
Bus
Truck

For every detected vehicle, the system obtains:

Vehicle class
Confidence score
Bounding box
Center position
Width
Height

Example:

CAR 0.91
TRUCK 0.87
MOTORCYCLE 0.82
BUS 0.89

The detected vehicles are displayed using bounding boxes in the processed output video.

3. Approaching Vehicle Detection

The system uses a basic tracking mechanism to compare detected vehicles between consecutive video frames.

The vehicle's:

Position
Width
Height
Bounding-box area

are compared with the previous frame.

If the vehicle becomes significantly larger, the system classifies it as:

APPROACHING

This provides a basic estimation of whether a vehicle is moving toward the camera.

4. Headlight Detection

After detecting a vehicle, the system extracts the vehicle region and analyzes the image using OpenCV.

The following image-processing techniques are used:

Grayscale conversion
Gaussian Blur
Brightness thresholding
Morphological opening
Morphological closing
Contour detection

Bright regions inside the detected vehicle area are treated as possible headlights.

The system calculates:

Headlight bounding box
Average brightness
Maximum brightness
Headlight area

Detected headlights are highlighted in the processed video.

5. Glare Analysis

The detected headlights are analyzed to estimate the glare condition.

The glare calculation considers:

Headlight brightness
Headlight area
Approaching vehicle condition

The final glare score is normalized between:

0 - 100

A higher score represents a stronger potential glare condition.

Glare Classification
Glare Score	Glare Level
0 - 39	LOW
40 - 69	MEDIUM
70 - 100	HIGH
LOW Glare

When the glare score is low:

Glare Level: LOW
Beam Intensity: 100%
Beam Direction: NORMAL
Action: NORMAL BEAM

The system does not recommend any beam reduction.

MEDIUM Glare

When the glare score is medium:

Glare Level: MEDIUM
Beam Intensity: 60%
Beam Direction: SLIGHTLY DOWNWARD
Action: REDUCE BEAM

The system recommends reducing the beam intensity and slightly redirecting the beam downward.

HIGH Glare

When the glare score is high:

Glare Level: HIGH
Beam Intensity: 30%
Beam Direction: DOWNWARD
Action: DIM + REDIRECT

The system recommends significantly reducing the simulated beam intensity and redirecting the beam downward.

6. Adaptive Beam Control Simulation

The current version is a software prototype.

It does not physically control a real vehicle headlight.

Instead, it simulates the required beam-control response based on the detected glare level.

The system generates decisions such as:

NORMAL BEAM
REDUCE BEAM
DIM + REDIRECT

The simulated beam intensity is:

LOW GLARE    -> 100%
MEDIUM GLARE -> 60%
HIGH GLARE   -> 30%

The beam direction is:

LOW GLARE    -> NORMAL
MEDIUM GLARE -> SLIGHTLY DOWNWARD
HIGH GLARE   -> DOWNWARD
7. Annotated Output Video

The processed video contains visual information about the AI analysis.

The output video displays:

Vehicle bounding boxes
Vehicle type
Confidence score
Approaching vehicle indication
Headlight bounding boxes
Glare level
Glare score
Number of vehicles
Number of approaching vehicles
Number of detected headlights
Beam intensity
Beam direction
Recommended action

Example:

AI ANTI-GLARE
HEADLIGHT SYSTEM

GLARE LEVEL
HIGH

GLARE SCORE
82 / 100

VEHICLES: 2
APPROACHING: 1
HEADLIGHTS: 2

BEAM INTENSITY: 30%
BEAM: DOWNWARD

ACTION: DIM + REDIRECT
8. CSV Data Logging

For every processed video, the system automatically generates a CSV report.

The CSV contains frame-by-frame system information.

The report includes:

Frame
Vehicles
Approaching Vehicles
Headlights
Glare Score
Glare Level
Beam Intensity
Beam Direction
Action

Example:

Frame	Vehicles	Approaching Vehicles	Headlights	Glare Score	Glare Level	Beam Intensity
1	1	0	1	25	LOW	100
2	1	0	1	31	LOW	100
3	1	1	2	65	MEDIUM	60
4	1	1	2	82	HIGH	30
9. Graphical Analysis

The Streamlit dashboard provides graphical analysis based on the generated CSV file.

The system displays several graphs.

Glare Score vs Frame

This graph shows how the detected glare score changes throughout the video.

Vehicle Detection vs Frame

This graph displays:

Total vehicles
Approaching vehicles
Headlights Detected vs Frame

This graph displays the number of detected headlights for each frame.

Adaptive Beam Intensity vs Frame

This graph shows how the simulated beam intensity changes according to the detected glare condition.

Glare Level Distribution

This graph displays the number of:

LOW glare frames
MEDIUM glare frames
HIGH glare frames
Average System Parameters

The system calculates and displays average:

Vehicle count
Approaching vehicle count
Headlight count
Glare score
Beam intensity
Technologies Used
Programming Language

Python

Artificial Intelligence

YOLO

YOLO is used for detecting vehicles in the input video.

Computer Vision

OpenCV

OpenCV is used for:

Video processing
Image preprocessing
Brightness analysis
Headlight detection
Contour detection
Bounding-box visualization
Web Application

Streamlit

Streamlit is used to create the interactive web interface.

Numerical Processing

NumPy

NumPy is used for image and numerical operations.

Data Analysis

Pandas

Pandas is used for:

Reading CSV reports
Processing detection data
Generating graphical analysis
Video Encoding

FFmpeg / imageio-ffmpeg

Used to generate browser-compatible H.264 MP4 output.

Project Architecture
AI_Anti_Glare_Headlight
│
├── app.py
│
├── video_processor.py
│
├── vehicle_detection.py
│
├── vehicle_tracker.py
│
├── headlight_detection.py
│
├── glare_analysis.py
│
├── beam_control.py
│
├── requirements.txt
│
├── input_videos
│   └── Uploaded night-driving videos
│
├── output_videos
│   └── Processed anti-glare videos
│
├── models
│   └── AI model files
│
├── results
│   └── CSV analysis reports
│
├── .streamlit
│   └── config.toml
│
└── venv
File Description
app.py

The main Streamlit application.

Responsibilities:

Video upload
Input video preview
Processing button
Processed video display
Video download
CSV download
Processing summary
Graphical analysis
Detection data table
video_processor.py

This is the main video-processing module.

Responsibilities:

Read video frames
Detect vehicles
Track vehicles
Detect headlights
Calculate glare
Determine beam-control action
Draw annotations
Generate processed video
Generate CSV report
Convert output video to H.264
vehicle_detection.py

This module performs vehicle detection using YOLO.

Supported classes:

Car
Motorcycle
Bus
Truck
vehicle_tracker.py

This module provides basic vehicle tracking between consecutive frames.

It compares vehicle:

Position
Size
Class

and estimates whether the vehicle is approaching.

headlight_detection.py

This module detects bright regions inside detected vehicle bounding boxes using OpenCV.

The process includes:

Vehicle ROI
    ↓
Grayscale
    ↓
Gaussian Blur
    ↓
Brightness Threshold
    ↓
Morphological Processing
    ↓
Contour Detection
    ↓
Possible Headlights
glare_analysis.py

This module calculates the glare score.

It returns:

Glare Score
Glare Level

Possible glare levels:

LOW
MEDIUM
HIGH
beam_control.py

This module determines the beam-control response.

The logic is:

LOW
↓
100% Beam
↓
NORMAL
MEDIUM
↓
60% Beam
↓
SLIGHTLY DOWNWARD
HIGH
↓
30% Beam
↓
DOWNWARD
Installation
1. Clone the Repository
git clone <YOUR_GITHUB_REPOSITORY_URL>

Move into the project directory:

cd AI_Anti_Glare_Headlight
2. Create a Virtual Environment

For Windows:

python -m venv venv

Activate the environment:

.\venv\Scripts\Activate.ps1

If PowerShell blocks activation:

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Then activate:

.\venv\Scripts\Activate.ps1
3. Install Dependencies

Upgrade pip:

python -m pip install --upgrade pip

Install the required packages:

python -m pip install -r requirements.txt
4. Run the Application

Run:

python -m streamlit run app.py

The Streamlit application will open in the browser.

requirements.txt
streamlit
opencv-python
numpy
pandas
ultralytics
imageio-ffmpeg
Input Video Requirements

For the best project demonstration, use a normal-speed night-driving video.

Recommended specifications:

Video Format: MP4
Resolution: 1280x720 or 1920x1080
Frame Rate: 25-30 FPS
Duration: 10-60 seconds
Camera: Front-facing / Dashboard
Environment: Night
Traffic: Moderate
Headlights: Clearly visible
Vehicles: Approaching the camera
Speed: Normal
Recommended Input Video Characteristics

A good input video should contain:

Front-facing road view
Normal-speed driving
Night-time environment
Multiple vehicles
Vehicles approaching from the opposite direction
Bright visible headlights
Good image quality
Minimum motion blur
Clear road visibility

The current system works best when an approaching vehicle becomes larger as it moves toward the camera.

Videos to Avoid

Avoid videos containing:

Slow motion
Timelapse
Drone footage
Extremely dark scenes
No vehicles
No visible headlights
Heavy motion blur
Very low resolution
Excessive camera movement

A normal-speed dashboard or front-facing night-driving video is preferred.

How to Use the Application
Step 1: Start the Application
python -m streamlit run app.py
Step 2: Upload a Video

Select a suitable night-driving MP4 video.

Step 3: Preview the Video

The uploaded video will be displayed in the Streamlit interface.

Step 4: Start Processing

Click:

PROCESS VIDEO
Step 5: AI Processing

The system processes the video frame by frame.

The processing pipeline is:

Input Video
    ↓
YOLO Vehicle Detection
    ↓
Vehicle Tracking
    ↓
Approaching Vehicle Analysis
    ↓
Headlight Detection
    ↓
Glare Analysis
    ↓
Beam Control Decision
    ↓
Output Video
    ↓
CSV Report
    ↓
Graphical Analysis
Step 6: View Output

The processed anti-glare video is displayed in the application.

Step 7: Download Results

The application provides options to download:

Processed video
CSV report
Example Processing
INPUT VIDEO

Night Driving
      |
      v
YOLO Vehicle Detection
      |
      v
2 Vehicles Detected
      |
      v
Vehicle Tracking
      |
      v
1 Approaching Vehicle
      |
      v
Headlight Detection
      |
      v
2 Headlights Detected
      |
      v
Glare Analysis
      |
      v
Glare Score = 82
      |
      v
Glare Level = HIGH
      |
      v
Beam Control
      |
      v
Beam Intensity = 30%
      |
      v
Beam Direction = DOWNWARD
      |
      v
Action = DIM + REDIRECT
Output Files

After processing a video, the system generates an output video.

Example:

output_videos/
└── night_drive_ANTI_GLARE.mp4

The system also generates a CSV report:

results/
└── night_drive_ANTI_GLARE_report.csv
Sample Output Information

The processed video may display:

AI ANTI-GLARE
HEADLIGHT SYSTEM

GLARE LEVEL: HIGH

GLARE SCORE: 82 / 100

VEHICLES: 2

APPROACHING: 1

HEADLIGHTS: 2

BEAM INTENSITY: 30%

BEAM: DOWNWARD

ACTION: DIM + REDIRECT
Advantages
AI-based vehicle detection
Automated approaching vehicle estimation
Headlight detection
Glare analysis
Adaptive beam-control simulation
Frame-by-frame analysis
CSV data logging
Graphical visualization
Interactive Streamlit interface
Browser-compatible MP4 output
Easy to demonstrate
Suitable for automotive safety applications
Can be extended to real hardware
Combines AI, Computer Vision, and Mechanical Engineering
Limitations

The current implementation is a software prototype.

1. Video-Based Input

The system currently processes uploaded videos rather than a live camera feed.

2. Basic Approaching Detection

Approaching vehicle detection is currently based on changes in bounding-box size between frames.

3. Headlight Detection

Bright regions inside detected vehicle bounding boxes are considered possible headlights.

Other bright objects may sometimes be detected as headlights.

4. Simulated Beam Control

The current system generates beam-control decisions but does not physically control real vehicle headlights.

5. Environmental Conditions

Performance can be affected by:

Rain
Fog
Reflections
Street lights
Camera exposure
Headlight brightness
Video quality
Weather conditions
Motion blur
Future Scope
1. Real-Time Camera Integration

The uploaded video can be replaced with a real-time camera mounted at the front of a vehicle.

Front Camera
     |
     v
Real-Time AI Processing
     |
     v
Vehicle Detection
     |
     v
Headlight Detection
     |
     v
Glare Analysis
     |
     v
Beam Control
2. Edge AI Deployment

The system can be deployed on embedded hardware such as:

Raspberry Pi
NVIDIA Jetson
Other edge-AI platforms

This can allow the system to operate inside a real vehicle.

3. Real Headlight Control

The software decision can be connected to a real headlight control system.

For example:

AI Decision
     |
     v
Microcontroller / ECU
     |
     v
Motor Driver / Lighting Controller
     |
     v
Headlight Adjustment
4. Servo-Based Beam Direction Control

A servo motor or suitable actuator can be used to physically adjust the headlight direction.

Example:

HIGH GLARE
     |
     v
Control Signal
     |
     v
Servo Motor
     |
     v
Headlight Moves Downward
5. Automatic Headlight Intensity Control

A suitable automotive lighting control circuit can be used to vary the headlight intensity.

Example:

LOW GLARE
    ↓
100% Intensity

MEDIUM GLARE
    ↓
60% Intensity

HIGH GLARE
    ↓
30% Intensity
6. Advanced Vehicle Tracking

A more advanced tracking algorithm can provide:

Unique vehicle IDs
Reliable vehicle tracking
Vehicle trajectory
Vehicle movement direction
Distance estimation
Time-to-collision estimation
7. Distance Estimation

The system can be enhanced to estimate the distance between the host vehicle and the approaching vehicle.

Example:

Approaching Vehicle
       |
       v
Distance Estimation
       |
       v
35 meters

Distance can then be included in glare estimation.

8. Advanced Glare Estimation

Future versions can consider additional parameters:

Headlight brightness
Headlight size
Vehicle distance
Vehicle position
Vehicle speed
Camera exposure
Ambient brightness
Road illumination
Weather conditions
Headlight direction

This can improve the reliability of glare estimation.

9. ADAS Integration

The system can potentially be integrated into an Advanced Driver Assistance System.

Forward Camera
      |
      v
AI Perception
      |
      v
Vehicle Detection
      |
      v
Vehicle Tracking
      |
      v
Headlight Detection
      |
      v
Glare Estimation
      |
      v
Adaptive Headlight Control
      |
      v
Driver Safety
Applications

The proposed system can be further developed for:

Passenger vehicles
Cars
Commercial vehicles
Highway driving
Urban night driving
Automotive safety systems
Advanced Driver Assistance Systems
Intelligent transportation systems
Smart vehicle lighting systems
Adaptive headlight systems
Project Objective

The main objective of this project is to develop a computer vision-based prototype capable of identifying approaching vehicles and analyzing their headlights to determine an appropriate adaptive headlight response.

The project combines:

Artificial Intelligence
        +
Computer Vision
        +
Automotive Engineering
        +
Adaptive Control

to address the problem of headlight glare during night driving.

Expected Outcome

The system is expected to:

Detect vehicles during night driving.
Identify approaching vehicles.
Detect bright headlight regions.
Estimate glare intensity.
Classify glare conditions.
Determine an adaptive beam-control action.
Generate an annotated output video.
Generate frame-by-frame CSV data.
Generate graphical analysis.
Provide a foundation for future hardware implementation.
Project Status
Project Type:
AI + Computer Vision + Automotive Safety

Project Status:
Working Software Prototype

Input:
Night-Driving MP4 Video

Processing:
Frame-by-Frame

Vehicle Detection:
YOLO

Vehicle Tracking:
Basic Bounding-Box Tracking

Headlight Detection:
OpenCV

Glare Analysis:
Implemented

Glare Classification:
LOW / MEDIUM / HIGH

Beam Control:
Simulated

CSV Logging:
Implemented

Graphical Analysis:
Implemented

Real-Time Camera:
Future Scope

Physical Headlight Control:
Future Scope
Performance Considerations

The quality of the output depends on the input video.

Better results can generally be obtained with:

High-resolution video
Good night-time visibility
Clearly visible headlights
Normal-speed traffic
Front-facing camera
Multiple approaching vehicles
Stable camera
Minimal motion blur

The system is intended as a project prototype and should not be considered a production-ready automotive safety system without extensive validation and hardware-level safety testing.

Safety Note

This project is a research and educational prototype.

The beam intensity and beam direction values generated by the system are simulated software decisions. They are not intended to directly control a real vehicle headlight without proper automotive hardware, electrical protection, safety validation, regulatory compliance, and testing.

Conclusion

The AI Anti-Glare Headlight System provides a software-based prototype for intelligent automotive lighting control.

By combining YOLO-based vehicle detection, vehicle tracking, OpenCV-based headlight detection, glare analysis, and adaptive beam-control logic, the system demonstrates how Artificial Intelligence and Computer Vision can be applied to improve night-driving safety.

The current prototype processes uploaded night-driving videos and generates an annotated anti-glare output video along with a CSV report and graphical analysis.

The system provides a foundation for future development using real-time cameras, embedded AI hardware, automotive ECUs, actuators, and adaptive headlight mechanisms.

The long-term objective is to develop an intelligent automotive lighting system that can automatically respond to approaching vehicles and excessive headlight glare while maintaining adequate road illumination.

Author

Naveen Kumar S

B.E. Mechanical Engineering
Knowledge Institute of Technology
Salem, Tamil Nadu, India

Keywords
AI Anti-Glare Headlight System
Adaptive Headlight Control
Automotive Safety
Computer Vision
YOLO
OpenCV
Artificial Intelligence
Night Driving
Headlight Detection
Glare Detection
Vehicle Detection
Vehicle Tracking
ADAS
Intelligent Transportation
Python
Streamlit
Machine Learning
Automotive Engineering
Mechanical Engineering
Smart Vehicle
Adaptive Lighting
Road Safety
