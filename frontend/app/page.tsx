'use client'

import { useState, useRef } from 'react';
import axios from 'axios';

const API_URI = process.env.NEXT_PUBLIC_API_URL;

const HomePage = () => {
    const [detectedImage, setDetectedImage] = useState<string | null>(null);
    const [userId, setUserId] = useState<string>('');
    const [cameraActive, setCameraActive] = useState<boolean>(false);

    const videoRef = useRef<HTMLVideoElement | null>(null);
    const canvasRef = useRef<HTMLCanvasElement | null>(null);
    const streamRef = useRef<MediaStream | null>(null);

    const startCamera = async () => {
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            if (videoRef.current) {
                videoRef.current.srcObject = stream;
                videoRef.current.play();
            }
            setCameraActive(true);
        }
    };

    const stopCamera = () => {
        if (streamRef.current) {
            streamRef.current.getTracks().forEach(track => track.stop());
            if (videoRef.current) {
                videoRef.current.pause();
                videoRef.current.srcObject = null;
            }
            setCameraActive(false);
        }
    };

    const captureImage = async (action: 'detect' | 'register' | 'recognize') => {
        if (videoRef.current && canvasRef.current) {
            const context = canvasRef.current.getContext('2d');
            if (context) {
                context.drawImage(videoRef.current, 0, 0, canvasRef.current.width, canvasRef.current.height);
                const imageData = canvasRef.current.toDataURL('image/jpeg');
                const blob = await (await fetch(imageData)).blob();
                const formData = new FormData();

                formData.append('image', blob, 'webcam.jpg');
                if (action === 'register') {
                    formData.append('user_id', userId);
                }
                // console.log(formData)

                const uri = `${API_URI}${action}`;
                console.log(uri)
                var response = await axios.post(uri, formData);
                console.log("Status: ", response.data.status)
                if (response.data.status == "success") {
                    var message = `${action} is ${response.data.status}`;
                    alert(message)
                } else {
                    var message = `${action} is error`;
                    alert(message)
                }
            }
        }
    };

    return (
        <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center">
            <h1 className="text-3xl font-bold mb-4">Webcam Face Detection and Recognition</h1>
            <div className="flex">
            </div>
            <div className="flex items-center mb-4">
                <div>
                    <button
                        onClick={startCamera}
                        className="bg-blue-500 text-white py-2 px-4 rounded m-2"
                    >
                        Start Camera
                    </button>
                    <canvas ref={canvasRef} width="640" height="480" className="hidden" />
                    <button
                        onClick={stopCamera}
                        className="bg-red-500 text-white py-2 px-4 rounded"
                        disabled={!cameraActive}
                    >
                        Stop Camera
                    </button>
                    <button
                        onClick={() => captureImage('detect')}
                        className="bg-green-500 text-white py-2 px-4 rounded m-2"
                    >
                        Detect Faces
                    </button>
                    <video ref={videoRef} width="640" height="480" className="mb-4 border-2 border-gray-300" />
                </div>

                <div>
                    {detectedImage && (
                        <div className="mt-4">
                            <img src={`data:image/jpeg;base64,${detectedImage}`} alt="Detected Faces" className="border-2 border-gray-300" />
                        </div>
                    )}
                </div>
            </div>

            <div className="flex flex-col items-center mb-4">
                <input
                    type="number"
                    placeholder="User ID"
                    value={userId}
                    onChange={(e) => setUserId(e.target.value)}
                    className="mb-2 p-2 border border-gray-300 rounded"
                />
                <button
                    onClick={() => captureImage('register')}
                    className={`py-2 px-4 rounded mb-2 text-white 
        ${userId ? 'bg-yellow-500 hover:bg-yellow-600' : 'bg-gray-300 cursor-not-allowed'}`}
                    disabled={!userId}
                >
                    Register Face
                </button>
                <button
                    onClick={() => captureImage('recognize')}
                    className="bg-purple-500 text-white py-2 px-4 rounded mb-2"
                >
                    Recognize Face
                </button>
            </div>

        </div>
    );
};

export default HomePage;
