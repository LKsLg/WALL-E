import { useEffect, useState, useRef } from 'react';
import { Simulation, GridState, SimulationConfig } from '../types/models';
import { createSimulation, getGridState, startSimulation, stepSimulation, getStats, resetSimulation } from '../services/api';
import ConfigForm from '../components/ConfigForm';
import Grid from '../components/Grid';
import Controls from '../components/Controls';
import StatsPanel from '../components/StatsPanel';

export default function Home() {
  const [simulation, setSimulation] = useState<Simulation | null>(null);
  const [gridState, setGridState] = useState<GridState | null>(null);
  const [stats, setStats] = useState<any>(null);
  const [isAutoRunning, setIsAutoRunning] = useState(false);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  async function updateGridAndStats(simId: number) {
    const grid = await getGridState(simId);
    const s = await getStats(simId);
    setGridState(grid);
    setStats(s);
    if (s.status === 'completed') {
      stopAuto();
    }
  }

  async function handleStart(config: SimulationConfig) {
    const newSim = await createSimulation(config);
    setSimulation(newSim);
    await startSimulation(newSim.id);
    await updateGridAndStats(newSim.id);
  }

  async function handleStep() {
    if (simulation) {
      await stepSimulation(simulation.id);
      await updateGridAndStats(simulation.id);
    }
  }

  function startAuto() {
    if (!simulation || isAutoRunning) return;

    setIsAutoRunning(true);

    const runStep = async () => {
      if (!simulation || !isAutoRunning) return;

      await stepSimulation(simulation.id);
      await updateGridAndStats(simulation.id);

      const s = await getStats(simulation.id);
      if (s.status !== 'completed' && isAutoRunning) {
        intervalRef.current = setTimeout(runStep, 500);
      } else {
        stopAuto();
      }
    };

    runStep();
  }

  function stopAuto() {
    setIsAutoRunning(false);
    if (intervalRef.current) {
      clearTimeout(intervalRef.current);
      intervalRef.current = null;
    }
  }

  async function handleReset() {
    if (simulation) {
      const sim = await resetSimulation(simulation.id);
      setSimulation(sim);
      await updateGridAndStats(sim.id);
    }
  }

  return (
    <div className="bg-dark min-h-screen text-white p-4">
      <ConfigForm onStart={handleStart} />
      {simulation && (
        <>
          <Controls onStep={handleStep} onAutoStart={startAuto} onAutoStop={stopAuto} onReset={handleReset} />
          <StatsPanel stats={stats} />
          {gridState && <Grid grid={gridState} />}
        </>
      )}
    </div>
  );
}