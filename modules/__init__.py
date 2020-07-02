import asab
from .my_service import MyService


class MyModule(asab.Module):
    def __init__(self, app):
        super().__init__(app)
        self.service = MyService(app, "MyService")
