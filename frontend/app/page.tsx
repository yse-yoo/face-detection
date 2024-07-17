'use client'

import { useState, useRef } from 'react';
import axios from 'axios';

const HomePage = () => {
  const [detectedImage, setDetectedImage] = useState<string | null>(null);
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  const startCamera = async () => {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play();
      }
    }
  };

  const captureImage = async () => {
    if (videoRef.current && canvasRef.current) {
      const context = canvasRef.current.getContext('2d');
      if (context) {
        context.drawImage(videoRef.current, 0, 0, canvasRef.current.width, canvasRef.current.height);
        const imageData = canvasRef.current.toDataURL('image/jpeg');
        const blob = await (await fetch(imageData)).blob();
        const formData = new FormData();
        formData.append('image', blob, 'webcam.jpg');

        try {
          const response = await axios.post('http://localhost:5000/detect', formData);
          setDetectedImage(response.data.image);
        } catch (error) {
          console.log(error)
        }
      }
    }
  };

  return (
    <div>
      <h1>Webcam Face Detection</h1>
      <button onClick={startCamera}>Start Camera</button>
      <button onClick={captureImage}>Capture Image</button>
      <div>
        <video ref={videoRef} width="640" height="480" />
        <canvas ref={canvasRef} width="640" height="480" style={{ display: 'none' }} />
      </div>
      {detectedImage && (
        <div>
          <h2>Detected Faces:</h2>
          <img src={`data:image/jpeg;base64,${detectedImage}`} alt="Detected Faces" />
        </div>
      )}
    </div>
  );
};

export default HomePage;