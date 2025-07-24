from rest_framework import serializers
from .models import Simulation, Robot, Waste

class RobotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Robot
        fields = ['robot_id', 'x', 'y', 'carrying_waste', 'strategy', 'memory']

class WasteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waste
        fields = ['x', 'y', 'collected']

class SimulationSerializer(serializers.ModelSerializer):
    robots = RobotSerializer(many=True, read_only=True)
    waste_items = WasteSerializer(many=True, read_only=True)
    
    class Meta:
        model = Simulation
        fields = ['id', 'name', 'grid_size', 'num_robots', 'num_waste', 
                 'base_x', 'base_y', 'status', 'current_turn', 
                 'created_at', 'updated_at', 'robots', 'waste_items']

class SimulationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Simulation
        fields = ['name', 'grid_size', 'num_robots', 'num_waste', 'base_x', 'base_y']
        
    def validate_grid_size(self, value):
        if value < 10 or value > 50:
            raise serializers.ValidationError("La taille de la grille doit être entre 10 et 50.")
        return value
    
    def validate_num_robots(self, value):
        if value < 1 or value > 20:
            raise serializers.ValidationError("Le nombre de robots doit être entre 1 et 20.")
        return value
    
    def validate_num_waste(self, value):
        if value < 1 or value > 100:
            raise serializers.ValidationError("Le nombre de déchets doit être entre 1 et 100.")
        return value
