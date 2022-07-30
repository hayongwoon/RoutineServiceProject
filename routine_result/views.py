from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions

from routine_result.models import RoutineResult as RoutineResultModel
from routine_result.permissions import RoutineIsMadeByMe as RoutineIsMadeByMePermission


# Create your views here.
class RoutineResultAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, RoutineIsMadeByMePermission]

    def put(self, request):
        RoutineResultModel.objects.filter(routine=request.data["routine_id"]).update(result=request.data["result"])
        return Response({'message': '수정 완료'}, status=status.HTTP_200_OK)
