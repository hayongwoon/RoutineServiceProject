from django.db import models

from core.models import BaseModel
from routine.models import Routine as RoutineModel

# Create your models here.
class RoutineResult(BaseModel):
    routine = models.OneToOneField(RoutineModel, verbose_name='루틴 결과', on_delete=models.CASCADE)

    RESULT_CHOICES = (
		('NOT', 'NOT'),
        ('TRY', 'TRY'),
        ('DONE', 'DONE'),
        )
    result = models.CharField('결과', max_length=50, choices=RESULT_CHOICES)
    is_deleted = models.BooleanField('삭제 여부', default=False)