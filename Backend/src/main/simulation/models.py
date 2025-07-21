from django.db import models
import json
import random
import math
from typing import List, Tuple, Dict, Optional

class Simulation(models.Model):
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('running', 'Running'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
    ]
    
    name = models.CharField(max_length=100)
    grid_size = models.IntegerField(default=32)
    num_robots = models.IntegerField(default=5)
    num_waste = models.IntegerField(default=20)
    base_x = models.IntegerField(default=16)
    base_y = models.IntegerField(default=16)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created')
    current_turn = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Simulation {self.name} - Turn {self.current_turn}"

class Robot(models.Model):
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE, related_name='robots')
    robot_id = models.IntegerField()
    x = models.IntegerField()
    y = models.IntegerField()
    carrying_waste = models.BooleanField(default=False)
    strategy = models.CharField(max_length=50, default='explore')
    memory = models.JSONField(default=dict)  # Pour stocker les zones explorées et déchets vus
    
    class Meta:
        unique_together = ['simulation', 'robot_id']

class Waste(models.Model):
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE, related_name='waste_items')
    x = models.IntegerField()
    y = models.IntegerField()
    collected = models.BooleanField(default=False)
    collected_by = models.ForeignKey(Robot, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        unique_together = ['simulation', 'x', 'y']
