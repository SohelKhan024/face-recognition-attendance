import React, { useRef } from 'react';

function Camera({ onCapture }) {
  const videoRef = useRef(null);

  const startCamera = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    videoRef.current.srcObject = stream;
  };

  const captureImage = () => {
    const canvas = document.createElement('canvas');
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(videoRef.current, 0, 0);
    canvas.toBlob(blob => onCapture(blob), 'image/jpeg');
  };

  return (
    <div>
      <video ref={videoRef} autoPlay width="300"></video><br />
      <button onClick={startCamera}>Start Camera</button>
      <button onClick={captureImage}>Capture</button>
    </div>
  );
}

export default Camera;
