import cv2
import time
import os
from ultralytics import YOLO

# Parameters
WRITE_OUTPUT_VIDEO = False # For output video generation, turn this True
MISSING_THRESHOLD = 3  # Frames to wait before considering object missing
CONFIDENCE_THRESHOLD = 0.5  # Confidence threshold for detections

# Load model
model = YOLO('yolov8m.pt')  # use 'yolov8m.pt' for much better detection

# Open video
cap = cv2.VideoCapture(0)  # 0 for webcam, or give video file path

# Initialize tracking
prev_objects = set()
seen_objects = set()
missing_announced_objects = set()
missing_counter = dict()
frame_count = 0
fps_start_time = time.time()

# Create output folders
os.makedirs('output_frames', exist_ok=True)

# Output video setup if enabled
if WRITE_OUTPUT_VIDEO:
    output_video = cv2.VideoWriter('output_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 20, (640, 480))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    # Resize frame
    frame = cv2.resize(frame, (640, 480))

    # Inference
    results = model.predict(frame, conf=CONFIDENCE_THRESHOLD, verbose=False)
    detections = results[0].boxes.xyxy.cpu().numpy()
    labels = results[0].boxes.cls.cpu().numpy()

    # Current objects
    current_objects = set(int(label) for label in labels)

    # Update missing counter
    for obj in prev_objects:
        if obj not in current_objects:
            missing_counter[obj] = missing_counter.get(obj, 0) + 1
        else:
            missing_counter[obj] = 0  # reset counter if object is seen

    # Detect new objects
    new_objects = current_objects - seen_objects

    # Detect missing objects
    truly_missing_objects = set()
    for obj, count in missing_counter.items():
        if count >= MISSING_THRESHOLD and obj not in missing_announced_objects:
            truly_missing_objects.add(obj)

    # Draw detections
    annotated_frame = results[0].plot()

    event_occurred = False  # Track if any new/missing event occurs this frame

    y = 20

    # New Objects
    if new_objects:
        print(f"\nFrame {frame_count}:")
        for obj in new_objects:
            print(f"  - New object detected: {model.names[int(obj)]}")
            cv2.putText(annotated_frame, f"New Object: {model.names[int(obj)]}", (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
            y += 20
        seen_objects.update(new_objects)
        event_occurred = True

    # Missing Objects (after smoothing)
    if truly_missing_objects:
        print(f"\nFrame {frame_count}:")
        for obj in truly_missing_objects:
            print(f"  - Object missing: {model.names[int(obj)]}")
            cv2.putText(annotated_frame, f"Missing Object: {model.names[int(obj)]}", (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
            y += 20
            missing_announced_objects.add(obj)
            seen_objects.discard(obj)  # allow re-appearance to be treated as new
        event_occurred = True

    # Save frame only if an event occurred
    if event_occurred:
        output_frame_path = f"output_frames/frame_{frame_count}.jpg"
        cv2.imwrite(output_frame_path, annotated_frame)
        print(f"  - Saved annotated frame: {output_frame_path}")

    # FPS calculation (live)
    elapsed_time = time.time() - fps_start_time
    fps = frame_count / elapsed_time
    cv2.putText(annotated_frame, f"FPS: {fps:.2f}", (10, annotated_frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    # Write frame to output video
    output_video.write(annotated_frame)

    # Display
    cv2.imshow('Real-Time Object Change Detection', annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Update previous frame objects
    prev_objects = current_objects

# Release everything
cap.release()
output_video.release()
cv2.destroyAllWindows()

# Final FPS calculation
total_elapsed_time = time.time() - fps_start_time
final_fps = frame_count / total_elapsed_time

print("\nDetection completed! Output video and event frames are saved.")
print(f"Average FPS: {final_fps:.2f}")
