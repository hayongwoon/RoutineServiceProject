from django.utils import timezone
import datetime
from rest_framework.permissions import BasePermission
from routine.models import Routine as RoutineModel


class RoutineIsMadeByMe(BasePermission):
    """
    루틴 결과는 루틴을 생성한 본인만 수정이 가능
    """
    message = '접근 권한이 없습니다.'

    def has_permission(self, request, view):
        user = request.user
        try:
            routine = RoutineModel.objects.get(id=request.data['routine_id'])
            if routine.account == user:
                return True

            return False

        except RoutineModel.DoesNotExist:
            self.message = '존재하지 않는 루틴 입니다.'
            return False