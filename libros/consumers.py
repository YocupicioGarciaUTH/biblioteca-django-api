import json
from channels.generic.websocket import AsyncWebsocketConsumer

class LibroConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "libros_updates"
        # Unirse al grupo de notificaciones
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Salir del grupo al desconectar
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # === AGREGAR ESTE MÉTODO PARA EL CHAT ===
    async def receive(self, text_data):
        """
        Recibe mensajes enviados desde el navegador (Frontend)
        y los reenvía a todos los demás usuarios conectados.
        """
        data = json.loads(text_data)
        message = data.get('message', '')
        username = data.get('username', 'Invitado')

        # Enviar el mensaje al grupo para que todos lo reciban
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message', # Este nombre debe coincidir con el método de abajo
                'message': message,
                'username': username
            }
        )

    # Manejador para los mensajes del chat
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username']
        }))

    # Manejador para las notificaciones automáticas de libros
    async def libro_notification(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'titulo': event['titulo'],
            'username': 'Sistema'
        }))