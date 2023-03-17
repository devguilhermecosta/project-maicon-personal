class ImageNotFoundError(BaseException):
    def __init__(self, msg: str, path=None):
        self.msg = msg
        self.path = path

    def __str__(self):
        if self.path is not None:
            return f'{self.msg} - Path: {self.path}'


class AttributeNotFound(BaseException):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self) -> str:
        return self.msg
