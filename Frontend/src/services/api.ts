import axios from 'axios';
import { Simulation, GridState, SimulationConfig } from '../types/models';

const BASE_URL = 'http://localhost:8000/api/simulations';

export async function createSimulation(config: SimulationConfig): Promise<Simulation> {
  const res = await axios.post(BASE_URL + '/', {
    name: "Sim",
    grid_size: 32,
    num_robots: config.robots,
    num_waste: config.trash,
    base_x: config.base.x,
    base_y: config.base.y,
  });
  return res.data;
}

export async function startSimulation(id: number) {
  await axios.post(`${BASE_URL}/${id}/start/`);
}

export async function pauseSimulation(id: number) {
  await axios.post(`${BASE_URL}/${id}/pause/`);
}

export async function stepSimulation(id: number) {
  await axios.post(`${BASE_URL}/${id}/step/`);
}

export async function resetSimulation(id: number) {
  const res = await axios.post(`${BASE_URL}/${id}/reset/`);
  return res.data;
}

export async function getGridState(id: number): Promise<GridState> {
  const res = await axios.get(`${BASE_URL}/${id}/grid_state/`);
  return res.data;
}

export async function getStats(id: number) {
  const res = await axios.get(`${BASE_URL}/${id}/statistics/`);
  return res.data;
}