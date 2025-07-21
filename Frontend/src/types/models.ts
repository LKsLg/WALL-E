export interface SimulationConfig {
  robots: number;
  trash: number;
  base: { x: number; y: number };
}

export interface GridCell {
  robot: boolean;
  trash: boolean;
  base: boolean;
}

export interface GridState {
  cells: GridCell[][];
  stats: {
    turns: number;
    remaining: number;
  };
}