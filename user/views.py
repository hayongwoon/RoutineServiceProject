from django.contrib.auth import authenticate, login, logout

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions

from user.serializers import UserSerializer
from user.models import User as UserModel


class CreateUserApiView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserLoginApiView(APIView):
    def post(self, request):
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        try:
            UserModel.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            if not user:
                return Response({"error": "패스워드가 일치하지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)

            login(request, user)
            return Response({"message": "로그인 성공!!"}, status=status.HTTP_200_OK)

        except UserModel.DoesNotExist:
            return Response({"error": "존재하지 않는 계정입니다."}, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"msg": "로그아웃 됐습니다."}, status=status.HTTP_202_ACCEPTED)
