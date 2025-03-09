import abc

from fastapi import status


class VisibleError(Exception, abc.ABC):
    @abc.abstractmethod
    def status_code(self) -> int: ...


class AlreadyExistsError(VisibleError):
    def __init__(self, *_: object) -> None:
        super().__init__("Already exists")

    def status_code(self) -> int:
        return status.HTTP_400_BAD_REQUEST


class NotFoundError(VisibleError):
    def __init__(self, *_: object) -> None:
        super().__init__("Not found")

    def status_code(self) -> int:
        return status.HTTP_404_NOT_FOUND


class NotAuthenticatedError(VisibleError):
    def __init__(self) -> None:
        super().__init__("Not authenticated")

    def status_code(self) -> int:
        return status.HTTP_401_UNAUTHORIZED


class NotAuthorizedError(VisibleError):
    def __init__(self) -> None:
        super().__init__("Not authorized")

    def status_code(self) -> int:
        return status.HTTP_403_FORBIDDEN
