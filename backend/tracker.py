# backend/tracker.py
import numpy as np
from scipy.optimize import linear_sum_assignment


class Track:
    def __init__(self, tid, bbox, max_history=30):
        self.id = tid
        self.bbox = np.array(bbox, dtype=float) # x1,y1,x2,y2
        self.hits = 1
        self.misses = 0
        self.history = [self.bbox.copy()]


    def predict(self):
        # Very simple: no motion model -> keep same bbox
        return self.bbox


    def update(self, bbox):
        self.bbox = np.array(bbox, dtype=float)
        self.hits += 1
        self.misses = 0
        self.history.append(self.bbox.copy())
        if len(self.history) > 50:
            self.history.pop(0)


class SimpleSORT:
    def __init__(self, iou_threshold=0.3, max_misses=5):
        self.tracks = []
        self.next_id = 1
        self.iou_threshold = iou_threshold
        self.max_misses = max_misses


    @staticmethod
    def iou(bb1, bb2):
        xA = max(bb1[0], bb2[0]); yA = max(bb1[1], bb2[1])
        xB = min(bb1[2], bb2[2]); yB = min(bb1[3], bb2[3])
        interW = max(0, xB-xA); interH = max(0, yB-yA)
        inter = interW*interH
        area1 = (bb1[2]-bb1[0])*(bb1[3]-bb1[1])
        area2 = (bb2[2]-bb2[0])*(bb2[3]-bb2[1])
        if area1+area2-inter == 0:
            return 0.0
        return inter / (area1+area2-inter)


    def update(self, detections):
        # detections: list of bbox arrays [x1,y1,x2,y2]
        if len(self.tracks)==0:
            for d in detections:
                self.tracks.append(Track(self.next_id, d))
                self.next_id += 1
            return self.tracks


        # Build cost matrix (1 - iou)
        M = len(self.tracks); N = len(detections)
        cost = np.ones((M,N))
        for i,t in enumerate(self.tracks):
            for j,d in enumerate(detections):
                cost[i,j] = 1 - self.iou(t.predict(), d)


        row_idx, col_idx = linear_sum_assignment(cost)
        assigned_tracks = set()
        assigned_dets = set()
        for r,c in zip(row_idx, col_idx):
            if cost[r,c] < (1 - self.iou_threshold):
                # accept
                self.tracks[r].update(detections[c])
                assigned_tracks.add(r); assigned_dets.add(c)


        # mark unassigned tracks as missed
        for i,t in enumerate(self.tracks):
            if i not in assigned_tracks:
                t.misses += 1
        # create new tracks for unassigned detections
        for j,d in enumerate(detections):
            if j not in assigned_dets:
                self.tracks.append(Track(self.next_id, d))
                self.next_id += 1

        self.tracks = [t for t in self.tracks if t.misses <= self.max_misses]
        #remove dead tracks
        return self.tracks