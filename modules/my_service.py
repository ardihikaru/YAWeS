import asab


class MyService(asab.Service):
    def __init__(self, app, service_name):
        super().__init__(app, service_name)

    def hallo(self):
        print("Hello, I am a service!")
