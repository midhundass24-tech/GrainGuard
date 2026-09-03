import React, { useState, useRef, useEffect } from 'react';
import { Camera, RefreshCw, Upload, Check, FlipHorizontal } from 'lucide-react';

export default function CameraCapture({ onCapture, onSamplePick }) {
  const [stream, setStream] = useState(null);
  const [cameraError, setCameraError] = useState(null);
  const [facingMode, setFacingMode] = useState('environment'); // Default to rear camera
  const [capturedPreview, setCapturedPreview] = useState(null);
  const videoRef = useRef(null);
  const fileInputRef = useRef(null);

  // Initialize camera stream
  const startCamera = async () => {
    setCameraError(null);
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
    }

    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: facingMode,
          width: { ideal: 1920 },
          height: { ideal: 1080 }
        },
        audio: false
      });
      setStream(mediaStream);
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
    } catch (err) {
      console.warn('Camera access error:', err);
      setCameraError('Camera stream unavailable. Please use file upload or demo samples.');
    }
  };

  useEffect(() => {
    startCamera();
    return () => {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
    };
  }, [facingMode]);

  const toggleCamera = () => {
    setFacingMode(prev => (prev === 'environment' ? 'user' : 'environment'));
  };

  const handleCaptureFrame = () => {
    if (!videoRef.current) return;

    const video = videoRef.current;
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth || 1280;
    canvas.height = video.videoHeight || 720;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(blob => {
      if (!blob) return;
      const previewUrl = URL.createObjectURL(blob);
      setCapturedPreview(previewUrl);
      onCapture(blob);
    }, 'image/jpeg', 0.92);
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const previewUrl = URL.createObjectURL(file);
      setCapturedPreview(previewUrl);
      onCapture(file);
    }
  };

  // Generate synthetic sample photo for rapid testing if no real photo is handy
  const handleGenerateSample = () => {
    const canvas = document.createElement('canvas');
    canvas.width = 1000;
    canvas.height = 1000;
    const ctx = canvas.getContext('2d');

    // Dark contrasting background tray
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 0, 1000, 1000);

    // Physical tray border
    ctx.strokeStyle = '#475569';
    ctx.lineWidth = 14;
    ctx.strokeRect(40, 40, 920, 920);

    // Draw realistic grain cluster
    const rows = 12;
    const cols = 14;
    for (let r = 1; r <= rows; r++) {
      for (let c = 1; c <= cols; c++) {
        const x = c * 62 + (Math.sin(r * c) * 12);
        const y = r * 68 + (Math.cos(r + c) * 10);
        
        ctx.save();
        ctx.translate(x, y);
        ctx.rotate((r * 37 + c * 19) * Math.PI / 180);

        const isDiscolored = (r * c) % 17 === 0;
        const isBroken = (r + c) % 11 === 0;
        const isInsect = (r * c) % 29 === 0;
        const isForeign = (r * c) % 43 === 0;

        if (isForeign) {
          ctx.fillStyle = '#7c3aed'; // Purple foreign stone
          ctx.beginPath();
          ctx.arc(0, 0, 8, 0, Math.PI * 2);
          ctx.fill();
        } else if (isInsect) {
          ctx.fillStyle = '#dc2626'; // Red insect damaged grain
          ctx.beginPath();
          ctx.ellipse(0, 0, 16, 6, 0, 0, Math.PI * 2);
          ctx.fill();
        } else if (isDiscolored) {
          ctx.fillStyle = '#d97706'; // Amber discolored
          ctx.beginPath();
          ctx.ellipse(0, 0, 18, 7, 0, 0, Math.PI * 2);
          ctx.fill();
        } else if (isBroken) {
          ctx.fillStyle = '#f8fafc'; // White broken half
          ctx.beginPath();
          ctx.ellipse(0, 0, 9, 6, 0, 0, Math.PI * 2);
          ctx.fill();
        } else {
          ctx.fillStyle = '#ffffff'; // Pristine whole grain
          ctx.beginPath();
          ctx.ellipse(0, 0, 20, 7, 0, 0, Math.PI * 2);
          ctx.fill();
        }

        ctx.restore();
      }
    }

    canvas.toBlob(blob => {
      if (!blob) return;
      const previewUrl = URL.createObjectURL(blob);
      setCapturedPreview(previewUrl);
      onCapture(blob);
    }, 'image/jpeg', 0.95);
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
      <div className="p-4 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
        <div>
          <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
            <Camera className="w-4 h-4 text-emerald-600" />
            Smartphone Sample Capture
          </h3>
          <p className="text-xs text-slate-500">
            Position smartphone directly top-down over contrasting sample tray
          </p>
        </div>

        {stream && (
          <button
            onClick={toggleCamera}
            className="flex items-center gap-1.5 text-xs text-slate-600 bg-white border border-slate-200 px-2.5 py-1.5 rounded-lg hover:bg-slate-100"
          >
            <FlipHorizontal className="w-3.5 h-3.5" />
            <span>Flip Cam</span>
          </button>
        )}
      </div>

      <div className="p-4">
        {capturedPreview ? (
          /* Captured Preview Confirmation */
          <div className="flex flex-col items-center">
            <div className="relative max-w-md w-full rounded-xl overflow-hidden border-2 border-emerald-500 shadow-md">
              <img src={capturedPreview} alt="Captured Sample" className="w-full h-auto object-cover" />
              <div className="absolute top-2 left-2 bg-emerald-600 text-white text-[11px] font-semibold px-2.5 py-1 rounded-full flex items-center gap-1 shadow">
                <Check className="w-3.5 h-3.5" /> Sample Photo Ready
              </div>
            </div>
            <div className="mt-4 flex gap-3">
              <button
                type="button"
                onClick={() => {
                  setCapturedPreview(null);
                  onCapture(null);
                }}
                className="px-4 py-2 border border-slate-300 rounded-lg text-xs font-semibold text-slate-700 hover:bg-slate-100 flex items-center gap-1.5"
              >
                <RefreshCw className="w-3.5 h-3.5" /> Retake Photo
              </button>
            </div>
          </div>
        ) : (
          /* Camera Viewport or Fallback */
          <div className="flex flex-col items-center">
            <div className="relative w-full max-w-md aspect-[4/3] bg-slate-950 rounded-xl overflow-hidden flex items-center justify-center border border-slate-800">
              {stream ? (
                <>
                  <video
                    ref={videoRef}
                    autoPlay
                    playsInline
                    muted
                    className="w-full h-full object-cover"
                  />
                  {/* Tray Alignment Overlay */}
                  <div className="absolute inset-6 border-2 border-dashed border-emerald-400/80 rounded-lg pointer-events-none flex flex-col justify-between p-3">
                    <span className="text-[10px] bg-slate-900/80 text-emerald-300 px-2 py-0.5 rounded self-start font-mono">
                      ALIGN TRAY BOUNDARY HERE
                    </span>
                    <span className="text-[10px] bg-slate-900/80 text-slate-300 px-2 py-0.5 rounded self-end">
                      Keep Camera Level
                    </span>
                  </div>
                </>
              ) : (
                <div className="text-center p-6 text-slate-400">
                  <Camera className="w-10 h-10 mx-auto mb-2 text-slate-600" />
                  <p className="text-xs">{cameraError || 'Loading camera stream...'}</p>
                </div>
              )}
            </div>

            {/* Shutter Button & Fallbacks */}
            <div className="mt-4 flex flex-wrap items-center justify-center gap-3">
              {stream && (
                <button
                  type="button"
                  onClick={handleCaptureFrame}
                  className="bg-emerald-600 hover:bg-emerald-700 text-white font-bold px-6 py-2.5 rounded-xl shadow-md flex items-center gap-2 text-sm transition-all transform active:scale-95"
                >
                  <Camera className="w-4 h-4" /> Capture Tray Photo
                </button>
              )}

              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                className="hidden"
                onChange={handleFileUpload}
              />
              <button
                type="button"
                onClick={() => fileInputRef.current?.click()}
                className="bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 font-semibold px-4 py-2.5 rounded-xl text-xs flex items-center gap-2 shadow-sm"
              >
                <Upload className="w-3.5 h-3.5 text-slate-500" /> Upload Image File
              </button>

              <button
                type="button"
                onClick={handleGenerateSample}
                className="bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold px-3.5 py-2.5 rounded-xl text-xs flex items-center gap-1.5"
                title="Generates high-contrast sample with mixed defects"
              >
                Use Sample Rice Tray
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
