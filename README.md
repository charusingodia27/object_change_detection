# object-change-detection

This project detects new and missing objects in real-time using computer vision techniques, powered by YOLOv8 for object detection. The system tracks objects across video frames, identifies when they appear and disappear, and outputs annotated video and frame images.

## Project Structure

The following files and directories are part of this project:

- **`detect_objects.py`** – The main script that runs object detection and change tracking.
- **`Dockerfile`** – The Docker setup for creating an isolated environment to run the project.
- **`requirements.txt`** – Python dependencies required to run the project.
- **`README.md`** – Documentation for the project.
- **`report_charusingodia_ML_Intern.docx`** – Report containing details about performance, hardware configuration, and optimizations.
- **`output_frames/`** – Directory where annotated frames are saved.
- **`output_video.mp4`** – The final output video with annotations.
  
## How It Works

The core logic of the project is implemented in **`detect_objects.py`**. Here’s how it works:

1. **Object Detection**: 
   - The YOLOv8 model is used to detect objects in real-time from the webcam or video file.
   - The model outputs bounding boxes and labels for each detected object in every frame.
   
2. **Object Change Tracking**:
   - The script tracks changes by comparing the current set of detected objects with the previous frame's objects.
   - It flags new and missing objects accordingly.

3. **Frame and Video Output**:
   - For each detected change (new or missing objects), the frame is saved in the `output_frames/` directory, and the annotated frames are added to the output video (`output_video.mp4`).

4. **FPS Calculation**:
   - The real-time performance of the system is measured by calculating the frames per second (FPS).

## Requirements

- **Python 3.8+**
- **YOLOv8 (ultralytics)**
- **OpenCV**
- **NumPy**

To install the necessary dependencies, run the following command:

```bash
pip install -r requirements.txt
```

## How to Run the Project
Step 1: Clone the repository
```bash
git clone https://github.com/your-username/object-change-detection.git
cd object-change-detection
```
Step 2: Install dependencies
Make sure all dependencies are installed by running:
```bash
pip install -r requirements.txt
```
Step 3: Run the object detection script
To start the object detection and tracking, use the following command:
```bash
python detect_objects.py
```
This will start reading from the webcam or the video file specified in the script and begin detecting objects, tracking changes, and generating the output.

## Output
- Annotated Frames: The frames with object annotations are saved in the `output_frames/` folder.

- Output Video: A video file named output_video.mp4 will be generated, showing the object tracking in real-time.

## Docker Setup (Optional)
Step 1: Build Docker Image
```bash
docker build -t object-change-detection .
```
Step 2: Run Docker Container
```bash
docker run -it --rm object-change-detection
```
This will run the project inside a Docker container with all dependencies installed.

## Performance and Optimization
This project uses YOLOv8 for object detection, which provides a good balance of speed and accuracy. The following optimizations were made to improve real-time performance:

- **Efficient Frame Processing:** The script processes frames at a controlled rate to prevent FPS drops.

- **Caching Mechanism:** Object states are cached between frames to minimize redundant calculations.

- **Video Output Optimization:** The video is written to disk only when necessary to prevent FPS drops.

### FPS Achieved
The FPS achieved during testing varies depending on the system hardware. On average, the FPS is around 30 FPS for a standard webcam input on mid-range systems.

## Hardware Configuration Used for Testing
- **CPU:** Intel Core i7 10th Gen (4 cores, 8 threads)

- **RAM:** 16 GB

- **GPU:** Integrated GPU (Intel UHD Graphics)

- **OS:** Ubuntu 20.04 LTS

## Report
For detailed performance metrics, hardware configuration, and optimization techniques, please refer to the report_charusingodia_ML_Intern.docx.
