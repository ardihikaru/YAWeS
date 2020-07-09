import asab.web
import asab.web.session


class WebSocketFactory(asab.web.WebSocketFactory):

    def __init__(self, app):
        super().__init__(app)

        app.PubSub.subscribe("Application.tick/10!", self.on_tick)

    async def on_request(self, request):
        session = request.get('Session')
        ws = await super().on_request(request)
        session.WebSockets.add(ws)
        return ws

    async def on_message(self, request, websocket, message):
        print("WebSocket message", message)

    def on_tick(self, event_name):
        message = {'event_name': event_name, 'type': 'factory'}

        wsc = list()
        for ws in self.WebSockets:
            wsc.append(ws.send_json(message))

        self.send_parallely(wsc)
