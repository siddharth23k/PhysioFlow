// MobileApp.js
import React, { useRef, useState, useEffect } from 'react';
import './MobileApp.css';

function MobileApp() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [cameraActive, setCameraActive] = useState(false);
  const [hasPermission, setHasPermission] = useState(null);
  const [feedbackText, setFeedbackText] = useState('');

  // Request camera permission and start stream
  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'user' }
      });
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        setCameraActive(true);
        setHasPermission(true);
        setFeedbackText('Camera started! Exercise tracking active.');
      }
    } catch (err) {
      console.error("Error accessing camera: ", err);
      setHasPermission(false);
      setFeedbackText('Camera permission denied or camera not available.');
    }
  };

  // Stop the camera stream
  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const tracks = videoRef.current.srcObject.getTracks();
      tracks.forEach(track => track.stop());
      videoRef.current.srcObject = null;
      setCameraActive(false);
      setFeedbackText('Camera stopped.');
    }
  };

  // Clean up on component unmount
  useEffect(() => {
    return () => {
      if (videoRef.current && videoRef.current.srcObject) {
        const tracks = videoRef.current.srcObject.getTracks();
        tracks.forEach(track => track.stop());
      }
    };
  }, []);

  return (
    <div className="mobile-app">
      <h1>Exercise Tracker</h1>
      
      <div className="video-container">
        <video
          ref={videoRef}
          autoPlay
          playsInline
          style={{ display: cameraActive ? 'block' : 'none' }}
        />
        <canvas
          ref={canvasRef}
          className="pose-canvas"
          style={{ display: cameraActive ? 'block' : 'none' }}
        />
      </div>

      <div className="feedback-area">
        <p>{feedbackText}</p>
      </div>

      <div className="controls">
        {!cameraActive ? (
          <button className="start-button" onClick={startCamera}>
            Start Exercise Tracking
          </button>
        ) : (
          <button className="stop-button" onClick={stopCamera}>
            Stop Camera
          </button>
        )}
      </div>
    </div>
  );
}

export default MobileApp;