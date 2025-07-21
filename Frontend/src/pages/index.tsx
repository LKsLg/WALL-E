import { useState, useEffect } from "react";
import ConfigForm from "../components/ConfigForm";                     
import Grid from "../components/Grid";
import Controls from "../components/Controls";
import StatsPanel from "../components/StatsPanel";
import { getSimulationState, startSimulation, pauseSimulation, resetSimulation } from "../services/api";
import { GridState } from "../types/models";

export default function Home() {
  const [grid, setGrid] = useState<GridState | null>(null);
  const [intervalId, setIntervalId] = useState<number | null>(null);

  useEffect(() => {
    if (intervalId) {
      const id = setInterval(async () => {
        const state = await getSimulationState();
        setGrid(state);
      }, 1000);
      return () => clearInterval(id);
    }
  }, [intervalId]);

  return (
    <div className="p-4 space-y-4">
      <ConfigForm onStart={async (config) => {
        await startSimulation(config);
        setIntervalId(setInterval(async () => {
          const state = await getSimulationState();
          setGrid(state);
        }, 1000));
      }} />
      <Controls
        onPause={async () => {
          await pauseSimulation();
          if (intervalId) clearInterval(intervalId);
        }}
        onReset={async () => {
          await resetSimulation();
          setGrid(null);
          if (intervalId) clearInterval(intervalId);
        }}
      />
      <StatsPanel stats={grid?.stats} />
      <Grid grid={grid} />
    </div>
  );
}