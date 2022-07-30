from rest_framework.permissions import BasePermission

from routine.models import Routine as RoutineModel


class RoutineIsMadeByMe(BasePermission):
    """
    루틴에 대한 수정과 삭제는 자신이 생성한 루틴에만 해당 권한이 주어진다.
    """
    SAFE_METHODS = ('GET', 'POST',)
    message = '접근 권한이 없습니다.'

    def has_permission(self, request, view):
        user = request.user
        if request.method in self.SAFE_METHODS:
                return True

        try:
            routine = RoutineModel.objects.get(id=request.data['routine_id'])
            if routine.account == user:
                return True

            return False

        except RoutineModel.DoesNotExist:
            self.message = '존재하지 않는 루틴 입니다.'
            return False