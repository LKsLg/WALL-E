import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Simulation
from .engine import SimulationEngine
from .serializers import SimulationSerializer
import asyncio

class SimulationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.simulation_id = self.scope['url_route']['kwargs']['simulation_id']
        self.simulation_group_name = f'simulation_{self.simulation_id}'
        
        # Rejoindre le groupe de la simulation
        await self.channel_layer.group_add(
            self.simulation_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        # Quitter le groupe de la simulation
        await self.channel_layer.group_discard(
            self.simulation_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']
        
        if action == 'start_auto_run':
            asyncio.create_task(self.auto_run_simulation())
        elif action == 'stop_auto_run':
            self.stop_auto_run = True
    
    async def auto_run_simulation(self):
        """Exécute automatiquement la simulation"""
        self.stop_auto_run = False
        
        while not self.stop_auto_run:
            simulation = await self.get_simulation()
            if not simulation or simulation.status != 'running':
                break
            
            # Exécuter un tour
            turn_actions = await self.process_simulation_turn()
            
            # Envoyer la mise à jour
            await self.channel_layer.group_send(
                self.simulation_group_name,
                {
                    'type': 'simulation_update',
                    'data': await self.get_simulation_data()
                }
            )
            
            # Attendre un peu avant le prochain tour
            await asyncio.sleep(0.5)  # 500ms entre chaque tour
    
    @database_sync_to_async
    def get_simulation(self):
        try:
            return Simulation.objects.get(id=self.simulation_id)
        except Simulation.DoesNotExist:
            return None
    
    @database_sync_to_async
    def process_simulation_turn(self):
        simulation = Simulation.objects.get(id=self.simulation_id)
        engine = SimulationEngine(simulation)
        return engine.process_turn()
    
    @database_sync_to_async
    def get_simulation_data(self):
        simulation = Simulation.objects.get(id=self.simulation_id)
        serializer = SimulationSerializer(simulation)
        return serializer.data
    
    async def simulation_update(self, event):
        # Envoyer la mise à jour au WebSocket
        await self.send(text_data=json.dumps({
            'type': 'update',
            'data': event['data']
        }))
