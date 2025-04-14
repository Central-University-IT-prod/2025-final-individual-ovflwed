class NotFoundError(Exception):
    detail: str

    def __init__(self, detail: str = "Сущность с данным ID не найдена.") -> None:
        self.detail = detail


class BusinessValidationError(Exception):
    detail: str

    def __init__(self, detail: str = "Некорректные данные запроса.") -> None:
        self.detail = detail


class AdAlreadyClickedError(Exception):
    pass


class AdWasNotShownBeforeError(Exception):
    pass
