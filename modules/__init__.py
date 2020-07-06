import asab
from .my_service import MyService
from .database import DatabaseService


class Modules(asab.Module):
    def __init__(self, app):
        super().__init__(app)
        self.service = MyService(app, "MyService")
        self.service = DatabaseService(app, "DatabaseService")
