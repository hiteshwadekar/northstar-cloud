
class BaseException(Exception):
    template = "An unknown exception occurred"

    def __init__(self, **kwargs):
        self.msg = self.template % kwargs
        super(BaseException, self).__init__(self.msg)


class JsonFileNotFound(BaseException):
    template = "error:JsonFileNotFound File:%(file_name)s"


class ImageNameNotProvided(BaseException):
    template = "error:request do not have image name or image id"
