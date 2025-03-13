const Controls = ({ isRunning, toggleTracking, mode, setMode, sensitivity, setSensitivity }) => {
  return (
    <div className="controls">
      <button 
        className={`control-btn ${isRunning ? 'stop' : 'start'}`}
        onClick={toggleTracking}
      >
        {isRunning ? 'Stop' : 'Start'}
      </button>

      <div className="mode-selector">
        <button 
          className={`mode-btn ${mode === 'cursor' ? 'active' : ''}`}
          onClick={() => setMode('cursor')}
        >
          Cursor Mode
        </button>
        <button 
          className={`mode-btn ${mode === 'wheel' ? 'active' : ''}`}
          onClick={() => setMode('wheel')}
        >
          Scroll Mode
        </button>
      </div>

      <div className="sensitivity-control">
        <label htmlFor="sensitivity">Sensitivity:</label>
        <input 
          type="range" 
          id="sensitivity" 
          min="1" 
          max="10" 
          value={sensitivity}
          onChange={(e) => setSensitivity(Number(e.target.value))}
        />
        <span>{sensitivity}</span>
      </div>
    </div>
  );
};

export default Controls;
