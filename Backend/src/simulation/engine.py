import random
import math
from .models import Robot, Waste

class SimulationEngine:
    def __init__(self, simulation):
        self.simulation = simulation
        self.grid_size = simulation.grid_size
        self.base_pos = (simulation.base_x, simulation.base_y)
        
    def get_grid_state(self):
        """Retourne l'état actuel de la grille sous forme de liste sérialisable"""
        robots = list(self.simulation.robots.all())
        waste_items = list(self.simulation.waste_items.filter(collected=False))
        
        grid = []

        # Ajout des robots
        for robot in robots:
            grid.append({
                'x': robot.x,
                'y': robot.y,
                'type': 'robot',
                'id': robot.robot_id,
                'carrying_waste': robot.carrying_waste
            })

        # Ajout des déchets
        for waste in waste_items:
            grid.append({
                'x': waste.x,
                'y': waste.y,
                'type': 'waste'
            })

        # Ajout de la base
        grid.append({
            'x': self.base_pos[0],
            'y': self.base_pos[1],
            'type': 'base'
        })

        return grid
    
    def get_robot_vision(self, robot, radius=5):
        """Retourne ce que le robot peut voir dans un rayon donné"""
        vision = {}
        robot_x, robot_y = robot.x, robot.y
        
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                x, y = robot_x + dx, robot_y + dy
                if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
                    # Vérifier s'il y a un déchet
                    waste = self.simulation.waste_items.filter(x=x, y=y, collected=False).first()
                    if waste:
                        vision[(x, y)] = 'waste'
                    # Vérifier s'il y a un autre robot
                    elif self.simulation.robots.filter(x=x, y=y).exclude(id=robot.id).exists():
                        vision[(x, y)] = 'robot'
                    # Vérifier si c'est la base
                    elif (x, y) == self.base_pos:
                        vision[(x, y)] = 'base'
                    else:
                        vision[(x, y)] = 'empty'
        
        return vision
    
    def update_robot_memory(self, robot):
        """Met à jour la mémoire du robot avec sa vision actuelle"""
        vision = self.get_robot_vision(robot)
        memory = robot.memory or {}
        
        # Mise à jour des zones explorées
        if 'explored' not in memory:
            memory['explored'] = []
        if 'known_waste' not in memory:
            memory['known_waste'] = []
        
        for (x, y), cell_type in vision.items():
            pos_tuple = [x, y]  # Convert to list for JSON serialization
            if pos_tuple not in memory['explored']:
                memory['explored'].append(pos_tuple)
            
            if cell_type == 'waste' and pos_tuple not in memory['known_waste']:
                memory['known_waste'].append(pos_tuple)
        
        # Nettoyer les déchets collectés de la mémoire
        memory['known_waste'] = [
            pos for pos in memory['known_waste']
            if self.simulation.waste_items.filter(x=pos[0], y=pos[1], collected=False).exists()
        ]
        
        robot.memory = memory
        robot.save()
    
    def get_valid_moves(self, robot):
        """Retourne les mouvements valides pour un robot"""
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # haut, bas, droite, gauche
        
        for dx, dy in directions:
            new_x, new_y = robot.x + dx, robot.y + dy
            
            # Vérifier les limites de la grille
            if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size:
                # Vérifier qu'aucun autre robot n'occupe cette position
                if not self.simulation.robots.filter(x=new_x, y=new_y).exclude(id=robot.id).exists():
                    moves.append((new_x, new_y))
        
        return moves
    
    def calculate_distance(self, pos1, pos2):
        """Calcule la distance Manhattan entre deux positions"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def robot_strategy_explore(self, robot):
        """Stratégie d'exploration intelligente avec communication"""
        memory = robot.memory or {}
        
        # Si le robot porte un déchet, aller à la base
        if robot.carrying_waste:
            return self.move_towards_target(robot, self.base_pos)
        
        # Chercher des déchets connus dans la mémoire
        known_waste = memory.get('known_waste', [])
        if known_waste:
            closest_waste = min(
                known_waste,
                key=lambda pos: self.calculate_distance((robot.x, robot.y), tuple(pos))
            )
            return self.move_towards_target(robot, tuple(closest_waste))
        
        # Exploration vers une zone inexplorée
        return self.explore_unknown_area(robot)
    
    def move_towards_target(self, robot, target_pos):
        """Déplace le robot vers une position cible"""
        valid_moves = self.get_valid_moves(robot)
        if not valid_moves:
            return 'wait'
        
        # Choisir le mouvement qui rapproche le plus de la cible
        best_move = min(
            valid_moves,
            key=lambda pos: self.calculate_distance(pos, target_pos)
        )
        
        robot.x, robot.y = best_move
        robot.save()
        return 'move'
    
    def explore_unknown_area(self, robot):
        """Explore une zone inconnue"""
        memory = robot.memory or {}
        explored = {tuple(pos) for pos in memory.get('explored', [])}
        
        valid_moves = self.get_valid_moves(robot)
        if not valid_moves:
            return 'wait'
        
        # Prioriser les mouvements vers des zones inexplorées
        unexplored_moves = [move for move in valid_moves if move not in explored]
        
        if unexplored_moves:
            chosen_move = random.choice(unexplored_moves)
        else:
            chosen_move = random.choice(valid_moves)
        
        robot.x, robot.y = chosen_move
        robot.save()
        return 'move'
    
    def process_robot_turn(self, robot):
        """Traite le tour d'un robot"""
        actions_taken = []
        
        # Mettre à jour la mémoire du robot
        self.update_robot_memory(robot)
        
        # Vérifier si le robot peut ramasser un déchet
        if not robot.carrying_waste:
            waste = self.simulation.waste_items.filter(
            x=robot.x, y=robot.y, collected=False
            ).first()
            if waste:
                robot.carrying_waste = True
                robot.save()
                waste.collected_by = robot
                waste.save()
                actions_taken.append('pickup')
                return actions_taken

        
        # Vérifier si le robot peut déposer un déchet à la base
        if robot.carrying_waste and (robot.x, robot.y) == self.base_pos:
            waste = self.simulation.waste_items.filter(
                collected_by=robot, collected=False
            ).first()
            if waste:
                waste.collected = True
                waste.save()

            robot.carrying_waste = False
            robot.save()
            actions_taken.append('deposit')
            return actions_taken

        # Exécuter la stratégie de mouvement
        action = self.robot_strategy_explore(robot)
        actions_taken.append(action)
        
        return actions_taken
    
    def process_turn(self):
        """Traite un tour complet de simulation"""
        if self.simulation.status != 'running':
            return False
        
        robots = list(self.simulation.robots.all())
        turn_actions = {}
        
        for robot in robots:
            actions = self.process_robot_turn(robot)
            turn_actions[robot.robot_id] = actions
        
        self.simulation.current_turn += 1
        self.simulation.save()
        
        # Vérifier si la simulation est terminée
        remaining_waste = self.simulation.waste_items.filter(collected=False).count()
        carrying_robots = self.simulation.robots.filter(carrying_waste=True).count()
        
        if remaining_waste == 0 and carrying_robots == 0:
            self.simulation.status = 'completed'
            self.simulation.save()
        
        return turn_actions
    
    def initialize_simulation(self):
        """Initialise la simulation avec des positions aléatoires"""
        # Nettoyer les données existantes
        self.simulation.robots.all().delete()
        self.simulation.waste_items.all().delete()
        
        occupied_positions = set()
        occupied_positions.add(self.base_pos)
        
        # Créer les robots
        for i in range(self.simulation.num_robots):
            while True:
                x = random.randint(0, self.grid_size - 1)
                y = random.randint(0, self.grid_size - 1)
                if (x, y) not in occupied_positions:
                    Robot.objects.create(
                        simulation=self.simulation,
                        robot_id=i,
                        x=x,
                        y=y,
                        memory={'explored': [], 'known_waste': []}
                    )
                    occupied_positions.add((x, y))
                    break
        
        # Créer les déchets
        for i in range(self.simulation.num_waste):
            while True:
                x = random.randint(0, self.grid_size - 1)
                y = random.randint(0, self.grid_size - 1)
                if (x, y) not in occupied_positions:
                    Waste.objects.create(
                        simulation=self.simulation,
                        x=x,
                        y=y
                    )
                    occupied_positions.add((x, y))
                    break
        
        self.simulation.current_turn = 0
        self.simulation.status = 'created'
        self.simulation.save()