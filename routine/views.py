from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions

from routine.serializers import RoutineSerialzer, GetTodayRoutineListSerializer
from routine.models import Routine as RoutineModel
from routine_result.models import RoutineResult as RoutineResultModel

from routine.services import routine_queryset_for_this_date
from routine.permissions import RoutineIsMadeByMe as RoutineIsMadeByMePermission


class RoutineAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, RoutineIsMadeByMePermission]

    def get(self, request):
        try:
            routine = RoutineModel.objects.filter(id=request.data["routine_id"]).get()
            return Response(RoutineSerialzer(routine).data, status=status.HTTP_200_OK)
            
        except RoutineModel.DoesNotExist:
            return Response({'message': '존재하지 않는 루틴 입니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    
    def post(self, request):
        serializer = RoutineSerialzer(data=request.data, context={'request':request}, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


    def put(self, request):
        routine = RoutineModel.objects.get(id=request.data['routine_id'])
        serializer = RoutineSerialzer(routine, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


    def delete(self, request):
        routine = RoutineModel.objects.get(id=request.data['routine_id'])
        if routine.is_deleted:
            RoutineModel.objects.filter(id=request.data['routine_id']).update(is_deleted=False)
            RoutineResultModel.objects.filter(routine=routine).update(is_deleted=False)
            return Response({'message': '삭제 취소!!'})

        else:
            RoutineModel.objects.filter(id=request.data['routine_id']).update(is_deleted=True)
            RoutineResultModel.objects.filter(routine=routine).update(is_deleted=True)
            return Response({'message': '삭제 완료!!'})


class GetRoutineListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        routines = routine_queryset_for_this_date(request)
        return Response(GetTodayRoutineListSerializer(routines, many=True).data, status=status.HTTP_200_OK)
            
