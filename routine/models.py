
from django.db import models

from core.models import BaseModel
from user.models import User as UserModel

# Create your models here.
class Routine(BaseModel):
    account = models.ForeignKey(UserModel, verbose_name='사용자', on_delete=models.CASCADE)
    title = models.CharField('제목', max_length=50)

    CATEGORY_CHOICES = (
		('MIRACLE', 'MIRACLE'),
        ('HOMEWORK', 'HOMEWORK'),
        )
    category = models.CharField('분류', max_length=50, choices=CATEGORY_CHOICES)
    
    goal = models.CharField('목표', max_length=50)
    is_alarm = models.BooleanField('알람 설정', default=False)
    is_deleted = models.BooleanField('삭제 여부', default=False)

    def __str__(self) -> str:
        return f'사용자: {self.account_id}, 제목: {self.title}, 분류: {self.category}'
    

class RoutineDay(BaseModel):
    day = models.CharField('요일', max_length=100)
    routine = models.ForeignKey(Routine, verbose_name='루틴', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.day



