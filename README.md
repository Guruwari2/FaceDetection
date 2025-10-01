# Real-Time Object Detection + Tracking Dashboard

A browser-based dashboard that performs real-time object detection and tracking on webcam or video streams. Draws bounding boxes, tracks objects over time, and displays counts/statistics.

This README is intended to be saved as `README.md` so you can download or include it directly in your repository.

## Features
- Real-time object detection using **YOLOv8**.
- Object tracking using a **SORT-like tracker** (IDs assigned to objects).
- Browser-based dashboard using **React**.
- Live overlay of bounding boxes and object IDs.
- WebSocket communication between frontend and backend.

## Project Structure
```
rt-det-track/
├─ backend/
│  ├─ app/main.py           # FastAPI server and WebSocket endpoint
│  ├─ detector.py           # YOLOv8 wrapper
│  ├─ tracker.py            # Simple SORT tracker
│  ├─ utils.py              # Helper functions
│  └─ requirements.txt      # Python dependencies
├─ frontend/
│  ├─ package.json          # React dependencies
│  └─ src/App.jsx           # React dashboard
└─ README.md               # This file
```

## Installation

### Backend
1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```
2. Install dependencies:
```bash
pip install -r backend/requirements.txt
```
3. Download YOLOv8 model
Before running the backend, download the YOLOv8 model for face detection:

```bash
wget https://github.com/lindevs/yolov8-face/releases/latest/download/yolov8n-face-lindevs.pt
```

4. Start the backend server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
1. Navigate to the frontend folder:
```bash
cd frontend
```
2. Install dependencies:
```bash
npm install
```
3. Start the frontend development server:
```bash
npm start
```

Open your browser at `http://localhost:3000` to see the dashboard.

## Usage
- The React frontend captures webcam frames and sends them to the backend via WebSocket.
- The backend runs YOLOv8 detection and updates the tracker.
- Detected objects with their IDs are sent back to the frontend for rendering.
- The dashboard displays bounding boxes, object IDs, and statistics.

## Next Steps / Improvements
- Replace simple tracker with **Kalman filter-based SORT** or **DeepSORT**.
- Add GPU support for faster YOLO inference.
- Display statistics over time (counts, dwell time, per-class charts).
- Support video file or RTSP stream input on the server side.
- Implement trails or heatmaps for tracked objects.

## References
- [YOLOv8 / Ultralytics Docs](https://docs.ultralytics.com/)
- [SORT Paper](https://arxiv.org/abs/1602.00763)
- [DeepSORT Repository](https://github.com/nwojke/deep_sort)

---

**Author:** Nathan Darjana  
**Date:** 2025-10-01

