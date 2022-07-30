from django.contrib import admin

from routine.models import Routine as RoutineModel
from routine.models import RoutineDay as RoutineDayModel
from routine_result.models import RoutineResult as RoutineResultModel

# Register your models here.
class RoutineResultInline(admin.StackedInline):
    model = RoutineResultModel

class RoutineAdmin(admin.ModelAdmin):
    inlines = (
            RoutineResultInline,
        )

admin.site.register(RoutineModel, RoutineAdmin)
admin.site.register(RoutineDayModel)