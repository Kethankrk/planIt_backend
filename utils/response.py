from rest_framework.views import Response
from rest_framework import status


class CustomResponse:
    def __init__(
        self,
        error: dict = {},
        message: str = "",
        response: dict = {},
        error_code: int = 0,
    ) -> None:
        self.error = error
        self.message = message
        self.response = response
        self.error_code = error_code

    def success(self, status: int = status.HTTP_200_OK) -> Response:
        return Response(
            data={
                "hasError": False,
                "error": self.error,
                "response": self.response,
                "message": self.message,
                "errorCode": self.error_code,
            },
            status=status,
        )

    def failure(self, status: int = status.HTTP_400_BAD_REQUEST) -> Response:
        return Response(
            data={
                "hasError": True,
                "error": self.error,
                "response": self.response,
                "message": self.message,
                "errorCode": self.error_code,
            },
            status=status,
        )
