# Vehicle Detection and Speed Estimation System

## Overview

This project detects vehicles in a traffic video, tracks them using unique IDs, and estimates their approximate speed. The processed video is generated with vehicle bounding boxes, tracking IDs, and speed annotations.

## Technologies Used

* Python
* OpenCV
* YOLOv8
* ByteTrack

## Project Structure

Vehicle-Speed-Estimation/

├── input/
│   └── traffic.mp4

├── output/
│   └── output.mp4

├── main.py

├── speed_estimator.py

├── requirements.txt

└── README.md

## Installation

Install dependencies:

pip install -r requirements.txt

## Execution

Place the traffic video inside the input folder.

Run:

python main.py

## Output

The processed video will be saved in:

output/output.mp4

## Notes

* Vehicle detection is performed using YOLOv8.
* Vehicle tracking is performed using ByteTrack.
* Speed values are approximate and based on vehicle displacement across frames.
* No camera calibration or real-world distance measurements were used.
