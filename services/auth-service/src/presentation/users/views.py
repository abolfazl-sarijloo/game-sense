from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from src.application.dto.register_user import RegisterUserDTO
from src.infrastructure.di.container import Container

from src.application.dto.login_user import LoginUserDTO
from .serializers import LoginUserSerializer
from .serializers import RegisterUserSerializer


class RegisterUserView(APIView):

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = RegisterUserDTO(
            username=serializer.validated_data["username"],
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        use_case = Container.register_user_use_case()

        try:
            user = use_case.execute(data)

        except ValueError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
            },
            status=status.HTTP_201_CREATED,
        )
    
class LoginUserView(APIView):

    def post(self, request):
        serializer = LoginUserSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        data = LoginUserDTO(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        use_case = Container.login_user_use_case()

        try:
            result = use_case.execute(data)

        except ValueError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response(
            {
                "access_token": result.access_token,
                "token_type": result.token_type,
            },
            status=status.HTTP_200_OK,
        )

class MeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        return Response(
            {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
            },
            status=status.HTTP_200_OK,
        )