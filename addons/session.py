import weakref
import asyncio

import asab.web
import asab.web.session


class AppSession(asab.web.session.Session):

    def __init__(self, storage, id, new, max_age=None):
        super().__init__(storage, id, new, max_age)
        storage.App.PubSub.subscribe("Application.tick!", self.on_tick)

        self.Loop = storage.App.Loop
        self.WebSockets = weakref.WeakSet()

    def on_tick(self, event_name):
        message = {'event_name': event_name, 'type': 'session'}

        wsc = list()
        for ws in self.WebSockets:
            wsc.append(ws.send_json(message))

        asyncio.gather(*wsc, loop=self.Loop)
