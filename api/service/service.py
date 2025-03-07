from api.repository import Repository
from api.service.user import UserService


class Service:
    def __init__(self, repository: Repository) -> None:
        self.user = UserService(repository=repository)
