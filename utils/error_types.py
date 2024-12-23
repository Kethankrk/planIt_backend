from enum import Enum

class ErrorTypes(Enum):
    INVALID_INPUT = 100
    EMAIL_ALREADY_EXISTS = 101
    EMAIL_NOT_VERIFIED = 102

    def __str__(self):
        return f"{self.code}: {self.message}"