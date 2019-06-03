
class BaseException(Exception):
    template = "An unknown exception occurred"

    def __init__(self, **kwargs):
        self.msg = self.template % kwargs
        super(BaseException, self).__init__(self.msg)


class JsonFileNotFound(BaseException):
    template = "error:JsonFileNotFound File:%(file_name)s"


class TopologicalSortKeyError(BaseException):
    template = "error:Unable to find vertex :%(vertex_key)s"


class DetectiveAPIUtilsFileNotFound(BaseException):
    template = "error:File not found :%(file_name)s"
