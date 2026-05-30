import cv2
from ultralytics import YOLO
from speed_estimator import SpeedEstimator

model = YOLO("yolov8n.pt")
video_path = "input/traffic.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error opening video")
    exit()
fps = cap.get(cv2.CAP_PROP_FPS)

if fps <= 0:
    fps = 25

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print(f"FPS: {fps}")
print(f"Total Frames: {total_frames}")

width = 720
height = 1280
output_path = "output/output.mp4"
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

out = cv2.VideoWriter(
    output_path,
    fourcc,
    fps,
    (width, height)
)
speed_estimator = SpeedEstimator()
vehicle_classes = [2, 3, 5, 7]
frame_count = 0

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break
    frame_count += 1
    if frame_count % 50 == 0:
        print(f"Processed {frame_count}/{total_frames}")

    frame = cv2.resize(frame, (width, height))
    results = model.track(
        frame,
        persist=True,
        tracker="bytetrack.yaml",
        conf=0.35,
        verbose=False
    )

    boxes = results[0].boxes
    current_vehicle_count = 0
    if boxes.id is not None:
        for box, track_id, cls in zip(
            boxes.xyxy,
            boxes.id,
            boxes.cls):

            cls = int(cls)
            if cls not in vehicle_classes:
                continue
            current_vehicle_count += 1
            track_id = int(track_id)
            x1, y1, x2, y2 = map(int, box)
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            speed = speed_estimator.estimate_speed(
                track_id,
                center_x,
                center_y,
                fps
            )
            if speed == 0:
                continue

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2)

            cv2.circle(
                frame,
                (center_x, center_y),
                4,
                (0, 0, 255),
                -1)

            cv2.putText(
                frame,
                f"ID {track_id}",
                (x1, y1 - 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 255, 255),
                2)

            cv2.putText(
                frame,
                f"{speed} km/h",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 255, 255),
                2)

    cv2.putText(
        frame,
        f"Vehicles Visible: {current_vehicle_count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2)
    out.write(frame)
print(f"Frames Processed: {frame_count}")
cap.release()
out.release()
cv2.destroyAllWindows()

print("Processing Completed")
print(f"Output saved at: {output_path}")