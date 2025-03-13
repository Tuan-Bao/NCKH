const VideoFeed = ({ videoRef, isRunning, canvasRef }) => {
  return (
    <div className="video-container">
      <video
        ref={videoRef}
        autoPlay
        playsInline
        className={`webcam-video ${isRunning ? "active" : ""}`}
      />
      <canvas ref={canvasRef} width="400" height="300"></canvas>
      {!isRunning && (
        <div className="video-overlay">
          <span>Camera Off</span>
        </div>
      )}
    </div>
  );
};

export default VideoFeed;
