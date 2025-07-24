import { useState } from "react";
import { SimulationConfig } from "../types/models";

export default function ConfigForm({ onStart }: { onStart: (config: SimulationConfig) => void }) {
  const [robots, setRobots] = useState(5);
  const [trash, setTrash] = useState(20);
  const [baseX, setBaseX] = useState(0);
  const [baseY, setBaseY] = useState(0);

  return (
    <form
      className="space-x-2 mb-4"
      onSubmit={(e) => {
        e.preventDefault();
        onStart({ robots, trash, base: { x: baseX, y: baseY } });
      }}
    >
      <input className="text-black" type="number" value={robots} onChange={(e) => setRobots(+e.target.value)} placeholder="Robots" />
      <input className="text-black" type="number" value={trash} onChange={(e) => setTrash(+e.target.value)} placeholder="Trash" />
      <input className="text-black" type="number" value={baseX} onChange={(e) => setBaseX(+e.target.value)} placeholder="Base X" />
      <input className="text-black" type="number" value={baseY} onChange={(e) => setBaseY(+e.target.value)} placeholder="Base Y" />
      <button className="bg-blue-600 px-2 py-1 rounded" type="submit">Start</button>
    </form>
  );
}