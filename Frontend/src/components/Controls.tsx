interface ControlsProps {
  onStep: () => void;
  onAutoStart: () => void;
  onAutoStop: () => void;
  onReset: () => void;
  isAutoRunning: boolean;
}

export default function Controls({ 
  onStep, 
  onAutoStart, 
  onAutoStop, 
  onReset, 
  isAutoRunning 
}: ControlsProps) {
  return (
    <div className="my-4 space-x-2">
      <button 
        onClick={onStep}
        disabled={isAutoRunning}
        className={`px-3 py-2 rounded transition-colors ${
          isAutoRunning ? 'bg-gray-500' : 'bg-yellow-600 hover:bg-yellow-700'
        }`}
      >
        Step
      </button>

      <button 
        onClick={onAutoStart}
        disabled={isAutoRunning}
        className={`px-3 py-2 rounded transition-colors ${
          isAutoRunning ? 'bg-gray-500' : 'bg-green-600 hover:bg-green-700'
        }`}
      >
        Start Auto
      </button>

      <button 
        onClick={onAutoStop}
        disabled={!isAutoRunning}
        className={`px-3 py-2 rounded transition-colors ${
          !isAutoRunning ? 'bg-gray-500' : 'bg-red-600 hover:bg-red-700'
        }`}
      >
        Stop Auto
      </button>

      <button 
        onClick={onReset}
        disabled={isAutoRunning}
        className={`px-3 py-2 rounded bg-blue-600 hover:bg-blue-700 transition-colors`}
      >
        Reset
      </button>
    </div>
  );
}
