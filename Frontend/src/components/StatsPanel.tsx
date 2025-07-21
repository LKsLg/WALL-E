export default function StatsPanel({ stats }: { stats?: { turns: number; remaining: number } }) {
  if (!stats) return null;
  return (
    <div>
      <p>Turns Elapsed: {stats.turns}</p>
      <p>Trash Remaining: {stats.remaining}</p>
    </div>
  );
}

