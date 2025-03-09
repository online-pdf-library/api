from api.service import Service
from api.use_case.auth import AuthUseCase


class UseCase:
    def __init__(self, service: Service) -> None:
        self.auth = AuthUseCase(service=service)
