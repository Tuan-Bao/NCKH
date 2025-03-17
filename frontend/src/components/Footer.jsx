const Footer = ({ isRunning, mode }) => {
  return (
    <footer>
      <div className="status-container">
        <div className="status">
          <span className={`status-indicator ${isRunning ? 'active' : 'inactive'}`}></span>
          <span>{isRunning ? 'System Active' : 'System Inactive'}</span>
        </div>
        <div className="mode-status">
          <span>Current Mode: {mode === 'cursor' ? 'Cursor Control' : 'Scroll Control'}</span>
        </div>
      </div>
      <div className="usage-guide">
        <h4>Usage Guide</h4>
        <ul>
          <li>
            <strong>In Cursor Control Mode:</strong>
            <ul>
              <li>Move the cursor left: Turn your head to the left. The system detects this motion and moves the cursor left.</li>
              <li>Move the cursor right: Turn your head to the right. The cursor will move right accordingly.</li>
              <li>Move the cursor up: Tilt your head upward. The cursor moves up on the screen.</li>
              <li>Move the cursor down: Tilt your head downward. The cursor moves down accordingly.</li>
              <li>Keep the cursor stationary: Look straight at the screen. If no face is detected, the cursor remains in place.</li>
              <li>Left-click: Tilt your head to the left to trigger a left-click.</li>
              <li>Right-click: Tilt your head to the right to trigger a right-click.</li>
            </ul>
          </li>
          <li>
            <strong>In Scroll Control Mode:</strong>
            <ul>
              <li>Scroll up: Turn your head to the left. The system detects this motion and scrolls the page up.</li>
              <li>Scroll down: Turn your head to the right. Similarly, the system scrolls the page down.</li>
            </ul>
          </li>
          <li><strong>Start/Stop:</strong> Use the button to start or stop the system.</li>
          <li><strong>Adjust Sensitivity:</strong> Customize settings as needed.</li>
          <li><strong>Support:</strong> Contact us if you encounter any issues.</li>
        </ul>
      </div>
      <div className="voice-guide">
        <h4>Voice Control Guide</h4>
        <ul>
          <li><strong>Start the camera:</strong> Say &quot;On camera&quot;.</li>
          <li><strong>Stop the camera:</strong> Say &quot;Off camera&quot;.</li>
          <li><strong>Switch to Cursor Control Mode:</strong> Say &quot;One&quot;.</li>
          <li><strong>Switch to Scroll Control Mode:</strong> Say &quot;Two&quot;.</li>
        </ul>
      </div>
      <div className="notes">
        <h4>Usage Notes:</h4>
        <ul>
          <li><strong>Lighting:</strong> Ensure sufficient lighting for face detection.</li>
          <li><strong>Sound:</strong> Use in a quiet environment to avoid noise interference. A microphone is recommended for better experience.</li>
          <li><strong>User Limit:</strong> The system supports only one user at a time.</li>
        </ul>
      </div>
    </footer>
  );
};

export default Footer;
