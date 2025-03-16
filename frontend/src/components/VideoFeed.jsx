const VideoFeed = ({ videoRef, isRunning, canvasRef }) => {
  const handlePiP = async () => {
    if (!videoRef.current) return;

    try {
      if (document.pictureInPictureElement) {
        await document.exitPictureInPicture(); // Thoát PiP nếu đang bật
      } else {
        await videoRef.current.requestPictureInPicture(); // Bật PiP
      }
    } catch (err) {
      console.error("PiP Error:", err);
    }
  };

  return (
    <div className="video-container">
      <video
        ref={videoRef}
        autoPlay
        playsInline
        className={`webcam-video ${isRunning ? "active" : ""}`}
      />
      <canvas ref={canvasRef} width="400" height="300"></canvas>

      {isRunning && document.pictureInPictureEnabled && (
        <button className="pip-button" onClick={handlePiP}>
          PiP
        </button>
      )}

      {!isRunning && (
        <div className="video-overlay">
          <span>Camera Off</span>
        </div>
      )}
    </div>
  );
};

export default VideoFeed;
