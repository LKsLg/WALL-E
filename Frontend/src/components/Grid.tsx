import { GridState } from "../types/models";

export default function Grid({ grid }: { grid: GridState | null }) {
  if (!grid) return null;
  return (
    <div className="grid grid-cols-32 gap-0.5">
      {grid.cells.flat().map((cell, i) => (
        <div
          key={i}
          className="w-4 h-4 border text-xs flex items-center justify-center"
          style={{ backgroundColor: cell.base ? "blue" : cell.trash ? "green" : cell.robot ? "red" : "white" }}
        >
          {cell.robot ? "🤖" : cell.trash ? "🗑️" : cell.base ? "🏠" : ""}
        </div>
      ))}
    </div>
  );
}