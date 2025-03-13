const Footer = ({ isRunning, mode }) => {
  return (
    <footer>
      <div className="status">
        <span className={`status-indicator ${isRunning ? 'active' : ''}`}></span>
        {isRunning ? 'System Active' : 'System Inactive'}
      </div>
      <div className="mode-status">
        Current Mode: {mode === 'cursor' ? 'Cursor Control' : 'Scroll Control'}
      </div>
    </footer>
  );
};

export default Footer;
