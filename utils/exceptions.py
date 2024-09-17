from rest_framework.serializers import ValidationError


class UnautherizedError(ValidationError):
    def __init__(self, detail="Something went wrong", status_code=403):
        self.detail = detail
        self.status_code = status_code


class UserNotVerifiedError(ValidationError):
    def __init__(self, detail="User email not verified", status_code=401):
        self.detail = detail
        self.status_code = status_code
