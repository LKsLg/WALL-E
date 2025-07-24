export default function StatsPanel({ stats }: { stats: any }) {
  if (!stats) return null;
  return (
    <div className="bg-gray-800 p-2 rounded my-2">
      <p>Turn: {stats.current_turn}</p>
      <p>Remaining Waste: {stats.remaining_waste}</p>
      <p>Collected Waste: {stats.collected_waste}</p>
      <p>Robots Carrying: {stats.robots_carrying}</p>
      <p>Status: {stats.status}</p>
    </div>
  );
}