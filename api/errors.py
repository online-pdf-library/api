import abc


class VisibleError(Exception, abc.ABC):
    pass


class AlreadyExistsError(VisibleError):
    def __init__(self, *_: object) -> None:
        super().__init__("Already exists")


class NotFoundError(VisibleError):
    def __init__(self, *_: object) -> None:
        super().__init__("Not found")


class NotAuthenticatedError(VisibleError):
    def __init__(self) -> None:
        super().__init__("Not authenticated")


class NotAuthorizedError(VisibleError):
    def __init__(self) -> None:
        super().__init__("Not authorized")
