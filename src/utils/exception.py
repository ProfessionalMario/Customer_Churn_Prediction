import sys


class AppException(Exception):
    """Base application exception."""

    def __init__(self, message: str, error_detail: sys = sys):
        super().__init__(message)

        _, _, exc_tb = error_detail.exc_info()

        if exc_tb:
            self.file = exc_tb.tb_frame.f_code.co_filename
            self.line = exc_tb.tb_lineno
        else:
            self.file = None
            self.line = None

        self.message = message

    def __str__(self):
        return f"{self.message} | File: {self.file} | Line: {self.line}"


class PredictionError(AppException):
    """Raised when prediction fails."""
    pass


class PipelineLoadError(AppException):
    """Raised when pipeline fails to load."""
    pass