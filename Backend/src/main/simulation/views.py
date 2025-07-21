from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Simulation, Robot, Waste
from .serializers import SimulationSerializer, SimulationCreateSerializer
from .engine import SimulationEngine

class SimulationViewSet(viewsets.ModelViewSet):
    queryset = Simulation.objects.all().order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return SimulationCreateSerializer
        return SimulationSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Créer la simulation
        simulation = serializer.save()
        
        # Initialiser avec l'engine
        engine = SimulationEngine(simulation)
        engine.initialize_simulation()
        
        # Retourner la simulation complète
        response_serializer = SimulationSerializer(simulation)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """Démarre la simulation"""
        simulation = self.get_object()
        if simulation.status in ['created', 'paused']:
            simulation.status = 'running'
            simulation.save()
            return Response({'status': 'started'})
        return Response(
            {'error': 'La simulation ne peut pas être démarrée'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=True, methods=['post'])
    def pause(self, request, pk=None):
        """Met en pause la simulation"""
        simulation = self.get_object()
        if simulation.status == 'running':
            simulation.status = 'paused'
            simulation.save()
            return Response({'status': 'paused'})
        return Response(
            {'error': 'La simulation ne peut pas être mise en pause'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=True, methods=['post'])
    def reset(self, request, pk=None):
        """Remet à zéro la simulation"""
        simulation = self.get_object()
        engine = SimulationEngine(simulation)
        engine.initialize_simulation()
        
        serializer = SimulationSerializer(simulation)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def step(self, request, pk=None):
        """Exécute un tour de simulation"""
        simulation = self.get_object()
        if simulation.status != 'running':
            return Response(
                {'error': 'La simulation doit être en cours pour exécuter un tour'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        engine = SimulationEngine(simulation)
        turn_actions = engine.process_turn()
        
        # Retourner l'état mis à jour
        serializer = SimulationSerializer(simulation)
        return Response({
            'simulation': serializer.data,
            'turn_actions': turn_actions
        })
    
    @action(detail=True, methods=['get'])
    def grid_state(self, request, pk=None):
        """Retourne l'état actuel de la grille"""
        simulation = self.get_object()
        engine = SimulationEngine(simulation)
        grid_state = engine.get_grid_state()
        
        return Response({
            'grid_state': grid_state,
            'grid_size': simulation.grid_size,
            'base_position': [simulation.base_x, simulation.base_y],
            'current_turn': simulation.current_turn,
            'status': simulation.status
        })
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Retourne les statistiques de la simulation"""
        simulation = self.get_object()
        
        total_waste = simulation.waste_items.count()
        collected_waste = simulation.waste_items.filter(collected=True).count()
        robots_carrying = simulation.robots.filter(carrying_waste=True).count()
        
        return Response({
            'current_turn': simulation.current_turn,
            'total_waste': total_waste,
            'collected_waste': collected_waste,
            'remaining_waste': total_waste - collected_waste,
            'robots_carrying': robots_carrying,
            'completion_percentage': (collected_waste / total_waste * 100) if total_waste > 0 else 0,
            'status': simulation.status
        })
