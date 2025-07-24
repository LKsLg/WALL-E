export interface Simulation {
  id: number;
  grid_size: number;
  current_turn: number;
  status: string;
}

export interface SimulationConfig {
  robots: number;
  trash: number;
  base: {
    x: number;
    y: number;
  };
}

export interface GridState {
  grid_state: Array<{ x: number; y: number; type: string; id?: number; carrying_waste?: boolean }>;
  grid_size: number;
  base_position: [number, number];
  current_turn: number;
  status: string;
  explored?: [number, number][];
}