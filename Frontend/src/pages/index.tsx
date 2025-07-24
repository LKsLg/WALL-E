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
  const isAutoRunningRef = useRef(false);
  const simulationRef = useRef<Simulation | null>(null);

  useEffect(() => {
    isAutoRunningRef.current = isAutoRunning;
  }, [isAutoRunning]);

  useEffect(() => {
    simulationRef.current = simulation;
  }, [simulation]);

  useEffect(() => {
    return () => {
      if (intervalRef.current) clearTimeout(intervalRef.current);
    };
  }, []);

  async function updateGridAndStats(simId: number) {
    try {
      const grid = await getGridState(simId);
      const s = await getStats(simId);
      setGridState(grid);
      setStats(s);
      if (s.status === 'completed' && isAutoRunningRef.current) stopAuto();
    } catch (error) {
      console.error('Error updating grid and stats:', error);
    }
  }

  async function handleStart(config: SimulationConfig) {
    try {
      stopAuto();
      const newSim = await createSimulation(config);
      setSimulation(newSim);
      await startSimulation(newSim.id);
      await updateGridAndStats(newSim.id);
    } catch (error) {
      console.error('Error starting simulation:', error);
    }
  }

  async function handleStep() {
    if (!simulationRef.current) return;
    try {
      await stepSimulation(simulationRef.current.id);
      await updateGridAndStats(simulationRef.current.id);
    } catch (error) {
      console.error('Error stepping simulation:', error);
    }
  }

  function startAuto() {
    if (!simulation || intervalRef.current) return;

    intervalRef.current = setInterval(async () => {
      await stepSimulation(simulation.id);
      await updateGridAndStats(simulation.id);
    }, 500);
}

  function stopAuto() {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  }

  async function handleReset() {
    try {
      stopAuto();
      if (!simulationRef.current) return;
      const resetSim = await resetSimulation(simulationRef.current.id);
      setSimulation(resetSim);
      await startSimulation(resetSim.id);
      await updateGridAndStats(resetSim.id);
    } catch (error) {
      console.error('Error resetting simulation:', error);
    }
  }

  return (
    <div className="bg-dark min-h-screen text-white p-4">
      <h1 className="text-2xl font-bold mb-4">WALL-E Simulation</h1>
      <ConfigForm onStart={handleStart} />
      {simulation && (
        <>
          <Controls 
            onStep={handleStep} 
            onAutoStart={startAuto} 
            onAutoStop={stopAuto} 
            onReset={handleReset}
            isAutoRunning={isAutoRunning}
          />
          <StatsPanel stats={stats} />
          {gridState && <Grid grid={gridState} />}
        </>
      )}
    </div>
  );
}