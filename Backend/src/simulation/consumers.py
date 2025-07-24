import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Simulation
from .engine import SimulationEngine
from .serializers import SimulationSerializer

class SimulationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.simulation_id = self.scope['url_route']['kwargs']['simulation_id']
        self.simulation_group_name = f'simulation_{self.simulation_id}'
        self.auto_task = None

        await self.channel_layer.group_add(
            self.simulation_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.simulation_group_name,
            self.channel_name
        )
        if self.auto_task:
            self.auto_task.cancel()

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'start_auto_run':
            if self.auto_task and not self.auto_task.done():
                self.auto_task.cancel()
            self.auto_task = asyncio.create_task(self.auto_run_simulation())

        elif action == 'stop_auto_run':
            if self.auto_task:
                self.auto_task.cancel()
                self.auto_task = None

    async def auto_run_simulation(self):
        try:
            while True:
                simulation = await self.get_simulation()
                if not simulation or simulation.status != 'running':
                    break

                await self.process_simulation_turn()

                await self.channel_layer.group_send(
                    self.simulation_group_name,
                    {
                        'type': 'simulation_update',
                        'data': await self.get_simulation_data()
                    }
                )

                await asyncio.sleep(0.5)
        except asyncio.CancelledError:
            pass

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
        await self.send(text_data=json.dumps({
            'type': 'update',
            'data': event['data']
        }))
