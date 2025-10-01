# backend/app/main.py
import cv2
import base64
import json
import numpy as np
import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from backend.detector import YoloWrapper
from backend.tracker import SimpleSORT

app = FastAPI()

det = YoloWrapper(model='yolov8n-face-lindevs.pt', device='cpu')
tracker = SimpleSORT()

@app.websocket('/ws')
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            data = await ws.receive_text()
            # Expect a base64 jpeg frame in JSON: {frame_id, jpeg_b64}
            msg = json.loads(data)
            b64 = msg.get('jpeg')
            frame_id = msg.get('frame_id')
            if not b64:
                await ws.send_text(json.dumps({'error':'no frame'}))
                continue
            jpg = base64.b64decode(b64)
            arr = np.frombuffer(jpg, np.uint8)
            frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
            dets = det.predict(frame)
            #person_dets = [d for d in dets if d['class'] == 'person']
            bboxes = [d['bbox'] for d in dets]
            #bboxes = [d['bbox'] for d in person_dets]
            tracks = tracker.update(bboxes)
            out = {'frame_id':frame_id,'tracks':[{'id':t.id,'bbox':t.bbox.tolist()} for t in tracks]}
            await ws.send_text(json.dumps(out))
    except Exception as e:
        print('ws closed', e)