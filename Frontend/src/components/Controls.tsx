export default function Controls({ onStep, onAutoStart, onAutoStop, onReset }: { onStep: () => void; onAutoStart: () => void; onAutoStop: () => void; onReset: () => void }) {
  return (
    <div className="my-2 space-x-2">
      <button onClick={onStep} className="bg-yellow-600 px-2 py-1 rounded">
        Next Turn
      </button>
      <button onClick={onAutoStart} className="bg-green-600 px-2 py-1 rounded">
        Start Auto
      </button>
      <button onClick={onAutoStop} className="bg-red-600 px-2 py-1 rounded">
        Stop Auto
      </button>
      <button onClick={onReset} className="bg-blue-600 px-2 py-1 rounded">
        Reset
      </button>
    </div>
  );
}