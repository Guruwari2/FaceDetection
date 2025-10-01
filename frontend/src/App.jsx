import React, { useRef, useEffect, useState } from 'react';

export default function App() {
    const videoRef = useRef();
    const canvasRef = useRef();
    const wsRef = useRef();
    const [connected, setConnected] = useState(false);

    useEffect(() => {
        draw({ tracks: [{ id: 1, bbox: [50, 50, 200, 200] }] });
        async function init() {
            try {
                // 1️⃣ Get webcam access
                const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                videoRef.current.srcObject = stream;
                await videoRef.current.play();

                // 2️⃣ Connect to backend websocket
                const ws = new WebSocket('ws://localhost:8000/ws');
                ws.onopen = () => setConnected(true);

                ws.onmessage = (evt) => {
                    const msg = JSON.parse(evt.data);
                    draw(msg);
                };

                wsRef.current = ws;

                // 3️⃣ Capture frames and send to backend
                const sendLoop = async () => {
                    if (ws.readyState === 1) {
                        const canvas = document.createElement('canvas');
                        canvas.width = videoRef.current.videoWidth || 640;
                        canvas.height = videoRef.current.videoHeight || 480;
                        const ctx = canvas.getContext('2d');
                        ctx.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
                        const jpeg = canvas.toDataURL('image/jpeg', 0.6).split(',')[1];

                        ws.send(JSON.stringify({ frame_id: Date.now(), jpeg }));
                    }
                    setTimeout(sendLoop, 200); // 5 FPS
                };
                sendLoop();
            } catch (err) {
                console.error('Webcam or WebSocket error:', err);
            }
        }

        init();
    }, []);

    const draw = (msg) => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        const w = videoRef.current.videoWidth;
        const h = videoRef.current.videoHeight;
        canvas.width = w;
        canvas.height = h;
        ctx.clearRect(0, 0, w, h);

        if (!msg.tracks) return;

        ctx.lineWidth = 2;
        ctx.font = '16px Arial';
        ctx.strokeStyle = 'red';
        ctx.fillStyle = 'red';

        msg.tracks.forEach((t) => {
            const [x1, y1, x2, y2] = t.bbox;
            ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);
            ctx.fillText(`ID:${t.id}`, x1, y1 - 6);
        });
    };

    return (
        <div style={{ padding: '10px' }}>
            <h1>Real-time Object Detection + Tracking</h1>
            <div style={{ position: 'relative', display: 'inline-block' }}>
                <video ref={videoRef} style={{ width: '640px' }} />
                <canvas
                    ref={canvasRef}
                    style={{ position: 'absolute', left: 0, top: 0 }}
                />
            </div>
            <div>Status: {connected ? 'Connected to backend' : 'Connecting...'}</div>
        </div>
    );
}
