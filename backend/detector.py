# backend/detector.py
from ultralytics import YOLO
import numpy as np


class YoloWrapper:
    def __init__(self, model='yolov8n.pt', device='cpu'):
        self.model = YOLO(model)
        self.device = device


    def predict(self, frame, conf=0.25):
    # frame: BGR numpy array
        res = self.model.predict(source=frame, imgsz=640, device=self.device, conf=conf, verbose=False)
        # res is list-like; take first
        r = res[0]
        boxes = []
        if r.boxes is None:
            return boxes
        for box in r.boxes.data.tolist():
            # box format: [x1,y1,x2,y2,score,class]
            x1,y1,x2,y2,score,cls = box
            boxes.append({'bbox':[x1,y1,x2,y2],'score':float(score),'class_id':int(cls)})
        return boxes    