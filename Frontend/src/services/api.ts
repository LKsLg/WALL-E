import axios from "axios";
import { SimulationConfig, GridState } from "../types/models";

const BASE_URL = "http://localhost:8000/api/simulation";

export async function startSimulation(config: SimulationConfig) {
    await axios.post(`${BASE_URL}/start`, config);
}

export async function pauseSimulation() {
    await axios.post(`${BASE_URL}/pause`);
}

export async function resetSimulation() {
    await axios.post(`${BASE_URL}/reset`);
}

export async function getSimulationState(): Promise<GridState> {
    const res = await axios.get<GridState>(`${BASE_URL}/state`);
    return res.data;
}