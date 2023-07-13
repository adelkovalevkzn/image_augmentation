class CoordinateError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class UnknownMethodError(Exception):
    def __init__(self):
        self.message = 'Неизвестный метод'

    def __str__(self):
        return self.message