export default function Controls({ onPause, onReset }: { onPause: () => void; onReset: () => void }) {
  return (
    <div className="space-x-2">
      <button onClick={onPause}>Pause</button>
      <button onClick={onReset}>Reset</button>
    </div>
  );
}