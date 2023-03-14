class ImageNotFoundError(BaseException):
    def __init__(self, msg: str, path=None):
        self.msg = msg
        self.path = path

    def __str__(self):
        if self.path is not None:
            return f'{self.msg} - Path: {self.path}'
