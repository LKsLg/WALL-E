import { GridState } from '../types/models';
import { Bot, Trash2, Home, HelpCircle } from 'lucide-react';

export default function Grid({ grid }: { grid: GridState }) {
  const size = grid.grid_size;
  const cells = Array.from({ length: size * size }, (_, i) => {
    const x = i % size;
    const y = Math.floor(i / size);
    const content = grid.grid_state.find((e) => e.x === x && e.y === y);
    const isExplored = grid.explored?.some(([ex, ey]) => ex === x && ey === y);

    let bg = isExplored ? 'bg-gray-700' : 'bg-gray-900';
    let icon = null;
    if (content?.type === 'robot') icon = <Bot size={14} />;
    else if (content?.type === 'waste' && isExplored) icon = <Trash2 size={14} />;
    else if (content?.type === 'base') icon = <Home size={14} />;
    else if (!isExplored) icon = <HelpCircle size={12} className="opacity-30" />;

    return (
      <div key={i} className={`w-4 h-4 flex items-center justify-center text-white text-[10px] ${bg}`}>
        {icon}
      </div>
    );
  });

  return <div className={`grid grid-cols-32 gap-px mt-4`}>{cells}</div>;
}